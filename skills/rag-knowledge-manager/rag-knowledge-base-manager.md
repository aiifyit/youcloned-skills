---
name: rag-knowledge-manager
description: "Manage the internal RAG knowledge base — uploading documents, ingesting new sources, querying what's stored, and troubleshooting the vector database."
---

# RAG Knowledge Manager Skill

The RAG (Retrieval-Augmented Generation) system is the agent's long-term memory — it stores the user's expertise, content, business documents, and everything that makes this agent uniquely theirs. You manage ingestion, search, and maintenance of this knowledge base.

## System Architecture

- **Vector database**: Qdrant or Supabase (check which is configured)
- **Embedding model**: Configured in `.env` (default: Anthropic or OpenAI embeddings)
- **Ingestion pipeline**: Files → chunking → embedding → vector storage
- **Retrieval**: Semantic search across all stored knowledge

## Ingestion

### Supported Input Types
- PDF documents
- Word documents (.docx)
- Text files (.txt, .md)
- Transcripts (meeting transcripts, podcast transcripts, video transcripts)
- Web pages (provide URL → fetch and extract → ingest)
- Email threads (export and ingest)
- Slide decks (.pptx — extract text from slides)
- CSV/spreadsheet data (structured data ingestion)
- Audio files (transcribe first, then ingest the transcript)
- Video files (extract transcript, then ingest)

### Ingestion Process

1. **Receive the file or content**
2. **Extract text**: Use appropriate parser for the file type
3. **Clean the text**: Remove formatting artifacts, headers/footers, page numbers
4. **Chunk the text**: Split into meaningful segments
   - Target chunk size: 500-1000 tokens
   - Overlap: 100 tokens between chunks
   - Respect natural boundaries (paragraphs, sections, headers)
   - Keep context: prepend the document title and section header to each chunk
5. **Generate metadata**: For each chunk, store:
   - Source document name
   - Document type (transcript, article, SOP, etc.)
   - Date ingested
   - Section/topic tags (auto-generated)
   - Original file path
6. **Generate embeddings**: Send each chunk through the embedding model
7. **Store in vector database**: Upload embeddings + metadata + raw text
8. **Confirm to user**: "Ingested [document name] — [X] chunks added to your knowledge base."

### Bulk Ingestion

For a folder of files:
1. List all files in the folder
2. Process each file sequentially
3. Report progress: "Processing file 3 of 15..."
4. Summary at the end: "Ingested 15 files, [X] total chunks added."

### Auto-Sync Folder

If configured, monitor a specific folder for new files:
- Check the folder periodically (configurable interval)
- Automatically ingest any new or modified files
- Skip files already ingested (check by filename + modification date)
- Log all auto-ingestions

## Retrieval / Search

When any skill (or the user directly) needs information from the knowledge base:

1. **Receive the query** — what information is needed
2. **Generate query embedding** — embed the search query
3. **Semantic search** — find the top N most relevant chunks (default: 5)
4. **Filter by metadata** — optionally filter by document type, date range, or tags
5. **Return results** — provide the relevant chunks with source attribution

### Search Quality

- If results aren't relevant, try reformulating the query (different keywords, broader or narrower)
- Use metadata filters to narrow results when the user asks about a specific document or topic
- For complex questions, do multiple searches with different query formulations and combine results
- Always attribute: "Based on [document name], [key finding]"

## Knowledge Base Maintenance

### Inventory
When asked "what's in my knowledge base" or similar:
- List all documents by category
- Show total chunks and approximate token count
- Show most recently added documents
- Flag any documents that might be outdated

### Deduplication
- Periodically check for duplicate or near-duplicate chunks
- Flag duplicates for user review
- Remove confirmed duplicates

### Updates
When a document is updated:
1. Remove the old version's chunks from the database
2. Re-ingest the new version
3. Confirm: "Updated [document name] in your knowledge base."

### Deletion
When the user wants to remove something:
1. Confirm what they want to delete: specific document, topic, or everything
2. Remove matching chunks from the vector database
3. Confirm deletion

## Integration with Other Skills

Every skill can query the knowledge base for context:
- **Copywriting**: Search for brand voice examples, past copy, product details
- **Customer support**: Search for product documentation, FAQ answers
- **Sales**: Search for case studies, testimonials, objection responses
- **Content**: Search for frameworks, ideas, past content to repurpose

When a skill needs context it doesn't have, it should query the RAG before asking the user.

## Troubleshooting

- **No results**: Check that the vector database is running and accessible. Verify embeddings were generated correctly.
- **Irrelevant results**: The query may be too broad or the knowledge base may not contain relevant content. Try different search terms or ask the user to upload relevant documents.
- **Slow queries**: Check the vector database health. Large databases may need index optimization.
- **Ingestion failures**: Check file format compatibility, file size limits, and API key validity for the embedding model.
