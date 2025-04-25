<!-- Optional: Add a project logo/banner here -->
<!-- ![FinanceChatBot Banner](link/to/your/banner.png) -->

# ✨Stock's Annual/Quaterly Report Analyzer  ✨

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
<!-- Add other badges like License, Build Status, etc. -->
<!-- [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) -->
<!-- [![Build Status](https://img.shields.io/travis/your_username/FinanceChatBot.svg?branch=main)](https://travis-ci.org/your_username/FinanceChatBot) -->

A Retrieval-Augmented Generation (RAG) application focused on financial data analysis 📈, built with Python, LangChain, Ollama, and Streamlit.

## 🚀 Overview

This application leverages the power of Large Language Models (LLMs) combined with a specialized vector database (ChromaDB) 🧠 to generate summaries and calculate important metrics based on the annual and quaterly returns filed by the company. It uses LangChain to orchestrate the complex RAG pipeline, Ollama for seamless integration with local LLMs 💻, and Streamlit to provide a sleek, user-friendly web interface 🌐.



## 🌟 Features (Potential)


*   📄 **Document Ingestion:** Pipeline for processing financial documents (e.g., SEC filings, annual reports).
*   🔍 **Smart Retrieval:** Fetches the most relevant information snippets from a vectorized knowledge base.
*   💡 **Contextual Answers:** Generates answers grounded in retrieved data using powerful LLMs.
*   🏡 **Local LLM Support:** Run entirely locally using Ollama.

## 📁 Project Structure

```
├── tests/              # Unit and integration tests
├── config/             # Configuration files
├── ui/                 # Streamlit user interface code (e.g., app.py)
├── utils/              # Utility scripts and functions
├── models/             # Potentially ML models or data models
├── data/               # Data storage (e.g., filings, vector store)
├── agents/             # LangChain agents or specific logic modules
├── setup.py            # Package setup script
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration for containerization
```

## 🛠️ Setup

### Prerequisites

*   🐍 Python 3.10 (check `.python-version`)
*   🐳 Docker (optional, for containerized deployment)
*   🦙 Ollama (if using local LLMs)

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url> # Replace <repository-url> with the actual URL
    cd FinanceChatBot
    ```

2.  **Set up Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
    *(Using a virtual environment is highly recommended!)*

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # Or, for development (installs package in editable mode):
    # pip install -e .
    ```

4.  **(Optional) Environment Variables:** Create a `.env` file in the root directory for API keys or specific configurations if needed (loaded via `python-dotenv`).

## ▶️ Running the Application

### Method 1: Using Streamlit Directly (Recommended for Development)

1.  Ensure all dependencies are installed (see Setup).
2.  Make sure you are in the project root directory (`FinanceChatBot`).
3.  Launch the Streamlit app:
    ```bash
    streamlit run ui/app.py
    ```
4.  Open your web browser and navigate to `http://localhost:8501`.

### Method 2: Using Docker (Recommended for Deployment/Isolation)

1.  Ensure Docker Desktop is installed and running.
2.  Build the Docker image:
    ```bash
    docker build -t finance-chatbot .
    ```
3.  Run the Docker container:
    ```bash
    # This maps the container's port 8501 to your machine's port 8501
    docker run -p 8501:8501 finance-chatbot
    ```
4.  Open your web browser and navigate to `http://localhost:8501`.

## 🧩 Dependencies

Key technologies powering FinanceChatBot:

*   `streamlit`: For the interactive web UI.
*   `langchain`: The core framework for building LLM applications.
*   `ollama`: To run and interact with local large language models.
*   `chromadb`: Vector store for efficient similarity search.
*   `llama-index`: Data framework complementing LangChain.
*   `pandas`, `numpy`: Essential for data manipulation.
*   `beautifulsoup4`, `requests`: For web scraping/data fetching capabilities.
*   `sentence-transformers`: To generate text embeddings.

Check `requirements.txt` for the complete list of dependencies and their versions.