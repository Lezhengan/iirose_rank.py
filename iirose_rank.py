import random
import json
import os  # 用于检查文件是否存在
from loguru import logger
from API.api_iirose import APIIirose  # 导入接口
from globals.globals import GlobalVal  # 全局变量
from API.decorator.command import on_command, MessageType  # 注册指令装饰器和消息类型Enum
import datetime  # 导入datetime模块

API = APIIirose()  # 实例化 APIIirose

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
    """从 exports.txt 加载签到记录"""
    global sign_in_records
    if os.path.exists(EXPORTS_FILE):
        with open(EXPORTS_FILE, 'r', encoding='utf-8') as file:
            sign_in_records = json.load(file)
            logger.info("成功加载签到记录")

def save_sign_in_records():
    """将签到记录保存到 exports.txt"""
    with open(EXPORTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(sign_in_records, file, ensure_ascii=False, indent=4)
        logger.info("成功保存签到记录")

@on_command('/z', False, command_type=[MessageType.room_chat, MessageType.private_chat])  # 注册签到指令
async def sign_in(Message):
    """处理签到指令的函数，记录用户签到信息"""
    user_id = Message.user_id  # 获取用户ID
    username = Message.user_name  # 获取用户名
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 获取当前日期（格式化为 YYYY-MM-DD）
    current_time = datetime.datetime.now().strftime("%H:%M")  # 获取当前时间（只显示小时和分钟）
    fortune = random.choice(fortune_list)  # 随机选择吉凶内容

    # 检查用户是否已签到
    if user_id in sign_in_records:
        user_info = sign_in_records[user_id]
        if user_info.get('date') == current_date:  # 检查当天的签到记录
            await API.send_msg(Message, f" [*{username}*]  ，你今天已经签到过了！")
            return  # 结束函数

    # 保存签到记录
    sign_in_records[user_id] = {
        'username': username,
        'date': current_date,  # 存储当前签到日期
        'time': current_time,
        'luck': fortune
    }

    logger.info(f"{username} 签到成功，时间: {current_time}")

    # 调用保存数据的函数
    save_sign_in_records()

    # 生成 Markdown 格式的签到信息
    # 在这里进行排序以计算排名
    sorted_sign_in_records = sorted(
        sign_in_records.items(),
        key=lambda item: (fortune_priority[item[1]['luck']], item[1]['time']),  # 按运势优先级和签到时间排序
        reverse=False  # 运势优先级越高，排在前面
    )

    # 查找当前用户的排名和签到顺序
    rank = next((idx + 1 for idx, (uid, _) in enumerate(sorted_sign_in_records) if uid == user_id), None)
    total_sign_ins_today = len([uid for uid, info in sign_in_records.items() if info['date'] == current_date])  # 今天的签到人数

    result = (r"\\\* " + f" ## #{total_sign_ins_today} **{username}**\n\n---\n\n"
                         f"用户名： **{username}**\n"
                         f"排名： **#{total_sign_ins_today}**\n"  # 使用实际计算出的排名
                         f"你是今天第 **{total_sign_ins_today}** 个签到的！\n"
                         f"时间： **{current_time}**\n\n"
                         f"**今日运势！ {fortune}**\n\n"
                         f"---\n\n*您可以发送 /rank 查看签到详情*")

    # 发送消息
    await API.send_msg(Message, result)

@on_command('/rank', False, command_type=[MessageType.room_chat, MessageType.private_chat])  # 注册排行榜指令
async def send_rank_list(Message):
    """处理排行榜指令的函数，返回当前房间的用户排行榜"""
    try:
        # 生成排序后的签到记录（按运势优先级和时间排序）
        sorted_sign_in_records = sorted(
            sign_in_records.items(),
            key=lambda item: (fortune_priority[item[1]['luck']], item[1]['time']),
            reverse=False  # 排序规则相同，上面与下面保持一致
        )[:20]  # 只取前20个

        # 构建Markdown格式的排版列表
        rank_list = []

        for idx, (user_id, user_info) in enumerate(sorted_sign_in_records):
            rank = idx + 1  # 排名从1开始
            username = user_info['username']  # 获取用户名
            luck = user_info['luck']  # 获取运势
            sign_in_time = user_info['time']  # 获取签到时间

            # 使用斜体显示
            username_display = f"_{username}_"
            luck_display = f"_{luck}_"

            # 使用 &nbsp; 增加列间距
            rank_list.append(f"| **{rank}**&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;**{username_display}**&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;**{luck_display}**&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;**{sign_in_time}**&nbsp;&nbsp;&nbsp;|")

        # 生成Markdown格式的排行榜
        if rank_list:
            header = r"\\\* " + "|  排名   | &nbsp;  用户名   &nbsp;|&nbsp;运势&nbsp;|   签到时间   |\n|:-|:-|:-:|-:|\n"
            rank_data = "\n".join(rank_list)
            result = header + rank_data
        else:
            result = "当前群组没有成员签到。"

        # 发送消息
        await API.send_msg(Message, result)

    except Exception as e:
        logger.error(f"发送排行榜时出错: {e}")
        await API.send_msg(Message, "发送排行榜时发生错误。")

async def on_init():
    """初始化时执行的函数"""
    load_sign_in_records()  # 加载签到记录
    logger.info('初始化排行榜插件完成')  # 日志信息
