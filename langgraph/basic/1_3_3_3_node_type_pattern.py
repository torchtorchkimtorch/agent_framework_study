'''
동기 노드
동기 노드는 가장 기본적인 형태로, 작업이 순차적으로 실행되며 완료될 때까지 다음 단계로 진행하지 않음
이는 간단한 계산이나 즉시 완료되는 작업에 적합하며, 코드가 직관적이고 디버깅이 용이함
CPU 집약적인 작업이나 로컬 데이터 처리에 주로 사용
'''
def sync_node(state: State) -> Dict[str, Any]:
    """
    동기 노드 - 일반적인 노드 타입
    순차적으로 실행되며 결과를 즉시 반환
    """
    # 동기 작업 수행
    result = perform_sync_operation(state['input'])
    return {"output":result}

'''
비동기 노드 - I/O 작업이나 외부 API 호출과 같이 대기 시간이 발생하는 작업에 효율적임
async/await 패턴을 활용하여 여러 작업을 동시에 실행할 수 있으며, asyncio.gather()를 통해 병렬 처리를 구현할 수 있음
'''
async def async_node(state: State) -> Dict[str, Any]:
    result = await perform_async_operation(state['input'])

    results = await asyncio.gather(
        fetch_data_1(),
        fetch_data_2(),
        fetch_data_3()
    )
    return {
        "output": result,
        "additional_data": results
    }

async def perform_async_operation(data):
    """비동기 작업"""
    await asyncio.sleep(0.1)
    return f"Async result: {data}"

async def fetch_data_2():
    await asyncio.sleep(0.05)
    return "data_2"

async def fetch_data_3():
    await asyncio.sleep(0.05)
    return "data_3"