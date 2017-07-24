import os
import datetime
import config

formatter = '%Y-%m-%d'
delimiter = '|'

def convert_yhd_url(suffix_url):
    """
    YHD url utils
    :param suffix_url:
    :return: the real url (i.e: http://list.xx.yhd.com)
    """
    if suffix_url and not str(suffix_url).startswith('http://'):
        if str(suffix_url).startswith("//"):
            suffix_url = suffix_url.replace('//', '')

        suffix_url = '%s%s' % ('http://', suffix_url)
        print suffix_url

    return suffix_url

def get_today_crawled_file_name():
    return '%s%s.txt' % (config.CRAWLED_MERCHANT_FILE_NAME_PREFIX, get_today_label())

def get_today_label():
    return datetime.datetime.today().strftime(formatter)

def append_content_to_file(filename, content):
    with open(os.path.join(config.get_output_dir(), filename), 'a') as fp:
        fp.write(delimiter.join([content, '']))
        fp.flush()

def append_contents_to_file(filename, contents):
    if len(contents) == 1:
        if type(contents) is set:
            contents.add('')
        else:
            contents.append('')

    with open(os.path.join(config.get_output_dir(), filename), 'a') as fp:
        c = '%s|' % delimiter.join(contents)
        fp.write(c)
        fp.flush()


def get_file_contents(filename):
    contents = None
    if os.path.exists(os.path.join(config.get_output_dir(), filename)):
        with open(os.path.join(config.get_output_dir(), filename), 'r') as fp:
            c = fp.read()
            if c:
                contents = c.split(delimiter)

    return contents