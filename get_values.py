from urllib.parse import urlparse, parse_qs

from global_config import stop_words, min_token_len


def get_values_from_entry(entry, enable_stopwords=True, min_len=min_token_len):
    """
    从 entry 中提取 values
    :param min_len: 最小 token 长度
    :param entry: entry 字典
    :param enable_stopwords: 是否启用过滤
    :return: 返回提取到的 values 列表
    """

    values_url = get_values_from_url(entry['request']['url'], enable_stopwords)
    values_headers = get_values_from_headers(entry['request']['headers'], enable_stopwords)
    values_cookies = get_values_from_cookies(entry['request']['cookies'], enable_stopwords)

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
        if enable_stopwords and header_item['name'].lower() in stop_words:
            continue

        # 跳过 cookie，有单独的处理方式
        if header_item['name'].lower() == 'cookie':
            continue

        if len(header_item['value']) < min_len:
            continue

        # for debug
        # if header_item['value'].find('iPhone10,3') != -1:
        #     print(f'key: {header_item["name"]}, value: {header_item["value"]}')

        values.append(header_item['value'])

    return values


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
        if enable_stopwords and key.lower() in stop_words:
            continue

        for value in values:
            if len(value) < min_len:
                continue

            # for debug
            # if value.find('com.tencent.xin') != -1:
            #     print(f'key: {key}, value: {values}')

            res_values.append(value)

    return list(set(res_values))


def get_values_from_cookies(cookies, enable_stopwords=True, min_len=min_token_len):
    """
    从 cookies 中提取 values
    :param min_len: 最小 token 长度
    :param cookies: cookies 列表
    :param enable_stopwords: 是否启用 enable_stopwords 过滤
    :return: 返回提取到的 values 列表
    """

    values = []

    for cookie in cookies:
        # TODO: 从 cookie 中提取 value
        if enable_stopwords and cookie['name'].lower() in stop_words:
            continue

        if len(cookie['value']) < min_len:
            continue

        # 不确定对value进行过滤是否会错过信息，暂注释掉
        # if enable_stopwords and cookie['value'].lower() in value_stop_words:
        #     continue

        # for debug
        # print(f'COOKIE_KEY: {cookie["name"]}, COOKIE_VALUE: {cookie["value"]}')

        values.append(cookie['value'])

    return list(set(values))
