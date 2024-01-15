# coding=utf-8
import redis_util
import os

import json
import time
import uuid

__tailparam = ''' -H "authority: www.taptap.com" -H "accept: application/json, text/plain, */*" -H "sec-fetch-dest: empty" -H "x-xsrf-token:'''
__tailparam2 = '''" -H "x-requested-with: XMLHttpRequest" -H "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0" -H "sec-fetch-site: same-origin" -H "sec-fetch-mode: cors" -H "referer: https://www.taptap.com/app/226776/review?sort=new" -H "accept-language: zh-CN,zh;q=0.9" -H "cookie:'''



def start_cookie_reply(pid):
    index = 0
    try:
        crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(crawler_time)


        strtmp = "relayloop, index= %d time= %s ,pid=%d" % (index, crawler_time, pid)
        print(strtmp)

        run_createcookie(pid)
        run_createparam(pid)

        index = index + 1
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        print("error,try again")
        time.sleep(10)


#
def run_createcookie(pid):
    try:
        cmd = "node get_cookies.js"
        status = os.system(cmd)
        if 0 != status:
            print("执行node get_cookies.js失败")
    except:
        print("执行node get_cookies.js出现异常")


def run_createparam(pid):

    filename = "cookies.json"
    f = open(filename, "r", encoding='UTF-8-sig')
    filestr = f.read()
    f.close()

    data = json.loads(filestr)
    cookiestr = ""
    xsrftoken = ""
    for v in data:
        if v['name'] == 'XSRF-TOKEN':
            xsrftoken = v['value']
        cookiestr = cookiestr + v['name'] + "=" + v['value'] + ";"

    localparam = __tailparam + xsrftoken + __tailparam2 + cookiestr + '''"'''

    redis_util.REDIS_UTIL.set("tapcookie_create", pid, str(localparam))

    redis_util.REDIS_UTIL.set("xsrftoken", pid, str(xsrftoken))
    redis_util.REDIS_UTIL.set("cookiestr", pid, str(cookiestr))

    cookieuuid = str(uuid.uuid4())
    redis_util.REDIS_UTIL.set("tapcookie_uuid", pid, cookieuuid)


if __name__ == '__main__':
    start_cookie_reply()
    # run_createcookie()
