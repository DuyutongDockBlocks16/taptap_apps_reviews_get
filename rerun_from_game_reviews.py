# coding=utf-8
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
            info_get_object.user_about(user_id, "1111")
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} finish user_about :{user_id} information get")
        except Exception as e:
            crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"pid= {pid} time= {crawler_time} user_about except:", e)
        crawler_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"pid= {pid} time= {crawler_time} begin user_review :{user_id} information get")
        try:
            info_get_object.user_review(user_id, "1111")
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
    process_num = (CPU_NUM - 1)*2
    #

    # driver of user info get
    info_get_object = all_info_get.TapInfoGet()
    raw_user_list = info_get_object.select_from_user_review()

    user_list = list()
    for i in raw_user_list:
        user_list.append(i.get("USER_ID"))
    user_info_queue = multiprocessing.Queue()
    user_info_jobs = list()

    user_info_worker_mission_num = math.ceil(len(user_list) / process_num)
    user_info_result_list = list()

    # workers of user info get
    for i in range(process_num):
        fracture_user_id_list = user_list[
                                i * user_info_worker_mission_num:i * user_info_worker_mission_num + user_info_worker_mission_num]
        user_info_p = multiprocessing.Process(target=user_info_worker, args=(fracture_user_id_list, user_info_queue))
        user_info_jobs.append(user_info_p)
        user_info_p.start()
    for user_info_p in user_info_jobs:
        user_info_p.join()

    # driver of user info get
    while not user_info_queue.empty():
        raw_user_list.extend(user_info_queue.get())

    for i in raw_user_list:
        print(i)

    pass
