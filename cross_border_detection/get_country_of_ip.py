import json
import os
import socket

import geoip2.database
import urllib.parse

from global_config import hostname_blacklist


def get_country_by_ip(ip_address):
    db_path = r'./geolite2/GeoLite2-Country.mmdb'

    try:
        with geoip2.database.Reader(db_path) as reader:
            response = reader.country(ip_address)
            country = response.country.name
            return country
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_all_hostname_from_zap_har(har, only_hostname=True, enable_blacklist=True):
    """
    从 zap 的 har 中提取所有的 url 或主机名
    :param har: zap 生成的 har，字典或文件路径
    :param only_hostname: 是否只返回 hostname
    :param enable_blacklist: 是否启用 hostname 黑名单
    :return: 返回不重复 url 列表
    """
    if isinstance(har, str) and os.path.exists(har):
        with open(har, "r", encoding="utf-8-sig") as f:
            har = json.load(f)
    elif not isinstance(har, dict):
        raise ValueError("har is not a dict or a valid file path")

    urls = []
    for entry in har['log']['entries']:
        url = entry['request']['url']

        # 屏蔽 localhost 等主机名
        if enable_blacklist and get_hostname_from_url(url) in hostname_blacklist:
            continue

        if only_hostname:
            urls.append(get_hostname_from_url(url))
        else:
            urls.append(url)
    return list(set(urls))


def get_hostname_from_url(url):
    return urllib.parse.urlparse(url).hostname


def get_ip_from_hostname(hostname):
    """通过主机名获取 IP 地址"""
    try:
        host_info = socket.getaddrinfo(hostname, None)
        ip_addresses = list(set([info[4][0] for info in host_info]))
        return ip_addresses
    except socket.gaierror as e:
        print(f"获取 IP 地址失败: {e}")
        return []


def test_ip_to_country():
    print(get_country_by_ip('8.8.8.8'))
    print(get_country_by_ip('114.114.114.114'))


def test_har_to_country(only_print_non_China=False):
    har_root_dir = r'../har_files/ZAP_test_20240810'
    har_files = [f for f in os.listdir(har_root_dir) if f.endswith('.har')]

    for har_file in har_files:
        print(f"处理 {har_file}...")

        har_file_path = os.path.join(har_root_dir, har_file)
        all_hostnames = get_all_hostname_from_zap_har(har_file_path)

        for hostname in all_hostnames:

            ip_addresses = get_ip_from_hostname(hostname)
            cnt = 0
            for ip_address in ip_addresses:
                country = get_country_by_ip(ip_address)
                if only_print_non_China and country == 'China':
                    continue

                # 这里我也不知道该怎么 print 了
                if country:
                    cnt += 1
                if cnt == 1:
                    print(f"hostname: {hostname}")
                print(f"IP {cnt}: {ip_address}, Country: {country}")
            if cnt != 0:
                print(r'-' * 40)

        print(r'=' * 60)


if __name__ == '__main__':
    test_har_to_country(only_print_non_China=True)