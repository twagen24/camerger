import datetime
import locale
import csv
import re
from moviepy.editor import *

VIDEOS_LOCATION = 'D:/raw/Kassette 1/'
DESCRIPTIONS_FILE_NAME = VIDEOS_LOCATION + 'Kassette 1.csv'
descriptions_map = {}

VIDEO_FILE_REGEX = '.+\.(\d{2}-\d{2}-\d{2})_\d{2}-\d{2}\.\d{2}\.avi'
VIDEO_CODEC = 'libx264'
VIDEO_FPS = 25
VIDEO_BITRATE = '8500k'
AUDIO_CODEC = 'aac'
AUDIO_FPS = 32000
AUDIO_BITRATE = '1024k'
FFMPEG_PARAMS = ['-vf', 'yadif']
SCREEN_SIZE = (720, 576)
locale.setlocale(locale.LC_ALL, 'de_AT.utf8')


def main():
    read_descriptions()
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


def extract_date(file_name: str):
    # print('Parsing date out of file \"' + file_name + '\".')
    date = re.search(VIDEO_FILE_REGEX, file_name)
    return date.group(1)


# reads csv-files per line where each date may or may not have a corresponding headline;
# linebreaks are realized by using the $-symbol within that file
def read_descriptions():
    with open(DESCRIPTIONS_FILE_NAME, encoding='utf8') as descriptions:
        reader = csv.reader(descriptions, delimiter=';')
        for line in enumerate(reader):
            descriptions_map[line[1][0]] = line[1][1].replace('$', '\n')


def merge_video_parts(video_parts: []):
    video_date = get_date_object(extract_date(video_parts[0]))
    print('\nCreating video \"' + str(video_date) + '.avi\", consisting of ' + str(len(video_parts)) + ' sub-video(s):')
    headline = ''
    if str(video_date) in descriptions_map:
        headline = descriptions_map[str(video_date)]
    video_file_clips = [create_intro(video_date, headline)]
    for i in video_parts:
        video_file_clips.append(VideoFileClip(VIDEOS_LOCATION + i))
    same_day_video = concatenate_videoclips(video_file_clips)
    same_day_video.write_videofile(VIDEOS_LOCATION + str(video_date) + '_' + get_allowed_filename(headline) + '.mp4',
                                   codec=VIDEO_CODEC,
                                   audio_codec=AUDIO_CODEC,
                                   # fps=VIDEO_FPS,
                                   bitrate=VIDEO_BITRATE,
                                   # audio_fps=AUDIO_FPS,
                                   # audio_bitrate=AUDIO_BITRATE,
                                   ffmpeg_params=FFMPEG_PARAMS,
                                   # write_logfile=True
                                   )


def get_allowed_filename(val: str) -> str:
    val = val.replace('\n', ' ')
    return val.translate({ord(i): None for i in '<>:"/\\|?*'})


def get_date_object(date: str) -> datetime:
    return datetime.datetime.strptime(date, '%y-%m-%d').date()


def create_intro(date: datetime, headline: str):
    date_formatted = date.strftime('%d. %B %Y')
    if headline == '':
        headline = date_formatted
    else:
        headline = date_formatted + '\n' + headline
    print('\nCreating intro \"' + headline + '\".')
    txt_clip = TextClip(headline,
                        font='MinionPro-Regular',
                        fontsize=48, color='black',
                        bg_color='white',
                        size=SCREEN_SIZE)
    intro = CompositeVideoClip([txt_clip])
    intro_file_name = VIDEOS_LOCATION + str(date) + '-intro.mp4'
    intro.subclip(0, 3) \
        .write_videofile(intro_file_name,
                         fps=VIDEO_FPS,
                         codec=VIDEO_CODEC,
                         bitrate=VIDEO_BITRATE)
    return VideoFileClip(intro_file_name)


main()
