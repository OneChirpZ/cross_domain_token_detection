# （keyname）根据 keyname 识别 token
token_key_names = ['key', 'token', 'secret', 'signature']
token_prefixes = ['session', 'access', 'auth', 'oauth', 'user', 'client', 'api', 'refresh']
token_others = ['jwt', 'bearer']

# （compare）根据多请求共有的 value 识别 token
stop_words = list({s.lower() for s in ['accept-encoding', 'connection', 'content-length', 'content-type',
                                       'host', 'hosts', 'accept-encoding', 'accept-language', 'user-agent',
                                       'sessionid', 'referer', 'cache-control', 'X-MMe-Client-Info']})

# （compare）提取的 value 的最小长度
min_token_len = 8

# 输出分隔符
bold_split = "==============================================================="
thin_split = "---------------------------------------------------------------"
