# ID의 중요성

from langchain_core.messages import HumanMessage, AIMessage

# ID가 있는 메시지
msg_with_id = HumanMessage(
    content="안녕하세요",
    id="user_msg_001" # 명시적 ID 지정
)

# ID 없이 생성하면 자동으로 UUID 할당 -> 현재는 바뀐듯? 
msg_auto_id = HumanMessage(content="안녕하세요")
print(msg_auto_id.id)
print(msg_with_id.id)

# 메시지 업데이트 패턴
def edit_message_node(state: ChatState) -> dict:
    """특정 메시지를 수정하는 노드"""
    # 마지막 AI 메시지의 ID를 가져옴
    last_ai_msg = state["messages"][-1]
    # 같은 ID로 새 메시지를 보내면 업데이트됨
    edited_msg = AIMessage(
        content = last_ai_msg.content + " (검토 완료)",
        id = last_ai_msg.id # 기존 ID 유지
    )
    return {"messages":[edited_msg]}

# 메세지 삭제 패턴
# add_messages는 RemoveMessage를 통한 삭제도 지원
from langgraph.graph.message import RemoveMessage

def cleanup_messages(state: ChatState) -> dict:
    """오래된 메시지 삭제"""
    # 처음 2개 메시지만 유지하고 나머지 삭제
    messages_to_remove = state["messages"][2:]

    return {
        "messages": [
            RemoveMessage(id=msg.id)
            for msg in messages_to_remove
        ]
    }

# 메시지 필터링
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def get_recent_exchanges(state: ChatState, n: int = 3) -> list:
    """최근 n개의 사용자-AI 대화쌍 추출"""
    messages = state["messages"]
    # 시스템 메시지 제외
    exchanges = [
        msg for msg in messagesif not isinstance(msg, SystemMessage)
    ]
    return exchanges[-(n*2):]

# 메시지 요약 패턴
from langchain_core.messages import SystemMessage

class SummarizableState(MessagesState):
    summary: str

def maybe_summarize(state: SummarizableState) -> dict:
    """메시지가 많아지면 요약"""
    if len(state["messages"]) <= 10:
        return {} # 변경 없음
    # 처음 8개 메시지를 요약
    old_messages = state["messages"][:8]
    summary_text = "이전 대화 요약: ..."
    return {
        "summary": summary_text,
        "messages": [
            RemoveMessage(id=msg.id)
            for msg in old_messages
        ]
    }
