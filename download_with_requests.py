#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用requests库批量下载番茄小说作家课堂文章
"""
import os
import re
import time
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin

# 配置
ARTICLE_DIR = r"D:\workspace\fanqie_novel_articles\分类进阶"
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d")

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def get_filename_from_url(url):
    """从URL获取对应的文件名"""
    # 读取URL映射文件
    url_file = Path(r"D:\workspace\fanqie_novel_articles\article_urls.txt")
    if url_file.exists():
        with open(url_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '|' in line:
                    parts = line.split('|')
                    if len(parts) == 2 and parts[1].strip() == url:
                        return parts[0].strip()
    return None

def fetch_with_requests(url):
    """使用requests获取网页内容"""
    try:
        print(f"  正在获取: {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"  请求错误: {e}")
        return None

def parse_html_content(html_content):
    """解析HTML内容，提取文章信息"""
    from bs4 import BeautifulSoup

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # 尝试多种方式提取标题
        title = None
        for selector in ['h1', 'title', '.article-title', '#article-title']:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text().strip()
                break

        # 尝试多种方式提取正文
        content = None
        for selector in [
            'article',
            '.article-content',
            '#article-content',
            '.content',
            '#content',
            '.post-content',
            '.entry-content'
        ]:
            elem = soup.select_one(selector)
            if elem:
                # 提取纯文本
                content = elem.get_text(separator='\n', strip=True)
                if len(content) > 100:  # 确保内容足够长
                    break

        # 如果仍然没有找到内容，尝试获取整个body的文本
        if not content or len(content) < 100:
            body = soup.find('body')
            if body:
                content = body.get_text(separator='\n', strip=True)

        return title, content

    except Exception as e:
        print(f"  解析错误: {e}")
        return None, None

def save_article(filepath, url, title, content):
    """保存文章到文件"""
    try:
        # 获取文件名（不含扩展名）作为默认标题
        default_title = Path(filepath).stem

        # 构建新的内容
        new_content = f"# {title or default_title}\n\n"
        new_content += f"> 来源: [番茄小说作家课堂]({url})\n"
        new_content += f"> 分类: 分类进阶\n"
        new_content += f"> 获取时间: {CURRENT_TIME}\n\n"
        new_content += "---\n\n"
        new_content += content or "内容获取失败，请手动检查"

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"  保存错误: {e}")
        return False

def main():
    """主函数"""
    # 读取URL列表
    url_file = Path(r"D:\workspace\fanqie_novel_articles\article_urls.txt")
    if not url_file.exists():
        print("错误: article_urls.txt 文件不存在")
        return

    # 读取所有URL
    articles = []
    with open(url_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '|' in line:
                parts = line.split('|')
                if len(parts) == 2:
                    filename = parts[0].strip()
                    url = parts[1].strip()
                    filepath = os.path.join(ARTICLE_DIR, filename)
                    articles.append((filepath, filename, url))

    print(f"找到 {len(articles)} 个文章需要处理")
    print("=" * 60)

    success_count = 0
    failed_count = 0
    failed_articles = []

    for index, (filepath, filename, url) in enumerate(articles, 1):
        print(f"\n[{index}/{len(articles)}] 处理: {filename}")

        # 检查文件是否存在
        if not os.path.exists(filepath):
            print(f"  ✗ 文件不存在: {filepath}")
            failed_count += 1
            failed_articles.append((filename, "文件不存在"))
            continue

        # 获取网页内容
        html_content = fetch_with_requests(url)

        if not html_content:
            print(f"  ✗ 无法获取网页内容")
            failed_count += 1
            failed_articles.append((filename, "无法获取网页"))
            time.sleep(5)  # 等待后继续
            continue

        # 解析HTML
        title, content = parse_html_content(html_content)

        if not title and not content:
            print(f"  ✗ 无法解析文章内容")
            failed_count += 1
            failed_articles.append((filename, "无法解析内容"))
            time.sleep(5)  # 等待后继续
            continue

        # 保存文章
        if save_article(filepath, url, title, content):
            print(f"  ✓ 保存成功")
            success_count += 1
        else:
            print(f"  ✗ 保存失败")
            failed_count += 1
            failed_articles.append((filename, "保存失败"))

        # 每10个文件报告一次
        if index % 10 == 0:
            print("\n" + "=" * 60)
            print(f"进度报告: 已处理 {index}/{len(articles)} 篇")
            print(f"  成功: {success_count} 篇")
            print(f"  失败: {failed_count} 篇")
            print("=" * 60)

        # 添加延迟，避免请求过快
        if index < len(articles):
            wait_time = 5  # 每个请求之间等待5秒
            print(f"  等待 {wait_time} 秒...")
            time.sleep(wait_time)

    # 最终报告
    print("\n" + "=" * 60)
    print("最终报告")
    print("=" * 60)
    print(f"总计: {len(articles)} 篇")
    print(f"成功: {success_count} 篇")
    print(f"失败: {failed_count} 篇")

    if failed_articles:
        print("\n失败列表:")
        for filename, reason in failed_articles:
            print(f"  - {filename}: {reason}")

    print("=" * 60)

if __name__ == "__main__":
    main()
