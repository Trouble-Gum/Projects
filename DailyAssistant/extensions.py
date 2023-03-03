import inspect
import os
import logging as lg

import googletrans as gts

DEBUG, INFO, WARNING, ERROR, CRITICAL = lg.DEBUG, lg.INFO, lg.WARNING, lg.ERROR, lg.CRITICAL


def log(msg, msg_type=INFO):
    """logging-function common for the whole application"""
    frm = inspect.stack()[1]
    lg.basicConfig(level=INFO, filename="py_telebot.log", filemode="a",
                   format="%(asctime)s %(levelname)s %(message)s")
    call_stack = f' at: {os.path.basename(frm.filename)}, {frm.function}, line: {frm.lineno}'
    func = lg.debug if msg_type == DEBUG else lg.info if msg_type == INFO else \
        lg.warning if msg_type == WARNING else lg.error if msg_type == ERROR else \
        lg.critical if msg_type == CRITICAL else None

    stack_info = msg_type == ERROR
    func(msg + call_stack, stack_info=stack_info)


LANGUAGES = gts.LANGUAGES

translator = gts.Translator()


def translate(text):
    """translates text using google translation API"""
    words = str(text).split()
    if words[0][0] == ':':
        lang = words[0][1:]
        words = ' '.join(words[1:])
    else:
        lang = 'ru'
        words = text
    try:
        res = translator.translate(words, dest=lang).text
        if words == res:
            res = translator.translate(words, dest='en').text
    except ValueError as e:
        res = e
    return res


class CleanExit(object):
    """context manager which provides guaranteed invoke procedure finish()"""
    def __init__(self, finish):
        self.finish = finish

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.finish()
        log('Context manager has executed clean exit', WARNING)


if __name__ == '__main__':
    print(translator.translate('Hello world!', dest='hy').text)
