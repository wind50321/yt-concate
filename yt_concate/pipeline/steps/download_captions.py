import time

from pytube import YouTube

from .step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):

        start = time.time()

        for yt in data:
            url = yt.url
            print('downloading caption for', url)
            if utils.caption_file_exists(yt):
                print('Found existing caption file')
                continue

            try:
                source = YouTube(url)
                en_caption = source.captions['a.en']
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except KeyError:
                print('KeyError when downloading caption for', url)
                continue

            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

        end = time.time()
        print('took', end - start, 'seconds')

        return data
