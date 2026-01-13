from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1단계: 데이터 저장소 만들기 (State)
# 프로그램이 기억해야 할 정보를 담는 상자 
class MyState(TypedDict):
    message: str

# 2단계: 작업 함수 만들기 (Node)
# 현재 상태를 받아서 새로운 상태를 돌려줌 
def say_hello(state):
    return {"message": "Hello, LangGraph!"}

# 만든 데이터 저장소를 사용하는 그래프 생성
graph = StateGraph(MyState)
# hello 라는 이름으로 작업을 추가 
graph.add_node("hello", say_hello)
# 시작 -> hello 작업으로 화살표를 그림
graph.add_edge(START, "hello")
# hello 작업 -> 끝으로 화살표를 그림 
graph.add_edge("hello", END)

# 그래프를 실행 가능한 프로그램으로 만듬
app = graph.compile()
# 빈 메시지로 프로그램을 시작 
result = app.invoke({"message":""})
print(result)