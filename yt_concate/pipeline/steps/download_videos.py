from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])  # 避免重複下載講多次關鍵字的影片
        print('video to download=', len(yt_set))
        for yt in yt_set:
            url = yt.url

            if utils.video_file_exists(yt):
                print(f'found existing video file {url}, skipping')
                continue

            print('downloading', url)
            YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)

        return data
