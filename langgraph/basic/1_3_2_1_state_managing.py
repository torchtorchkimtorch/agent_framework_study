from typing import TypedDict, Annotated, List
from operator import add

class BasicState(TypedDict):
    # 단순 값들 - 덮어쓰기 방식
    current_step: str
    user_id: str
    # 누적되는 값들 - 추가 방식
    # 커스텀 리듀서 (add를 사용한 누적)
    # 기존 리듀서는 새 값이 들어오면 기존 값은 완전히 사라짐
    messages: Annotated[List[str], add]
    processing_log: Annotated[List[str], add]


