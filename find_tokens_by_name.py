import hashlib
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

        entry_str = json.dumps(entry, ensure_ascii=False, sort_keys=True)
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
    遍历 HAR 中记录的请求，在请求头和 url 中查找 token
    :param enable_print: 是否打印详细信息到控制台
    :param har_path: har 文件路径
    :return: dict, key: url, value: tokens list
    """

    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)

    tokens_found = 0
    res = {}
    for entry in har['log']['entries']:
        url = entry['request']['url']
        if 'md5' not in entry.keys():
            entry_str = json.dumps(entry, ensure_ascii=False, sort_keys=True)
            entry_hash = hashlib.md5(entry_str.encode()).hexdigest()
            entry['md5'] = entry_hash
        md5 = entry['md5']
        headers = entry['request']['headers']

        tokens_url = find_tokens_in_url(url, level=2)
        tokens_headers = find_tokens_in_headers(headers[0], level=2)

        tokens = {**tokens_url, **tokens_headers}  # 合并两个字典
        if tokens:
            tokens_found += 1
            res[md5] = tokens
            if enable_print:
                print(f"url: {url}\nentry md5: {md5}\ntokens found: {tokens}\n{thin_split}")

    if enable_print:
        print(f"Tokens found (found/total): {tokens_found}/{len(har['log']['entries'])}")
    return res


def test_all(only_hash=False):
    """
    遍历 ./har_files 目录下的所有 har 文件
    :param only_hash: 只测试 add_md5_to_entries.py 预处理后的 har 文件（带 _md5.har 后缀）
    """
    har_files = os.listdir("./har_files")
    count = 0
    for har_file in har_files:
        if har_file.endswith(".har"):
            if only_hash and not har_file.endswith("_md5.har"):
                continue

            count += 1
            print(f"Processing {har_file}...")
            res = find_tokens_by_keyname(f"./har_files/{har_file}", enable_print=True)
            print(len(res))
            print(f"{bold_split}")

    print(f"HAR files tested: {count}\n{bold_split}")


if __name__ == '__main__':
    # find_tokens_by_keyname("./har_files/GaoDe_240324.har", enable_print=True)
    test_all(only_hash=True)
    pass
