from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# 1. Load PDF
loader = PyPDFLoader("app/Knowledge/HIG_AI_Automation_RAG_Knowledge_Base.pdf"
)

documents = loader.load()


# 2. Split PDF into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)


# 3. Create embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 4. Store chunks + embeddings in ChromaDB
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)


# 5. Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# 6. Create LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def ask_rag(question: str) -> str:
    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
    Answer the question using only the information provided in the context.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)

    return response.content

question="Where HIG AI Automation located?"
result=ask_rag(question)

print("Customer:", question)
print("Bot:", result)