from urllib.parse import parse_qs, urlparse

token_key_names = ['key', 'token', 'secret', 'signature']
token_prefixes = ['session', 'access', 'auth', 'oauth', 'user', 'client', 'api', 'refresh']
token_others = ['jwt', 'bearer']

bold_split = "============================================"
thin_split = "--------------------------------------------"


def is_token_key(param_keyname, level=0):
    """
    判断参数名是否为token
    :param param_keyname: 参数名
    :param level: 检测等级
        level 0: keyname 精准匹配 token_key_names 中的任意一个
        level 1: level 0 + keyname 以 token_prefixes 中的任意一个开头，且包含 token_key_names 中的任意一个
        level 2: level 1 + keyname 中包含 token_others 中的任意一个
    :return: 返回是否为token
    """

    param_keyname = param_keyname.lower()

    if param_keyname in token_key_names:
        return True
    if (level >= 1
            and any(key_name in param_keyname for key_name in token_key_names)
            and any(param_keyname.startswith(prefix) for prefix in token_prefixes)):
        return True
    if level >= 2 and any(other in param_keyname for other in token_others):
        return True

    return False


def find_tokens_in_url(url, level=0):
    """
    从 URL 中提取 tokens
    :param url: 完整的 URL
    :param level: 检测等级
    :return: 返回提取到的 tokens 字典
    """

    tokens = {}

    try:
        query = urlparse(url).query
        params = parse_qs(query)

        for key, values in params.items():
            if is_token_key(key, level):
                tokens[key] = values[0]

    except Exception as e:
        print(f'Error parsing URL: {e}')

    return tokens


def test():
    """测试函数"""

    test_url = ('https://www.example.com/service/v1/'
                '?access_token=456'
                '&auth_secret=7A8b9C'
                '&time_stamp=12315'  # not a token
                '&user_id=65535'  # not a token
                '&client_bearer=gHi'
                '&token=a7a8XksAA78'
                '&api_key=jk342l123'
                '&refresh_token=mNo')

    for i in range(3):
        tokens = find_tokens_in_url(test_url, i)
        print(f'level {i} find {len(tokens)} tokens: {tokens}\n{bold_split}')


if __name__ == '__main__':
    test()
    pass
