import json
import os

from base import get_md5_from_entry
from find_tokens import find_tokens_in_url, find_tokens_in_headers, find_tokens_in_post_body
from get_values import get_values_from_entry
from global_config import bold_split, thin_split


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

        md5 = get_md5_from_entry(entry)

        headers = entry['request']['headers']

        post_data = entry['request']['postData']

        tokens_url = find_tokens_in_url(url, level=2)
        tokens_headers = find_tokens_in_headers(headers, level=2)
        tokens_post_body = find_tokens_in_post_body(post_data, level=2)

        tokens = {**tokens_url, **tokens_headers, **tokens_post_body}  # 合并两个字典
        if tokens:
            tokens_found += 1
            res[md5] = tokens
            if enable_print:
                print(f"url: {url}")
                # print(f"entry md5: {md5}")
                print(f"tokens found: {tokens}\n{thin_split}")

    if enable_print:
        print(f"Tokens found (found / total entries): {tokens_found}/{len(har['log']['entries'])}")
    return res


def find_tokens_by_compare(har_path, enable_print=False, only_multi=False):
    """
    通过比较的方式，查找 har 中的 tokens
    :param har_path: har 文件路径
    :param enable_print: 是否打印详细信息到控制台
    :param only_multi: 是否只打印多次出现的 tokens
    :return:
    """

    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)

    value_dict = {}

    for entry in har['log']['entries']:
        md5 = get_md5_from_entry(entry)

        values = get_values_from_entry(entry, enable_stopwords=True)

        if values:
            for value in values:
                if value in value_dict.keys():
                    value_dict[value].append(md5)
                else:
                    value_dict[value] = [md5]

    if enable_print:

        multi_count = len([v for v in value_dict.values() if len(v) > 1])
        for k, v in value_dict.items():
            if only_multi and len(v) == 1:
                continue
            print(f"value: {k}\nappeared in request (md5): {v}\n{bold_split}")

        print(f"find {len(value_dict)} values, "
              f'{multi_count} appeared more than once in "{os.path.basename(har_path)}"\n'
              f"{bold_split}")

    return value_dict


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
            print(f"\n{bold_split}\n")
            print(f"Find tokens by keyname, processing {har_file}...\n")
            res_keyname = find_tokens_by_keyname(f"./har_files/{har_file}",
                                                 enable_print=True)
            print(f"\n{bold_split}\n")
            print(f"Find tokens by compare, processing {har_file}...\n")
            res_compare = find_tokens_by_compare(f"./har_files/{har_file}",
                                                 enable_print=True,
                                                 only_multi=True)
            print(f"{bold_split}")

    print(f"HAR files tested: {count}\n{bold_split}")


if __name__ == '__main__':
    # find_tokens_by_keyname("./har_files/meituan_md5.har", enable_print=True)
    # find_tokens_by_compare("./har_files/GaoDe_240324_md5.har", enable_print=True, only_multi=True)
    test_all(only_hash=True)
    pass
