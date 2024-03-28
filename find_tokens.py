from urllib.parse import urlparse, parse_qs

from base import is_token_key


def find_tokens_in_url(url, level=0):
    """
    从 URL 中提取 tokens
    :param url: 完整的 URL
    :param level: 检测等级
    :return: 返回提取到的 tokens 字典
    """

    tokens = {}

    query = urlparse(url).query
    params = parse_qs(query)

    for key, values in params.items():
        if is_token_key(key, level):
            if len(values) != 1:
                raise ValueError(f'values has more than one item: {values}')

            tokens[key] = values[0]

    return tokens


def find_tokens_in_headers(headers, level=0):
    """
    从 headers 中提取 tokens
    :param headers: headers 字典
    :param level: 检测等级
    :return: 返回提取到的 tokens 字典
    """

    tokens = {}

    for header in headers:
        for key, value in header.items():
            if is_token_key(key, level):
                tokens[key] = value

    return tokens


def find_tokens_in_post_body(post_body, level=0):
    """
    从 post_body 中提取 tokens
    :param post_body: post_body 字符串
    :param level: 检测等级
    :return: 返回提取到的 tokens 字典
    """

    tokens = {}

    # TODO: 从 post_body 中提取 tokens
    pass

    return tokens
