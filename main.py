import json
import os

from base import get_md5_from_entry, get_entry_by_md5
from find_tokens import find_tokens_in_url, find_tokens_in_headers, find_tokens_in_post_body
from get_values import get_values_from_entry
from global_config import bold_split, thin_split
from detect_cross_domain import *


def find_tokens_by_keyname(har, enable_print=False):
    """
    遍历 HAR 中记录的请求，在请求头和 url 中查找 token
    :param enable_print: 是否打印详细信息到控制台
    :param har: har 文件路径或 har 字典
    :return: dict, key: url, value: tokens list
    """

    if isinstance(har, str) and os.path.exists(har):
        with open(har, "r", encoding="utf-8-sig") as f:
            har = json.load(f)
    elif not isinstance(har, dict):
        raise ValueError("har is not a dict or a valid file path")

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


def find_tokens_by_compare(har, enable_print=False, only_multi=False):
    """
    通过比较的方式，查找 har 中的 tokens
    :param har: har 文件路径或 har 字典
    :param enable_print: 是否打印详细信息到控制台
    :param only_multi: 是否只打印多次出现的 tokens
    :return: 字典, key: token, value: md5 list, 出现这个 value 的请求的 md5 列表
    """

    if isinstance(har, str) and os.path.exists(har):
        with open(har, "r", encoding="utf-8-sig") as f:
            har = json.load(f)
    elif not isinstance(har, dict):
        raise ValueError("har is not a dict or a valid file path")

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
              f'{multi_count} appeared more than once in "{os.path.basename(har)}"\n'
              f"{bold_split}")

    return value_dict


def test_all(only_hash=False, enable_print=True):
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

            with open(os.path.join("./har_files", har_file), "r", encoding="utf-8-sig") as f:
                har = json.load(f)

            count += 1
            print(f"\n{bold_split}\nFind tokens by keyname, processing {har_file}...\n")

            res_keyname = find_tokens_by_keyname(har,
                                                 enable_print=enable_print)

            print(f"\n{bold_split}\nFind tokens by compare, processing {har_file}...\n")

            res_compare = find_tokens_by_compare(har,
                                                 enable_print=enable_print,
                                                 only_multi=True)

            print(f"{bold_split}")

    print(f"HAR files tested: {count}\n{bold_split}")


def test_cross_domain_detection(only_hash=True, enable_print=False, only_multi=True):
    """
    测试跨域请求检测
    """

    har_files = os.listdir("./har_files")
    count = 0
    for har_file in har_files:
        if not har_file.endswith(".har"):
            continue
        if only_hash and not har_file.endswith("_md5.har"):
            continue

        har_path = os.path.join("./har_files", har_file)

        with open(har_path, "r", encoding="utf-8-sig") as f:
            har = json.load(f)

        count += 1
        print(f'\n{bold_split}\nFind tokens by compare, processing "{har_file}"...')
        res_compare = find_tokens_by_compare(har,
                                             enable_print=enable_print,
                                             only_multi=only_multi)

        value_domain = {}
        for value, md5_list in res_compare.items():
            if len(md5_list) > 1:
                url_list = []
                for md5 in md5_list:
                    url = get_entry_by_md5(har_path, md5)['request']['url']
                    url_list.append((url, md5))

                value_domain[value] = url_list

        have_cross_domain = False
        for value, url_list in value_domain.items():
            res = group_by_domain(url_list, level=2, with_suffix=False)
            if len(res) > 1:
                have_cross_domain = True
                group_domain = [get_domain(group[0][0], domain_level=0) for group in res]

                print(f"value: {value}\n"
                      f"group by domain: {res}\n"
                      f"domain of each group: {group_domain}\n"
                      f"len of res subgroup: {[len(g) for g in res]}\n"
                      f"{thin_split}")

        if not have_cross_domain:
            print(f'No cross domain detected in "{har_file}".\n{bold_split}')

    print(f'HAR files tested: {count}\n{bold_split}')


if __name__ == '__main__':
    # find_tokens_by_keyname("./har_files/meituan_md5.har", enable_print=True)
    # find_tokens_by_compare("./har_files/GaoDe_240324_md5.har", enable_print=True, only_multi=True)
    # test_all(only_hash=True, enable_print=True)
    test_cross_domain_detection()

    pass
