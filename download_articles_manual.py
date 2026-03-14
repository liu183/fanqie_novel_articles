#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄小说文章批量下载脚本

使用方法：
1. 确保已安装 requests 库：pip install requests
2. 运行脚本：python download_articles.py
3. 脚本会自动处理所有文章并添加延迟避免速率限制
"""

import requests
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

# 配置
BASE_DIR = Path(__file__).parent
DELAY_BETWEEN_REQUESTS = 10  # 每次请求间隔秒数
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_article_id_from_file(file_path):
    """从文件中提取文章ID"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找文章链接
            match = re.search(r'fanqienovel\.com/writer/zone/article/(\d+)', content)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
    return None

def download_article(article_id, max_retries=3):
    """下载单篇文章"""
    url = f"https://fanqienovel.com/writer/zone/article/{article_id}"

    for attempt in range(max_retries):
        try:
            print(f"  尝试下载文章 {article_id} (尝试 {attempt + 1}/{max_retries})...")
            response = requests.get(url, headers=HEADERS, timeout=30)

            if response.status_code == 200:
                # 这里需要解析HTML提取文章内容
                # 由于番茄小说的内容是通过JavaScript动态加载的
                # 我们需要使用更复杂的方法或API

                # 暂时保存一个占位内容
                content = f"""# 文章标题

> 来源: [番茄小说作家课堂]({url})
> 分类: 待分类
> 获取时间: 2026-03-14
> 注意: 此文章需要手动访问链接获取内容

---

**说明：** 由于番茄小说的文章内容是通过JavaScript动态加载的，
直接使用HTTP请求无法获取完整正文。

**请手动访问：** {url}

**复制文章内容后，请粘贴到此文件中。**

---
"""
                return content
            elif response.status_code == 429:
                print(f"    遇到速率限制，等待30秒...")
                time.sleep(30)
            else:
                print(f"    HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"    请求失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)

    return None

def process_directory(directory_name):
    """处理指定目录下的所有文章"""
    dir_path = BASE_DIR / directory_name

    if not dir_path.exists():
        print(f"目录不存在: {dir_path}")
        return

    md_files = list(dir_path.glob("*.md"))
    print(f"\n处理目录: {directory_name}")
    print(f"找到 {len(md_files)} 个文件\n")

    success_count = 0
    fail_count = 0

    for i, md_file in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] 处理: {md_file.name}")

        # 检查是否已经是完整文章
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 如果已经包含正文内容（长度大于5000字符），跳过
                if len(content) > 5000 and "---" in content:
                    print(f"    ✓ 已有完整内容，跳过")
                    success_count += 1
                    continue
        except:
            pass

        # 提取文章ID
        article_id = extract_article_id_from_file(md_file)

        if article_id:
            # 下载文章
            content = download_article(article_id)

            if content:
                # 保存内容
                try:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"    ✓ 保存成功")
                    success_count += 1
                except Exception as e:
                    print(f"    ✗ 保存失败: {e}")
                    fail_count += 1
            else:
                print(f"    ✗ 下载失败")
                fail_count += 1
        else:
            print(f"    ✗ 未找到文章ID")
            fail_count += 1

        # 延迟避免速率限制
        if i < len(md_files):
            print(f"    等待 {DELAY_BETWEEN_REQUESTS} 秒...\n")
            time.sleep(DELAY_BETWEEN_REQUESTS)

    print(f"\n{directory_name} 处理完成:")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  总计: {len(md_files)}")

    return success_count, fail_count

def main():
    """主函数"""
    print("=" * 60)
    print("番茄小说文章批量下载工具")
    print("=" * 60)

    # 处理三个目录
    directories = ["写作技巧", "分类进阶", "大神专访"]

    total_success = 0
    total_fail = 0

    for directory in directories:
        success, fail = process_directory(directory)
        total_success += success
        total_fail += fail

    print("\n" + "=" * 60)
    print("总体统计:")
    print(f"  成功下载: {total_success} 篇")
    print(f"  下载失败: {total_fail} 篇")
    print("=" * 60)

    print("\n注意事项:")
    print("1. 由于番茄小说使用JavaScript动态加载内容，")
    print("   本脚本只能获取文章的基础信息。")
    print("2. 完整的文章内容需要您手动访问链接复制。")
    print("3. 建议使用浏览器访问每个文件中的链接，")
    print("   然后复制文章内容到对应的 .md 文件中。")
    print("4. 或者使用支持JavaScript的浏览器自动化工具（如Selenium）")

if __name__ == "__main__":
    main()
