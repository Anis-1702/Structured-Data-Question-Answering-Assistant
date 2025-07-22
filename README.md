# 🧠 GenAI Structured Data Question Answering Assistant

This project is an **AI-powered assistant** that can answer natural language questions based on structured data provided in **CSV format**. It supports **two execution backends**:
- 🐼 **Pandas** (for Python-native data analysis)
- 🦆 **DuckDB** (for SQL-style queries on in-memory data)

The app uses **OpenAI's GPT-4** to translate user questions into valid executable code (Pandas or SQL), executes it, and returns the result — all within a user-friendly Streamlit interface.

---

## 🚀 Features

- Accepts natural language questions like:  
  > "What was the total churn last month for country 'AAA'?"

- Dynamically interprets user intent using **GPT-4**
- Executes:
  - 🐼 Python code (using Pandas)
  - 🦆 SQL queries (using DuckDB)
- Displays tabular results or computed metrics
- Modular codebase using **LangGraph** for step-by-step reasoning

---

## 📂 Project Structure
├── data/

├── sample_bo_tbl_large.csv

├── sample_sub_details_large.csv

└── sample_revenue_large.csv

├── StreamlitApp.py

├── langgraph_app.py

├── config.py

└── README.md

Here few responses from **AI-powered assistant**

<img width="547" height="299" alt="example 1" src="https://github.com/user-attachments/assets/d37e8721-78f9-416d-b148-63ffe4978169" />

<img width="560" height="301" alt="Example 2" src="https://github.com/user-attachments/assets/48980f71-0f61-4588-ba1d-ad7d1627f535" />

<img width="525" height="311" alt="Example 3" src="https://github.com/user-attachments/assets/22e94074-f257-42a9-b727-aadd78415489" />


