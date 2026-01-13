from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# .env 파일에서 환경 변수 로드
load_dotenv()

# GPT-4.1-mini 설정
gpt4_mini = ChatOpenAI(
    model_name="gpt-4.1-mini",
    temperature=0.7,
    max_tokens=150,
)

response = gpt4_mini.invoke([HumanMessage(content="Hello, how are you?")])
print(response)
