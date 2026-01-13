from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, AIMessage

class ChatState(MessagesState):
    user_name: str

def greet_user(state: ChatState) -> dict:
    """사용자 인사 처리"""
    user_msg = state["messages"][-1]
    response = AIMessage(
        content=f"안녕하세요, {state['user_name']}님! 무엇을 도와드릴까요?"
    )
    return {"messages": [response]}

def process_question(state: ChatState) -> dict:
    """질문 처리"""
    user_msg = state["messages"][-1]
    response = AIMessage(
        content = f"'{user_msg.content}'에 대한 답변입니다."
    )
    return {"messages": [response]}

graph = StateGraph(ChatState)
graph.add_node("greet", greet_user)
graph.add_node("answer", process_question)

graph.add_edge(START, "greet")
graph.add_edge("greet", "answer")
graph.add_edge("answer", END)

app = graph.compile()

result = app.invoke({
    "messages": [HumanMessage(content="안녕하세요")],
    "user_name": "홍길동"
})

print(f"메시지 수: {len(result['messages'])}")
for msg in result["messages"]:
    role = "User" if isinstance(msg, HumanMessage) else "AI"
    print(f"{role}: {msg.content}")