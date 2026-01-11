import express from 'express';
import { Readability } from '@mozilla/readability';
import { JSDOM } from 'jsdom';
import fetch from 'node-fetch';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Configuration
const CONFIG = {
  port: parseInt(process.env.PORT || '3000'),
  token: process.env.MCP_HTTP_TOKEN || 'dev-token',
  googleApiKey: process.env.GOOGLE_API_KEY,
  googleCseId: process.env.GOOGLE_CSE_ID,
  ollamaBaseUrl: process.env.OLLAMA_BASE_URL || 'http://localhost:11434',
  ollamaModel: process.env.OLLAMA_MODEL || 'llama3',
  outputDir: process.env.OUTPUT_DIR || './briefs'
};

// Tool schemas for GET /tools
const TOOL_SCHEMAS = {
  search_web: {
    name: 'search_web',
    description: 'Search the web for a given query and return top results',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query' },
        k: { type: 'integer', description: 'Number of results to return', default: 5 }
      },
      required: ['query']
    },
    outputSchema: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          url: { type: 'string' },
          snippet: { type: 'string' },
          source: { type: 'string' }
        }
      }
    }
  },
  fetch_readable: {
    name: 'fetch_readable',
    description: 'Fetch a URL and extract the main readable content',
    inputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string', description: 'URL to fetch and extract content from' }
      },
      required: ['url']
    },
    outputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string' },
        title: { type: 'string' },
        text: { type: 'string' }
      }
    }
  },
  summarize_with_citations: {
    name: 'summarize_with_citations',
    description: 'Summarize documents into exactly 5 bullet points with inline citations',
    inputSchema: {
      type: 'object',
      properties: {
        topic: { type: 'string', description: 'Topic being summarized' },
        docs: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              title: { type: 'string' },
              url: { type: 'string' },
              text: { type: 'string' }
            }
          },
          description: 'Documents to summarize'
        }
      },
      required: ['topic', 'docs']
    },
    outputSchema: {
      type: 'object',
      properties: {
        bullets: {
          type: 'array',
          items: { type: 'string' },
          description: 'Exactly 5 bullet points, each ≤200 chars, with [1]..[N] inline markers'
        },
        sources: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              i: { type: 'integer' },
              title: { type: 'string' },
              url: { type: 'string' }
            }
          }
        }
      }
    }
  },
  save_markdown: {
    name: 'save_markdown',
    description: 'Save markdown content to a file',
    inputSchema: {
      type: 'object',
      properties: {
        filename: { type: 'string', description: 'Filename for the markdown file' },
        content: { type: 'string', description: 'Markdown content to save' }
      },
      required: ['filename', 'content']
    },
    outputSchema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Path to the saved file' }
      }
    }
  }
};

// Express app setup
const app = express();
app.use(express.json({ limit: '10mb' }));

// Bearer token authentication middleware
function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid Authorization header' });
  }
  
  const token = authHeader.slice(7);
  if (token !== CONFIG.token) {
    return res.status(401).json({ error: 'Invalid token' });
  }
  
  next();
}

// Apply auth to all routes except health check
app.use('/tools', authMiddleware);

// Health check endpoint (no auth)
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// GET /tools - List available tools
app.get('/tools', (req, res) => {
  const tools = Object.values(TOOL_SCHEMAS).map(t => ({
    name: t.name,
    description: t.description,
    inputSchema: t.inputSchema
  }));
  res.json(tools);
});

// POST /tools/search_web
app.post('/tools/search_web', async (req, res) => {
  try {
    const { query, k = 5 } = req.body;
    
    if (!query) {
      return res.status(400).json({ error: 'Missing required parameter: query' });
    }
    
    if (!CONFIG.googleApiKey || !CONFIG.googleCseId) {
      return res.status(500).json({ 
        error: 'Google API not configured. Set GOOGLE_API_KEY and GOOGLE_CSE_ID in .env' 
      });
    }
    
    const url = new URL('https://www.googleapis.com/customsearch/v1');
    url.searchParams.set('key', CONFIG.googleApiKey);
    url.searchParams.set('cx', CONFIG.googleCseId);
    url.searchParams.set('q', query);
    url.searchParams.set('num', Math.min(k, 10).toString());
    
    const response = await fetch(url.toString());
    const data = await response.json();
    
    if (!response.ok) {
      console.error('Google API error:', data);
      return res.status(response.status).json({ 
        error: data.error?.message || 'Search API error' 
      });
    }
    
    const results = (data.items || []).map(item => ({
      title: item.title,
      url: item.link,
      snippet: item.snippet,
      source: new URL(item.link).hostname
    }));
    
    res.json(results);
  } catch (error) {
    console.error('search_web error:', error);
    res.status(500).json({ error: error.message });
  }
});

// POST /tools/fetch_readable
app.post('/tools/fetch_readable', async (req, res) => {
  try {
    const { url } = req.body;
    
    if (!url) {
      return res.status(400).json({ error: 'Missing required parameter: url' });
    }
    
    // Fetch the page
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; ResearchBriefingBot/1.0)'
      },
      timeout: 15000
    });
    
    if (!response.ok) {
      return res.status(response.status).json({ 
        error: `Failed to fetch URL: ${response.status} ${response.statusText}` 
      });
    }
    
    const html = await response.text();
    
    // Parse with JSDOM and extract readable content
    const dom = new JSDOM(html, { url });
    const reader = new Readability(dom.window.document);
    const article = reader.parse();
    
    if (!article) {
      return res.json({
        url,
        title: dom.window.document.title || 'Unknown',
        text: ''
      });
    }
    
    // Clean up the text content
    const text = article.textContent
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 15000); // Limit to 15k chars
    
    res.json({
      url,
      title: article.title || dom.window.document.title || 'Unknown',
      text
    });
  } catch (error) {
    console.error('fetch_readable error:', error);
    res.status(500).json({ error: error.message });
  }
});

// POST /tools/summarize_with_citations
app.post('/tools/summarize_with_citations', async (req, res) => {
  try {
    const { topic, docs } = req.body;
    
    if (!topic) {
      return res.status(400).json({ error: 'Missing required parameter: topic' });
    }
    if (!docs || !Array.isArray(docs) || docs.length === 0) {
      return res.status(400).json({ error: 'Missing or empty docs array' });
    }
    
    // Build source mapping
    const sources = docs.map((doc, i) => ({
      i: i + 1,
      title: doc.title,
      url: doc.url
    }));
    
    // Build context for LLM
    const docContext = docs.map((doc, i) => 
      `[Source ${i + 1}] ${doc.title}\n${doc.text.slice(0, 4000)}`
    ).join('\n\n---\n\n');
    
    const prompt = `You are a research assistant. Based on the following sources about "${topic}", create exactly 5 bullet points summarizing the key information.

RULES:
1. Each bullet must be ≤200 characters
2. Include inline citation markers like [1], [2], etc. referencing the source numbers
3. Be factual and informative
4. Return ONLY a JSON object with a "bullets" array containing exactly 5 strings

SOURCES:
${docContext}

Respond with ONLY valid JSON in this format:
{"bullets": ["First bullet point with citation [1]", "Second bullet [2]", "Third bullet [1][3]", "Fourth bullet [2]", "Fifth bullet [3]"]}`;

    // Call Ollama
    const ollamaResponse = await fetch(`${CONFIG.ollamaBaseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: CONFIG.ollamaModel,
        messages: [{ role: 'user', content: prompt }],
        stream: false,
        options: {
          temperature: 0.3,
          num_predict: 1000
        }
      })
    });
    
    if (!ollamaResponse.ok) {
      const errorText = await ollamaResponse.text();
      console.error('Ollama error:', errorText);
      return res.status(500).json({ 
        error: `Ollama API error: ${ollamaResponse.status}. Is Ollama running with model "${CONFIG.ollamaModel}"?` 
      });
    }
    
    const ollamaData = await ollamaResponse.json();
    const rawContent = ollamaData.message?.content || '';
    
    // Extract JSON from response
    const bullets = extractBullets(rawContent);
    
    if (!bullets || bullets.length !== 5) {
      console.error('Failed to parse LLM response:', rawContent);
      // Fallback: generate basic bullets from docs
      const fallbackBullets = docs.slice(0, 5).map((doc, i) => {
        const snippet = doc.text.slice(0, 180).replace(/\s+/g, ' ').trim();
        return `${snippet}... [${i + 1}]`;
      });
      while (fallbackBullets.length < 5) {
        fallbackBullets.push(`Additional information available in sources. [1]`);
      }
      return res.json({ bullets: fallbackBullets.slice(0, 5), sources });
    }
    
    // Ensure each bullet is ≤200 chars
    const validatedBullets = bullets.map(b => 
      b.length > 200 ? b.slice(0, 197) + '...' : b
    );
    
    res.json({ bullets: validatedBullets, sources });
  } catch (error) {
    console.error('summarize_with_citations error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Helper to extract bullets from LLM response
function extractBullets(content) {
  try {
    // Try to find JSON in the response
    const jsonMatch = content.match(/\{[\s\S]*"bullets"[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      if (Array.isArray(parsed.bullets)) {
        return parsed.bullets;
      }
    }
    
    // Try parsing the entire content as JSON
    const parsed = JSON.parse(content);
    if (Array.isArray(parsed.bullets)) {
      return parsed.bullets;
    }
    
    return null;
  } catch (e) {
    // Try to extract bullet points from text
    const lines = content.split('\n').filter(l => l.trim().startsWith('-') || l.trim().startsWith('•'));
    if (lines.length >= 5) {
      return lines.slice(0, 5).map(l => l.replace(/^[-•]\s*/, '').trim());
    }
    return null;
  }
}

// POST /tools/save_markdown
app.post('/tools/save_markdown', async (req, res) => {
  try {
    const { filename, content } = req.body;
    
    if (!filename) {
      return res.status(400).json({ error: 'Missing required parameter: filename' });
    }
    if (!content) {
      return res.status(400).json({ error: 'Missing required parameter: content' });
    }
    
    // Sanitize filename
    const safeName = filename.replace(/[^a-zA-Z0-9_\-\.]/g, '_');
    const finalName = safeName.endsWith('.md') ? safeName : `${safeName}.md`;
    
    // Ensure output directory exists
    const outputDir = path.resolve(CONFIG.outputDir);
    await fs.mkdir(outputDir, { recursive: true });
    
    const filePath = path.join(outputDir, finalName);
    await fs.writeFile(filePath, content, 'utf-8');
    
    res.json({ path: filePath });
  } catch (error) {
    console.error('save_markdown error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(CONFIG.port, () => {
  console.log(`Research Briefing Server running on http://localhost:${CONFIG.port}`);
  console.log(`\nConfiguration:`);
  console.log(`  - Token: ${CONFIG.token === 'dev-token' ? 'dev-token (default)' : '***configured***'}`);
  console.log(`  - Google API: ${CONFIG.googleApiKey ? 'configured' : 'NOT CONFIGURED'}`);
  console.log(`  - Ollama: ${CONFIG.ollamaBaseUrl} (model: ${CONFIG.ollamaModel})`);
  console.log(`  - Output dir: ${CONFIG.outputDir}`);
  console.log(`\nEndpoints:`);
  console.log(`  GET  /tools                      - List available tools`);
  console.log(`  POST /tools/search_web           - Search the web`);
  console.log(`  POST /tools/fetch_readable       - Extract readable content from URL`);
  console.log(`  POST /tools/summarize_with_citations - Summarize with LLM`);
  console.log(`  POST /tools/save_markdown        - Save markdown file`);
});

export default app;
