# coding=utf-8
import os
import time

import mysql_operate
from config import GET_TAIL_PARAM, GET_HEADERS, WEBSITE_NAME, PER_APP_REVIEW_THRESHOLD
import json
import requests
import re
from new_cookie_create import start_cookie_reply
import random


class TapInfoGet:
    def __init__(self):
        # 初始化，获取进程id以及程序开始执行的时间
        self.pid = os.getpid()
        self.crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")

        pass

    def __get_next_page(self, data):
        return data.get('next_page')

    def select_from_user_review(self):
        submit_sql = f"SELECT USER_ID FROM game_review WHERE USER_ID not in (SELECT user_id from user_review ur) GROUP BY USER_ID;"
        data = mysql_operate.db.select_db(submit_sql)
        return data

    def __getapiinfo(self, url, pre_function, user_id, function=''):
        # 获取response
        response = requests.get(url, headers=GET_HEADERS(self.pid, pre_function, user_id, function))

        print(f"pid= {self.pid} time= {self.crawler_time}  len of response.text : {len(response.text)}")
        try:
            data = json.loads(response.text)
            # 每次成功获取data的json后随机sleep,防止被taptap判断为机器人
            time.sleep(random.randint(0, 20))
            start_cookie_reply(self.pid)
            return data
        except Exception as e:
            # 如果失败了,就随机sleep多一些时间
            print(f"pid= {self.pid} time= {self.crawler_time}  __getapiinfo expect: {e} ,now sleep 300")
            time.sleep(600+random.randint(600, 1200))
            start_cookie_reply(self.pid)
            return self.__getapiinfo(url, pre_function, user_id, function)

    # 用命令行的方式获取数据,已经被废弃了
    def __getapiinfo_cmd(self, url, pre_function, user_id, function=''):
        cmd = 'curl -s –connect-timeout 10 -m 20 "%s"' % url + GET_TAIL_PARAM(self.pid)
        data = json.loads(os.popen(cmd).read())
        return data

    # 获取游戏的tag
    def __get_tags(self, tags, game_id):
        game_id = str(game_id)
        # 去数据库里面查这个game的tag是否已经存在
        review_check_sql = f"SELECT IFNULL((SELECT TRUE FROM user_game_label WHERE game_id={game_id} LIMIT 1),FALSE) "
        print(f"pid= {self.pid} time= {self.crawler_time} review_check_sql: {review_check_sql}")
        result_data = mysql_operate.db.select_db(review_check_sql)[0].values()
        check_result_list = list()
        for result in result_data:
            check_result_list.append(result)
        check_result = check_result_list[0]
        # 如果这个游戏的tag已经被记录过了，或者有tags，才写入数据库
        if check_result == 0 and tags:
            for tag in tags:
                submit_sql = "INSERT INTO user_game_label(" \
                             "game_id, " \
                             "label_id, " \
                             "label_name) " \
                             "VALUES('{}', '{}', '{}')". \
                    format(game_id,
                           str(tag.get('id')),
                           str(tag.get('value'))
                           )
                mysql_operate.db.execute_db(submit_sql)

    # 获取游戏的信息
    def app_detail(self, app_id):
        start_cookie_reply(self.pid)
        url = WEBSITE_NAME + f"/webapiv2/app/v2/detail-by-id/{app_id}?" + GET_TAIL_PARAM(self.pid)
        print(f"pid= {self.pid} time= {self.crawler_time} url:{url}")
        raw_appdetail = self.__getapiinfo(url, '/app', '/' + str(app_id))
        # raw_appdetail = self.__getapiinfo_cmd(url, '/app', '/' + str(app_id))

        app_data = raw_appdetail.get('data')
        app_id_info = app_data.get('id')

        for i in app_data.get('tags'):
            submit_sql = "INSERT INTO game_label(game_id, label_id, label_name) " \
                         "VALUES('{}', '{}', '{}')".format(str(app_id_info),
                                                           str(i.get('id')),
                                                           str(i.get('value'))
                                                           )
            mysql_operate.db.execute_db(submit_sql)

        review_count = app_data.get('stat').get('review_count')
        submit_sql = "INSERT INTO game_info(game_id, game_name, review_num , rating) " \
                     "VALUES('{}', '{}', '{}', '{}')".format(str(app_id_info),
                                                             str(app_data.get('title')),
                                                             str(review_count),
                                                             str(app_data.get('stat').get('rating')).replace("\'", "\"")
                                                             )
        mysql_operate.db.execute_db(submit_sql)

        return review_count

    # 获取游戏下的评论
    def app_review(self, app_id, from_num):
        user_list = list()
        cop = re.compile("[^0-9a-zA-Z\u4e00-\u9fa5.，,。？…&“”《》~_（）<>！；：]")
        num = 1
        url = WEBSITE_NAME + f"/webapiv2/review/v2/by-app?app_id={app_id}&from={from_num}&limit=10&sort=new&" + GET_TAIL_PARAM(self.pid)
        while True:
            time.sleep(10)
            if num >= PER_APP_REVIEW_THRESHOLD:
                print(f"pid= {self.pid} time= {self.crawler_time} app_review is reached PER_APP_REVIEW_THRESHOLD,break")
                break
            if num % 7 == 0:
                start_cookie_reply(self.pid)
            raw_review_data = self.__getapiinfo(url, '/app', '/' + str(app_id), '/review')
            # raw_review_data = self.__getapiinfo_cmd(url, '/app', '/' + str(app_id), '/review')
            print(f"pid= {self.pid} time= {self.crawler_time} type of raw_review_data")
            print(type(raw_review_data))
            print(f"pid= {self.pid} time= {self.crawler_time} len of raw_review_data")
            print(len(raw_review_data))
            print(f"pid= {self.pid} time= {self.crawler_time} type of raw_review_data.get('data')")
            print(type(raw_review_data.get('data')))
            print(f"pid= {self.pid} time= {self.crawler_time} type of raw_review_data.get('data').get('list')")
            print(type(raw_review_data.get('data').get('list')))
            for i in raw_review_data.get('data').get('list'):
                user_id = str(i.get('moment').get('author').get('user').get('id'))
                current_review = i.get('moment').get('extended_entities').get('reviews')[0]

                review_id = str(current_review.get('id'))
                # review_check_sql = f"SELECT IFNULL((SELECT TRUE FROM game_review gr WHERE review_id={review_id} LIMIT 1),FALSE) "
                # print(f"app_review review_check_sql:{review_check_sql}")
                # result_data = mysql_operate.db.select_db(review_check_sql)[0].values()
                # check_result_list = list()
                # for result in result_data:
                #     check_result_list.append(result)
                # check_result = check_result_list[0]
                # if check_result == 1:
                #     print("check_result == 1,then return")
                #     return user_list

                submit_sql = "INSERT INTO game_review(" \
                             "game_id, " \
                             "user_id, " \
                             "rating, " \
                             "review_id, " \
                             "review_text, " \
                             "score,ups, " \
                             "downs, " \
                             "comments, " \
                             "is_edited, " \
                             "played_spent, " \
                             "re_updated_time, " \
                             "re_created_time) " \
                             "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')". \
                    format(str(app_id),
                           user_id,
                           str(current_review.get('ratings')).replace("\'", "\""),
                           review_id,
                           cop.sub('', str(
                               current_review.get('contents').get('text'))),
                           str(current_review.get('score')),
                           str(current_review.get('ups')),
                           str(current_review.get('downs')),
                           str(current_review.get('comments')),
                           str(current_review.get('edited')),
                           str(current_review.get('played_spent')),
                           str(current_review.get('updated_time')),
                           str(current_review.get('created_time'))
                           )

                mysql_operate.db.execute_db(submit_sql)
                user_list.append(user_id)
            next_page = self.__get_next_page(raw_review_data.get('data'))
            print(next_page)
            # 如果下一页是空，则循环break
            if next_page is '':
                print(f"pid= {self.pid} time= {self.crawler_time} app_review next page is empty,break")
                break
            url = WEBSITE_NAME + next_page + '&' + GET_TAIL_PARAM(self.pid)
            num += 1

        return user_list

    # 获取用户的信息
    def user_about(self, user_id, app_id):
        url = WEBSITE_NAME + "/webapiv2/user/v1/detail?id=+" + str(user_id) + "&" + GET_TAIL_PARAM(self.pid)
        raw_user_about = self.__getapiinfo(url, '/user', '/' + str(user_id), '/about')
        # raw_user_about = self.__getapiinfo_cmd(url, '/user', '/' + str(user_id), '/about')
        user_about_data = raw_user_about.get('data')
        cop = re.compile("[^0-9a-zA-Z\u4e00-\u9fa5.，,。？…&“”《》_（）<>！；：]")
        cop2 = re.compile("[^0-9+]")

        # 将birthday转化为json，方便入库
        if user_about_data.get('birthday'):
            birthday = str(user_about_data.get('birthday')).replace("\'", "\"")
        else:
            birthday = "{}"

        # 检查用户是否已经在数据库中了
        review_check_sql = f"SELECT IFNULL((SELECT TRUE FROM user_info WHERE user_id={str(user_id)} LIMIT 1),FALSE) "
        result_data = mysql_operate.db.select_db(review_check_sql)[0].values()
        check_result_list = list()
        for result in result_data:
            check_result_list.append(result)
        check_result = check_result_list[0]
        # 如果已经有这个用户了，直接返回
        if check_result == 1:
            return

        submit_sql = "INSERT INTO user_info(" \
                     "user_name, " \
                     "user_id," \
                     "gender, " \
                     "birth, " \
                     "fans_count, " \
                     "following_count, " \
                     "following_developer_count, " \
                     "following_app_count, " \
                     "following_console_game_app_count, " \
                     "following_group_count, " \
                     "voteup_count, " \
                     "spent_tips, " \
                     "created_days, " \
                     "played_count, " \
                     "from_app_id) " \
                     "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}')". \
            format(cop.sub('', str(user_about_data.get('name'))),
                   str(user_about_data.get('id')),
                   str(user_about_data.get('gender')),
                   birthday,
                   str(user_about_data.get('stat').get('fans_count')),
                   str(user_about_data.get('stat').get('following_count')),
                   str(user_about_data.get('stat').get('following_developer_count')),
                   str(user_about_data.get('stat').get('following_app_count')),
                   str(user_about_data.get('stat').get('following_console_game_app_count')),
                   str(user_about_data.get('stat').get('following_group_count')),
                   str(user_about_data.get('stat').get('voteup_count')),
                   cop2.sub('', str(user_about_data.get('stat').get('spent_tips'))),
                   str(user_about_data.get('stat').get('created_days')),
                   str(user_about_data.get('stat').get('played_count')),
                   str(app_id)
                   )
        mysql_operate.db.execute_db(submit_sql)

    # 获取用户的评论
    def user_review(self, user_id, app_id):
        cop = re.compile("[^0-9a-zA-Z\u4e00-\u9fa5.，,。？…&“”《》_~（）<>！；：]")
        cop_2 = re.compile("[^0-9+]")
        num = 1
        url = WEBSITE_NAME + f"/webapiv2/feed/v6/by-user?type=review&user_id={str(user_id)}&from=0&limit=10&" + GET_TAIL_PARAM(self.pid)
        start_cookie_reply(self.pid)
        while True:
            if num % 7 == 0:
                start_cookie_reply(self.pid)
            num += 1
            raw_user_review = self.__getapiinfo(url, '/user', '/' + str(user_id), '/reviews')
            # raw_user_review = self.__getapiinfo_cmd(url, '/user', '/' + str(user_id), '/reviews')
            for i in raw_user_review.get('data').get('list'):
                current_moment = i.get('moment')
                if current_moment.get('app'):
                    current_app = current_moment.get('app')
                    current_review = current_moment.get('extended_entities').get('reviews')[0]

                    review_id = str(current_review.get('id'))
                    # review_check_sql = f"SELECT IFNULL((SELECT TRUE FROM user_review WHERE review_id={review_id} LIMIT 1),FALSE) "
                    # result_data = mysql_operate.db.select_db(review_check_sql)[0].values()
                    # check_result_list = list()
                    # for result in result_data:
                    #     check_result_list.append(result)
                    # check_result = check_result_list[0]
                    # if check_result == 1:
                    #     return

                    submit_sql = "INSERT INTO user_review(" \
                                 "user_id, " \
                                 "game_id, " \
                                 "game_name, " \
                                 "rating, " \
                                 "review_id, " \
                                 "review_text, " \
                                 "score, " \
                                 "ups, " \
                                 "downs, " \
                                 "comments, " \
                                 "is_edited, " \
                                 "played_spent, " \
                                 "re_updated_time, " \
                                 "re_created_time, " \
                                 "from_app_id) " \
                                 "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')". \
                        format(str(user_id),
                               str(current_app.get('id')),
                               str(current_app.get('title')),
                               str(current_review.get('ratings')).replace("\'", "\""),
                               review_id,
                               cop.sub('', str(
                                   current_review.get('contents').get('text'))),
                               str(current_review.get('score')),
                               str(current_review.get('ups')),
                               str(current_review.get('downs')),
                               str(current_review.get('comments')),
                               str(current_review.get('edited')),
                               str(current_review.get('played_spent')),
                               str(current_review.get('updated_time')),
                               str(current_review.get('created_time')),
                               str(app_id)
                               )
                    mysql_operate.db.execute_db(submit_sql)

                    self.__get_tags(current_app.get('tags'), str(current_app.get('id')))

            next_page = self.__get_next_page(raw_user_review.get('data'))
            print(f"pid= {self.pid} time= {self.crawler_time} next_page: {next_page}")
            # 如果下一页为空，则循环break
            if next_page is '':
                print(f"pid= {self.pid} time= {self.crawler_time} user_review next page is empty,break")
                break
            url = WEBSITE_NAME + next_page + '&' + GET_TAIL_PARAM(self.pid)

    # 获取用户关注的游戏
    def user_following(self, user_id):
        num = 1
        url = WEBSITE_NAME + f"/webapiv2/friendship/v1/following-by-user?user_id={str(user_id)}&type=app&" + GET_TAIL_PARAM(self.pid)
        start_cookie_reply(self.pid)
        while True:
            if num % 10 == 0:
                start_cookie_reply(self.pid)
            num += 1
            raw_user_following = self.__getapiinfo(url, '/user', '/' + str(user_id), '/following')
            for current_following in raw_user_following.get('data').get('list'):
                game_id = str(current_following.get('id'))
                # 查询这条数据是否已经存在
                review_check_sql = f"SELECT IFNULL((SELECT TRUE FROM user_following WHERE user_id={str(user_id)} AND game_id={game_id} LIMIT 1),FALSE) "
                result_data = mysql_operate.db.select_db(review_check_sql)[0].values()
                check_result_list = list()
                for result in result_data:
                    check_result_list.append(result)
                check_result = check_result_list[0]
                # 如果不存在再获取信息
                if check_result == 0:
                    submit_sql = "INSERT INTO user_following(" \
                                 "user_id, " \
                                 "game_id, " \
                                 "game_name )" \
                                 "VALUES('{}', '{}', '{}')". \
                        format(str(user_id),
                               game_id,
                               str(current_following.get('title')),
                               )
                    mysql_operate.db.execute_db(submit_sql)

                    self.__get_tags(current_following.get('tags'), str(current_following.get('id')))

            next_page = self.__get_next_page(raw_user_following.get('data'))
            print(f"pid= {self.pid} time= {self.crawler_time} next_page: {next_page}")
            if next_page is '':
                print(f"pid= {self.pid} time= {self.crawler_time} user_following next page is empty,break")
                break
            url = WEBSITE_NAME + next_page + '&' + GET_TAIL_PARAM(self.pid)

    # # 获取用户的游戏时长，由于不需要这个信息，这个方法在各个主函数中没有被调用
    # def user_played(self, user_id):
    #     num = 1
    #     url = WEBSITE_NAME + f"/webapiv2/user-app/v1/user-spent-list?user_id={str(user_id)}&" + GET_TAIL_PARAM(self.pid)
    #     start_cookie_reply(self.pid)
    #     while True:
    #         if num % 10 == 0:
    #             start_cookie_reply(self.pid)
    #         num += 1
    #         raw_user_played = self.__getapiinfo(url, '/user', '/' + str(user_id), '/most-played')
    #         for current_played in raw_user_played.get('data').get('list'):
    #             play_spent = current_played.get("spent")
    #             current_app = current_played.get("app")
    #             game_id = current_app.get("id")
    #             game_name = current_app.get("title")
    #             review_check_sql = f"SELECT IFNULL((SELECT TRUE FROM user_played WHERE user_id={str(user_id)} AND game_id={game_id} LIMIT 1),FALSE) "
    #             result_data = mysql_operate.db.select_db(review_check_sql)[0].values()
    #             check_result_list = list()
    #             for result in result_data:
    #                 check_result_list.append(result)
    #             check_result = check_result_list[0]
    #             if check_result == 0:
    #                 submit_sql = "INSERT INTO user_played(" \
    #                              "user_id, " \
    #                              "game_id, " \
    #                              "game_name, " \
    #                              "play_spent)" \
    #                              "VALUES('{}', '{}', '{}')". \
    #                     format(str(user_id),
    #                            str(game_id),
    #                            str(game_name),
    #                            str(play_spent)
    #                            )
    #                 mysql_operate.db.execute_db(submit_sql)
    #                 self.__get_tags(current_app.get('tags'), str(game_id))
    #
    #         next_page = self.__get_next_page(raw_user_played.get('data'))
    #         print(next_page)
    #         if next_page is '':
    #             break
    #         url = WEBSITE_NAME + next_page + '&' + GET_TAIL_PARAM(self.pid)
