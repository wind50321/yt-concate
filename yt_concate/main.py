import sys
sys.path.append('../')  # 把視野清單改成上一層，讓CMD可以找得到yt_concate
import getopt
import logging

from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.download_captions_thread import DownloadCaptionsThread
from yt_concate.pipeline.steps.download_captions_concur_thread import DownloadCaptionsConcurThread
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.download_videos_thread import DownloadVideosThread
from yt_concate.pipeline.steps.download_videos_concur_thread import DownloadVideosConcurThread
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils


def print_usage():
    print('python argv.py OPTIONS')
    print('{:>6} {:<12} {}'.format('-c', '--channel', 'Channel id for searching videos. (Required)'))
    print('{:>6} {:<12} {}'.format('-w', '--word', 'Word for searching from captions. (Required)'))
    print('{:>6} {:<12} {}'.format('-l', '--limit', 'Limit for concatenating found videos. (Required)'))
    print('{:>6} {:<12} {}'.format('', '--cleanup', 'Clean up downloaded captions and video after outputting. (Default=False)'))
    print('{:>6} {:<12} {}'.format('', '--fast', 'Check downloaded captions and videos for faster task. (Default=True)'))
    print('{:>6} {:<12} {}'.format('', '--log', 'Logger level for printing on screen. (Default=WARNING)'))


def set_inputs(inputs):
    short_opts = 'hc:w:l:'
    long_opts = 'help channel= word= limit= cleanup= fast= log='.split()

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel') and arg:
            inputs['channel_id'] = arg
        elif opt in ('-w', '--word') and arg:
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit') and arg.isdigit():
            inputs['limit'] = int(arg)
        elif opt == '--cleanup' and arg == 'True':
            inputs['cleanup'] = True
        elif opt == '--fast' and arg == 'False':  # bool('False') returns True
            inputs['fast'] = False
        elif opt == '--log':
            arg = arg.upper()
            if arg == 'DEBUG':
                inputs['log_level'] = logging.DEBUG
            elif arg == 'INFO':
                inputs['log_level'] = logging.INFO
            elif arg == 'WARNING':
                inputs['log_level'] = logging.WARNING
            elif arg == 'ERROR':
                inputs['log_level'] = logging.ERROR
            elif arg == 'CRITICAL':
                inputs['log_level'] = logging.CRITICAL

    if not inputs['channel_id'] or not inputs['search_word'] or not inputs['limit']:
        print_usage()
        sys.exit(2)

    return inputs


def config_logger(level):
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)  # logger的level不能比handler高
    formatter = logging.Formatter('%(asctime)s   %(levelname)-10s   %(filename)-20s   %(funcName)-12s   %(message)s')
    file_handler = logging.FileHandler('log.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger  # 不一定要return


def main():
    inputs = {
        'channel_id': '',
        'search_word': '',
        'limit': 0,
        'cleanup': False,
        'fast': True,
        'log_level': logging.WARNING,
    }
    inputs = set_inputs(inputs)  # set command line arguments
    logger = config_logger(inputs['log_level'])
    logger.info(inputs)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptionsConcurThread(),
        ReadCaption(),
        Search(),
        DownloadVideosConcurThread(),
        EditVideo(),
        Postflight(),
    ]

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
