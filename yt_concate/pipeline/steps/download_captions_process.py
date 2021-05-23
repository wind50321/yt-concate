from multiprocessing import Process
import time

from pytube import YouTube

from .step import Step
from .step import StepException


class DownloadCaptionsProcess(Step):
    def process(self, data, inputs, utils):

        start = time.time()

        processes = []
        for i in range(4):
            print('registering process %d' % i)
            processes.append(Process(target=self.download_captions, args=(data[i::4], inputs, utils)))  # 將data以4為遞增值分配下載網址

        for process in processes:
            process.start()
        for process in processes:
            process.join()

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    def download_captions(self, data, inputs, utils):
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
