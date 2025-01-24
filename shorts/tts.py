import requests 
import json
import os
from dotenv import load_dotenv 

load_dotenv()

def generate_tts(text, voice_tag):
  url = "https://typecast.ai/api/speak"

  voice = ['632293f759d649937b97f323', '66d01e17a0b11cba718e8fe3', '66d01e57a0b11cba718e9041', '66d01e3845a4605d68e2588a', '632a7588e7c78a412f5a36cd']
  tone = ['normal-1', 'normal-1', 'normal-1', 'normal-1', 'tonemid-1']

  print(voice[voice_tag])
  print(tone[voice_tag])


  payload = json.dumps({
    "actor_id": voice[voice_tag],
    "text": text,
    "lang": "auto",
    "tempo": 1.1,
    "volume": 100,
    "pitch": 0,
    "xapi_hd": True,
    "max_seconds": 60,
    "model_version": "latest",
    "xapi_audio_format": "wav",
    "emotion_tone_preset": tone[voice_tag],
    "last_pitch": -2
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization':f'Bearer {os.environ.get('TYPECAST_API_KEY')}'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  speak_url = response.json()['result']['speak_v2_url']


  import time
  from moviepy import AudioFileClip

  for _ in range(120):
      r = requests.get(speak_url, headers=headers)
      ret = r.json()['result']
      if ret['status'] == 'done':
          r = requests.get(ret['audio_download_url'])
          with open('test.wav', 'wb') as f:
              f.write(r.content)
          return AudioFileClip('test.wav')
      else:
          print(f"status: {ret['status']}, waiting 1 second")
          time.sleep(1)
