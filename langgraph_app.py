import os
import pandas as pd
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from config import DATA_PATH,OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

print("DATA_PATH:", DATA_PATH)
print("Exists?", os.path.exists(DATA_PATH))
print("Is Dir?", os.path.isdir(DATA_PATH))
print("Contents:", os.listdir(DATA_PATH) if os.path.exists(DATA_PATH) else "Not Found")

bo = pd.read_csv(f"{DATA_PATH}/sample_bo_tbl_large.csv", parse_dates=['date'])
subs = pd.read_csv(f"{DATA_PATH}/sample_sub_details_large.csv", parse_dates=['date'])
rev = pd.read_csv(f"{DATA_PATH}/sample_revenue_large.csv", parse_dates=['date'])
dfs = {'bo': bo, 'subs': subs, 'rev': rev}

# Normalize column names for consistency
for df in [bo, subs, rev]:
    df.columns = [col.lower() for col in df.columns]

# Extract column names and store globally
bo_cols = bo.columns.tolist()
subs_cols = subs.columns.tolist()
rev_cols = rev.columns.tolist()

#type Answer = str
class QAState(TypedDict):
    user_query: str
    pandas_code: str
    answer: str


import re 

def plan_node(state):
    question = state["user_query"]

    prompt = f"""
You are a data analyst assistant. You will be given a question and three dataframes: bo, subs, rev.

Use only these columns:

- bo: {bo_cols}
- subs: {subs_cols}
- rev: {rev_cols}

Generate valid Python code only — do NOT include markdown formatting like ```python or explanations. Just the code. Assign the final result to a variable called 'answer'.

Question: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    raw_code = response.choices[0].message.content

    # 🧼 Clean: strip markdown fences like ```python ... ```
    cleaned_code = re.sub(r"```(?:python)?\n(.*?)```", r"\1", raw_code, flags=re.DOTALL).strip()

    state["pandas_code"] = cleaned_code
    return state

def execute_code_node(state):
    import pandas as pd
    from config import DATA_PATH

    # Load datasets
    bo = pd.read_csv(f"{DATA_PATH}/sample_bo_tbl_large.csv", parse_dates=["date"])
    subs = pd.read_csv(f"{DATA_PATH}/sample_sub_details_large.csv", parse_dates=["date"])
    rev = pd.read_csv(f"{DATA_PATH}/sample_revenue_large.csv", parse_dates=["date"])
    dfs = {"bo": bo, "subs": subs, "rev": rev}

    # Standardize column names to lowercase
    for df in [bo, subs, rev]:
        df.columns = [col.lower() for col in df.columns]

    # Inject pandas (`pd`) and dataframes into local execution scope
    local_vars = {"pd": pd, **dfs}

    try:
        print("\n🔎 Generated Pandas Code:\n", state["pandas_code"], "\n")

        exec(state["pandas_code"], {}, local_vars)
        state["answer"] = local_vars.get("answer", "⚠️ Code executed but no 'answer' variable found.")
    except Exception as e:
        state["answer"] = f"⚠️ Error executing code: {e}"

    return state

def build_graph():
    graph = StateGraph(QAState)
    graph.add_node("plan", plan_node)
    graph.add_node("execute", execute_code_node)
    graph.set_entry_point("plan")
    graph.add_edge("plan", "execute")
    graph.set_finish_point("execute")
    return graph.compile()

# Utility for Streamlit to use
compiled_graph = build_graph()

def ask_question(query: str) -> str:
    init_state: QAState = {"user_query": query, "pandas_code": "", "answer": ""}
    final_state = compiled_graph.invoke(init_state)
    return final_state['answer']
