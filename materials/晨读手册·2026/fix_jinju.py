#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门修复金句格式的脚本
"""

import re

def fix_jinju_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    in_jinju = False
    
    for line in lines:
        stripped = line.strip()
        
        # 检测金句标题
        if '**金句**：' in line:
            in_jinju = True
            result.append(line)
            continue
        
        if in_jinju:
            # 退出条件: 空行、标题、资料标题
            if (stripped == '' 
                or stripped.startswith('#') 
                or stripped.startswith('**【资料')
                or stripped.startswith('####')):
                in_jinju = False
                result.append(line)
                continue
            
            # 1. 移除整句加粗
            line = re.sub(r'^\*\*(.+?)\*\*$', r'\1', line)
            
            # 2. 替换数字列表 (1. 或 1。) 为 -
            line = re.sub(r'^\s*\d+[.。]\s*', '- ', line)
            
            # 3. 如果有内容但没有列表符号,添加
            if line.strip() and not line.strip().startswith('- '):
                line = '- ' + line.strip()
        
        result.append(line)
    
    # 合并回去
    content = '\n'.join(result)
    
    # 修复资料标题的加粗问题: **【资料 1】内容** → **【资料 1】内容** (保持原样)
    # 移除资料标题末尾多余的 **
    content = re.sub(r'(\*\*【资料 \d+】[^\n]+?)\*\*\s*$', r'\1', content, flags=re.MULTILINE)
    
    # 统一引用出处
    content = re.sub(r'--(\S)', r'-- \1', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 金句格式修复完成!")

if __name__ == '__main__':
    input_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    output_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    fix_jinju_format(input_path, output_path)
