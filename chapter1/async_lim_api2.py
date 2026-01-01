import asyncio
import os
from openai import OpenAI
from dotenv import load_dotenv
from openai import AsyncOpenAI
import logging
import random 
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

#로깅설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#비동기 클라이언트 생성
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
openai_client=AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def simulate_random_failure():
  if random.random() < 0.5:
    logger.warning("인위적으로 API 호출 실패 발생(테스트용)")
    raise ConnectionError("인위적으로 발생시킨 연결 오류(테스트용)")
    await asyncio.sleep(random.uniform(0.1, 0.5))
#tenacity를 사용한 재시도 데코레이터 적용
@retry(
  stop=stop_after_attempt(3), #최대 3번 시도
  wait=wait_exponential(multiplier=1,min=2,max=10), #지수 백오프: 2초, 4초, 8초
  retry=retry_if_exception_type(), # 모든 에외에 대한 재시도
  before_sleep=lambda retry_state: logger.warning(
    f"API 호출 실패: {retry_state.outcome.exception()},{retry_state.attempt_number}번째 재시도 중..."
  )
)

#랜덤한 확률로 실패하는 call_async_openai 함수
async def call_async_gpt5(prompt: str, model: str = "gpt-5-mini") -> str:
  logger.info(f"GPT5 API 호출 시작: {model}")
  #awit를 사용해 비동기적으로 API 응답을 기다림
  await simulate_random_failure()

  response = await openai_client.chat.completions.create(
    model=model,
    messages=[{"role":"user", "content":prompt}],
  )
  logger.info("OpenAI API 호출 성공")
  return response.choices[0].message.content

async def call_async_gpt4(prompt: str, model: str = "gpt-4o-mini") -> str:
  logger.info(f"GPT4 API 호출 시작: {model}")
  await simulate_random_failure()  
  response = await openai_client.chat.completions.create(
    model=model,
    messages=[{"role":"user", "content":prompt}],
  )
  logger.info("OpenAI API 호출 성공")
  return response.choices[0].message.content

async def main():
  print("동시에 API 호출하기")
  prompt = "비동기 프로그래밍에 대해 두세 문장으로 설명해주세요."
  gpt5_task = call_async_gpt5(prompt)
  gpt4_task = call_async_gpt4(prompt)
  #gather는 전체 작업 중 하나라도 실패하면 예외 발생
  try:
    gpt5_response, gpt4_response = await asyncio.gather(gpt5_task, gpt4_task, return_exceptions=False)
    print(f"gpt5 응답: {gpt5_response}")
    print(f"gpt4 응답: {gpt4_response}")
  except Exception as e:
    logger.error(f"API 호출 중 처리되지 않은 오류 발생: {e}")

if __name__ == "__main__":
  asyncio.run(main())  
