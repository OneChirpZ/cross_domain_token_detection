import json
import os
import time

from base import get_md5_from_entry, select_test_files_by_date
from debug_tools import get_entry_by_md5
from find_tokens import find_tokens_in_url, find_tokens_in_headers, find_tokens_in_post_body
from get_values import get_values_from_entry
from global_config import bold_split, thin_split
from detect_cross_domain import *


def find_tokens_by_keyname(har, enable_print=False, enable_stopwords=True):
    """
    遍历 HAR 中记录的请求，在请求头和 url 中查找 token
    :param enable_print: 是否打印详细信息到控制台
    :param har: har 文件路径或 har 字典
    :return: dict
        key: 请求的 md5
        value: 这条请求中根据 key name 发现的 tokens 的 dict
                这个 dict 的 key 是 token 的 keyname，value 是 token 的值
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

        tokens_url = find_tokens_in_url(url, level=2,
                                        enable_stopwords=enable_stopwords)
        tokens_headers = find_tokens_in_headers(headers, level=2,
                                                enable_stopwords=enable_stopwords)
        tokens_post_body = find_tokens_in_post_body(post_data, level=2,
                                                    enable_stopwords=enable_stopwords)

        # tokens 是一个字典，key 是 token 的 keyname，value 是 token 的值
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


def find_tokens_by_compare(har, enable_print=False, show_skip_info=True, only_multi=False, enable_stopwords=True):
    """
    通过比较的方式，查找 har 中的 tokens
    :param show_skip_info: 是否打印被跳过的 value 的信息
    :param enable_stopwords: 使用停用词过滤
    :param har: har 文件路径或 har 字典
    :param enable_print: 是否打印详细信息到控制台
    :param only_multi: 只打印、返回多次出现的 tokens
        如果设置为 False，将会能覆盖到根据 keyname 找到的所有 tokens
    :return: 字典, key: token value, value: md5 list, 出现这个 value 的请求的 md5 列表
    """

    if isinstance(har, str) and os.path.exists(har):
        with open(har, "r", encoding="utf-8-sig") as f:
            har = json.load(f)
    elif not isinstance(har, dict):
        raise ValueError("har is not a dict or a valid file path")

    value_dict = {}

    for entry in har['log']['entries']:
        md5 = get_md5_from_entry(entry)

        values = get_values_from_entry(entry, enable_stopwords=enable_stopwords)

        if values:
            for value in values:
                if value in value_dict.keys():
                    value_dict[value].append(md5)
                else:
                    value_dict[value] = [md5]

    if enable_print:
        for k, v in value_dict.items():
            if only_multi and len(v) == 1:
                continue
            print(f"value: {k}\nappeared in request (md5): {v}\n{bold_split}")

        multi_count = len([v for v in value_dict.values() if len(v) > 1])
        print(f"find {len(value_dict)} values, "
              f'{multi_count} appeared more than once in "{os.path.basename(har)}"\n'
              f"{bold_split}")

    if only_multi:
        if show_skip_info:
            skipped_values = [k for k, v in value_dict.items() if len(v) == 1]
            if skipped_values:
                print(f"Skipped values by 'only_multi': {skipped_values}")
            else:
                print(f"No value skipped by 'only_multi'")

        value_dict = {k: v for k, v in value_dict.items() if len(v) > 1}

    return value_dict


def test_cross_domain_detection(file_list=None,
                                only_hash=True,
                                enable_verbose_print=False,
                                show_skip_info=False,
                                only_multi=True,
                                enable_stopwords=True):
    """
    测试跨域请求检测
    """

    def do_test(har_path):
        start_time = time.time()
        file_name = os.path.basename(har_path)
        with open(har_path, "r", encoding="utf-8-sig") as f:
            har = json.load(f)

        print(f'\n{bold_split}\n'
              f'Find tokens by compare, processing "{file_name}"...\n'
              f'{bold_split}')

        res_compare = find_tokens_by_compare(har,
                                             enable_print=enable_verbose_print,
                                             show_skip_info=show_skip_info,
                                             only_multi=only_multi,
                                             enable_stopwords=enable_stopwords)

        value_domain = {}
        for value, md5_list in res_compare.items():
            if len(md5_list) > 1:
                url_list = []
                for md5 in md5_list:
                    url = get_entry_by_md5(har, md5)['request']['url']
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
                      f"len of each group: {[len(g) for g in res]}\n"
                      f"{thin_split}")

        if not have_cross_domain:
            print(f'No cross domain detected in "{file_name}".\n{bold_split}')

        print(f'Test "{file_name}" done, time cost: {time.time() - start_time:.2f}s\n'
              f'{bold_split}')

    # ----------------- 主测试代码 -----------------

    print(f'test setup:\n'
          f'    file_list: {file_list}\n'
          f'    only_hash: {only_hash}\n'
          f'    enable_verbose_print: {enable_verbose_print}\n'
          f'    show_skip_info: {show_skip_info}\n'
          f'    only_multi: {only_multi}\n'
          f'    enable_stopwords: {enable_stopwords}\n'
          f'{bold_split}\n')

    if file_list is None:
        count = 0

        har_files = os.listdir("./har_files")
        for har_file in har_files:
            if not har_file.endswith(".har"):
                continue
            if only_hash and not har_file.endswith("_md5.har"):
                continue

            har_path = os.path.join("./har_files", har_file)
            do_test(har_path)
            count += 1

        print(f'HAR files tested: {count}\n{bold_split}')
    else:
        for har_path in file_list:
            do_test(har_path)

        print(f'HAR files tested: {len(file_list)}\n{bold_split}')


def test_keyname(file_list=None):
    all_res = {}
    for file_path in file_list:
        res = find_tokens_by_keyname(file_path, enable_print=False, enable_stopwords=True)
        for md5, key_value in res.items():
            print(f"request md5: {md5}")
            print(f"key_value: ")
            for key, value in key_value.items():
                print(f"    {key}: {value}")
            print(f"{thin_split}")
        print(f"{bold_split}")

        all_res[file_path] = res

    return all_res


def compare_2_methods_res(har_path):
    res_by_keyname = find_tokens_by_keyname(har_path,
                                            enable_print=False,
                                            enable_stopwords=True)

    values_by_keyname = []
    for md5, key_value in res_by_keyname.items():
        for key, value in key_value.items():
            values_by_keyname.append(value)

    values_by_keyname = list(set(values_by_keyname))

    res_by_compare = find_tokens_by_compare(har_path,
                                            enable_print=False,
                                            only_multi=True,
                                            enable_stopwords=True)

    values_by_compare = list(res_by_compare.keys())

    values_same = [v for v in values_by_keyname if v in values_by_compare]
    values_only_keyname = [v for v in values_by_keyname if v not in values_by_compare]
    values_only_compare = [v for v in values_by_compare if v not in values_by_keyname]

    print(f'len of values_by_keyname: {len(values_by_keyname)}')
    print(f'len of values_by_compare: {len(values_by_compare)}')
    print(f'len of values_same: {len(values_same)}')

    # 检查 values_by_keyname 是否是 values_by_compare 的子集
    if set(values_by_keyname).issubset(set(values_by_compare)):
        print('通过 key name 找到的 tokens 是通过多请求共有字段找到的 tokens 的子集')
    else:
        print('两种方法找到的 tokens 不完全一致')


if __name__ == '__main__':
    test_file_list = select_test_files_by_date(only_hash=True)

    # find_tokens_by_keyname("./har_files/meituan_md5.har", enable_verbose_print=True)
    # find_tokens_by_compare("./har_files/GaoDe_240324_md5.har", enable_verbose_print=True, only_multi=True)

    # test_all(only_hash=True, enable_verbose_print=True)

    # test_cross_domain_detection()
    # test_cross_domain_detection(file_list=test_file_list, enable_stopwords=True)

    test_cross_domain_detection(test_file_list,
                                only_hash=True,
                                enable_verbose_print=False,
                                show_skip_info=True,
                                only_multi=True,
                                enable_stopwords=True)

    pass
