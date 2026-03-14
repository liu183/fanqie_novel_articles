# 番茄小说大神专访文章下载方案

## 当前状态

- 总文章数: 66篇
- 已成功下载: 1篇
- 待下载: 65篇
- 主要障碍: WebReader API速率限制

## 问题分析

在使用WebReader工具批量下载文章时，遇到了以下问题：

1. **API速率限制**: 错误代码1302，提示"Rate limit reached for requests"
2. **请求间隔**: 需要在每次请求之间等待至少5-10秒
3. **批量处理**: 66篇文章需要分批处理，每批建议不超过10篇

## 解决方案

### 方案一：使用Python脚本 + WebReader API（推荐）

创建一个自动化脚本，包含速率限制和重试机制：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄小说文章批量下载脚本
"""

import time
import os
import re
from datetime import datetime

def download_article(url, max_retries=3):
    """
    下载单篇文章（需要集成WebReader API）
    """
    for attempt in range(max_retries):
        try:
            # 这里需要调用实际的WebReader API
            # 由于速率限制，每次请求后需要等待
            time.sleep(5)  # 等待5秒

            # 模拟API调用
            # content = call_webreader_api(url)

            # 如果成功，返回内容
            return content, None

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10  # 递增等待时间
                print(f"  请求失败，{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                return None, str(e)

def process_article(filepath, article_id):
    """
    处理单篇文章
    """
    url = f"https://fanqienovel.com/writer/zone/article/{article_id}"

    print(f"正在下载: {os.path.basename(filepath)}")
    print(f"  URL: {url}")

    content, error = download_article(url)

    if error:
        print(f"  ✗ 下载失败: {error}")
        return False, error

    # 提取标题
    filename = os.path.basename(filepath)
    title = filename.replace('.md', '')

    # 构建新的markdown内容
    new_content = f"""# {title}

> 来源: [番茄小说作家课堂]({url})
> 分类: 大神专访
> 获取时间: {datetime.now().strftime('%Y-%m-%d')}

---

{content}
"""

    # 保存文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ 下载成功")
        return True, None
    except Exception as e:
        print(f"  ✗ 保存失败: {e}")
        return False, str(e)

def main():
    """
    主函数
    """
    directory = r"D:\workspace\fanqie_novel_articles\大神专访"

    # 获取所有md文件
    files = [f for f in os.listdir(directory) if f.endswith('.md')]

    # 跳过已下载的文件（检查文件大小）
    downloaded_files = []
    for f in files:
        filepath = os.path.join(directory, f)
        if os.path.getsize(filepath) > 1000:  # 已下载的文件通常大于1KB
            downloaded_files.append(f)

    print(f"总文件数: {len(files)}")
    print(f"已下载: {len(downloaded_files)}")
    print(f"待下载: {len(files) - len(downloaded_files)}")
    print("=" * 80)

    # 提取待下载的文章
    articles_to_download = []
    for filename in files:
        if filename in downloaded_files:
            continue

        filepath = os.path.join(directory, filename)

        # 提取文章ID
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'article/(\d+)', content)
                if match:
                    article_id = match.group(1)
                    articles_to_download.append((filepath, filename, article_id))
        except:
            pass

    print(f"\n准备下载 {len(articles_to_download)} 篇文章\n")

    success_count = 0
    fail_count = 0
    failed_articles = []

    # 分批处理
    batch_size = 10
    for i in range(0, len(articles_to_download), batch_size):
        batch = articles_to_download[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(articles_to_download) + batch_size - 1) // batch_size

        print(f"\n【第{batch_num}/{total_batches}批】处理 {len(batch)} 篇文章")
        print("-" * 80)

        for j, (filepath, filename, article_id) in enumerate(batch, 1):
            print(f"[{i+j}/{len(articles_to_download)}] {filename}")

            success, error = process_article(filepath, article_id)

            if success:
                success_count += 1
            else:
                fail_count += 1
                failed_articles.append(f"{filename} - {error}")

            print()

        print(f"第{batch_num}批完成")
        print(f"  成功: {success_count}")
        print(f"  失败: {fail_count}")
        print("=" * 80)

        # 批次之间等待更长时间
        if batch_num < total_batches:
            print("等待30秒后处理下一批...")
            time.sleep(30)

    # 最终报告
    print("\n" + "=" * 80)
    print("最终报告")
    print("=" * 80)
    print(f"总计: {len(articles_to_download)} 篇")
    print(f"成功: {success_count} 篇")
    print(f"失败: {fail_count} 篇")

    if failed_articles:
        print("\n失败的文件:")
        for failed in failed_articles:
            print(f"  - {failed}")

if __name__ == "__main__":
    main()
```

### 方案二：手动逐个下载

由于API限制，可以手动逐个使用WebReader工具下载：

1. 每次下载一篇文章
2. 等待5-10秒
3. 继续下一篇
4. 每完成10篇报告一次进度

具体步骤：

```
1. 使用WebReader工具获取文章内容：
   mcp__web_reader__webReader(
       url="https://fanqienovel.com/writer/zone/article/[文章ID]",
       return_format="markdown",
       retain_images=false
   )

2. 等待5-10秒

3. 将内容保存到对应的md文件

4. 重复步骤1-3
```

### 方案三：使用curl命令行工具

如果WebReader工具持续受限，可以使用curl命令：

```bash
#!/bin/bash

# 文章列表
articles=(
    "7585478927619997720"
    "7577778558118920216"
    "7577731229638737982"
    # ... 其他文章ID
)

BASE_URL="https://fanqienovel.com/writer/zone/article"
OUTPUT_DIR="D:\workspace\fanqie_novel_articles\大神专访"

for article_id in "${articles[@]}"; do
    echo "下载文章: $article_id"

    # 使用curl下载
    curl -s "${BASE_URL}/${article_id}" \
         -H "User-Agent: Mozilla/5.0" \
         -o "${OUTPUT_DIR}/temp_${article_id}.html"

    # 等待5秒
    sleep 5

    # 解析HTML并提取内容（需要使用html2text或类似工具）
    # html2text "${OUTPUT_DIR}/temp_${article_id}.html" > "${OUTPUT_DIR}/${article_id}.md"

    echo "完成: $article_id"
done
```

## 推荐执行步骤

1. **第一阶段**: 下载前10篇文章（文章ID: 7585478927619997720 到 7525034514356109337）
2. **等待30秒**
3. **第二阶段**: 下载第11-20篇文章
4. **等待30秒**
5. **第三阶段**: 下载第21-30篇文章
6. **依此类推...**

## 文章ID列表（按批次）

### 第1批（已完成1篇，剩余9篇）
- 7585478927619997720 (番茄大师课_东西)
- 7577778558118920216 (十二日谈｜阿来、刘慈欣等)
- 7577731229638737982 (十二日谈｜王跃文等)
- 7577730557451190334 (十二日谈｜阿来、管平潮等)
- 7576975849325330456 (番茄大师课_阿来)
- 7576970189472808984 (番茄大师课_格非)
- 7522364779684446233 (番茄作者的十年成长)
- 7520184286729748504 (从孤独写手到情感共鸣者)
- 7524921385353740313 (她的江湖是从心出发)
- 7525034514356109337 (爆款制造者)

### 第2批（10篇）
- 7470485838405582910 到 7221745416633581627

### 第3批（10篇）
- 7211442623062474812 到 7069669035889131527

### 第4批（10篇）
- 7062639869519986695 到 7091875924219527176

### 第5批（10篇）
- 7097121555632619550 到 7026224049063723044

### 第6批（10篇）
- 7026224824481480717 到 7138359901453025317

### 第7批（6篇）
- 7136107228288778253 到 7149101743404482591

## 注意事项

1. **速率限制**: 每次请求间隔至少5秒
2. **错误处理**: 遇到错误时增加等待时间并重试
3. **内容验证**: 下载后检查文件大小，确保内容完整
4. **备份数据**: 定期备份已下载的文章
5. **网络稳定**: 确保网络连接稳定，避免中断

## 完成标准

- 成功下载65篇文章（除已完成的1篇）
- 所有文章格式统一
- 每篇文章包含完整的标题、来源、分类、时间和正文内容
- 生成最终报告，包含成功和失败列表
