import hashlib
import json
import os

from global_config import token_key_names, token_others, stop_words_key, bold_split, thin_split


def is_token_key(param_keyname, level=0, enable_stopwords=True):
    """
    判断参数名是否为token
    :param enable_stopwords: 是否启用停用词过滤
    :param param_keyname: 参数名
    :param level: 检测等级
        level 0: keyname 精确匹配 token_key_names 中的任意一个
        level 1: keyname 中包含 token_key_names 中的任意一个
        level 2: level 1 + keyname 中包含 token_others 中的任意一个
    :return: 返回是否为token
    """

    if isinstance(param_keyname, str):
        param_keyname = param_keyname.lower()
    elif param_keyname is None:
        return False
    else:
        raise ValueError(f"param_keyname is not a string, but {type(param_keyname)}")

    if enable_stopwords and param_keyname.lower() in stop_words_key:
        return False

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


def get_test_file_list(only_hash=True, enable_print=False):
    """获取测试文件列表"""

    def to_YYYY_MM_DD(date):
        return f"20{date[:2]}-{date[2:4]}-{date[4:]}"

    file_paths = {}
    for root, dirs, files in os.walk("./har_files"):
        for file in files:
            if file.endswith('.har'):
                if only_hash and not file.endswith("_md5.har"):
                    continue
                file_name, ext = os.path.splitext(file)
                file_date = to_YYYY_MM_DD(file_name.split('_')[1])
                file_paths.setdefault(file_date, []).append(os.path.join(root, file))

    if enable_print:
        for date in sorted(file_paths.keys()):
            print(f"{date}: {len(file_paths[date])} files")
            for file in file_paths[date]:
                print(f"    {file}")

    return file_paths


def select_test_files_by_date(file_paths=None, only_hash=True):
    """根据日期获取待测试的文件路径列表"""
    if file_paths is None:
        file_paths = get_test_file_list(only_hash=only_hash,
                                        enable_print=False)

    wanted_paths = []
    for date in sorted(file_paths.keys(), reverse=True):
        print(f"{date}: {len(file_paths[date])} files")
        for file in file_paths[date]:
            print(f"    {file}")

        options = input("Add? Press y/n (default add): ")
        if options.lower() != 'n':
            wanted_paths.extend(file_paths[date])

        ctn = input("Continue? Press y/n (default continue): ")
        if ctn.lower() == 'n':
            break

        print(f"\n{thin_split}")

    print(bold_split)

    return wanted_paths
