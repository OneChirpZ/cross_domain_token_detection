import json
from urllib.parse import urlparse, parse_qs

from base import is_token_key


def find_tokens_in_url(url, level=0, enable_stopwords=True):
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
        if is_token_key(key, level, enable_stopwords):
            if len(values) != 1:
                raise ValueError(f'values has more than one item: {values}')

            tokens[key] = values[0]

    return tokens


def find_tokens_in_headers(headers, level=0, enable_stopwords=True):
    """
    从 headers 中提取 tokens
    :param headers: headers 字典
    :param level: 检测等级
    :return: 返回提取到的 tokens 字典
    """

    tokens = {}

    for header in headers:
        if is_token_key(header['name'], level, enable_stopwords):
            # print(f"key: {header['name']}, value: {header['value']}")
            tokens[header['name']] = header['value']

    return tokens


def find_tokens_in_post_body(post_data, level=0, enable_stopwords=True):
    """
    从 post_body 中提取 tokens
    :param post_data: post_data 字典
    :param level: 检测等级
    :return: 返回提取到的 tokens 字典
    """

    tokens = {}

    # 暂先只考虑了从mimeType为 'application/json' , 'application/x-www-form-urlencoded' 的表单数据里找token
    # 根据 application/json 类型 post data 里的 text 字典里的 key 来判断是否有 token 可能存在
    if post_data['mimeType'] == 'application/json':
        # 如果不以 { 或者 [ 开头，则返回
        # sf_mad.har 有一段 text = 'datalist=...(部分可由base64解码)'，为避免 json.loads受影响用此方法将其过滤，详情见飞书
        if not (post_data['text'].startswith('[') or post_data['text'].startswith('{')):
            return tokens

        text_dict = json.loads(post_data['text'])

        # 如果解析出的是列表，并且列表不为空，则取出第一个元素
        if isinstance(text_dict, list) and len(text_dict) > 0:
            for t in text_dict:
                for key, value in t.items():
                    if is_token_key(key, level, enable_stopwords) and value != '':
                        tokens[key] = value

        elif isinstance(text_dict, dict):
            for key, value in text_dict.items():
                if is_token_key(key, level, enable_stopwords) and value != '':
                    tokens[key] = value

        else:
            raise ValueError(f'post_data["text"] is not a dict or a list, but "{type(text_dict)}"')

    # 根据 application/x-www-form-urlencoded 类型 post data 里的
    # params 里的 name 来判断是否有 token 可能存在
    elif post_data['mimeType'] == 'application/x-www-form-urlencoded':
        for param in post_data['params']:
            if is_token_key(param['name'], level, enable_stopwords):
                tokens[param['name']] = param['value']

    return tokens
