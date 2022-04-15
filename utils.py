import gettext
import json
import os
import sys
import urllib
from pathlib import Path

import dateutil
import prompt_toolkit
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter, FuzzyWordCompleter
from prompt_toolkit.validation import ValidationError, Validator

import config


def load_translation():
    el = gettext.translation('excel', localedir='locales', languages=[config.language])
    el.install()
    return el.gettext


_ = load_translation()


def to_simple_local_date_string(date):
    d = dateutil.parser.isoparse(date)
    return d.strftime(_("%d/%m/%Y"))


def create_folder(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    except TypeError as e:
        return False
    return True


def in_list(element, list, ignore_case=False):
    if ignore_case:
        return element.lower() in (string.lower() for string in list)
    else:
        return element in list


def convert_yn_to_bool(yn):
    if yn.lower() == 'y':
        return True
    else:
        return False


class YNValidator(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, document):
        text = document.text
        if not (in_list(text, self.options, True)):
            raise ValidationError(message=_('This input is not accepted'))


def default_input(prompt, default, options=[], ignore_case=False, retry=False):
    if options:
        completer = FuzzyWordCompleter(options)
        return prompt_toolkit.prompt(prompt, default=default, completer=completer, complete_while_typing=True,
                                     validator=YNValidator(options))
    return prompt_toolkit.prompt(prompt, default=default)


def session_input(prompt, session, default):
    return session.prompt(prompt, default=default, auto_suggest=AutoSuggestFromHistory())


# takes a url and downloads image from that url
def image_downloader(img_links, folder_name, overwrite=True):
    """
    Download images from a list of image urls.
    :param img_links:
    :param folder_name:
    :param overwrite: if True, overwrite existing files
    :return: list of image names downloaded
    """
    img_names = []

    try:
        parent = os.getcwd()
        try:
            folder = os.path.join(parent, folder_name)
            create_folder(folder)
            os.chdir(folder)
        except Exception:
            print("Error in changing directory.")

        for link in img_links:
            img_name = "None"

            if link != "None":
                img_name = link.split("/")[-1]
                try:
                    img_file = Path(folder + "/" + img_name)
                    if not img_file.is_file() or overwrite:
                        urllib.request.urlretrieve(link, img_name)
                except Exception:
                    img_name = "None"

            img_names.append(img_name)

    except Exception:
        print("Exception (image_downloader):", sys.exc_info()[0])
    finally:
        os.chdir(parent)
    return img_names

# -------------------------------------------------------------
