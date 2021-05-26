import concurrent.futures
import time
import logging

from pytube import YouTube

from .step import Step
from .step import StepException


class DownloadCaptionsConcurThread(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('main')
        logger.info(f'captions to download = {len(data)}')
        start = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for yt in data:
                if inputs['fast'] and utils.caption_file_exists(yt):
                    logger.debug(f'found existing caption file {yt.url}, skipping')
                    continue
                executor.submit(self.download_captions, yt, inputs, utils, logger)

        end = time.time()
        logger.debug(f'took {end - start} seconds')

        return data

    def download_captions(self, yt, inputs, utils, logger):
        logger.debug(f'downloading caption for {yt.url}')
        try:
            source = YouTube(yt.url)
            en_caption = source.captions['a.en']
            en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        except KeyError:
            logger.error(f'KeyError when downloading caption for {yt.url}')
