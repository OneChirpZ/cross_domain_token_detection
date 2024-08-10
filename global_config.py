# （keyname）根据 keyname 识别 token
token_key_names = ['key', 'token', 'secret', 'signature']
token_prefixes = ['session', 'access', 'auth', 'oauth', 'user', 'client', 'api', 'refresh']
token_others = ['jwt', 'bearer']

# （compare）根据多请求共有的 value 识别 token
stop_words_key_wait_list = ['Origin', 'sec-ch-ua-platform', 'SDK-Version', 'Upload-Time', 'Sec-Fetch-Site',
                            'M-APPKEY', 'Accept', 'down_x', 'down_y', 'X-Requested-With', 'Sec-Fetch-Dest',
                            'Sec-Fetch-Mode', 'Origin', 'Referer']
stop_words_key = list({s.lower() for s in (['accept-encoding', 'connection', 'content-length', 'content-type',
                                            'host', 'hosts', 'accept-encoding', 'accept-language', 'user-agent',
                                            'sessionid', 'referer', 'cache-control', 'X-MMe-Client-Info',
                                            'timezone', 'appVersion', 'pragma-os', 'appver', 'reportVersion',
                                            'Proxy-Connection', 'Connection', 'app_ver', 'version'] +
                                           stop_words_key_wait_list)})

# stop_words_value = list({s.lower() for s in [' ', '\%']}) # 进一步过滤掉不符合token条件的value

# 提取的 token value 的最小长度
min_token_len = 8

# 主机名屏蔽列表
hostname_blacklist = ['localhost', '127.0.0.1', '0.0.0.0']

# 输出分隔符
bold_split = r'=' * 60
thin_split = r'-' * 60
