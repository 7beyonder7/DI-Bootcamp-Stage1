# cURL Examples for Research Briefing Server

All examples assume the server is running on `http://localhost:3000` with token `dev-token`.

## Health Check (No Auth Required)

```bash
curl http://localhost:3000/health
```

**Response:**
```json
{"status":"ok","timestamp":"2024-01-15T12:00:00.000Z"}
```

---

## GET /tools - List Available Tools

```bash
curl -H "Authorization: Bearer dev-token" \
  http://localhost:3000/tools
```

**Response:**
```json
[
  {
    "name": "search_web",
    "description": "Search the web for a given query and return top results",
    "inputSchema": {
      "type": "object",
      "properties": {
        "query": {"type": "string", "description": "Search query"},
        "k": {"type": "integer", "description": "Number of results to return", "default": 5}
      },
      "required": ["query"]
    }
  },
  {
    "name": "fetch_readable",
    "description": "Fetch a URL and extract the main readable content",
    "inputSchema": {
      "type": "object",
      "properties": {
        "url": {"type": "string", "description": "URL to fetch and extract content from"}
      },
      "required": ["url"]
    }
  },
  {
    "name": "summarize_with_citations",
    "description": "Summarize documents into exactly 5 bullet points with inline citations",
    "inputSchema": {
      "type": "object",
      "properties": {
        "topic": {"type": "string", "description": "Topic being summarized"},
        "docs": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "title": {"type": "string"},
              "url": {"type": "string"},
              "text": {"type": "string"}
            }
          },
          "description": "Documents to summarize"
        }
      },
      "required": ["topic", "docs"]
    }
  },
  {
    "name": "save_markdown",
    "description": "Save markdown content to a file",
    "inputSchema": {
      "type": "object",
      "properties": {
        "filename": {"type": "string", "description": "Filename for the markdown file"},
        "content": {"type": "string", "description": "Markdown content to save"}
      },
      "required": ["filename", "content"]
    }
  }
]
```

---

## POST /tools/search_web - Web Search

### Basic Search
```bash
curl -X POST http://localhost:3000/tools/search_web \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence 2024"}'
```

### Search with Custom Result Count
```bash
curl -X POST http://localhost:3000/tools/search_web \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "climate change solutions", "k": 10}'
```

**Response:**
```json
[
  {
    "title": "Artificial Intelligence - Wikipedia",
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "snippet": "Artificial intelligence (AI) is the intelligence of machines...",
    "source": "en.wikipedia.org"
  },
  {
    "title": "AI Trends in 2024",
    "url": "https://example.com/ai-trends",
    "snippet": "The latest trends in artificial intelligence...",
    "source": "example.com"
  }
]
```

---

## POST /tools/fetch_readable - Extract Content

### Fetch Article Content
```bash
curl -X POST http://localhost:3000/tools/fetch_readable \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Artificial_intelligence"}'
```

**Response:**
```json
{
  "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
  "title": "Artificial intelligence - Wikipedia",
  "text": "Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of humans or animals..."
}
```

---

## POST /tools/summarize_with_citations - LLM Summarization

### Summarize Multiple Documents
```bash
curl -X POST http://localhost:3000/tools/summarize_with_citations \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Renewable Energy Progress",
    "docs": [
      {
        "title": "Solar Energy Growth Report",
        "url": "https://example.com/solar",
        "text": "Solar energy capacity has grown by 25% in 2024. Major installations in the US, China, and Europe have driven this growth. Cost per watt continues to decline, making solar competitive with fossil fuels."
      },
      {
        "title": "Wind Power Advances",
        "url": "https://example.com/wind",
        "text": "Offshore wind farms are expanding rapidly. The UK and Denmark lead in offshore installations. New turbine designs can generate 15MW per unit. Storage solutions are improving to handle intermittency."
      },
      {
        "title": "Grid Modernization",
        "url": "https://example.com/grid",
        "text": "Smart grid technology enables better renewable integration. AI-powered load balancing optimizes distribution. Battery storage costs dropped 40% since 2020. Vehicle-to-grid technology shows promise."
      }
    ]
  }'
```

**Response:**
```json
{
  "bullets": [
    "Solar energy capacity grew 25% in 2024 with major installations across US, China, and Europe [1]",
    "Offshore wind farms are expanding rapidly, with new turbines generating up to 15MW each [2]",
    "Battery storage costs have dropped 40% since 2020, improving renewable viability [3]",
    "Smart grid technology and AI-powered load balancing optimize energy distribution [3]",
    "Cost per watt for solar continues to decline, making it competitive with fossil fuels [1][2]"
  ],
  "sources": [
    {"i": 1, "title": "Solar Energy Growth Report", "url": "https://example.com/solar"},
    {"i": 2, "title": "Wind Power Advances", "url": "https://example.com/wind"},
    {"i": 3, "title": "Grid Modernization", "url": "https://example.com/grid"}
  ]
}
```

---

## POST /tools/save_markdown - Save File

### Save a Brief
```bash
curl -X POST http://localhost:3000/tools/save_markdown \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "brief_2024-01-15",
    "content": "# Research Brief: AI Trends\n\n**Date:** 2024-01-15\n\n## Key Findings\n\n- Finding one [1]\n- Finding two [2]\n\n## Sources\n\n1. [Source One](https://example.com/1)\n2. [Source Two](https://example.com/2)\n"
  }'
```

**Response:**
```json
{
  "path": "/home/user/research-briefing-server/briefs/brief_2024-01-15.md"
}
```

---

## Error Responses

### 401 Unauthorized - Missing Token
```bash
curl http://localhost:3000/tools
```
```json
{"error":"Missing or invalid Authorization header"}
```

### 401 Unauthorized - Invalid Token
```bash
curl -H "Authorization: Bearer wrong-token" http://localhost:3000/tools
```
```json
{"error":"Invalid token"}
```

### 400 Bad Request - Missing Parameters
```bash
curl -X POST http://localhost:3000/tools/search_web \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{}'
```
```json
{"error":"Missing required parameter: query"}
```

### 500 Server Error - Google API Not Configured
```bash
# When GOOGLE_API_KEY or GOOGLE_CSE_ID not set
curl -X POST http://localhost:3000/tools/search_web \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```
```json
{"error":"Google API not configured. Set GOOGLE_API_KEY and GOOGLE_CSE_ID in .env"}
```

---

## Full Workflow Example

Run these commands in sequence to perform a complete research brief:

```bash
# 1. Search for topic
RESULTS=$(curl -s -X POST http://localhost:3000/tools/search_web \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "quantum computing 2024", "k": 3}')

echo "Search results:"
echo "$RESULTS" | jq .

# 2. Fetch first result (extract URL from results)
URL=$(echo "$RESULTS" | jq -r '.[0].url')
CONTENT=$(curl -s -X POST http://localhost:3000/tools/fetch_readable \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"$URL\"}")

echo "Fetched content:"
echo "$CONTENT" | jq .

# 3. Summarize (you'd normally fetch multiple URLs and combine)
SUMMARY=$(curl -s -X POST http://localhost:3000/tools/summarize_with_citations \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d "{
    \"topic\": \"Quantum Computing 2024\",
    \"docs\": [$CONTENT]
  }")

echo "Summary:"
echo "$SUMMARY" | jq .

# 4. Save markdown
curl -s -X POST http://localhost:3000/tools/save_markdown \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d "{
    \"filename\": \"brief_$(date +%Y-%m-%d)\",
    \"content\": \"# Quantum Computing Brief\\n\\n$(echo $SUMMARY | jq -r '.bullets | map(\"- \" + .) | join(\"\\n\")')\"
  }"
```
