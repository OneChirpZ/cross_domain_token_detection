import json
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
        # 这里的key = 'name/value', value = 'Connection/Close...'，搜寻无效
        # for key, value in header.items():
        #     print(f"key:{key}, value:{value}")
        #     if is_token_key(key, level):
        #         tokens[key] = value
        # 改为：
        if is_token_key(header['name'], level):
            # debug
            # print(f"key: {header['name']}, value: {header['value']}")

            tokens[header['name']] = header['value']

    return tokens


def find_tokens_in_post_body(post_data, level=0):
    """
    从 post_body 中提取 tokens
    :param post_data: post_data 字典
    :param level: 检测等级
    :return: 返回提取到的 tokens 字典
    """

    tokens = {}

    # TODO: 从 post_body 中提取 tokens
    # 暂先只考虑了从mimeType为 'application/json' , 'application/x-www-form-urlencoded'的表单数据里找token

    # 根据 application/json 类型 postdata 里的 text 字典里的 key 来判断是否有 token 可能存在
    if post_data['mimeType'] == 'application/json':
        # 不以 { 或者 [ 开头，返回：sf_mad.har有一 text = 'datalist=...(部分可由base64解码)'，为避免 json.loads受影响用此方法将其过滤，详情见飞书
        if not (post_data['text'].startswith('[') or post_data['text'].startswith('{')):
            return tokens

        # 将json文本转成字典对其key进行判断，符合的存入tokens
        text_str = post_data['text']
        text_dict = json.loads(text_str)

        # 如果解析出的是列表，并且列表不为空，则取出第一个元素
        if isinstance(text_dict, list) and len(text_dict) > 0:
            text_dict = text_dict[0]

        for key, value in text_dict.items():
            if is_token_key(key, level) and value != '':
                tokens[key] = value
                # debug
                print(f"key: {key}, value: {value}")

        return tokens

    # 根据 application/x-www-form-urlencoded 类型 postdata 里的 params 里的 name 来判断是否有 token 可能存在
    if post_data['mimeType'] == 'application/x-www-form-urlencoded':
        for par in post_data['params']:
            if is_token_key(par['name'], level):
                tokens[par['name']] = par['value']
                # debug
                # print(f"name: {par['name']}, value: {par['value']}")
        return tokens

    return tokens
