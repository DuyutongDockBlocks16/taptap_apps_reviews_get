url = 'https://www.taptap.com/webapiv2/review/v2/by-app?app_id=137515&from=120&limit=10&sort=new&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D65%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D9d960b45-4e34-425a-9447-1252e59ab04b%26DT%3DPC%26OS%3DWindows%26OSV%3D10'
app_id = 137515
import os
import time

import mysql_operate
from config import GET_TAIL_PARAM, GET_HEADERS, WEBSITE_NAME
import json
import requests
import re


def __getapiinfo(url, pre_function, user_id, function=''):
    response = requests.get(url, headers=GET_HEADERS(pre_function, user_id, function))
    print(url)
    data = json.loads(response.text)
    return data


__getapiinfo(url, '/app', '/' + str(app_id), '/review')
