# Research Briefing Server

An HTTP server exposing research briefing tools with a CLI client. Uses Google Custom Search for web searching and Ollama for local LLM summarization.

## Architecture

```
CLI (brief)  ──HTTP──>  Server /tools/...  ──calls──> Google Search API (free)
                                │
                                ├─HTTP──> Ollama (local LLM)
                                │
                                └─Disk──> brief_YYYY-MM-DD.md
```

## Features

- **Bearer Token Authentication** - Simple, secure API access
- **Web Search** - Google Programmable Search Engine integration
- **Content Extraction** - Mozilla Readability for clean text extraction
- **LLM Summarization** - Ollama integration for local, free summarization
- **Markdown Export** - Save research briefs with citations

## Prerequisites

- **Node.js 18+** (or 20+ recommended)
- **Google Custom Search API** credentials (100 queries/day free)
- **Ollama** installed locally with a model (e.g., `llama3`)

## Quick Start

### 1. Clone and Install

```bash
git clone <your-repo>
cd research-briefing-server
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
PORT=3000
MCP_HTTP_TOKEN=your-secret-token

# Google Custom Search
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CSE_ID=your-custom-search-engine-id

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

OUTPUT_DIR=./briefs
```

### 3. Set Up Google Custom Search

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project (or select existing)
3. Enable the "Custom Search API"
4. Create an API key and copy it to `GOOGLE_API_KEY`
5. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
6. Create a new search engine
7. Copy the Search Engine ID to `GOOGLE_CSE_ID`

### 4. Set Up Ollama

```bash
# Install Ollama (macOS)
brew install ollama
# Install Ollama (Windows)
winget install Ollama.Ollama

# Or download from https://ollama.com

# Start Ollama and pull a model
ollama run llama3
```

### 5. Start the Server

```bash
npm start
```

### 6. Run a Brief

```bash
# In a new terminal
npm run brief -- "artificial intelligence trends 2024"

# Or if installed globally
brief "climate change solutions"
```

## API Endpoints

All endpoints (except `/health`) require authentication:

```
Authorization: Bearer <MCP_HTTP_TOKEN>
```

### GET /tools

List available tools with their input schemas.

```bash
curl -H "Authorization: Bearer dev-token" \
  http://localhost:3000/tools
```

### POST /tools/search_web

Search the web for a query.

```bash
curl -X POST http://localhost:3000/tools/search_web \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "quantum computing", "k": 5}'
```

**Response:**

```json
[
  {
    "title": "Quantum Computing - Wikipedia",
    "url": "https://en.wikipedia.org/wiki/Quantum_computing",
    "snippet": "Quantum computing is a type of computation...",
    "source": "en.wikipedia.org"
  }
]
```

### POST /tools/fetch_readable

Extract readable content from a URL.

```bash
curl -X POST http://localhost:3000/tools/fetch_readable \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

**Response:**

```json
{
  "url": "https://example.com/article",
  "title": "Article Title",
  "text": "The main content of the article..."
}
```

### POST /tools/summarize_with_citations

Summarize documents into 5 bullet points with citations.

```bash
curl -X POST http://localhost:3000/tools/summarize_with_citations \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI Trends",
    "docs": [
      {"title": "Source 1", "url": "https://...", "text": "Content..."},
      {"title": "Source 2", "url": "https://...", "text": "Content..."}
    ]
  }'
```

**Response:**

```json
{
  "bullets": [
    "Generative AI continues to transform industries [1]",
    "Enterprise adoption grew by 40% in 2024 [2]",
    "Open source models challenge proprietary solutions [1][2]",
    "Regulation frameworks are emerging globally [2]",
    "Multimodal capabilities are the new frontier [1]"
  ],
  "sources": [
    { "i": 1, "title": "Source 1", "url": "https://..." },
    { "i": 2, "title": "Source 2", "url": "https://..." }
  ]
}
```

### POST /tools/save_markdown

Save markdown content to a file.

```bash
curl -X POST http://localhost:3000/tools/save_markdown \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "brief_2024-01-15",
    "content": "# My Brief\n\nContent here..."
  }'
```

**Response:**

```json
{
  "path": "/path/to/briefs/brief_2024-01-15.md"
}
```

## CLI Usage

```bash
# Basic usage
brief "your research topic"

# With npm
npm run brief -- "your research topic"

# Help
brief --help
```

### Example Output

```
🔍 Researching: "quantum computing advances"

Step 1/4: Searching the web...
   Found 5 results
Step 2/4: Fetching content from top sources...
   ✓ Fetched: IBM Quantum Computing Overview...
   ✓ Fetched: Google's Quantum Supremacy...
   ✓ Fetched: MIT Quantum Research...
Step 3/4: Summarizing with LLM...
Step 4/4: Saving markdown...

✅ Brief saved to: ./briefs/brief_2024-01-15.md
```

## Sample Output File

See `briefs/brief_YYYY-MM-DD.md` for the generated brief format:

```markdown
# Research Brief: Quantum Computing Advances

**Date:** 2024-01-15

## Key Findings

- Quantum computers now achieve 1000+ qubits [1]
- Error correction breakthrough enables practical applications [2]
- IBM and Google lead in quantum hardware development [1][3]
- Quantum advantage demonstrated for specific problems [2]
- Hybrid classical-quantum algorithms show promise [3]

## Sources

1. [IBM Quantum Computing](https://ibm.com/quantum)
2. [Google Quantum AI](https://quantumai.google)
3. [MIT Quantum Research](https://mit.edu/quantum)

---

_Generated by Research Briefing Server_
```

## Troubleshooting

### 401 Unauthorized

- Check `Authorization: Bearer <token>` header
- Verify `MCP_HTTP_TOKEN` in `.env` matches your request

### Search 403 Error

- Verify Google API key is valid
- Check Custom Search Engine ID (cx)
- Ensure Custom Search API is enabled in Google Cloud Console
- Check you haven't exceeded 100 queries/day

### Ollama Connection Refused

```bash
# Start Ollama service
ollama serve

# Or check if it's running
curl http://localhost:11434/api/tags
```

### LLM JSON Parse Failures

- The server includes fallback logic for malformed responses
- Try a more capable model: `OLLAMA_MODEL=llama3.1`
- Lower temperature is used (0.3) for more consistent output

### Readability Returns Empty Text

- Some sites block bots; try different sources
- Increase `k` parameter to get more search results
- Check the URL is accessible

## Project Structure

```
research-briefing-server/
├── package.json
├── .env.example
├── README.md
├── src/
│   ├── server.js    # Main HTTP server
│   └── cli.js       # CLI client
├── briefs/          # Output directory
└── curl-examples.md # cURL examples
```
