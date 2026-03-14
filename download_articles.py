#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量下载番茄小说作家课堂文章
"""

import os
import re
import time
from datetime import datetime

# 模拟的WebReader函数（实际使用时需要替换为真实的WebReader调用）
def fetch_article_content(url):
    """
    使用WebReader获取文章内容
    """
    # 这里应该调用实际的WebReader工具
    # 由于我们在脚本环境中，我们需要返回内容
    print(f"正在获取: {url}")
    # 返回占位符，实际使用时需要调用WebReader
    return None

def extract_article_id_from_file(filepath):
    """
    从文件中提取文章ID
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找文章ID
            match = re.search(r'article/(\d+)', content)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"读取文件错误 {filepath}: {e}")
    return None

def process_file(filepath, article_id):
    """
    处理单个文件：获取内容并更新文件
    """
    url = f"https://fanqienovel.com/writer/zone/article/{article_id}"

    # 获取文章内容
    content = fetch_article_content(url)

    if not content:
        return False, "无法获取内容"

    # 提取标题（从文件名）
    filename = os.path.basename(filepath)
    title = filename.replace('.md', '')

    # 构建新的markdown内容
    new_content = f"""# {title}

> 来源: [番茄小说作家课堂]({url})
> 分类: 分类进阶
> 获取时间: {datetime.now().strftime('%Y-%m-%d')}

---

{content}
"""

    # 写入文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    """
    主函数
    """
    directory = r"D:\workspace\fanqie_novel_articles\分类进阶"

    # 获取所有md文件
    files = [f for f in os.listdir(directory) if f.endswith('.md')]

    print(f"找到 {len(files)} 个markdown文件")
    print("=" * 50)

    success_count = 0
    fail_count = 0
    failed_files = []

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(directory, filename)

        print(f"\n[{i}/{len(files)}] 处理: {filename}")

        # 提取文章ID
        article_id = extract_article_id_from_file(filepath)
        if not article_id:
            print(f"  ✗ 跳过 - 未找到文章ID")
            fail_count += 1
            failed_files.append(f"{filename} (无ID)")
            continue

        print(f"  文章ID: {article_id}")

        # 处理文件
        success, error = process_file(filepath, article_id)

        if success:
            print(f"  ✓ 下载成功")
            success_count += 1
        else:
            print(f"  ✗ 下载失败: {error}")
            fail_count += 1
            failed_files.append(f"{filename} - {error}")

        # 每10个文件报告一次进度
        if i % 10 == 0:
            print("\n" + "=" * 50)
            print(f"进度报告: 已处理 {i} 篇")
            print(f"  成功: {success_count} 篇")
            print(f"  失败: {fail_count} 篇")
            print("=" * 50)

        # 添加延迟避免请求过快
        time.sleep(1)

    # 最终报告
    print("\n" + "=" * 50)
    print("最终报告")
    print("=" * 50)
    print(f"总计: {len(files)} 篇")
    print(f"成功: {success_count} 篇")
    print(f"失败: {fail_count} 篇")

    if failed_files:
        print("\n失败的文件:")
        for failed in failed_files:
            print(f"  - {failed}")

    print("=" * 50)

if __name__ == "__main__":
    main()
