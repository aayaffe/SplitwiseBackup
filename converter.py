import io
import json

import utils


def convert_file_names(json_infilename, json_outfilename, prefix=''):
    """
    Copies and converts receipt filenames for easier identification.
    :param json_infilename: The original json file from splitwise exporter.
    :param json_outfilename: The output json file with the updated filenames under the field "filename".
    :param prefix: a prefix to add to the filename. the rest of the filename is a sequential number.
    :return: None
    """
    dst_dir = 'export/converted/receipts'
    j = json.load(io.open(json_infilename, 'r', encoding='utf-8-sig'))
    num = 1
    for expense in j['expenses']:
        url = expense['receipt']['original']
        if url is not None:
            filename = utils.get_file_from_url(url)
            extension = utils.get_extension(filename)
            new_name = prefix + str(num)
            utils.file_copy_rename('export/receipts/' + filename, dst_dir, new_name)
            expense['filename'] = new_name + extension
            num += 1

    with open(json_outfilename, 'w', encoding='utf-8') as outfile:
        json.dump(j, outfile, ensure_ascii=False, indent=4)

