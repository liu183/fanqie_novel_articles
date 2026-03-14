#!/bin/bash

# 设置目录
DIR="D:\workspace\fanqie_novel_articles\大神专访"
SUCCESS_COUNT=0
FAIL_COUNT=0
FAILED_LIST=()

# 计数器
TOTAL=0
PROGRESS_INTERVAL=10

# 遍历所有md文件
for file in "$DIR"/*.md; do
    # 提取文件名
    filename=$(basename "$file")
    TOTAL=$((TOTAL + 1))

    # 提取文章ID
    article_id=$(grep -oP 'article/\K[0-9]+' "$file" 2>/dev/null | head -1)

    if [ -z "$article_id" ]; then
        echo "跳过 $filename - 未找到文章ID"
        FAILED_LIST+=("$filename (无ID)")
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi

    # 构建URL
    url="https://fanqienovel.com/writer/zone/article/$article_id"

    echo "[$TOTAL] 正在下载: $filename"
    echo "    URL: $url"

    # 使用curl下载内容
    content=$(curl -s -L "$url" 2>&1)

    if [ $? -ne 0 ] || [ -z "$content" ]; then
        echo "    下载失败"
        FAILED_LIST+=("$filename")
        FAIL_COUNT=$((FAIL_COUNT + 1))
    else
        echo "    下载成功"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    fi

    # 每处理10个文件报告一次进度
    if [ $((TOTAL % PROGRESS_INTERVAL)) -eq 0 ]; then
        echo "===== 进度报告 ====="
        echo "已处理: $TOTAL 篇"
        echo "成功: $SUCCESS_COUNT 篇"
        echo "失败: $FAIL_COUNT 篇"
        echo "==================="
    fi

    # 添加延迟避免请求过快
    sleep 1
done

# 最终报告
echo ""
echo "===== 最终报告 ====="
echo "总计: $TOTAL 篇"
echo "成功: $SUCCESS_COUNT 篇"
echo "失败: $FAIL_COUNT 篇"
echo ""
if [ $FAIL_COUNT -gt 0 ]; then
    echo "失败的文件:"
    for failed in "${FAILED_LIST[@]}"; do
        echo "  - $failed"
    done
fi
echo "==================="

