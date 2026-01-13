'''
노드는 그래프 내에서 특정 작업을 수행하는 독립적인 처리 단위
LangGraph 설계 철학에서 "노드가 작업을 수행하고, 엣지가 다음 할 일을 알려줌
'''
# 노드 함수 시그니처
# 1. 기본 시그니처 (state만)
# 가장 단순한 형태로, 상태만 받음
def simple_node(state: State) -> dict:
    return {"key": "value"}

# 2. 확장 시그니처 (state + config)
# 설정 정보가 필요할 때 RunnableConfig를 추가로 받습니다
from langchain_core.runnables import RunnableConfig

def node_with_config(state: State, config: RunnableConfig) -> dict:
    # config에서 thread_id, tags 등 접근 가능
    thread_id = config.get("configurable", {}).get("thread_id")
    print(f"Thread ID: {thread_id}")
    return {"processed": True}

# 3. 전체 시그니처 (state + config + runtime)
# 스토어나 스트림 기능이 필요할 때 Runtime 객체를 추가
from langgraph.types import Runtime

def node_with_runtime(
        state: State,
        config: RunnableConfig,
        *,
        store: BaseStore,
        stream_writer: StreamWriter
) -> dict:
    # store: 장기 메모리 저장소 접근
    # stream_writer: 커스텀 스트리밍 출력
    stream_writer({"progress": "50%"})
    return {"status":"done"}

# 동기 vs 비동기 노드

# 동기 노드
def sync_node(state: State) -> dict:
    # 동기적으로 실행
    result = some_computation(state["data"])
    return {"result": result}

# 비동기 노드
# I/O 바운드 작업에 적합
async def async_node(state: State) -> dict:
    # 비동기 API 호출 등
    result = await async_api_call(state["query"])
    return {"response": result}
# 비동기 노드 사용시 ainvoke() 또는 astream()으로 실행
    result = await app.ainvoke({"query": "검색어"})

# 노드 추가 방법
# 함수로 추가
def my_node(state: State) -> dict:
    return {"key": "value"}

graph.add_node("my_node", my_node)
# 이름 생략 시 함수 이름이 노드 이름으로 자동 지정
# LangChain의 Runnable 객체도 노드로 추가 가능
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
graph.add_node("llm", llm)

# 노드 캐싱
# LangGraph는 노드 결과를 캐싱하여 동일한 입력에 대해 재계산 방지

from langgraph.cache import InMemoryCache
from langgraph.cache.policy import CachePolicy

# 캐시 정책 정의
policy = CachePolicy(
    ttl=300, # 5분간 캐시 유지
    key_func=lambda state: hash(state["query"])
)

# 노드에 캐시 정책 적용
graph.add_node("expensive_node", expensive_function, cache_policy=policy)

# 캐시와 함께 컴파일
app = graph.compile(cache=InMemoryCache())