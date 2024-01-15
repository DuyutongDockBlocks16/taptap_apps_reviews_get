import all_info_get
from config import APP_ID_LIST, GET_APP_ID_LIST
import multiprocessing
import math
import os
import time
import random
from new_cookie_create import start_cookie_reply

CPU_NUM = multiprocessing.cpu_count()


def make_list_unique(raw_list):
    unique_list = list()
    for element in raw_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list


def game_info_worker(worker_app_id_list, process_queue):
    print(f"worker_app_id_list: {worker_app_id_list}")
    time.sleep(random.randint(0, 15))
    pid = os.getpid()
    # cookie initialization
    start_cookie_reply(pid)


    info_get_object = all_info_get.TapInfoGet()
    worker_raw_user_list = list()
    for app_id in worker_app_id_list:
        try:
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} begin app :{app_id[0]} information get")
            review_count = info_get_object.app_detail(app_id[0])
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} finish app_detail :{app_id} information get")
            per_app_user_list = info_get_object.app_review(app_id[0], app_id[1])
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} finish app_review :{app_id[0]} information get")
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} finish app :{app_id[0]} information get")
            worker_raw_user_list.extend(per_app_user_list)
        except Exception as e:
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} GameID: {app_id[0]} info obtain failed, reason: {e}")

    process_queue.put(worker_raw_user_list)


def user_info_worker(worker_user_list, process_queue):
    time.sleep(random.randint(0, 15))
    pid = os.getpid()
    # cookie initialization
    start_cookie_reply(pid)
    crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"pid= {pid} time= {crawler_time}worker_user_list :{worker_user_list} ")
    info_get_object = all_info_get.TapInfoGet()
    user_num = 0
    for user_id in worker_user_list:
        crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"pid= {pid} time= {crawler_time} begin user :{user_id} information get")
        crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"pid= {pid} time= {crawler_time} begin user_about :{user_id} information get")
        try:
            info_get_object.user_about(user_id, app_id_list[0])
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} finish user_about :{user_id} information get")
        except Exception as e:
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} user_about except:", e)
        crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"pid= {pid} time= {crawler_time} begin user_review :{user_id} information get")
        try:
            info_get_object.user_review(user_id, app_id_list[0])
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} finish user_review :{user_id} information get")
        except Exception as e:
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} user_review except:", e)
        crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"pid= {pid} time= {crawler_time} begin user_following :{user_id} information get")
        try:
            info_get_object.user_following(user_id)
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} finish user_following :{user_id} information get")
        except Exception as e:
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} user_following except:", e)
        user_num += 1
    crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
    job_result = f"pid= {pid} time= {crawler_time}user_info_worker job is done"
    print(job_result)
    process_queue.put(job_result)


if __name__ == '__main__':
    # resource application
    process_num = (CPU_NUM - 1)*5

    # driver of game info get
    game_info_queue = multiprocessing.Queue()
    game_info_jobs = list()

    app_id_list = GET_APP_ID_LIST()
    print(f"app_id_list: {app_id_list} ")
    game_info_worker_mission_num = math.ceil(len(app_id_list) / process_num)
    raw_user_list = list()

    # workers of game info get
    for i in range(process_num):
        fracture_app_id_list = app_id_list[
                               i * game_info_worker_mission_num:i * game_info_worker_mission_num + game_info_worker_mission_num]
        print(f"fracture_app_id_list: {fracture_app_id_list} ")
        game_info_p = multiprocessing.Process(target=game_info_worker, args=(fracture_app_id_list, game_info_queue))
        game_info_jobs.append(game_info_p)
        game_info_p.start()
    for game_info_p in game_info_jobs:
        game_info_p.join()

    # driver of game info get
    # while not game_info_queue.empty():
    #     raw_user_list.extend(game_info_queue.get())
    #
    # print(f"len of raw_user_list:{len(raw_user_list)}")
    # user_list = make_list_unique(raw_user_list)
    # print(f"len of user_list:{len(user_list)}")
    #
    # # driver of user info get
    # user_info_queue = multiprocessing.Queue()
    # user_info_jobs = list()
    #
    # user_info_worker_mission_num = math.ceil(len(user_list) / process_num)
    # user_info_result_list = list()
    #
    # # workers of user info get
    # for i in range(process_num):
    #     fracture_user_id_list = user_list[
    #                             i * user_info_worker_mission_num:i * user_info_worker_mission_num + user_info_worker_mission_num]
    #     user_info_p = multiprocessing.Process(target=user_info_worker, args=(fracture_user_id_list, user_info_queue))
    #     user_info_jobs.append(user_info_p)
    #     user_info_p.start()
    # for user_info_p in user_info_jobs:
    #     user_info_p.join()
    #
    # # driver of user info get
    # while not user_info_queue.empty():
    #     raw_user_list.extend(user_info_queue.get())
    #
    # for i in raw_user_list:
    #     print(i)
