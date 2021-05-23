from multiprocessing import Process
import time
import os

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideosProcess(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        yt_set = set([found.yt for found in data])  # 避免重複下載講多次關鍵字的影片
        print('video to download=', len(yt_set))

        processes = []
        for i in range(4):
            print('registering process % d' % i)
            processes.append(Process(target=self.download_yt, args=(list(yt_set)[i::4], inputs, utils)))  # 以4為遞增值分配下載網址

        for process in processes:
            process.start()
        for process in processes:
            process.join()

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    def download_yt(self, data, inputs, utils):
        print('video to download=', len(data))
        for yt in data:
            url = yt.url

            if utils.video_file_exists(yt):
                print(f'found existing video file {url}, skipping')
                continue

            print('downloading', url)
            YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
