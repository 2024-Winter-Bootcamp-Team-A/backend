import json
import os
from .dalle import generate_image
from .crop import crop_image
from .tts import generate_tts
from .image_move_audio import create_video_with_audio_and_subtitles


def generate_dalle_video(scene_count, prompt, script, video_name) : 
    prompt_json = json.loads(prompt)
    style = prompt_json["style"]
    descriptions_array = [prompt_json["descriptions"][i]["description"] for i in range(scene_count)]  # <- 여기에 반드시 숫자 조절해야 한다!!! 

    image_urls = []
    for description in descriptions_array:
        image_url = generate_image(style+", "+description)
        image_urls.append(image_url)

    croped_images = []
    for image_url in image_urls:
        croped_image = crop_image(image_url)
        croped_images.append(croped_image)

    script_json = json.loads(script)
    outputs = [script_json["steps"][i]["output"] for i in range(scene_count)]
    voice_tags = [script_json["steps"][i]["voice_tag"] for i in range(scene_count)]  # <- 여기에 반드시 숫자 조절해야 한다!!! 


    audios = []
    for i in range(scene_count):
        audio = generate_tts(outputs[i], 0)
        audios.append(audio)

    durations = [audios[i].duration for i in range(scene_count)] # <- 여기에 반드시 숫자 조절해야 한다!!! 
    durations = [round(d) + 1 for d in durations] 

    import random
    options = [(True, False), (False, True), (True, True), (False, False)]
    move_directions = [random.choice(options) for _ in range(scene_count)]


    storage_url = create_video_with_audio_and_subtitles(
        croped_images, 
        audios, 
        outputs, 
        video_name, 
        durations, 
        fps=30, 
        zoom_factors= [1.2] * len(croped_images), 
        move_directions=move_directions, 
        move_amounts = [0.8] * len(croped_images),
        font_path=os.path.join(os.path.dirname(__file__), 'HMKMRHD.TTF')
    )

    return storage_url