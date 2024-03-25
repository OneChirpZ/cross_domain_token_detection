import json

from base import *


def find_tokens_by_compare(har_path, enable_print=False):
    # TODO: 待补充
    pass

    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)
