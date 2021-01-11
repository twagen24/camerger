import datetime
import os
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips

VIDEOS_LOCATION = 'C:/Users/Thomas/Desktop/Temp/Heuernte Obernparz 2005/'
VIDEOS_NAME = 'Kassette 3'

VIDEO_FILE_REGEX = '.+\.(\d{2}-\d{2}-\d{2})_\d{2}-\d{2}\.\d{2}\.avi'
VIDEO_CODEC = 'libx264'
VIDEO_FPS = 25
VIDEO_BITRATE = '8500k'
AUDIO_CODEC = 'aac'
AUDIO_FPS = 32000
AUDIO_BITRATE = '1024k'
FFMPEG_PARAMS = ['-vf', 'yadif']


def main():
    videos = get_all_videos()
    same_day_videos = []
    last_video_date = extract_date(videos[0])
    for i in videos:
        if extract_date(i) == last_video_date:
            same_day_videos.append(i)
        else:
            merge_video_parts(same_day_videos)
            same_day_videos = [i]
            last_video_date = extract_date(i)
    merge_video_parts(same_day_videos)


def get_all_videos() -> []:
    videos = []
    for i in os.listdir(VIDEOS_LOCATION):
        if re.match(VIDEO_FILE_REGEX, i):
            videos.append(i)
    print(videos)
    return videos


def extract_date(file_name):
    # print('Parsing date out of file \"' + file_name + '\".')
    date = re.search(VIDEO_FILE_REGEX, file_name)
    return date.group(1)


def merge_video_parts(video_parts):
    video_date = get_date_object(extract_date(video_parts[0])).date()
    print('\nCreating video \"' + str(video_date) + '.avi\", consisting of ' + str(len(video_parts)) + ' sub-video(s):')
    video_file_clips = []
    for i in video_parts:
        video_file_clips.append(VideoFileClip(VIDEOS_LOCATION + i))
    same_day_video = concatenate_videoclips(video_file_clips)
    same_day_video.write_videofile(VIDEOS_LOCATION + str(video_date) + '.mp4',
                                   codec=VIDEO_CODEC,
                                   audio_codec=AUDIO_CODEC,
                                   # fps=VIDEO_FPS,
                                   bitrate=VIDEO_BITRATE,
                                   # audio_fps=AUDIO_FPS,
                                   # audio_bitrate=AUDIO_BITRATE,
                                   ffmpeg_params=FFMPEG_PARAMS,
                                   # write_logfile=True
                                   )


def get_date_object(date) -> datetime:
    return datetime.datetime.strptime(date, '%y-%m-%d')


main()