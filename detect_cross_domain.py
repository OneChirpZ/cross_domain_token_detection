from urllib.parse import urlparse

from global_config import bold_split


def get_domain(url, domain_level=0, with_suffix=False):
    """
    从 URL 中提取域名
    :param url: 完整的 URL
    :param domain_level: 域名级别
        0: 返回完整域名
        1: 仅返回顶级域名
        2: 仅返回次级域名（二级域名）
        ...
    :param with_suffix: 是否包含域名后缀
    :return: 返回提取到的域名，如果不存在则返回空字符串
    """

    if domain_level == 0:
        return urlparse(url).netloc

    domain_name = urlparse(url).netloc
    domain_parts = domain_name.split('.')

    if len(domain_parts) < domain_level:
        return ''

    if with_suffix:
        return '.'.join(domain_parts[-domain_level:])
    else:
        domain_parts.reverse()
        return domain_parts[domain_level - 1]


def is_same_domain(url1, url2, level=2, with_suffix=False):
    """
    检查两个 URL 是否来自同一个域名，忽略 www 前缀，并根据指定的 level 进行域名比较。
    :param level: 域名比较的级别
        level 0: 完整域名比较
        level 1: 顶级域名比较
        level 2: 二级域名比较 (常用)
        ...
    :param with_suffix: 比较时是否包含域名后缀（包含更顶级的域名）
    :return: 两个 URL 是否来自同一个域名
    """
    domain1 = get_domain(url1, domain_level=level, with_suffix=with_suffix)
    domain2 = get_domain(url2, domain_level=level, with_suffix=with_suffix)

    return domain1 == domain2


def group_by_domain(urls, level=2, with_suffix=False):
    """
    将 URL 列表按照域名进行分组
    :param urls: list[tuple(url, md5), tuple(url, md5), ...]
    :param level: 同 is_same_domain 方法
    :param with_suffix: 同 is_same_domain 方法
    :return: 返回分组后的二维列表, 第二维每个子列表中的 url 为同一个 domain，[[same domain urls], [same domain urls], ...]
    """
    res = []
    for i in range(len(urls)):
        for j in range(i + 1, len(urls)):
            if is_same_domain(urls[i][0], urls[j][0], level=level, with_suffix=with_suffix):
                res.append([urls[i], urls[j]])

    res = merge_lists(res)

    # 将没有 grouped 的 URL 单独放入一个子列表
    for url in urls:
        if not any(url in group for group in res):
            res.append([url])

    return res


def merge_lists(lst):
    """
    对二维列表中的第二维（子列表们）进行合并，合并的依据是两个被合并的子列表中有公共元素
    例如：[[1, 2], [3, 4, 5], [2, 7]] -> [[1, 2, 7], [3, 4, 5]]
    :param lst: 应是一个二维列表，不会对该列表进行修改
    :return: 返回新的列表
    """
    # 创建一个字典来存储元素与其所在子列表的映射
    element_to_set = {}
    merged_sets = []

    for sublist in lst:
        current_set = set(sublist)
        to_merge = []

        # 找出所有需要合并的集合
        for element in sublist:
            if element in element_to_set:
                existing_set = element_to_set[element]
                if existing_set not in to_merge:
                    to_merge.append(existing_set)
                    current_set |= existing_set

        # 合并子集，并更新字典中的映射
        for s in to_merge:
            merged_sets.remove(s)
        merged_sets.append(current_set)

        # 更新字典中元素到其所属集合的映射
        for element in current_set:
            element_to_set[element] = current_set

    # 将集合转换回列表
    return [list(s) for s in merged_sets]


# 测试函数
def test():
    url1 = "http://www.example.com/path/to/page"
    url2 = "https://example.com/another/path"
    url3 = "http://sub.example.com/different/path"

    url4 = "http://sub.example2.org/different/path"
    url5 = "http://sub.example2.com/different/path2"
    url6 = "http://services.example2.com/v1/path3"

    urls = [(url1, 1), (url2, 2), (url3, 3), (url4, 4), (url5, 5), (url6, 6)]

    res1 = group_by_domain(urls, level=2, with_suffix=True)
    for group in res1:
        print(group)

    print(bold_split)

    res2 = group_by_domain(urls, level=2, with_suffix=False)
    for group in res2:
        print(group)


if __name__ == '__main__':
    test()
    pass
