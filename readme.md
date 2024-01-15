0x00 项目功能
    
    功能描述：获取taptap目标游戏的基本信息、评论，以及评论用户的信息、评论
    工程输入：目标游戏的id，config.py中GET_APP_ID_LIST类
    工程输出：相关目标表

0x01 项目基本信息
    
    用于启动项目的堡垒机：阿里云：47.93.86.224，内网ip：10.116.150.141。外网ip曾用：39.97.184.99
    工程路径：/home/duyt/MultiTaptapAppsReviewGet
    工程虚拟环境：/home/duyt/ENV_TaptapAppReviewGet/bin
    工程redis路径：/usr/local/redis
    工程mysql路径：/usr/lib64 用户名：root 密码：7D9gQwpiI8n4TyV_7D9gQwpiI8n4TyV DB：data_pub

0x02 入口函数

    ~~[main.py]~~
    功能：单进程启动工程

    ~~[multi_processing_main.py]~~
    功能：多进程启动工程

    ~~[rerun_from_game_reviews.py]~~
    功能：获取所有用户id，直接启动获取用户信息以及用户评论的流程（每次更换完IP之后，直接启动这个.py即可）
    python rerun_from_game_reviews.py