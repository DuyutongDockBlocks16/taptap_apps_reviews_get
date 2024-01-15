# coding=utf-8
import redis_util
import os

__tailparampre = "X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D65%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3D" \
                 "Android%26UID%3D"

def GET_TAIL_PARAM(pid):
    localparam = redis_util.REDIS_UTIL.get("tapcookie_uuid", pid)
    if None != localparam:
        localparam = localparam.decode('utf-8')
    else:
        localparam = ""
    return __tailparampre + localparam + "%26DT%3DPC%26OS%3DWindows%26OSV%3D10"


def GET_LOCAL_PARAM(pid):
    localparam = redis_util.REDIS_UTIL.get("tapcookie_create", pid)
    if None != localparam:
        localparam = localparam.decode('utf-8')
    else:
        localparam = ""

    return localparam


def GET_HEADERS(pid, pre_function, uid,  function=''):
    from fake_useragent import UserAgent

    # solution from https://blog.csdn.net/m0_37952030/article/details/84143738
    ua = UserAgent(use_cache_server=False)


    # cookie='locale=zh_CN; _uab_collina=165035278768870823362514; ACCOUNTS_USER_ID=456256367; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImVIdDA3eU1UbjJTajU1SGc5b2R5OWc9PSIsInZhbHVlIjoiS1lldThUWkl3aW92SE5rWFFva1FxM0dmcjFBd2loSzRwdVwvanRxdXYxMmpQcHBQR3Q5b1wvWUpDUnZTK01QK0tWckllTEJ1dmhPVFprMHdEQjJLTng0Q1RuWE9LUyttSXdhRjZlOFZiTnd5OD0iLCJtYWMiOiJiYTVkNzQ5NDc3ZTY3ODI2MmZhNDAzMDFkZGM5YTVkMmQwNTFkZGYyMDhjZDVmMWQzZjQ1MzIxZjBhYWI1OWYzIn0%3D; user_id=456256367; ACCOUNT_LOGGED_USER_FROM_WWW=2kG%2FCybeQv3ULFOWGtF8hA%3D%3D; CONSOLES_TOKEN_FROM_WWW=RUCfugONmNqNrGdinjoGUQ%3D%3D; GATEWAY_LOGGED_USER_FROM_WWW=cx0SCFgzIUtT-FSCQgfhhAXUQ7pTIHEseOfdlI-U38Gg3UtCixrEVg; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22456256367%22%2C%22%24device_id%22%3A%221804b2e9a32d12-0114610f2a753c-5d462912-2073600-1804b2e9a33bc6%22%2C%22props%22%3A%7B%7D%2C%22first_id%22%3A%221804b2e9a32d12-0114610f2a753c-5d462912-2073600-1804b2e9a33bc6%22%7D; tap_theme=light; acw_tc=276077c916506148292074390ecdc9586aadf32f6b2c522bdc075f68a7ecaf; acw_sc__v2=62626484f6fa52ca6b760debb9b364aac03f2e67; ssxmod_itna=eqUx0Dc70Qqmq0K40dD=wgDfG8TcDiKDCCIFRDBkDO4iNDnD8x7YDvImLK=I4PaQ+i3PAzlkpxzL4P4rfYtbOYoNdTDCPGnDB9+iOGQxii9DCeDIDWeDiDG4GmB4GtDpxG=yDm4i3jxWPDYxDrjOKDRxi7DD5Q8x07DQ5kijGxj=AF5Fywu60GqQDkD7HmDlP4Izg+vIfxlp+ODlIjDC91c2ICN4Gd/Wr3hW2eZiRoxHGYtQ4NwQxx4Xhxjnu4tjipTkG77nqKqDDWGg6DD=; ssxmod_itna2=eqUx0Dc70Qqmq0K40dD=wgDfG8TcDiKDCCIFD8qp0xGXxrYGa4cmOs1Kmym5KoG407K8x7=D+OiD; XSRF-TOKEN=eyJpdiI6IjRlbjRwbDJES3RCV1pwZlNBRUpJcHc9PSIsInZhbHVlIjoieDk0cHFDbmFwZEdhZlwva2NIQmxQZXZuc2EyTGU3amt4V0dSMk4wc2dFQXFPbWlKaUEyVDQwOW5wNHdqZGI3bTJZZjRNaFZoTW9CSUR4eDFcL0R5WVlwZz09IiwibWFjIjoiM2I2YjJiNjMzYThmZTU2ZWFmMjJhY2JmN2Y4NzNjNzIwZGY0Y2ZlMGMxMmNlMWY1MjJmN2RmZGE3MzMzOTRjMCJ9; tap_sess=eyJpdiI6IkE1SmhtVlVSMmlIVngyV3QwQ1VyWHc9PSIsInZhbHVlIjoiUVN0WmtTM3FUdnVwTXJjcCtrWFV2NjhYVGc4dDhnNlwvcWdCR2dja0o4Q1I3T0xqZ3NnR2I0WEl3VXlzdFJXbVZmMWhKMUhZN3JTdUZHNm02V3MwdG1BPT0iLCJtYWMiOiI3MWI1Y2ViYWE2N2U2MGFiNzVkZjU2NGMzMWI3MTYzYjFhMTBmMDhkNzZjZTdhNjNmMjQyMzRiZjY0NWU1MGIzIn0%3D'
    # x_xsrf_token='eyJpdiI6IjRlbjRwbDJES3RCV1pwZlNBRUpJcHc9PSIsInZhbHVlIjoieDk0cHFDbmFwZEdhZlwva2NIQmxQZXZuc2EyTGU3amt4V0dSMk4wc2dFQXFPbWlKaUEyVDQwOW5wNHdqZGI3bTJZZjRNaFZoTW9CSUR4eDFcL0R5WVlwZz09IiwibWFjIjoiM2I2YjJiNjMzYThmZTU2ZWFmMjJhY2JmN2Y4NzNjNzIwZGY0Y2ZlMGMxMmNlMWY1MjJmN2RmZGE3MzMzOTRjMCJ9'

    cookie = redis_util.REDIS_UTIL.get("cookiestr", pid)
    x_xsrf_token = redis_util.REDIS_UTIL.get("xsrftoken", pid)
    headers = {
        'authority': 'www.taptap.com',
        'accept': 'application/json, text/plain, */*',
        'sec-fetch-dest': 'empty',
        'x-xsrf-token': x_xsrf_token,
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': ua.random,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://www.taptap.com' + pre_function + uid + function,
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie
    }
    return headers


WEBSITE_NAME = 'https://www.taptap.com'

PER_APP_REVIEW_THRESHOLD = 10000


def GET_APP_ID_LIST():
    app_id_list = list()
    aim_game_dict = {
        # "烟雨江湖": (169054, 8930),
        # "放置奇兵": (19562, 8930),
        # "高能手办团": (187667, 8960),
        # "闪烁之光": (153837, 5350),
        # "上古有灵妖": (199139, 4920),
        # "魔镜物语": (220640, 3360),
        # "上古王冠": (204923, 6520),
        "小浣熊百将传": (210009, 6720),
        # "绯石之心": (159368, 3940),
        # "艾尔多战记": (216958, 7300),
        # "武林闲侠": (204487, 8940),
        # "剑与远征": 137515, # finish
        # "圣树唤歌": 212038, # finish
        # "千秋辞": 187386   # finish
    }
    for game_id in aim_game_dict.values():
        app_id_list.append(game_id)
    return app_id_list


APP_ID_LIST = [137515]

CMD_HANDLE = 'curl -s –connect-timeout 10 -m 20 "%s"'

# dev_env_mysql
# MYSQL_HOST = "192.168.58.6"
# MYSQL_PORT = 3306
# MYSQL_USER = "root"
# MYSQL_PASSWD = "123456"
# MYSQL_DB = "hxz_test"

# test_env_mysql
# MYSQL_HOST = "192.168.7.195"
# MYSQL_PORT = 4306
# MYSQL_USER = "dev_cag_rwl"
# MYSQL_PASSWD = "7D9gQwpiI8n4TyV"
# MYSQL_DB = "data_pub"

# aliyun
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_DB = "data_pub"
MYSQL_PASSWD = "7D9gQwpiI8n4TyV_7D9gQwpiI8n4TyV"
