from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# State
class CounterState(TypedDict):
    count: int

# 노드
# 노드의 규칙: 
# 1. 항상 state를 첫 번째 매개변수로 받음
# 2. 딕셔너리 형태로 새로운 상태를 반환
# 3. 반환하지 않는 필드는 기존 값을 유지

def first_increment(state):
    print(f"현재 카운트: {state['count']}")
    new_count = state["count"] + 1
    print(f"새로운 카운트: {new_count}")
    return {"count": new_count}

def second_increment(state):
    print(f"현재 카운트: {state['count']}")
    new_count = state["count"] + 10
    print(f"새로운 카운트: {new_count}")
    return {"count": new_count}

# Edge: 노드들을 연결하는 그래프
graph = StateGraph(CounterState)
graph.add_node("first_increment", first_increment)
graph.add_node("second_increment", second_increment)
graph.add_edge(START, "first_increment")
graph.add_edge("first_increment", "second_increment")
graph.add_edge("second_increment", END)

app = graph.compile()
result = app.invoke({"count": 0})
print(f"최종 결과: {result}")