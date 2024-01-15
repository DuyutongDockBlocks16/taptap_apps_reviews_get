import all_info_get
from config import APP_ID_LIST,GET_APP_ID_LIST

def make_list_unique(raw_list):
    unique_list=list()
    for element in raw_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list


# solo_process
if __name__ == '__main__':
    info_get_object = all_info_get.TapInfoGet()

    app_id_list = APP_ID_LIST

    raw_user_list = list()
    for app_id in app_id_list:
        print(f"begin app :{app_id} information get")
        review_count = info_get_object.app_detail(app_id)
        print(f"finish app_detail :{app_id} information get")
        per_app_user_list = info_get_object.app_review(app_id, 0)
        print(f"finish app_review :{app_id} information get")
        print(f"finish app :{app_id} information get")
        raw_user_list.extend(per_app_user_list)

    print(f"len of raw_user_list:{len(raw_user_list)}")
    user_list = make_list_unique(raw_user_list)
    print(f"len of user_list:{len(user_list)}")

    user_num = 0
    for user_id in user_list:
        print(f"begin user :{user_id} information get")

        print(f"begin user_about :{user_id} information get")
        try:
            info_get_object.user_about(user_id, app_id_list[0])
            print(f"finish user_about :{user_id} information get")
        except Exception as e:
            print("user_about except:", e)

        print(f"begin user_review :{user_id} information get")
        try:
            info_get_object.user_review(user_id, app_id_list[0])
            print(f"finish user_review :{user_id} information get")
        except Exception as e:
            print("user_review except:", e)

        print(f"begin user_following :{user_id} information get")
        try:
            info_get_object.user_following(user_id)
            print(f"finish user_following :{user_id} information get")
        except Exception as e:
            print("user_following except:", e)
        user_num += 1
