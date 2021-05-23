import concurrent.futures
import time
import os

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideosConcurThread(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        yt_set = set([found.yt for found in data])  # 避免重複下載講多次關鍵字的影片
        print('video to download=', len(yt_set))

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for yt in yt_set:
                if utils.video_file_exists(yt):
                    print(f'found existing video file {yt.url}, skipping')
                    continue

                executor.submit(self.download_yt, yt, inputs, utils)

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    def download_yt(self, yt, inputs, utils):
        print('downloading', yt.url)
        YouTube(yt.url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
