import hashlib
import json
import os

from global_config import token_key_names, token_others, bold_split, thin_split


def is_token_key(param_keyname, level=0):
    """
    判断参数名是否为token
    :param param_keyname: 参数名
    :param level: 检测等级
        level 0: keyname 精确匹配 token_key_names 中的任意一个
        level 1: keyname 中包含 token_key_names 中的任意一个
        level 2: level 1 + keyname 中包含 token_others 中的任意一个
    :return: 返回是否为token
    """

    param_keyname = param_keyname.lower()

    if param_keyname in token_key_names:
        return True

    if level >= 1 and any(key_name in param_keyname for key_name in token_key_names):
        return True

    if level >= 2 and any(other in param_keyname for other in token_others):
        return True

    return False


def get_md5_from_entry(entry):
    """
    从 entry 中获取 md5, 如果没有则生成并添加到 entry 中
    :param entry: entry 字典
    :return: 返回 md5
    """

    if 'md5' not in entry.keys():
        entry_str = json.dumps(entry, ensure_ascii=False, sort_keys=True)
        entry_hash = hashlib.md5(entry_str.encode()).hexdigest()
        entry['md5'] = entry_hash

    return entry['md5']


def get_entries_with_str(har_path, target_str, enable_print=False):
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


def get_entry_by_md5(har, md5):
    """
    通过 md5 获取 entry
    :param har: har 字典对象或 .har 文件路径
    :param md5: entry 的 md5
    :return: 返回 entry，找不到则返回 None
    """

    if isinstance(har, str) and os.path.exists(har):
        with open(har, "r", encoding="utf-8-sig") as f:
            har = json.load(f)

    for entry in har['log']['entries']:
        if get_md5_from_entry(entry) == md5:
            return entry

    return None
