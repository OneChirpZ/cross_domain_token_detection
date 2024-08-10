import json
import os

from base import get_md5_from_entry
from global_config import bold_split, thin_split

import urllib.parse


def print_entry_by_md5(md5, only_hash=True):
    """
    在所有 har 文件中查找具有特定 md5 的 entry，并打印
    :param md5: entry 的 md5
    :param only_hash: 只测试带 _md5 后缀的 har 文件
    """
    har_files = os.listdir("./har_files")
    for har_file in har_files:
        if har_file.endswith(".har"):
            if only_hash and not har_file.endswith("_md5.har"):
                continue

            har_file_path = os.path.join("./har_files", har_file)

            entry_found = get_entry_by_md5(har_file_path, md5)
            if entry_found:
                print(f"entry found in {har_file}")
                print(json.dumps(entry_found, ensure_ascii=False, indent=2))
                return

    print(f"\n未找到 md5 为 {md5} 的 entry")


def get_entries_with_str(target_str, only_hash=True, print_context=5):
    har_files = os.listdir("./har_files")

    res = {}
    for har_file in har_files:
        if har_file.endswith(".har"):
            if only_hash and not har_file.endswith("_md5.har"):
                continue

            har_file_path = os.path.join("./har_files", har_file)

            res.update(get_entries_with_str_in_har(har_file_path, target_str))

    total_count = 0
    not_found_file = []
    for har_path, entries in res.items():
        if len(entries) != 0:
            total_count += len(entries)
        else:
            not_found_file.append(har_path)

    print(f"未找到包含字符串 '{target_str}' 的 entry 的 har 文件：")
    for file in not_found_file:
        print(f"    {os.path.basename(file)}")

    print(f"找到 {total_count} 个 entry 符合条件：")
    for har_file_path, entry_res in res.items():
        if len(entry_res) != 0:
            print(f"    {os.path.basename(har_file_path)}: {len(entry_res)}")

    if total_count != 0:
        show_res = input("是否显示结果？(y/n)")
        if show_res.lower() != "n":
            har_count = 0
            for har_file_path, entry_res in res.items():
                har_count += 1
                entry_count = 0
                for entry in entry_res:
                    entry_count += 1
                    print(thin_split)
                    print(f"entry {entry_count} / {len(entry_res)} | entry md5: {get_md5_from_entry(entry)}"
                          f" | har {har_count} / {len(res)} | har: {har_file_path}")
                    print(thin_split)

                    entry_str = json.dumps(entry, ensure_ascii=False, indent=2)
                    entry_str = entry_str.split('\n')
                    for i, line in enumerate(entry_str):
                        if target_str in line:
                            for j in range(i - print_context, i + print_context + 1):
                                if 0 <= j < len(entry_str):
                                    print(entry_str[j])
                            break


def get_entries_with_str_in_har(har_path, target_str):
    """在 har 的 entries 中，查找包含特定字符串的 entry，返回 dit: {har_path: 符合条件的 entry 列表}"""

    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)
    res = []

    for entry in har['log']['entries']:
        url = entry['request']['url']

        entry_str = json.dumps(entry, ensure_ascii=False, sort_keys=True)
        if target_str in entry_str:
            res.append(entry)

    return {har_path: res}


def get_entry_by_md5(har, md5):
    """
    通过 md5 获取 entry
    :param har: har 字典对象或 .har 文件路径
    :param md5: entry 的 md5
    :return: 返回 entry，找不到则抛出异常
    """

    if isinstance(har, str) and os.path.exists(har):
        with open(har, "r", encoding="utf-8-sig") as f:
            har = json.load(f)
    elif not isinstance(har, dict):
        raise ValueError("har must be a dict or a valid file path")

    for entry in har['log']['entries']:
        if get_md5_from_entry(entry) == md5:
            return entry

    return None


def url_decode(target_url):
    """URL 解码"""
    return urllib.parse.unquote(target_url)


if __name__ == '__main__':
    menu = ['1. 通过 md5 查找 entry',
            '2. 查找包含特定字符串的 entry',
            '3. URL 解码', ]
    menu_text = "\n".join(menu) + "\n请选择操作："

    while True:
        option = input(menu_text)

        if option == "1":
            md5 = input("输入 md5：")
            only_hash = input("只查找 md5 文件？(y/all, press Enter to y)")
            if only_hash.lower() != "all":
                only_hash = True
            else:
                only_hash = False

            print_entry_by_md5(md5, only_hash=only_hash)

        elif option == "2":
            target_str = input("输入要查找的字符串：")
            if target_str == "":
                print("无效输入，请重新输入")
                continue

            only_hash = input("只查找 md5 文件？(y/all, press Enter to y)")
            if only_hash.lower() != "all":
                only_hash = True
            else:
                only_hash = False

            short_print = input('只显示关键词前后 x 行？(默认 5, 输入 0 为完整打印): ')
            if short_print == "":
                short_print = 5
            else:
                short_print = int(short_print)

            get_entries_with_str(target_str, only_hash=only_hash, print_context=int(short_print))

        elif option == "3":
            url = input("输入待解码的 URL: ")
            print(f'解码前的 url: \n{url}'
                  f'')
            print(f'解码后的 url: \n{url_decode(url)}')

        else:
            print("无效输入，请重新输入")

        print(f'\n{bold_split}\n')
