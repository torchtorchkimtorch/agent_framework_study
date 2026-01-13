'''
스키마 설계 원칙

1. 명확성 원칙

각 필드의 목적과 사용법이 명확해야 함: 필드 이름은 그 용도를 명확히 나타내야 하며, 타입 힌팅과 문서화를 통해 사용법을 명시
실천 방법: 
    의미있는 필드명 사용 - data (x), user_profile (o)
    타입 힌팅 활용: - messages: list (x), messages: List[str] (o)
    문서화 추가: docstring이나 주석으로 각 필드 설명

2. 캡슐화 원칙

내부 처리용 데이터와 외부 인터페이스를 구분해야 함
개념설명: LangGraph에서는 입력/출력 스키마를 분리하여 내부 구현을 숨기고 명확한 인터페이스 제공

3. 단일 책임 원칙

각 상태 스키마는 하나의 명확한 목적을 가져야 함
개념설명: 하나의 스키마가 너무 많은 책임을 가지면 복잡도가 증가하고 변경이 어려워짐 
'''

'''
기본 스키마

개념: 입력과 출력이 동일한 단일 스키마를 사용하는 가장 기본적인 형태
설명: 가장 단순하고 이해하기가 쉬움. 모든 노드가 같은 상태 구조를 공유하므로, 데이터 흐름이 명확하고 디버깅이 쉬움. 
    하지만 시스템이 복잡해지면 불필요한 필드가 많아질 수 있고, 모든 노드가 전체 상태에 접근 가능하기 때문에 보안 문제 발생이 생길 수 있음
'''

from typing_extensions import TypedDict
from typing import Annotated
from operator import add

class BasicState(TypedDict):
    user_input: str
    ai_response: str
    conversation_history: Annotated[list[str], add]

# 실 사용 예시
def chatbot_node(state: BasicState) -> BasicState:
    response = f"사용자님이 '{state['user_input']}'라고 하셨군요!"
    return {
        "ai_response": response,
        "conversation_history": [f"User: {state['user_input']}", f"AI: {response}"]
    }

# 모든 노드가 BasicState 전체를 받고 반환
# conversation_history는 add 리듀서로 자동 누적

'''
명시적 입출력 스키마

개념: 입력과 출력을 별도로 정의하여 인터페이스를 명확하게 제어
설명: 이 패턴은 API 설계에서 자주 사용됨. 외부에서 보는 인터페이스와 내부 처리용 데이터를 구분하여, 내부 구현의 변경이 외부 인터페이스에 영향을 주지 않도록 함
'''

class InputState(TypedDict):
    question: str # 외부에서 받는 질문

class OutputState(TypedDict):
    answer: str # 외부로 반환하는 답변

# OverallState는 InputState와 OutputState를 상속받습니다

class OverallState(InputState, OutputState):
    intermediate_data: str # 내부 처리용 (외부에 노출 x)
    search_results: list[str] # 내부 처리용
    confidence_score: float # 내부 처리용

# 실 사용 예시
def search_node(state: InputState) -> dict:
    results = ["결과1", "결과2", "결과3"]
    return {
        "search_results": results,
        "intermediate_data": f"'{state['question']}'에 대한 검색 완료"
    }

def answer_node(state: OverallState) -> OutputState:
    answer = f"검색 결과를 바탕으로: {state['search_results'][0]}"
    return {"answer": answer}

builder = StateGraph(
    OverallState,
    input=InputState,
    output=OutputState
)

'''
다중 스키마

개념: 내부 노드 간 통신을 위한 private 스키마를 포함하는 복잡한 구조
설명: 다중 스키마 패턴은 각 단계에 최적화된 스키마를 사용하면서도 데이터 흐름을 체계적으로 관리할 수 있게 하나, 상태 변환 오버헤드가 발생할 수 있음 
'''
class OverallState(TypedDict):
    question: str
    answer: str

class QueryOutputState(TypedDict):
    query: str
    query_type: str

class DocumentOutputState(TypedDict):
    docs: list[str]
    relevance_scores: list[float]

class GenerateInputState(OverallState, DocumentOutputState):
    pass

