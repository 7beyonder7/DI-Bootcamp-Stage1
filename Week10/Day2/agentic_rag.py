"""
Agentic RAG Core Module
=======================
Single source of truth for the agentic RAG system.
Used by both app.py (Streamlit) and agentic_rag.ipynb (notebook).

Components:
- Vector retrieval using FAISS
- Web search using Tavily
- LLM inference using Groq
- Agentic workflow using LangGraph
"""

import os
from typing import List, Dict, Any, Optional, TypedDict
from dataclasses import dataclass


# ============================================
# Agent State Definition
# ============================================
class AgentState(TypedDict):
    """State passed between nodes in the agent graph."""
    query: str
    reasoning: str
    retrieved_docs: List[Dict[str, Any]]
    web_results: List[Dict[str, Any]]
    needs_web_search: bool
    final_answer: str
    sources: List[Dict[str, Any]]
    steps: List[str]


# ============================================
# Sample Knowledge Base
# ============================================
SAMPLE_DOCUMENTS = [
    {
        "content": """
        Retrieval-Augmented Generation (RAG) is a technique that combines the power of 
        large language models with external knowledge retrieval. RAG systems first retrieve
        relevant documents from a knowledge base, then use these documents as context for
        the LLM to generate accurate, grounded responses. Key benefits include:
        reduced hallucinations, access to up-to-date information, transparent sourcing,
        and cost-effectiveness compared to fine-tuning.
        """,
        "title": "RAG Overview",
        "type": "knowledge_base"
    },
    {
        "content": """
        Agentic RAG extends traditional RAG by adding reasoning and decision-making capabilities.
        Instead of simply retrieving and generating, agentic systems can:
        plan multi-step retrieval strategies, decide when to search the web vs. local knowledge,
        self-correct and refine answers, and use tools like calculators and APIs.
        The key insight is treating the LLM as an agent that orchestrates information gathering.
        """,
        "title": "Agentic RAG Concepts",
        "type": "knowledge_base"
    },
    {
        "content": """
        LangGraph is a library for building stateful, multi-actor applications with LLMs.
        It extends LangChain with graph-based workflows where nodes represent computation steps,
        edges define the flow between nodes, state is passed and updated through the graph,
        and cycles and conditionals enable complex reasoning patterns.
        LangGraph is ideal for building agents, chatbots, and agentic RAG systems.
        """,
        "title": "LangGraph Introduction",
        "type": "knowledge_base"
    },
    {
        "content": """
        Groq provides ultra-fast LLM inference through their custom LPU (Language Processing Unit).
        Key features include sub-second response times, support for Llama and Mixtral models,
        simple API compatible with OpenAI format, and suitability for real-time applications.
        Groq's speed makes it excellent for agentic systems requiring multiple LLM calls.
        """,
        "title": "Groq LLM Platform",
        "type": "knowledge_base"
    },
    {
        "content": """
        Tavily is a search API designed specifically for AI agents and RAG applications.
        Unlike traditional search APIs, Tavily returns clean parsed content ready for LLM consumption,
        includes relevance scoring, supports different search depths, and provides source URLs
        and titles for attribution. It's commonly used as the web search tool in agentic RAG systems.
        """,
        "title": "Tavily Search API",
        "type": "knowledge_base"
    },
]


# ============================================
# AgenticRAG Class
# ============================================
class AgenticRAG:
    """
    Agentic RAG system combining:
    - Vector retrieval from a local knowledge base
    - Web search via Tavily for current information
    - Groq LLM for fast reasoning and generation
    - LangGraph for orchestrating the agent workflow
    """

    def __init__(
        self,
        groq_api_key: str,
        tavily_api_key: str,
        google_api_key: Optional[str] = None,
        model_name: str = "llama-3.1-8b-instant",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        """
        Initialize the Agentic RAG system.

        Args:
            groq_api_key: API key for Groq LLM
            tavily_api_key: API key for Tavily search
            google_api_key: Optional API key for Google AI
            model_name: Groq model to use
            embedding_model: HuggingFace model for embeddings
        """
        # Set environment variables
        os.environ["GROQ_API_KEY"] = groq_api_key
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key

        # Import dependencies
        from langchain_groq import ChatGroq
        from langchain_community.tools.tavily_search import TavilySearchResults
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document

        # Initialize LLM
        self.llm = ChatGroq(
            model=model_name,
            temperature=0.1,
            max_tokens=2048,
        )

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cpu"},
        )

        # Initialize Tavily search
        self.search_tool = TavilySearchResults(
            max_results=3, search_depth="basic")

        # Build vector store from sample documents
        docs = [
            Document(page_content=d["content"], metadata={
                     "title": d["title"], "type": d["type"]})
            for d in SAMPLE_DOCUMENTS
        ]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)
        self.vector_store = FAISS.from_documents(splits, self.embeddings)

        # Build the agent graph
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph workflow."""
        from langgraph.graph import StateGraph, END

        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("reason", self._reason_node)
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("web_search", self._web_search_node)
        workflow.add_node("synthesize", self._synthesize_node)

        # Set entry point and edges
        workflow.set_entry_point("reason")
        workflow.add_edge("reason", "retrieve")
        workflow.add_conditional_edges(
            "retrieve",
            self._should_search_web,
            {"web_search": "web_search", "synthesize": "synthesize"}
        )
        workflow.add_edge("web_search", "synthesize")
        workflow.add_edge("synthesize", END)

        return workflow.compile()

    def _reason_node(self, state: AgentState) -> AgentState:
        """Analyze query and plan retrieval strategy."""
        from langchain_core.messages import HumanMessage, SystemMessage

        messages = [
            SystemMessage(content="""You are a reasoning agent analyzing a user query.
            Determine what information is needed and whether current/real-time info is required.
            Respond with a brief reasoning plan (2-3 sentences)."""),
            HumanMessage(content=f"Query: {state['query']}")
        ]

        response = self.llm.invoke(messages)

        # Detect if web search is needed
        query_lower = state["query"].lower()
        needs_web = any(term in query_lower for term in [
            "latest", "recent", "current", "today", "news",
            "2024", "2025", "now", "this year", "this month"
        ])

        # Get existing steps or initialize empty list
        current_steps = list(state.get("steps") or [])
        current_steps.append(f"🧠 Reasoning: {response.content[:100]}...")

        return {
            "query": state["query"],
            "reasoning": response.content,
            "retrieved_docs": state.get("retrieved_docs") or [],
            "web_results": state.get("web_results") or [],
            "needs_web_search": needs_web,
            "final_answer": state.get("final_answer") or "",
            "sources": state.get("sources") or [],
            "steps": current_steps,
        }

    def _retrieve_node(self, state: AgentState) -> AgentState:
        """Retrieve documents from vector store."""
        docs = self.vector_store.similarity_search(state["query"], k=3)

        retrieved = [
            {
                "content": doc.page_content,
                "title": doc.metadata.get("title", "Document"),
                "type": doc.metadata.get("type", "knowledge_base"),
            }
            for doc in docs
        ]

        current_steps = list(state.get("steps") or [])
        current_steps.append(f"📚 Retrieved {len(retrieved)} documents")

        return {
            "query": state["query"],
            "reasoning": state.get("reasoning") or "",
            "retrieved_docs": retrieved,
            "web_results": state.get("web_results") or [],
            "needs_web_search": state.get("needs_web_search") or False,
            "final_answer": state.get("final_answer") or "",
            "sources": state.get("sources") or [],
            "steps": current_steps,
        }

    def _should_search_web(self, state: AgentState) -> str:
        """Routing: decide whether to search web."""
        if state.get("needs_web_search", False):
            return "web_search"
        if not state.get("retrieved_docs"):
            return "web_search"
        return "synthesize"

    def _web_search_node(self, state: AgentState) -> AgentState:
        """Search the web using Tavily."""
        current_steps = list(state.get("steps") or [])

        try:
            print(f"🔍 Searching web for: {state['query']}")  # Debug
            results = self.search_tool.invoke({"query": state["query"]})
            print(f"📥 Got {len(results)} results from Tavily")  # Debug

            web_results = [
                {
                    "content": r.get("content", ""),
                    "title": r.get("title", "Web Result"),
                    "url": r.get("url", ""),
                    "type": "web_search",
                }
                for r in results
            ]
            current_steps.append(f"🌐 Web search: {len(web_results)} results")
        except Exception as e:
            print(f"❌ Web search failed: {e}")  # Debug
            web_results = []
            current_steps.append(f"⚠️ Web search error: {str(e)}")

        return {
            "query": state["query"],
            "reasoning": state.get("reasoning") or "",
            "retrieved_docs": state.get("retrieved_docs") or [],
            "web_results": web_results,
            "needs_web_search": state.get("needs_web_search") or False,
            "final_answer": state.get("final_answer") or "",
            "sources": state.get("sources") or [],
            "steps": current_steps,
        }

    def _synthesize_node(self, state: AgentState) -> AgentState:
        """Synthesize final answer from all sources."""
        from langchain_core.messages import HumanMessage, SystemMessage

        # Combine sources
        all_sources = []
        context_parts = []

        for doc in (state.get("retrieved_docs") or []):
            all_sources.append(doc)
            context_parts.append(
                f"[Knowledge Base - {doc['title']}]\n{doc['content']}")

        for result in (state.get("web_results") or []):
            all_sources.append(result)
            context_parts.append(
                f"[Web - {result['title']}]\n{result['content']}")

        context = "\n\n".join(context_parts)

        messages = [
            SystemMessage(content="""You are a helpful assistant that synthesizes information 
            from multiple sources. Base your answer on the provided context, cite sources,
            and acknowledge if information is incomplete. Be concise but comprehensive."""),
            HumanMessage(
                content=f"Context:\n{context}\n\nQuestion: {state['query']}\n\nProvide a well-sourced answer:")
        ]

        response = self.llm.invoke(messages)

        current_steps = list(state.get("steps") or [])
        current_steps.append("✅ Synthesized answer")

        return {
            "query": state["query"],
            "reasoning": state.get("reasoning") or "",
            "retrieved_docs": state.get("retrieved_docs") or [],
            "web_results": state.get("web_results") or [],
            "needs_web_search": state.get("needs_web_search") or False,
            "final_answer": response.content,
            "sources": all_sources,
            "steps": current_steps,
        }

    def add_documents(self, texts: List[str], titles: Optional[List[str]] = None):
        """Add new documents to the knowledge base."""
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document

        if titles is None:
            titles = [f"Document {i+1}" for i in range(len(texts))]

        docs = [
            Document(page_content=text, metadata={
                     "title": title, "type": "user_upload"})
            for text, title in zip(texts, titles)
        ]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)
        self.vector_store.add_documents(splits)

    def query(self, question: str) -> Dict[str, Any]:
        """
        Execute a query through the agentic RAG pipeline.

        Args:
            question: User's question

        Returns:
            Dict with 'answer', 'sources', and 'reasoning_steps'
        """
        initial_state: AgentState = {
            "query": question,
            "reasoning": "",
            "retrieved_docs": [],
            "web_results": [],
            "needs_web_search": False,
            "final_answer": "",
            "sources": [],
            "steps": [],
        }

        try:
            result = self.graph.invoke(initial_state)
            return {
                "answer": result["final_answer"],
                "sources": result["sources"],
                "reasoning_steps": result["steps"],
            }
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": [],
                "reasoning_steps": [f"❌ Error: {str(e)}"],
            }


# ============================================
# CLI for standalone testing
# ============================================
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

    if not groq_key or not tavily_key:
        print("❌ Please set GROQ_API_KEY and TAVILY_API_KEY in .env file")
        exit(1)

    print("Initializing Agentic RAG...")
    agent = AgenticRAG(groq_api_key=groq_key, tavily_api_key=tavily_key)
    print("✅ Ready! Type 'quit' to exit.\n")

    while True:
        query = input("You: ").strip()
        if query.lower() in ["quit", "exit", "q"]:
            break
        if not query:
            continue

        print("\n🤔 Thinking...")
        result = agent.query(query)

        print(f"\nAssistant: {result['answer']}")
        print(
            f"\n[Sources: {len(result['sources'])} | Steps: {len(result['reasoning_steps'])}]\n")
