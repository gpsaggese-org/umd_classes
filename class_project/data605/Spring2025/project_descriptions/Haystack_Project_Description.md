### **Haystack**

**Title**: Real-Time Bitcoin News Analysis & Q\&A System with Haystack  
**Difficulty**: 2 (medium)  
**Description**  
**Describe technology**  
**Haystack** is an open-source NLP framework by deepset for building end-to-end question answering, retrieval, and semantic search systems. Key features:

- **Document Stores**: Integrate databases (Elasticsearch, FAISS) for vector/text storage.  
- **Retrievers/Pipelines**: Fetch relevant documents using BM25/neural models.  
- **QA Models**: Leverage transformers (e.g., BERT, RoBERTa) for context-aware answers.  
  Example: Analyze Bitcoin news articles to answer questions like *"What caused the price drop on May 12?"*

**Describe the project**  
Build a Haystack pipeline to ingest real-time Bitcoin news/articles, analyze sentiment, and answer time-sensitive questions. Steps:

1. **Data Ingestion**:  
   - Scrape Bitcoin news headlines/articles (e.g., CryptoPanic API) or tweets (Twitter API v2) in real-time.  
   - Store in Elasticsearch document store with metadata (timestamp, source).  
2. **Preprocessing**:  
   - Clean text (remove URLs, special characters).  
   - Use Haystack’s `PreProcessor` to split documents into paragraphs.  
3. **Pipeline Setup**:  
   - **Retriever**: Use `BM25Retriever` to find relevant articles for a query.  
   - **Reader**: Fine-tune a RoBERTa model on financial QA data (e.g., FiQA dataset) for precise answers.  
   - **Generator**: Add a `Seq2SeqGenerator` (e.g., T5) for open-ended questions like *"Summarize Bitcoin’s price drivers this week."*  
4. **Sentiment Analysis**:  
   - Integrate a custom Haystack node using `transformers` pipeline to score article sentiment (positive/negative).  
5. **Interface**:  
   - Build a CLI/Streamlit app where users ask questions and get answers with source citations.

**Useful resources**

- Haystack Documentation: [https://haystack.deepset.ai/](https://haystack.deepset.ai/)  
- CryptoPanic News API: [https://cryptopanic.com/developers/api/](https://cryptopanic.com/developers/api/)  
- FiQA Dataset for Financial QA: [https://sites.google.com/view/fiqa/](https://sites.google.com/view/fiqa/)

**Is it free?**  
Yes. Haystack is Apache-2.0 licensed. CryptoPanic API offers 100 free calls/day.

**Python libraries / bindings**

- haystack-core: Core framework for pipelines.  
- elasticsearch: Document storage/retrieval.  
- transformers: QA/sentiment models (e.g., roberta-base, t5-small).  
- requests: Fetch news data.
