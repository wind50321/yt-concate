from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

from .step import Step


class EditVideo(Step):
    def process(self, data, inputs, utils):
        videos = []
        for found in data:
            start, end = self.parse_caption_time(found.time)
            video = VideoFileClip(found.yt.video_filepath).subclip(start, end)
            videos.append(video)
            if len(videos) >= inputs['limit']:
                break

        final_video = concatenate_videoclips(videos)
        output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'])
        final_video.write_videofile(output_filepath)

        for video in videos:
            video.close()

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h), int(m), int(s) + int(ms) / 1000
