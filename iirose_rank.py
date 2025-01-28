import random
import json
import os
from loguru import logger
from API.api_iirose import APIIirose
from API.decorator.command import on_command, MessageType
import datetime

API = APIIirose()

# 定义吉凶运势列表及其优先级
fortune_list = [
    "上上",
    "上吉",
    "中吉",
    "中平",
    "下下"
]

# 定义优先级字典
fortune_priority = {
    "上上": 1,
    "上吉": 2,
    "中吉": 3,
    "中平": 4,
    "下下": 5
}

# 全局字典来存储用户签到信息
sign_in_records = {}

# 定义文件名
EXPORTS_FILE = 'exports.txt'


def load_sign_in_records():
    global sign_in_records
    if os.path.exists(EXPORTS_FILE):
        with open(EXPORTS_FILE, 'r', encoding='utf-8') as file:
            sign_in_records = json.load(file)
            logger.info("成功加载签到记录")


def save_sign_in_records():
    with open(EXPORTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(sign_in_records, file, ensure_ascii=False, indent=4)
        logger.info("成功保存签到记录")


# 预定义的图像链接列表，可自行添加
IMAGE_URLS = [
    "https://i1.hdslb.com/bfs/article/7df388701fc9d2201062cd2bf5b71bb2187345532.png",
    "https://i1.hdslb.com/bfs/article/c735fdada1c84ccb990df3c84d0d0d19187345532.jpg",
    "https://i1.hdslb.com/bfs/article/5ed89847b3227c1ad850477efd60f296187345532.jpg",
    "https://i1.hdslb.com/bfs/article/076db75e41dd607f9bae27c38f4da2e7187345532.jpg",
    "https://i1.hdslb.com/bfs/article/3ce7cd601ceefc34780358d4114f287a187345532.jpg",
    "https://i1.hdslb.com/bfs/article/e619312854249c75f5dcb2c4b8ff9b8b187345532.jpg",
    "https://i1.hdslb.com/bfs/article/9076f17c77bab06e575635bd9faa22e1187345532.jpg",
    "https://i1.hdslb.com/bfs/article/a1f80bb3a688d54bc472dbaf77db2e11187345532.jpg",
    "https://i1.hdslb.com/bfs/article/befb84f2038a4c8360493a2b419e1e17187345532.jpg",
    "https://i1.hdslb.com/bfs/article/f085a699e009e8d5ce79471b6acdb83a187345532.jpg",
    "https://i1.hdslb.com/bfs/article/d222f8dc27335a4ec3af8d4a43fc13a7187345532.jpg",
    "https://i1.hdslb.com/bfs/article/00198821daf78ca3fb15c349990773b1187345532.png",
    "https://i1.hdslb.com/bfs/article/6ed11dd08d11cfb6cd5eee9a163b9a18187345532.jpg",
    "https://i1.hdslb.com/bfs/article/52638d678523b29c60379717defcc87b187345532.jpg",
    "https://i1.hdslb.com/bfs/article/8c02301176406c601ca227c07d2927bb187345532.png",
    "https://i1.hdslb.com/bfs/article/908f9ba98eb30c3048057ad00916103f187345532.jpg",
    "https://i1.hdslb.com/bfs/article/e777f641ecd0d5821d4923c2013fe01e187345532.jpg",
    "https://i1.hdslb.com/bfs/article/582d48841f9ec5783d83285833c75632c9c38f53.jpg",
    "https://i1.hdslb.com/bfs/article/a067e5e1a81de28acf5002cb89b70e319a461b92.jpg",
    "https://i1.hdslb.com/bfs/article/8e3ae4416b5b227673dcacb2af1389628e07d301.jpg",
    "https://i1.hdslb.com/bfs/article/00281594b3d1918572efb9fb5c165eff7c5b67f5.jpg",
    "https://i1.hdslb.com/bfs/article/581fe55dafb67e7137f5cea9f36e68f3b13ed95c.jpg",
    "https://i1.hdslb.com/bfs/article/762c689080542b5cc393b62b0e9982d19d3fca89.jpg",
    "https://i1.hdslb.com/bfs/article/82bf625a3e27f75e7652c4f1ef59e85d1cf09322.jpg",
    "https://i1.hdslb.com/bfs/article/5997bc5d38c76663975d8d33841ec26bb68c7c44.jpg",
    "https://i1.hdslb.com/bfs/article/9afb0152ed12b6966b173f469bf04352b515eceb.jpg",
    "https://i1.hdslb.com/bfs/article/a41198011dbe88dc5bb29708fea477cdd2a44d95.jpg",
    "https://i1.hdslb.com/bfs/article/8f7226d8b904e8da6459ce8bde687524c92746ca.jpg",
    "https://i1.hdslb.com/bfs/article/ab39f8fb6aaacb1173725a5c1eab516c43612a49.jpg",
    "https://i1.hdslb.com/bfs/article/5d04c59671bfb9b2be6ecff6f20435c76b0eb5e0.jpg",
    "https://i1.hdslb.com/bfs/article/524c1a65868f82b966ad608aef82a6d63352b4a6.jpg",
    "https://i1.hdslb.com/bfs/article/25f1fc5e41f056b5a72166d85732c58dc921dc6e.jpg",
    "https://i1.hdslb.com/bfs/article/4c34ec366579818171760fdd71fa15390fdbf1e6.jpg",
    "https://i1.hdslb.com/bfs/article/c67f2a9b2837ad70e7c9be6136c5eea68180ba96.jpg",
    "https://i1.hdslb.com/bfs/article/003d2b3af0b40cf391fe78cf00ef07c07942b2e9.jpg",
    "https://i1.hdslb.com/bfs/article/d3821b710e1551e8087974386fd0a54ba78b997b.jpg",
    "https://i1.hdslb.com/bfs/article/728a67bc939706ad310a29cde9034842f176db1c.jpg",
    "https://i1.hdslb.com/bfs/article/2e24e1b0f7242c52c531747cbccb3827ffb7c692.jpg",
    "https://i1.hdslb.com/bfs/article/cb5bec20757b8891a040fddaff4e4a5669eb214b.jpg",
    "https://i1.hdslb.com/bfs/article/1969944a66e726d8712fd47574a23ea6ee8b3e8c.jpg",
    "https://i1.hdslb.com/bfs/article/31be46d3482651db0c62f375a457aa2ea5e0b838.jpg",
    "https://i1.hdslb.com/bfs/article/f29fbc7a358a72fccc1cdff082e14220bce517bf.jpg",
    "https://i1.hdslb.com/bfs/article/d069149e3f58ed58b3babaa79939cc472c723f92.jpg",
    "https://i1.hdslb.com/bfs/article/33fe412269f4bb9d4334a90e82c8191928a630a8.jpg",
    "https://i1.hdslb.com/bfs/article/2b001325f7cbf3f7e7b4b27057c686803cc3c0a1.jpg",
    "https://i1.hdslb.com/bfs/article/99cef8eb229b7de61e9d614c5a92f130daa8d4a2.jpg",
    "https://i1.hdslb.com/bfs/article/750650bb2db2563ad8c7b79d326eb77bdcf25c0e.jpg",
    "https://i1.hdslb.com/bfs/article/dded3b2f863666a37b1533e389bdb113b0a00dba.jpg",
    "https://i1.hdslb.com/bfs/article/d303acd795150103f762adc8bd1ccbe9b1afb441.png",
    "https://i1.hdslb.com/bfs/article/539c30bed6138e2f1fe000118a3820c4451e6c34.png",
    "https://i1.hdslb.com/bfs/article/3d6a4431660a92a16293d37e0f18dde182908390.jpg",
    "https://i1.hdslb.com/bfs/article/a6304e78e123f6e4791b20e2f8891ca70b96dba7.png",
    "https://i1.hdslb.com/bfs/article/389c1517f6298dcc62d0e8197d2f755e3285642b.png",
    "https://i1.hdslb.com/bfs/article/afe56d3109868d0471455e1b0cd226bbe2892815.png",
    "https://i1.hdslb.com/bfs/article/ee12e6767745aec1b4bdab27843d07a3ec431fa4.jpg",
    "https://i1.hdslb.com/bfs/article/51e16b38416d0a8079f0eaae6d7f59e0401dba25.jpg",
    "https://i1.hdslb.com/bfs/article/1ee24d31f004811001f942ae5608c6672b86c2b0.jpg",
    "https://i1.hdslb.com/bfs/article/61c5a3dea386684016be43e6ef4c1429144a2c66.jpg",
    "https://i1.hdslb.com/bfs/article/1b69c92f96a130bcd7e62d3ca53741792e89fa78.jpg",
    "https://i1.hdslb.com/bfs/article/eae78af3928e10acf4f455651af007539e57e896.jpg",
    "https://i1.hdslb.com/bfs/article/774996c983ce16cff9995dc18d5a479d4d55d4fd.jpg",
    "https://i1.hdslb.com/bfs/article/45c852a2e22a06aa211e7f6cb419c1ce0b2a864f.jpg",
    "https://i1.hdslb.com/bfs/article/39e49451cb2e97b3e80a5c290c65b916a6a9db67.jpg",
    "https://i1.hdslb.com/bfs/article/7b244f6f980f608c26c0a999ce47b550d60581bc.jpg",
    "https://i1.hdslb.com/bfs/article/6d9f631fcd272614b6e07076e505d6024a33e915.jpg",
    "https://i1.hdslb.com/bfs/article/ea3d0e6b3ccec0b8475fc72597ab420243b01970.jpg",
    "https://i1.hdslb.com/bfs/article/d89decfa9d251a1a7a67f4caa0e3002e1ef9dbb9.jpg",
    "https://i1.hdslb.com/bfs/article/48e31ead60f9944604faccbe261b52823a1ad5f0.jpg",
    "https://i1.hdslb.com/bfs/article/e07bb9ee0217455715afbb467ab0aa5740bae01e.jpg",
    "https://i1.hdslb.com/bfs/article/646f17c027dc560228753f452cdc83b32553c6bd.jpg",
    "https://i1.hdslb.com/bfs/article/2f488c8e553280810c5d95d565e269fda127ef74.jpg",
    "https://i1.hdslb.com/bfs/article/de587052adf390bd3c2deed732c98b3df909ae6b.jpg",
    "https://i1.hdslb.com/bfs/article/974c6acf66ceed48e2b4a596e6448e4afbfd9e1a.jpg",
    "https://i1.hdslb.com/bfs/article/f3116a41b891fa9d03f4bdbe8414047e70b06a86.jpg",
    "https://i1.hdslb.com/bfs/article/1e1147adbc48176ee2f638887e4cd06b91511272.jpg",
    "https://i1.hdslb.com/bfs/article/2a7911ddd53349abbf0b2eb96dd4e0d3e05cbef4.jpg",
    "https://i1.hdslb.com/bfs/article/9aac49917c8cc16fe9c00fab6204058cd1e1f417.jpg",
    "https://i1.hdslb.com/bfs/article/aeee12a4b9f10339c1607d39e99cee52cbed0afc.jpg",
    "https://i1.hdslb.com/bfs/article/d6b05bb225a77b29391b5d10035c64d7036d2174.jpg",
    "https://i1.hdslb.com/bfs/article/bca39b5b1df087b8c95e0fa78daf7f40ef56524c.jpg",
    "https://i1.hdslb.com/bfs/article/508d35d2b551cad4cce2e9658ea29eb07aa4520d.jpg",
    "https://i1.hdslb.com/bfs/article/690ab4ea9e472941f7bc479ca77933f328614f96.jpg",
    "https://i1.hdslb.com/bfs/article/e13225293061ed6c20138aba4ad935be001fb187.jpg",
    "https://i1.hdslb.com/bfs/article/8127bcdbb9148c1221d17464b92c3b3ce8320a34.jpg",
    "https://i1.hdslb.com/bfs/article/cb089c1b6c2952987365b9a548e1fd90644c5507.jpg",
    "https://i1.hdslb.com/bfs/article/99fa49fa83746c40311b3b45f5bd3c3eef29eb7b.jpg",
    "https://i1.hdslb.com/bfs/article/06f87dd45c3d6e99b8153ffa0ed62e7e828d9cad.jpg",
    "https://i1.hdslb.com/bfs/article/1397d917df33ee3b23ec469bbc4403e8610a2d9d.jpg",
    "https://i1.hdslb.com/bfs/article/a849f7d58e658660b1ef9afcad3db68befa0c789.jpg",
    "https://i1.hdslb.com/bfs/article/28afdd4b265d9de32f841a4861fc0d204be18ef0.jpg",
    "https://i1.hdslb.com/bfs/article/29bd837b7ae46c5aa8c64bb9c4d2f9b4b6663be4.jpg",
    "https://i1.hdslb.com/bfs/article/cb2688a28592326122182a330bfeb789486c5e16.jpg",
    "https://i1.hdslb.com/bfs/article/013321eeed2975a1b081c612c0bb0dc0e176d2a9.jpg",
    "https://i1.hdslb.com/bfs/article/9bdda218a098da693492ba5c4ef35e83f5804429.jpg",
    "https://i1.hdslb.com/bfs/article/90088c32e0c67b58123a3133e20cc4a4232a249f.jpg",
    "https://i1.hdslb.com/bfs/article/2161401f9928fb82c09c6010fda23cde2b7b95dc.jpg",
    "https://i1.hdslb.com/bfs/article/9069d2708f9dcd96524f72bc468c8d10ff5df741.jpg",
    "https://i1.hdslb.com/bfs/article/56b877e8ae92e3ed4c9e1d282038c50201d32761.jpg",
    "https://i1.hdslb.com/bfs/article/bce8464988b539dfdb1e5fa8e9b06cc18db4fc0b.jpg",
    "https://i1.hdslb.com/bfs/article/bce701b300c4529daca1f6ce32f6c383045cb07f.jpg",
    "https://i1.hdslb.com/bfs/article/4d1640f0975c7046798acc284602dec9fb7c5e94.jpg",
    "https://i1.hdslb.com/bfs/article/7f101abcbe8ce9f2af8fad45e067aeeba52176c5.jpg",
]

def fetch_image() -> str:
    """从预定义的图像列表中随机获取一张图片的直链"""
    if IMAGE_URLS:  # 确保 IMAGE_URLS 列表不为空
        return random.choice(IMAGE_URLS)  # 随机选择一张图片
    else:
        logger.warning("图像列表为空，未获取到图片")
        return "https://via.placeholder.com/150"  # 返回占位符图片


@on_command('/z', False, command_type=[MessageType.room_chat, MessageType.private_chat])
async def sign_in(Message):
    user_id = Message.user_id
    username = Message.user_name
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M")
    fortune = random.choice(fortune_list)

    if user_id in sign_in_records:
        user_info = sign_in_records[user_id]
        if user_info.get('date') == current_date:
            await API.send_msg(Message, f" [*{username}*]  ，你今天已经签到过了！")
            return

    sign_in_records[user_id] = {
        'username': username,
        'date': current_date,
        'time': current_time,
        'luck': fortune
    }

    logger.info(f"{username} 签到成功，时间: {current_time}")

    save_sign_in_records()

    sorted_sign_in_records = sorted(
        sign_in_records.items(),
        key=lambda item: (fortune_priority[item[1]['luck']], item[1]['time']),
        reverse=False
    )

    total_sign_ins_today = len([uid for uid, info in sign_in_records.items() if info['date'] == current_date])

    # 获取美图
    image_url = fetch_image()  # 调用获取图片的函数

    result = (r"\\\* " + f" ## #{total_sign_ins_today} **{username}**\n\n---\n\n"
                         f"用户名： **{username}**\n"
                         f"你是今天第 **{total_sign_ins_today}** 个签到的！\n"
                         f"时间： **{current_time}**\n\n"
                         f"**今日运势！ {fortune}**\n\n"
                         f"![美图]({image_url})\n\n"  # 嵌入美图的 Markdown 语法
                         f"---\n\n*您可以发送 /rank 查看签到详情*")

    await API.send_msg(Message, result)


@on_command('/rank', False, command_type=[MessageType.room_chat, MessageType.private_chat])
async def send_rank_list(Message):
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 获取今天的日期
        # 仅筛选出今天的签到记录
        today_sign_in_records = {user_id: info for user_id, info in sign_in_records.items() if info['date'] == current_date}

        sorted_sign_in_records = sorted(
            today_sign_in_records.items(),
            key=lambda item: (fortune_priority[item[1]['luck']], item[1]['time']),
            reverse=False
        )[:20]

        rank_list = []

        for idx, (user_id, user_info) in enumerate(sorted_sign_in_records):
            rank = idx + 1
            username = user_info['username']
            luck = user_info['luck']
            sign_in_time = user_info['time']
            username_display = f"_{username}_"
            luck_display = f"_{luck}_"
            rank_list.append(
                f"| **{rank}**&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;**{username_display}**&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;**{luck_display}**&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;**{sign_in_time}**&nbsp;&nbsp;&nbsp;|")

        if rank_list:
            header = r"\\\* " + "|  排名   | &nbsp;  用户名   &nbsp;|&nbsp;运势&nbsp;|   签到时间   |\n|:-|:-|:-:|-:|\n"
            rank_data = "\n".join(rank_list)
            result = header + rank_data
        else:
            result = "当前群组没有成员签到。"

        await API.send_msg(Message, result)

    except Exception as e:
        logger.error(f"发送排行榜时出错: {e}")
        await API.send_msg(Message, "发送排行榜时发生错误。")


async def on_init():
    load_sign_in_records()
    logger.info('初始化排行榜插件完成')
