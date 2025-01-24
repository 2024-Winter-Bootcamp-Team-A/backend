from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv 

load_dotenv()

def generate_video_prompt(script) :
    
  client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
  )


  class Step(BaseModel):
      scene_num: int
      description: str

  class Description(BaseModel):
      style : str
      descriptions: list[Step]

  developer_prompt = ("이야기의 각 장면에 대한 설명이 제공됩니다. 다음 지침에 따라 DALL-E에 사용할 효과적인 이미지 생성 프롬프트를 작성해주세요:\n"
  "먼저 이야기에 어울리는 전반적인 아트 스타일을 선택하세요. 예: 일본 애니메이션, 한국 서정 애니메이션, 픽사 3D 애니메이션, 서양 클래식 회화 등\n"
  "각 장면에 대해 다음 요소를 포함한 상세한 설명을 작성하세요:\n"
  "등장인물의 외형"
  "인물의 행동과 표정, "
  "배경과 환경, "
  "조명과 분위기\n"
  "## 프롬프트 작성 규칙:\n"
  "장면에 대해서 모든 이름은 그 등장인물에 대한 구체적인 외형묘사로 변경하여 나타낸다.\n"
  "예: '민철'이 아닌 '짧은 검정 머리에 파란색 교복을 입은 소년'\n"
  "동일한 인물이 여러 장면에 등장할 경우, 매 장면마다 동일한 상세 외형 묘사를 반복하세요. 절대 생략하지 마세요\n"
  "각 문장은 하나의 주요 요소(행동 또는 배경)만 다루세요.\n"
  "구체적이고 시각적으로 묘사 가능한 표현을 사용하세요.\n"
  "설명형 문장으로 작성하고, 대화형이나 명령형은 피하세요.\n"
  "추상적인 개념보다는 직접적이고 명확한 묘사를 사용하세요.\n"

  "## 예시:\n"
  "'descriptions' : '짧은 검정 머리에 파란색 교복을 입은 소년이 교실 창가에 서 있다. 소년의 눈에는 결의에 찬 표정이 어려있다. 교실 창 밖으로는 벚꽃 나무가 만개한 학교 정원이 보인다. 따뜻한 봄 햇살이 교실 내부를 부드럽게 비추고 있다.'},\n"
  "'descriptions' : ' 긴 갈색 머리에 치마와 셔츠를 입은 소녀가 짧은 검정 머리에 파란색 교복을 입은 소년에게 꽃을 건네준다. 교실 내부는 벚꽃이 피어난다. 강한 햇살이 소년과 소녀를 비춘다'},\n"
  )
  user_prompt = script

  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
      {"role": "developer", "content": f"{developer_prompt}"},
      {"role": "user", "content": f"{user_prompt}"}
    ],
    response_format=Description,
  )


  return completion.choices[0].message.content

