import json
from urllib.parse import urlparse, parse_qs

from global_config import stop_words_key, min_token_len


def get_values_from_entry(entry, enable_stopwords=True, min_len=min_token_len):
    """
    从 entry 中提取 values
    :param min_len: 最小 token 长度
    :param entry: entry 字典
    :param enable_stopwords: 是否启用过滤
    :return: 返回提取到的 values 列表
    """

    values_url = get_values_from_url(entry['request']['url'],
                                     enable_stopwords=enable_stopwords,
                                     min_len=min_len)

    values_headers = get_values_from_headers(entry['request']['headers'],
                                             enable_stopwords=enable_stopwords,
                                             min_len=min_len)

    values_cookies = get_values_from_cookies(entry['request']['cookies'],
                                             enable_stopwords=enable_stopwords,
                                             min_len=min_len)

    # try:
    #     values_cookies = get_values_from_cookies(entry['request']['cookies'], enable_stopwords)
    # except ValueError as e:
    #     print(f"error: {e}")
    #     print(f"entry: {json.dumps(entry, ensure_ascii=False, sort_keys=True, indent=2)}")

    return list(set(values_url + values_headers + values_cookies))


def get_values_from_headers(headers, enable_stopwords=True, min_len=min_token_len):
    """
    从 headers 中提取 values
    :param min_len: 最小 token 长度
    :param headers: headers 字典
    :param enable_stopwords: 是否启用过滤
    :return: 返回提取到的 values 列表
    """

    values = []

    for header_item in headers:
        # print(f"debug: header_item: {header_item}")
        if enable_stopwords and header_item['name'].lower() in stop_words_key:
            continue

        if header_item['name'].lower() == 'cookie':
            # cookie 以字符串形式重复出现在 headers 中
            # 已经在 entry['request']['cookies'] 中提取过了
            # values.extend(get_values_from_cookies(header_item['value'], enable_stopwords))
            continue

        if len(header_item['value']) < min_len:
            continue

        # if header_item['value'].find('iPhone10,3') != -1:
        #     print(f'debug: key: {header_item["name"]}, value: {header_item["value"]}')

        values.append(header_item['value'])

    return values


def get_values_from_cookies(cookies, enable_stopwords=True, min_len=min_token_len):
    """
    从 cookies 中提取 values，注意 entry['request']['headers'] 中，和 entry['request']['cookies'] 均有 cookie
    :param min_len: 最小 token 长度
    :param cookies: 支持 cookies 列表，或 http header 中的 cookie 字符串
    :param enable_stopwords: 是否启用 enable_stopwords 过滤
    :return: 返回提取到的 values 列表
    """

    values = []

    if not cookies:
        return values

    if isinstance(cookies, str):  # http header 中的 cookie 字符串，位于 entry['request']['headers'] 中的 cookie 字段
        cookie_list = [c.strip() for c in cookies.split(';')]

        for cookie in cookie_list:
            cookie_key, cookie_value = cookie.split('=', maxsplit=1)

            if enable_stopwords and cookie_key.lower() in stop_words_key:
                continue
            if len(cookie_value) < min_len:
                continue

            values.append(cookie_value)

    elif isinstance(cookies, list):  # cookies 列表，位于 entry['request']['cookies']
        for cookie in cookies:
            if enable_stopwords and cookie['name'].lower() in stop_words_key:
                continue
            if len(cookie['value']) < min_len:
                continue

            values.append(cookie['value'])

    else:
        raise ValueError('cookies is not a string or list')

    return list(set(values))


def get_values_from_url(url, enable_stopwords=True, min_len=min_token_len):
    """
    从 URL 中提取 values
    :param min_len: 最小 token 长度
    :param url: 完整的 URL
    :param enable_stopwords: 是否启用 stopwords 过滤
    :return: 返回提取到的 values 列表
    """

    res_values = []

    query = urlparse(url).query
    params = parse_qs(query)

    for key, values in params.items():
        if enable_stopwords and key.lower() in stop_words_key:
            continue

        for value in values:
            if len(value) < min_len:
                continue

            # for debug
            # if value.find('com.tencent.xin') != -1:
            #     print(f'key: {key}, value: {values}')

            res_values.append(value)

    return list(set(res_values))
