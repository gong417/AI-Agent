import os
from dotenv import load_dotenv
from openai import OpenAI
import rich

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

default_model = "gpt-5-mini"

#스트리밍이란? 요청에 대한 결과를 한번에 보내는 것이 아닌, 결과값을 계속해서 흘려보내는 방식
def stream_chat_completion(prompt, model):
  #1. chat.completions API를 사용한 스트리밍 응답 함수
  stream = client.chat.completions.create(
    model=model,
    messages=[{"role":"user", "content":prompt}],
    stream=True #2. 스트리밍 모드 활성화
  )
  for chunk in stream: #3. 응답 청크(조각)를 하나씩 처리
    content = chunk.choices[0].delta.content
    if content is not None:
      print(content, end="")

def stream_response(prompt, model):
  #4. 새로운 리스폰스 API를 사용한 스트리밍 함수
  with client.responses.stream(model=model, input=prompt) as stream:
    for event in stream: # 5.스트림에서 발생하는 각 이벤트 처리
      if "output_text" in event.type: #6. 텍스트 출력 이벤트인 경우
        rich.print(event)
  rich.print(stream.get_final_response()) #최종 응답 출력


if __name__ == "__main__":
  stream_chat_completion("스트리밍이 뭔가요?", default_model)
  stream_response("점심 메뉴 추천 해주세요.", default_model)