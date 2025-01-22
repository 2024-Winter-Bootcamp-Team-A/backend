from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv 

load_dotenv()

def generate_book_script(story):

  client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
  )

  class Step(BaseModel):
      voice_tag: int
      output: str

  class Script(BaseModel):
      title: str
      steps: list[Step]



  developer_prompt = ("책에 대한 설명이 제공됩니다."
  "설명을 토대로 책 독자들이 호기심을 유발하도록 자극적인 숏츠 Script가 작성되어야 합니다."
  "목적은 장편 스토리 초반부의 흥미를 끌어어 나머지 이야기를 읽게 만드는 것입니다."
  "흥미롭고 강렬한 도입부로 사람들의 호기심을 자극하세요"
  "그리고 앞으로 더 많은 이야기가 전개됨을 암시해야합니다"
  "문단간의 내용 흐름이 매끄러워야 합니다."
  "캐릭터 이름을 말할 때, 캐릭터에 대한 아주 간단한 설명을 해주세요."
  "답변은 한글로 작성하고, 존댓말을 써주세요"
  "문장 끝에 마침표는 사용하지 마세요."
  "전체 분량은 '반드시' 11문장으로 작성해주세요."
  "한 문장이 15글자보다 긴 문장은 적절한 부분에 \\n를 넣어주세요"
  "각 문장에 해당하는 voice_tag를 숫자로 붙여주세요.\n"
  "voice_tag 규칙:\n"
      "- 쌍따옴표(\")로 감싸진 대사가 아닌 모든 문장은 '나레이션'으로 0을 붙입니다\n"
      "- 쌍따옴표로 감싸진 대사는 화자의 특성에 따라 다음 tag를 붙입니다 (이 경우 나레이션 tag인 0은 사용불가):\n"
      "  * 중년여성 대사: 1\n"
      "  * 중년남성 대사: 2\n"
      "  * 청소년여성 대사: 3\n"
      "  * 청소년남성 대사: 4\n"
  "내용을 바탕으로 자극적인 유튜브용 title을 15자 내외로 만들주세요.")

  example_prompt = ("무미건조한 인생을 살고 있는 고등학교 2학년생 가미야 도루. 괴롭힘당하는 친구를 돕기 위해 나섰다가 의도치 않은 일에 휘말린다. "
                    "“1반의 히노 마오리에게 고백하면 더 이상 괴롭히지 않을게.”"
  "어쩔 수 없이 하게 된 거짓 고백. 당연히 거절당할 줄 알았지만, 히노는 세 가지 조건을 내걸고 고백을 받아들인다. “첫째, 학교 끝날 때까지 서로 말 걸지 말 것. 둘째, 연락은 되도록 짧게 할 것. 셋째, 날 정말로 좋아하지 말 것.”"
  "그렇게 시작한 가짜 연애. 함께 보내는 시간이 쌓여갈수록 히노를 향한 마음은 점점 커져가고, 도루는 세 번째 조건을 깨고 고백을 하고 만다. 그리고 충격적인 사실을 알게 되는데…. “나는 병이 있어. 선행성 기억상실증이라고 하는데, 밤에 자고 일어나면 잊어버려. 그날 있었던 일을 전부.”"
  "날마다 기억을 잃는 히노와 매일 새로운 사랑을 쌓아가는 날들. 도루는 히노의 내일을 언제까지고 지켜줄 수 있을까? 이들의 관계를 뒤흔들 어두운 그늘의 정체는 무엇일까?")


  assistant_prompt = ("""{
    "title": "기억을 잃는 소녀와 매일 시작하는 사랑",
    "steps": [
      {
        "voice_tag": 0,
        "output": "고등학교 2학년생 도루는\n그저 평범한 일상을 살아가는 학생입니다"
      },
      {
        "voice_tag": 0,
        "output": "하지만 어느 날,\n괴롭힘당하는 친구를 돕기 위해 나섰다가\n난처한 상황에 처하게 됩니다"
      },
      {
        "voice_tag": 2,
        "output": "“1반의 히노 마오리에게 고백하면\n더 이상 괴롭히지 않을게”"
      },
      {
        "voice_tag": 0,
        "output": "당연히 거절당할 거라 생각했지만,\n마오리는 세 가지 조건을 내걸며\n고백을 받아들입니다"
      },
      {
        "voice_tag": 3,
        "output": "“첫째, 학교 끝날 때까지 서로 말 걸지 말 것\n둘째, 연락은 되도록 짧게 할 것\n셋째, 날 정말로 좋아하지 말 것”"
      },
      {
        "voice_tag": 0,
        "output": "이 기묘한 조건 속에서 시작된 가짜 연애"
      },
      {
        "voice_tag": 0,
        "output": "그러나 함께 보내는 시간이 쌓이면서\n도루의 마음은 점점 진심으로 변해갑니다"
      },
      {
        "voice_tag": 0,
        "output": "결국 그는 용기 내어 고백을 하지만,\n충격적인 진실이 밝혀집니다"
      },
      {
        "voice_tag": 3,
        "output": "“나는 밤에 자고 일어나면\n그날 있었던 일을 모두 잊어버려”"
      },
      {
        "voice_tag": 0,
        "output": "날마다 기억을 잃는 마오리,\n그리고 매일 새로운 사랑을 시작하는 도루"
      },
      {
        "voice_tag": 0,
        "output": "이들의 사랑은 과연\n어떤 결말을 맞이하게 될까요?"
      }
    ],
  }""")

  user_prompt = story

  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
      {"role": "developer", "content": f"{developer_prompt}"},
      {"role": "user", "content": f"{example_prompt}"},
      {"role": "assistant", "content": f"{assistant_prompt}"},
      {"role": "user", "content": f"{user_prompt}"}
    ],
    response_format=Script,
  )

  return completion.choices[0].message.content