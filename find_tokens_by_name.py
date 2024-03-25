import json

from base import *


def find_entries_with_str(har_path, target_str):
    """在 har 的 entries 中，查找包含特定字符串的 entry"""
    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)

    count = 0
    for entry in har['log']['entries']:
        url = entry['request']['url']

        entry_str = json.dumps(entry, indent=2, ensure_ascii=False)
        if target_str in entry_str:
            count += 1
            # print(entry_str)
            print(url)
            print(bold_split)

    print(f"find {count} entries with target string: '{target_str}'\n{bold_split}")


def find_tokens_by_keyname(har_path):
    """
    在 HAR 文件记录的请求中，查找包含 token 的 url，并输出 token 和 url
    :param har_path: har 文件路径
    :return: dict, key: url, value: tokens list
    """

    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)

    tokens_found = 0
    res = {}
    for entry in har['log']['entries']:
        url = entry['request']['url']

        tokens = find_tokens_in_url(url, level=2)
        if tokens:
            tokens_found += 1
            res[url] = tokens
            print(f"url: {url}\ntokens found: {tokens}\n{bold_split}")

    print(f"Tokens found (found/total): {tokens_found}/{len(har['log']['entries'])}")
    return res


if __name__ == '__main__':
    find_tokens_by_keyname("./har_files/GaoDe_240324.har")
    pass
