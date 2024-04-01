from urllib.parse import urlparse


def normalize_domain(domain, level):
    """
    返回
    :param domain: 原始域名
    :param level:
        level 2: 只返回顶级域名
        level 3: 返回顶级域名和次级域名
    :return:
    """

    # 按点分割域名，逆序排列以方便提取顶级域名及次级域名
    parts = domain.split('.')
    parts.reverse()

    # 提取指定级别的域名部分
    domain_parts = parts[:level]
    domain_parts.reverse()

    return '.'.join(domain_parts)


def is_same_domain(url1, url2, level):
    """
    检查两个 URL 是否来自同一个域名，忽略 www 前缀，并根据指定的 level 进行域名比较。
    :param level:
        level 1: 只返回顶级域名
        level 2: 返回顶级域名和次级域名
    :return: 两个 URL 是否来自同一个域名
    """
    domain1 = urlparse(url1).netloc
    domain2 = urlparse(url2).netloc

    normalized_domain1 = normalize_domain(domain1, level)
    normalized_domain2 = normalize_domain(domain2, level)

    print(f"level: {level}")
    print(f"domain1: {domain1}")
    print(f"domain2: {domain2}")
    print(f"normalized_domain1: {normalized_domain1}")
    print(f"normalized_domain2: {normalized_domain2}")

    return normalized_domain1 == normalized_domain2


# 测试函数
def test():
    url1 = "http://www.example.com/path/to/page"
    url2 = "https://example.com/another/path"
    url3 = "http://sub.example.com/different/path"
    url4 = "http://sub.example.org/different/path"

    print(is_same_domain(url1, url2, level=2))  # 应该输出 True
    print(is_same_domain(url1, url3, level=3))  # 应该输出 False
    print(is_same_domain(url3, url4, level=3))  # 应该输出 True


if __name__ == '__main__':
    test()
