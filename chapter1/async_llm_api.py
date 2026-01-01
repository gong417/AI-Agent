import asyncio
import os
from openai import OpenAI
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)
#비동기 클라이언트 생성
#비동기(병렬)
openai_client=AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def call_async_gpt5(prompt: str, model: str = "gpt-5-mini") -> str:
  #await를 사용해 비동기적으로 API 응답을 기다림
  response = await openai_client.chat.completions.create(
    model=model,
    messages=[{"role":"user", "content":prompt}],
  )
  return response.choices[0].message.content

async def call_async_gpt4(prompt: str, model: str = "gpt-4o-mini") -> str:
  response = await openai_client.chat.completions.create(
    model=model,
    messages=[{"role":"user", "content":prompt}],
  )
  return response.choices[0].message.content

async def main():
  print("동시에 API 호출하기")
  prompt = "비동기 프로그래밍에 대해 두세 문장으로 설명해주세요."
  gpt5_task = call_async_gpt5(prompt)
  gpt4_task = call_async_gpt4(prompt)

  # 두API 호출을 병렬로 실행하고 둘 다 완료될 때까지 대기
  gpt5_response, gpt4_response = await asyncio.gather(gpt5_task, gpt4_task)
  print(f"gpt5 응답: {gpt5_response}")
  print(f"gpt4 응답: {gpt4_response}")

if __name__ == "__main__":
  asyncio.run(main())


