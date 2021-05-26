import concurrent.futures
import time
import logging

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideosConcurThread(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('main')
        start = time.time()

        yt_set = set([found.yt for found in data])  # 避免重複下載講多次關鍵字的影片
        logger.info(f'video to download = {len(yt_set)}')

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for yt in yt_set:
                if inputs['fast'] and utils.video_file_exists(yt):
                    logger.debug(f'found existing video file {yt.url}, skipping')
                    continue
                executor.submit(self.download_video, yt, inputs, utils, logger)

        end = time.time()
        logger.debug(f'took {end - start} seconds')

        return data

    def download_video(self, yt, inputs, utils, logger):
        logger.debug(f'downloading video for {yt.url}')
        YouTube(yt.url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
