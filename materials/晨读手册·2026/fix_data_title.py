#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复资料标题格式的脚本
"""

import re

def fix_data_title(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复资料标题的加粗问题: **【资料 1】** 内容 → **【资料 1】内容**
    # 这个问题比较复杂,我们逐行处理
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # 检测资料标题行
        if '**【资料' in line:
            # 修复: **【资料 1】** 内容 → **【资料 1】内容**
            line = re.sub(r'\*\*【资料 (\d+)】\*\*\s*([^\n]+)', r'**【资料 \1】\2**', line)
            # 修复: **【资料 1】标题** → 保持原样(已正确)
            # 修复: 【资料 1】标题 → **【资料 1】标题**
            if not line.startswith('**【资料') and '【资料' in line:
                line = re.sub(r'【资料 (\d+)】([^\n]+)', r'**【资料 \1】\2**', line)
        
        result.append(line)
    
    content = '\n'.join(result)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 资料标题格式修复完成!")

if __name__ == '__main__':
    input_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    output_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    fix_data_title(input_path, output_path)
