import concurrent.futures
import time

from pytube import YouTube

from .step import Step
from .step import StepException


class DownloadCaptionsConcurThread(Step):
    def process(self, data, inputs, utils):

        print('download captions:', len(data))
        start = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for yt in data:
                print('downloading caption for', yt.url)
                if utils.caption_file_exists(yt):
                    print('Found existing caption file')
                    continue

                executor.submit(self.download_captions, yt, inputs, utils)

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    def download_captions(self, yt, inputs, utils):
        try:
            source = YouTube(yt.url)
            en_caption = source.captions['a.en']
            en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        except KeyError:
            print('KeyError when downloading caption for', yt.url)
