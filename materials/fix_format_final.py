#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结构化面试观点认知类资料 - 最终格式修复脚本
功能: 稳健修复,不破坏原有格式
"""

import re

def fix_format_final(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ==================== 1. 统一金句标题 ====================
    # 将 **【金句】** 改为 **金句**：
    content = re.sub(r'\*\*【金句】\*\*', '**金句**：', content)
    
    # ==================== 2. 统一引用出处 ====================
    # --习近平 → -- 习近平
    content = re.sub(r'--(\S)', r'-- \1', content)
    
    # ==================== 3. 处理资料标题 ====================
    # - 【资料 1】 → **【资料 1】**
    content = re.sub(r'^- \【资料 (\d+)】', r'**【资料 \1】**', content, flags=re.MULTILINE)
    # 【资料 1】 → **【资料 1】**
    content = re.sub(r'^【资料 (\d+)】', r'**【资料 \1】**', content, flags=re.MULTILINE)
    
    # ==================== 4. 逐行处理金句列表 ====================
    lines = content.split('\n')
    result = []
    in_jinju = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 检测金句开始
        if '**金句**：' in line:
            in_jinju = True
            result.append(line)
            continue
        
        if in_jinju:
            # 检测金句结束
            if (stripped == '' 
                or stripped.startswith('#') 
                or stripped.startswith('**【资料')
                or stripped.startswith('####')
                or stripped.startswith('**（')):
                in_jinju = False
                result.append(line)
                continue
            
            # 处理金句内容
            # 1. 移除整句加粗
            line = re.sub(r'^\*\*(.+?)\*\*$', r'\1', line)
            
            # 2. 替换数字列表 (1. 或 1。) 为 -
            line = re.sub(r'^\s*\d+[.。]\s*', '- ', line)
            
            # 3. 如果有内容但没有 - ,添加
            if line.strip() and not line.strip().startswith('- '):
                line = '- ' + line.strip()
        
        result.append(line)
    
    content = '\n'.join(result)
    
    # ==================== 5. 统一简版/详版格式 ====================
    # **简版：内容** → **简版：** 内容
    content = re.sub(r'\*\*简版：(.+?)\*\*', r'**简版：** \1', content)
    content = re.sub(r'\*\*详版：(.+?)\*\*', r'**详版：** \1', content)
    
    # ==================== 6. 清理多余空行 ====================
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 最终格式修复完成!")
    print(f"📁 输入: {input_file}")
    print(f"📁 输出: {output_file}")

if __name__ == '__main__':
    input_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料.md'
    output_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    fix_format_final(input_path, output_path)
