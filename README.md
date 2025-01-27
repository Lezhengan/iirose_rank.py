markdown
# 签到系统插件

这是一个用于房间聊天的签到系统插件。用户可以通过发送特定的指令进行签到，系统会记录用户的签到信息并生成排名。

## 功能

- **签到功能**：用户可以随时通过 `/z` 指令进行签到。
- **运势判断**：签到时系统将随机生成运势（上上签、上吉签、中吉签、中平签、下下签）。
- **排名系统**：根据运势的优劣进行排名，并提供今天的签到情况。
- **排行榜指令**：用户可以通过 `/rank` 指令查看当前的签到排行榜。

## 安装

确保你有Python 3.11 及以上环境，并安装以下依赖包：

```bash
pip install loguru
```
并放置于iirosebot目录下的plugin文件夹内
## 使用方法

1. 在你的聊天系统中将该插件集成。
2. 使用 `/z` 指令进行签到。例如：
   ```
   /z
   ```
3. 使用 `/rank` 指令查看当前的签到排行榜。例如：
   ```
   /rank
   ```

## 签到信息

每次用户签到后，系统会返回用户的签到信息，包括：

- 用户名
- 排名
- 今日的运势
- 签到时间

如果用户当天已签到，则系统会提示用户。

## 示例

用户 A 签到后，系统返回的消息可能如下所示：
```
## # **乐正安**

---

用户名： **落零レ**
排名： **#5**
你是今天第 **5** 个签到的！
时间： **03:22**

**今日运势！ 中平**

---

*您可以发送 /rank 查看签到详情*
```
## 贡献

欢迎提交问题、建议或贡献代码！
