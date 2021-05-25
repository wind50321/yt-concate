from .step import Step


class Postflight(Step):
    def process(self, data, inputs, utils):
        print('in Postflight')
        if inputs['cleanup']:
            if utils.output_file_exists(inputs['channel_id'], inputs['search_word']):
                print('found existing output file')
                print('cleaning up files')
                utils.remove_dirs()
