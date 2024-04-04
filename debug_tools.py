import json
import os

from base import get_md5_from_entry
from global_config import bold_split, thin_split


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


def get_entries_with_str(target_str, only_hash=True):
    har_files = os.listdir("./har_files")

    res = []
    for har_file in har_files:
        if har_file.endswith(".har"):
            if only_hash and not har_file.endswith("_md5.har"):
                continue

            har_file_path = os.path.join("./har_files", har_file)

            res += get_entries_with_str_in_har(har_file_path, target_str)

    print(f'找到 {len(res)} 个 entry，包含字符串 "{target_str}"')

    if len(res) != 0:
        show_res = input("是否显示结果？(y/n)")
        if show_res.lower() != "n":
            count = 0
            for entry in res:
                count += 1
                print(f"{thin_split}\n"
                      f"entry {count} / {len(res)}:\n"
                      f"{json.dumps(entry, ensure_ascii=False, indent=2)}\n"
                      f"{thin_split}")


def get_entries_with_str_in_har(har_path, target_str):
    """在 har 的 entries 中，查找包含特定字符串的 entry，返回符合条件的 entry 列表"""

    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)
    res = []

    for entry in har['log']['entries']:
        url = entry['request']['url']

        entry_str = json.dumps(entry, ensure_ascii=False, sort_keys=True)
        if target_str in entry_str:
            res.append(entry)

    return res


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
    import urllib.parse
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

            get_entries_with_str(target_str, only_hash=only_hash)

        elif option == "3":
            url = input("输入待解码的 URL: ")
            print(f'解码前的 url: |{url}|')
            print(f'解码后的 url: |{url_decode(url)}|')

        else:
            print("无效输入，请重新输入")

        print(f'\n{bold_split}\n')
