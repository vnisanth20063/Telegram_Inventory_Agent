from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent

from .tools import (
    check_inventory,
    calculate_replenishment,
    list_low_stock_products
)

from .rag import ask_rag

load_dotenv()


# --------------------------------------------------
# RAG TOOL
# --------------------------------------------------

@tool
def supply_chain_knowledge(question: str) -> str:
    """
    Search the existing company supply-chain
    documents using the old RAG system.
    """

    return ask_rag(question)


# --------------------------------------------------
# INVENTORY TOOL
# --------------------------------------------------

@tool
def inventory_database(product_id: str) -> str:
    """
    Get real-time inventory information from
    the PostgreSQL inventory database.
    """

    return check_inventory(product_id)


# --------------------------------------------------
# REPLENISHMENT TOOL
# --------------------------------------------------

@tool
def replenishment_calculator(
    current_stock: int,
    daily_demand: int,
    lead_time_days: int,
    safety_stock: int
) -> str:
    """
    Calculate reorder point and determine
    whether replenishment is required.
    """

    return calculate_replenishment(
        current_stock,
        daily_demand,
        lead_time_days,
        safety_stock
    )


# --------------------------------------------------
# LOW STOCK TOOL
# --------------------------------------------------

@tool
def low_stock_products() -> str:
    """
    Find all products that currently need
    replenishment.
    """

    return list_low_stock_products()


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------

SYSTEM_PROMPT = """
You are an AI Inventory Replenishment Agent.

You help users manage inventory and supply-chain
information through Telegram.

You have access to four tools.

1. inventory_database
2. replenishment_calculator
3. low_stock_products
4. supply_chain_knowledge


IMPORTANT TOOL RULES
====================

CURRENT INVENTORY QUESTIONS
---------------------------

If the user asks about:

- current stock
- inventory
- product quantity
- available quantity
- stock level
- daily demand
- lead time
- safety stock
- product inventory

you MUST use inventory_database.

Do NOT answer these questions using RAG.


LOW STOCK QUESTIONS
-------------------

If the user asks:

- Which products are low?
- Which products need replenishment?
- Show low-stock products
- What should we reorder?

use low_stock_products.


REPLENISHMENT QUESTIONS
-----------------------

If the user asks:

- Should I reorder?
- Does this product need replenishment?
- How much should I order?
- What is the reorder point?

First get the product's real information
using inventory_database.

Then use replenishment_calculator.


COMPANY KNOWLEDGE QUESTIONS
---------------------------

If the user asks about:

- company policies
- inventory policies
- supply-chain procedures
- documented procedures
- information from company PDFs
- company rules

use supply_chain_knowledge.


IMPORTANT
=========

Never invent inventory values.

Never assume database values.

Never use old RAG information for current
inventory numbers.

Never claim that an order was actually placed.

You can only calculate or recommend a
replenishment quantity.

Clearly distinguish database information
from document information.
"""


# --------------------------------------------------
# AGENT
# --------------------------------------------------

agent = create_agent(
    model=llm,
    tools=[
        inventory_database,
        replenishment_calculator,
        low_stock_products,
        supply_chain_knowledge
    ],
    system_prompt=SYSTEM_PROMPT
)


# --------------------------------------------------
# ASK AGENT
# --------------------------------------------------

def ask_agent(message: str) -> str:

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
    )

    return result["messages"][-1].content