from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages  import HumanMessage, AIMessage, SystemMessage

myLLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    vertexai=True,                  # <--- Force Vertex AI backend
    project="gd-gcp-gridu-genai",  # <--- Your GCP Project ID
)

class GenState(TypedDict):
    nature: str
    prompt: str
    response: str
    cleaned_response: str
    
class GenWorkflow:
    def _llm_response(self, state: GenState):
        prompts = [
            SystemMessage(content=state['nature']),
            HumanMessage(content=state['prompt'])
        ]
        llm_response = myLLM.invoke(prompts)
        state['response'] = llm_response.content if isinstance(llm_response, AIMessage) else str(llm_response)
        return state
    
    def _llm_clean_response(self, state: GenState):
        prompts = [
            SystemMessage(content="""
You are an SQL extraction engine.

Extract only executable PostgreSQL SQL statements from the input.

Requirements:
- Output only SQL.
- Remove all natural language.
- Remove markdown code fences.
- Remove labels such as "Here is the SQL:", "Explanation:", or "Analysis:".
- Preserve semicolons.
- Preserve statement order.
- Do not invent or modify SQL.
- Do not include comments.

If no executable SQL exists, return exactly:
NO_VALID_SQL
"""),
            HumanMessage(content=state['response'])
        ]
        llm_response = myLLM.invoke(prompts)
        state['cleaned_response'] = llm_response.content.strip() if isinstance(llm_response, AIMessage) else str(llm_response).strip()
        return state
        
    def __init__(self, prompt):
        gen_graph = StateGraph(GenState)
        gen_graph.add_node("response", self._llm_response)
        gen_graph.add_node("cleaned_response", self._llm_clean_response)
        gen_graph.add_edge(START, "response")
        gen_graph.add_edge("response", "cleaned_response")
        gen_graph.add_edge("cleaned_response", END)
        self.gen_graph_flow = gen_graph.compile()
        self.nature_change_prompt = prompt

    def workflow_response(self, prompt: str) -> str:
        state: GenState = {
            "nature": self.nature_change_prompt, 
            "prompt": prompt, "response": "", 
            "cleaned_response": ""
        }
        final_state = self.gen_graph_flow.invoke(state)
        return final_state['cleaned_response']