import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def get_response(prompt, model="gpt-5-mini"):
  #1. 입력된 프로프트에 대한 AI응답을 받아오는 함수
  response = client.responses.create(
    model=model,#사용할 모델 지정
    tools=[{"type":"web_search_preview"}],#2. 웹도구 활성화
    input=prompt #사용자 입력전달
  )
  #텍스트 응답만 반환
  return response.output_text

#3. 스크립트가 직접 실행될때 실행
if __name__=="__main__":
  prompt="""
 https://platform.openai.com/docs/guides/text
  를 읽어서 Text generation에 대해 요약 정리해주세요.
  """
  output=get_response(prompt)
  print(output) #결과출력