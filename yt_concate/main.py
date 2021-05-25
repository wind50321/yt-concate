import sys
sys.path.append('../')  # 把視野清單改成上一層，讓CMD可以找得到yt_concate
import getopt

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


def set_inputs(inputs):
    short_opts = 'hc:w:l:'
    long_opts = 'help channel= word= limit= cleanup= fast='.split()

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

    if not inputs['channel_id'] or not inputs['search_word'] or not inputs['limit']:
        print_usage()
        sys.exit(2)

    return inputs


def main():
    inputs = {
        'channel_id': '',
        'search_word': '',
        'limit': 0,
        'cleanup': False,
        'fast': True,
    }
    inputs = set_inputs(inputs)
    print(inputs)

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
