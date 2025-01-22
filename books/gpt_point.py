from openai import OpenAI
import os
from dotenv import load_dotenv 

load_dotenv()

def generate_book_point(story):

  client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
  )


  developer_prompt = ("책에 대한 설명이 제공된다"
  "책의 주제를 가장 잘 나타내는 ‘단일 핵심 문장 또는 대사’를 작성해라"
  "강렬한 메시지를 포함해 독자가 책의 주제와 분위기를 한눈에 이해할 수 있어야 한다"
  "반드시 40자 이내로 작성해 주세요."
  "하나의 대사형태로 작성하세요"
  "서평에 등장한 표현이나 대사를 활용할 수 있다")

  example_prompt = ("‘소년이 온다’는 광주민주화운동과 그로 인한 고통을 그린 소설이다."
                    "주인공 동호는 친구의 죽음을 목격한 후, 도청 상무관에서 시신을 처리하며 폭력과 고통 속에서 어린 생명들의 영혼을 위로한다."
                    "“당신이 나를 밝은 쪽으로, 빛이 비치는 쪽으로, 꽃이 핀 쪽으로 끌고 가기를 바랍니다.”"
                    "이 작품은 광주의 비극을 그리고, 살아남은 이들의 고통과 그들의 아픔을 진지하게 탐구한다."
                    "핵심은 인간으로서, 우리가 서로에게 무엇을 할 수 있는가에 대한 질문이다.")

  assistant_prompt = "“당신이 나를 밝은 쪽으로, 빛이 비치는 쪽으로, 꽃이 핀 쪽으로 끌고 가기를 바랍니다.”"

  user_prompt = story

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "developer", "content": f"{developer_prompt}"},
      {"role": "user", "content": f"{example_prompt}"},
      {"role": "assistant", "content": f"{assistant_prompt}"},
      {"role": "user", "content": f"{user_prompt}"}
    ]
  )


  return completion.choices[0].message.content

