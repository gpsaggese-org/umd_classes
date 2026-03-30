# txtai Market Research Platform

Multi-agent market research platform built on txtai. No LangChain or LlamaIndex — pure txtai for agent orchestration, embeddings, and LLM calls.

## Architecture

| Layer | Component | Description |
|-------|-----------|-------------|
| 1 | **Data Ingestion** | Fetchers in `app/tools/` pull from NewsAPI, Alpha Vantage, SEC EDGAR, web scraping, PRAW/StockTwits |
| 2 | **txtai Pipeline** | Chunks (512 tokens), embeds (sentence-transformers), indexes (SQLite) with metadata tagging |
| 3 | **txtai Agents** | 6 specialized agents: orchestrator, sentiment, diligence, web_research, earnings, regulatory |
| 4 | **LLM Provider** | OpenAI gpt-4o-mini with HuggingFace Mistral-7B fallback |
| 5 | **Streamlit UI** | Dashboard tab for ticker analysis, Research Chat for free-text Q&A |

## Quick Start

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add OPENAI_API_KEY

# Ingest data for a ticker
python -m app.pipeline.ingest --ticker AAPL

# Launch UI
streamlit run app/main.py
```

## Docker

```bash
docker build -t txtai-market-research .
docker run -p 8501:8501 -e OPENAI_API_KEY=$KEY -v $(pwd)/data:/app/data .
```

## Deploy to Hugging Face Spaces

1. Create Space at https://huggingface.co/spaces (SDK: Docker)
2. Push code: `git clone`, copy files, `git push`
3. Add secrets: `OPENAI_API_KEY` (required), optional: `NEWSAPI_KEY`, `ALPHAVANTAGE_API_KEY`, `REDDIT_*`
4. App available at `https://YOUR_USERNAME-txtai-market-research.hf.space`

**Notes:**
- `data/` is ephemeral on Spaces
- Free tier is CPU-only
- Build time: ~5 minutes

## API Usage

```python
from app.agents.orchestrator import run as run_orchestrator
from app.pipeline.ingest import ingest_all

# Ingest
ingest_all("AAPL")  # Returns: {'news': 25, 'sec': 10, 'web': 15, 'social': 30}

# Query
result = run_orchestrator("What's the sentiment on AAPL?", context={"ticker": "AAPL"})
print(result["response"], result["sources"], result["agents_used"])
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| No documents to index | Verify API keys in `.env`, check rate limits |
| LLM parsing failed | Check `OPENAI_API_KEY`, verify credits |
| Index not found | Run ingest first, confirm `data/index.db` exists |

