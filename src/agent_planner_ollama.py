# src/agent_planner_ollama.py
import json
import logging
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from tools import search_hotels, search_flights, search_activities, book_item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------- Konfigurasi LLM -------------
llm = ChatOllama(model="llama3.2:latest", temperature=0)

# ------------- Tools (wrappers ke mock API) -------------
tools = [
    Tool(name="search_hotels", func=search_hotels, description="Search hotels by location and max price. Returns JSON."),
    Tool(name="search_flights", func=search_flights, description="Search flights by origin/destination and max price. Returns JSON."),
    Tool(name="search_activities", func=search_activities, description="Search activities by location and max price. Returns JSON."),
    Tool(name="book_item", func=book_item, description="Book an item (hotel/flight/activity). Use ONLY after explicit user confirmation and with payment_token."),
]

# ------------- Prompt Template (minta output JSON ketat) -------------
prompt_template = """
You are VacationPlanner. The user request:
{user_input}

You MUST use the available tools to fetch live options (search_hotels, search_flights, search_activities).
Output STRICT JSON only (no extra commentary) with keys:
- itinerary: list of days, each day has 'day', 'activity', 'hotel' (name), 'flight' (id/name optional)
- total_cost: integer (IDR)
- booking_plan: list of {"type":"hotel|flight|activity","id":"<item_id>"}
- questions: list of strings (if more info needed; empty list if none)

Important rules:
1) Use tools to ground price & availability. Do not hallucinate prices.
2) Do NOT call book_item by yourself. Only produce booking_plan. Booking executed only after explicit user confirmation & valid payment_token.
3) Keep results realistic and respect user's budget if provided.
Return JSON only.
"""

prompt = PromptTemplate(input_variables=["user_input"], template=prompt_template)

# ------------- Initialize agent (Zero-shot react) -------------
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ------------- Helper runner -------------
def run_planner(user_input: str):
    """
    Runs the agent on the given user_input and returns parsed JSON (dict).
    """
    logger.info("Running planner for input: %s", user_input)
    raw = agent.run(prompt.format_prompt(user_input=user_input).to_string())
    # agent.run may return a textual JSON; try parse
    try:
        # find first { and last } in raw
        s = raw.strip()
        start = s.find("{")
        end = s.rfind("}") + 1
        json_text = s[start:end]
        data = json.loads(json_text)
        return {"ok": True, "data": data}
    except Exception as e:
        logger.error("Failed to parse agent output as JSON: %s", e)
        return {"ok": False, "error": str(e), "raw": raw}

# ------------- CLI (quick test) -------------
if __name__ == "__main__":
    # contoh input
    example = "I want 3 days in Bali, for 2 people, budget 6,000,000 IDR, travel style: relax, must-have: snorkeling"
    res = run_planner(example)
    if res["ok"]:
        print(json.dumps(res["data"], indent=2, ensure_ascii=False))
    else:
        print("ERROR:", res.get("error"))
        print("RAW:", res.get("raw"))
