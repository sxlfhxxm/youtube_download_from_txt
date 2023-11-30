import yt_dlp
from unidecode import unidecode
import time
# yt-dlp 2023.10.13   
# Unidecode  1.3.7


def get_titles_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        titles = [line.strip() for line in file.readlines()]
        return titles

def contains_non_english(text):
    return any(ord(char) > 127 for char in text)

def download_audio(title, index, total, failed_file):
    if contains_non_english(title):
        title = unidecode(title)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
        'outtmpl': f'{title}.mp3'
    }

    max_attempts = 3  # Максимальна кількість спроб завантаження
    attempts = 0

    while attempts < max_attempts:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as video:
                search_query = f"ytsearch:{title} audio"
                info_dict = video.extract_info(search_query, download=True)
                if 'entries' in info_dict:
                    video_url = info_dict['entries'][0]['webpage_url']
                    video_title = info_dict['entries'][0]['title']
                    print(f"Завантажено {index}/{total} - {video_title}")
                    video.download([video_url])
                    print("Successfully Downloaded - check the local folder")
                break  # Виходимо з циклу, якщо завантаження пройшло успішно
        except Exception as e:
            print(f"Помилка під час завантаження: {e}")
            attempts += 1
            if attempts == max_attempts:
                with open(failed_file, 'a', encoding='utf-8') as failed:
                    failed.write(f"{title}\n")
            time.sleep(3)  # Затримка перед наступною спробою

file_path = 'unique_song_playlist1.txt'
titles = get_titles_from_file(file_path)
total_tracks = len(titles)
failed_file = 'failed_downloads.txt'

for index, title in enumerate(titles, start=1):
    download_audio(title, index, total_tracks, failed_file)
