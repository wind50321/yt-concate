import logging

from .step import Step


class Preflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger('main')
        logger.debug('in Preflight')
        utils.create_dirs()