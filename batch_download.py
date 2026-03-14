#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量下载番茄小说作家课堂文章 - 分批处理版本
由于API限制，需要分批处理并添加延迟
"""

import os
import re
import time
import subprocess
import json
from datetime import datetime

def call_webreader(url):
    """
    调用WebReader MCP工具
    """
    # 由于速率限制，这里需要等待
    time.sleep(3)  # 每次请求等待3秒

    # 构建MCP调用（这需要实际集成到Claude Code环境中）
    # 这里返回None表示需要手动处理
    return None

def extract_article_info(filepath):
    """
    从文件中提取文章信息
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取文章ID
        match = re.search(r'article/(\d+)', content)
        if not match:
            return None, None

        article_id = match.group(1)
        url = f"https://fanqienovel.com/writer/zone/article/{article_id}"

        # 提取标题
        filename = os.path.basename(filepath)
        title = filename.replace('.md', '')

        return title, url

    except Exception as e:
        print(f"读取文件错误 {filepath}: {e}")
        return None, None

def generate_article_links():
    """
    生成所有需要下载的文章链接列表
    """
    directory = r"D:\workspace\fanqie_novel_articles\大神专访"
    files = [f for f in os.listdir(directory) if f.endswith('.md')]

    articles = []

    for filename in sorted(files):
        filepath = os.path.join(directory, filename)
        title, url = extract_article_info(filepath)

        if url:
            articles.append({
                'filename': filename,
                'filepath': filepath,
                'title': title,
                'url': url
            })

    return articles

def main():
    """
    主函数 - 生成文章列表供手动处理
    """
    articles = generate_article_links()

    print(f"找到 {len(articles)} 篇文章")
    print("\n文章列表:")
    print("=" * 80)

    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   URL: {article['url']}")
        print(f"   File: {article['filepath']}")
        print()

    # 保存到JSON文件供后续处理
    output_file = r"D:\workspace\fanqie_novel_articles\articles_list.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"文章列表已保存到: {output_file}")
    print("\n建议分批处理（每批10篇），每次请求间隔3秒以上")

if __name__ == "__main__":
    main()
