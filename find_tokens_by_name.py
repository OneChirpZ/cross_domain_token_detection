import json
import os

from base import *


def find_entries_with_str(har_path, target_str, enable_print=False):
    """在 har 的 entries 中，查找包含特定字符串的 entry，返回符合条件的 entry 列表"""
    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)

    count = 0
    res = []
    for entry in har['log']['entries']:
        url = entry['request']['url']

        entry_str = json.dumps(entry, indent=2, ensure_ascii=False)
        if target_str in entry_str:
            count += 1
            res.append(entry)
            if enable_print:
                # print(entry_str)
                print(url)
                print(bold_split)

    if enable_print:
        print(f"find {count} entries with target string: '{target_str}'\n{thin_split}")

    return res


def find_tokens_by_keyname(har_path, enable_print=False):
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
            if enable_print:
                print(f"url: {url}\ntokens found: {tokens}\n{thin_split}")

    if enable_print:
        print(f"Tokens found (found/total): {tokens_found}/{len(har['log']['entries'])}")
    return res


def test_all():
    # 遍历 ./har_files 目录下的所有 har 文件
    har_files = os.listdir("./har_files")
    for har_file in har_files:
        if har_file.endswith(".har"):
            print(f"Processing {har_file}...")
            res = find_tokens_by_keyname(f"./har_files/{har_file}", enable_print=True)
            print(len(res))
            print(f"{bold_split}")


if __name__ == '__main__':
    # find_tokens_by_keyname("./har_files/GaoDe_240324.har", enable_print=True)
    test_all()
    pass
