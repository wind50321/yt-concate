import logging

from .step import Step


class Postflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('main')
        logger.debug('in Postflight')
        if inputs['cleanup']:
            if utils.output_file_exists(inputs['channel_id'], inputs['search_word']):
                logger.debug('found existing output file')
                logger.debug('cleaning up files')
                utils.remove_dirs()
