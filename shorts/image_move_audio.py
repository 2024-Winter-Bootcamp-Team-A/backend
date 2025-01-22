import cv2
import numpy as np
import os
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
from .s3 import upload_file

def create_moving_zoomed_video(image, duration=5, fps=30, zoom_factor=1.2, move_x=True, move_y=False, move_amount=0.5):
    height, width = image.shape[:2]
    zoomed_height = int(height * zoom_factor)
    zoomed_width = int(width * zoom_factor)
    
    frames = []
    for t in np.linspace(0, 1, duration*fps):
        zoomed = cv2.resize(image, (zoomed_width, zoomed_height))
        x_offset = int((zoomed_width - width) * t * move_amount) if move_x else int((zoomed_width - width) * (1-t) * move_amount)
        y_offset = int((zoomed_height - height) * t * move_amount) if move_y else int((zoomed_height - height) * (1-t) * move_amount)
        frame = zoomed[y_offset:y_offset+height, x_offset:x_offset+width]
        frames.append(frame)
    
    return frames

from moviepy import TextClip, CompositeVideoClip, CompositeAudioClip

def create_video_with_audio_and_subtitles(images, audio_paths, subtitles, output_path, durations, fps=30, zoom_factors=None, move_directions=None, move_amounts=None, font_path="./HMKMRHD.TTF"):
    if zoom_factors is None:
        zoom_factors = [1.2] * len(images)
    if move_directions is None:
        move_directions = [(True, False)] * len(images)
    if move_amounts is None:
        move_amounts = [0.5] * len(images)
    
    temp_video_paths = []
    video_clips = []

    for i, (image, audio_path, subtitle_text) in enumerate(zip(images, audio_paths, subtitles)):
        temp_video_path = f'temp_video_{i}.mp4'
        frames = create_moving_zoomed_video(
            image, 
            duration=durations[i], 
            fps=fps, 
            zoom_factor=zoom_factors[i],
            move_x=move_directions[i][0],
            move_y=move_directions[i][1],
            move_amount=move_amounts[i]
        )
        
        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))
        
        for frame in frames:
            video.write(frame)
        
        video.release()
        temp_video_paths.append(temp_video_path)

        video_clip = VideoFileClip(temp_video_path)
        audio_clip = audio_path
        video_clip = video_clip.with_audio(audio_clip)

        subtitle_clip = TextClip(
            font=font_path,
            text=subtitle_text,
            font_size=25,
            color="white",
            stroke_color="black",
            stroke_width=5
        ).with_position(("center", height * 0.7)).with_duration(video_clip.duration)

        video_clip = CompositeVideoClip([video_clip, subtitle_clip])

        video_clips.append(video_clip)

    final_clip = concatenate_videoclips(video_clips)
    back_path = os.path.join(os.path.dirname(__file__), 'background.mp3')
    background_music = AudioFileClip(back_path)
    background_music = background_music.subclipped(0, final_clip.duration)

    background_music = background_music.with_volume_scaled(0.2)
    final_audio = CompositeAudioClip([final_clip.audio, background_music])
    final_clip = final_clip.with_audio(final_audio)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    storage_url = upload_file(output_path)
    os.remove(output_path)

    for temp_path in temp_video_paths:
        os.remove(temp_path)
    
    return storage_url



