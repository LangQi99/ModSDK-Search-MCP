from mcp.server.fastmcp import FastMCP
from loguru import logger
import os
import re

mcp = FastMCP()
root_path = "C:/Users/LangQi-Pro/Desktop/github/netease-modsdk-wiki-main/docs/mcdocs/1-ModAPI/接口/"


def clean_markdown_text(text: str) -> str:
    """
    清理markdown文本
    1.|换成空格
    2.清除 | :--- |
    3.清除```
    4.清除##
    5.把连续的空行合并成一个空行
    6.把连续的空格合并成一个空格
    7.把两个相邻的空格和换行符合并成一个空格
    7.去除<xxx>
    """
    # 1
    text = re.sub(r' \| ', ' ', text, flags=re.DOTALL)
    # 2
    text = re.sub(r' :--- ', ' ', text, flags=re.DOTALL)
    # 3
    text = re.sub(r'```', '', text, flags=re.DOTALL)
    # 4
    text = re.sub(r'##(.*?)##', '', text, flags=re.DOTALL)
    # 5
    text = re.sub(r'\n+', '\n', text)
    # 6
    text = re.sub(r'\s+', ' ', text)
    # 7
    text = re.sub(r'\n\s+', ' ', text)
    # 8
    text = re.sub(r'<[^>]*>', '', text)
    return text


@mcp.tool()
def search_api_by_keyword(keyword: str) -> str:
    """
    根据英文或中文关键词搜索实现该功能的ModSKD-API的用法
    """
    result = {}
    for root, dirs, files in os.walk(root_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".md") and "索引" not in file:
                markdown_text = ""
                with open(file_path, "r", encoding="utf-8") as f:
                    markdown_text = f.read()

                # 按照 ## 分段
                sections = re.split(r'(?=## )', markdown_text)
                for section in sections:
                    # 跳过第一个可能不是以 ## 开头的部分
                    if not section.strip().startswith("## "):
                        continue

                    if keyword in section:
                        clean_section = clean_markdown_text(section)
                        key = clean_section.split(" ")[1]
                        result[key] = clean_section
    if len(result) == 0:
        return "没有找到相关内容 请尝试各种其他关键词/同义词等"
    if len(result) > 10:
        return "找到太多相关内容 以下仅仅是函数名 找到可能合适的函数名 把它当做关键词搜索 以获取更多信息"+str(list(result.keys()))
    return result


if __name__ == "__main__":
    # logger.info(search_api_by_Chinese_keyword("经验"))
    mcp.run()
