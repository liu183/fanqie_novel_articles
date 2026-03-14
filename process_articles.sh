#!/bin/bash
# 批量处理番茄小说文章

ARTICLE_DIR="D:\\workspace\\fanqie_novel_articles\\分类进阶"
CURRENT_DATE=$(date +%Y-%m-%d)

# 创建临时文件来存储失败列表
FAILED_LIST="D:\\workspace\\fanqie_novel_articles\\failed_articles.txt"
echo "" > "$FAILED_LIST"

# 计数器
total=0
success=0
failed=0

# 遍历所有md文件
for file in "$ARTICLE_DIR"/*.md; do
    if [ -f "$file" ]; then
        total=$((total + 1))
        filename=$(basename "$file")

        echo "[$total] 处理: $filename"

        # 提取链接
        url=$(grep -oE 'https://fanqienovel\.com/writer/zone/article/[0-9]+' "$file" | head -1)

        if [ -z "$url" ]; then
            echo "  ✗ 跳过 - 未找到链接"
            failed=$((failed + 1))
            echo "$filename - 未找到链接" >> "$FAILED_LIST"
            continue
        fi

        echo "  链接: $url"

        # 这里需要调用webReader工具
        # 由于shell脚本无法直接调用MCP工具，我们需要使用其他方法
        echo "  注意: 需要使用webReader工具获取内容"

        # 每10个文件报告一次
        if [ $((total % 10)) -eq 0 ]; then
            echo ""
            echo "=== 进度报告 ==="
            echo "已处理: $total"
            echo "成功: $success"
            echo "失败: $failed"
            echo ""
        fi
    fi
done

echo ""
echo "=== 最终报告 ==="
echo "总计: $total"
echo "成功: $success"
echo "失败: $failed"
