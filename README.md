# 🤖 Telegram AI Inventory & Supply Chain Agent

An **Agentic AI-powered Inventory and Supply Chain Assistant** that works through Telegram.

The system combines:

- Telegram Bot
- FastAPI Webhook
- PostgreSQL
- LangChain Agent
- Groq LLM
- Existing RAG system
- Inventory management tools
- Replenishment calculations

The AI agent decides whether to retrieve information from the **live PostgreSQL inventory database** or from the **existing company-document RAG system** based on the user's question.

---

## 🚀 Project Overview

Traditional RAG chatbots mainly answer questions from documents.

This project extends a RAG chatbot into an **Agentic AI system** that can interact with real application data and tools.

For example:

> "What is the current stock of P1001?"

The agent does not search the PDF.

Instead, it calls the PostgreSQL inventory tool and retrieves the current stock.

For:

> "What is our inventory policy?"

The agent uses the existing RAG system to search company documents.

Therefore, the agent can decide which source is appropriate for each question.

---

# 🧠 Core Idea

The project combines two sources of information:

### 1. PostgreSQL Inventory Database

Contains live inventory information such as:

- Product ID
- Product name
- Current stock
- Daily demand
- Supplier lead time
- Safety stock

### 2. Existing RAG System

Used for answering questions from company documents such as:

- Inventory policies
- Supply-chain procedures
- Company guidelines
- Replenishment procedures
- Safety-stock policies

The AI agent decides which source to use.

---

# 🏗️ System Architecture

```text
                         ┌───────────────┐
                         │    Telegram   │
                         │     User      │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │     ngrok     │
                         │ HTTPS Tunnel  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    FastAPI    │
                         │    Webhook    │
                         └───────┬───────┘
                                 │
                                 ▼
                       ┌───────────────────┐
                       │    AI Agent       │
                       │   GPT-OSS 120B    │
                       └─────────┬─────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
       ┌──────────────────┐            ┌──────────────────┐
       │ Inventory Tools  │            │   Existing RAG   │
       └────────┬─────────┘            └────────┬─────────┘
                │                               │
                ▼                               ▼
       ┌──────────────────┐            ┌──────────────────┐
       │   PostgreSQL     │            │ Company PDFs /   │
       │    Database      │            │ Documents        │
       └──────────────────┘            └──────────────────┘