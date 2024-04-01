import hashlib
import json

from global_config import token_key_names, token_others


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

    if isinstance(param_keyname, str):
        param_keyname = param_keyname.lower()
    else:
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
