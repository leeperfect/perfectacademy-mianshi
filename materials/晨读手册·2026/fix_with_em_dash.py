#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用中文破折号的格式修复脚本
功能: 统一使用中文破折号（——）作为引用出处
"""

import re

def fix_with_em_dash(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ==================== 1. 统一使用中文破折号 ====================
    # 将 -- 或 -- 替换为 ——
    content = re.sub(r'--\s*', '—— ', content)
    
    # ==================== 2. 统一金句标题 ====================
    content = re.sub(r'\*\*【金句】\*\*', '**金句**：', content)
    
    # ==================== 3. 处理资料标题 ====================
    content = re.sub(r'^- \【资料 (\d+)】', r'**【资料 \1】**', content, flags=re.MULTILINE)
    content = re.sub(r'^【资料 (\d+)】', r'**【资料 \1】**', content, flags=re.MULTILINE)
    
    # ==================== 4. 逐行处理金句列表 ====================
    lines = content.split('\n')
    result = []
    in_jinju = False
    
    for line in lines:
        stripped = line.strip()
        
        if '**金句**：' in line:
            in_jinju = True
            result.append(line)
            continue
        
        if in_jinju:
            if (stripped == '' 
                or stripped.startswith('#') 
                or stripped.startswith('**【资料')
                or stripped.startswith('####')
                or stripped.startswith('**（')):
                in_jinju = False
                result.append(line)
                continue
            
            line = re.sub(r'^\*\*(.+?)\*\*$', r'\1', line)
            line = re.sub(r'^\s*\d+[.。]\s*', '- ', line)
            if line.strip() and not line.strip().startswith('- '):
                line = '- ' + line.strip()
        
        result.append(line)
    
    content = '\n'.join(result)
    
    # ==================== 5. 统一简版/详版格式 ====================
    content = re.sub(r'\*\*简版：(.+?)\*\*', r'**简版：** \1', content)
    content = re.sub(r'\*\*详版：(.+?)\*\*', r'**详版：** \1', content)
    
    # ==================== 6. 清理多余空行 ====================
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 使用中文破折号的格式修复完成!")
    print(f"📁 输入: {input_file}")
    print(f"📁 输出: {output_file}")
    print(f"📝 引用出处已统一使用中文破折号（——）")

if __name__ == '__main__':
    input_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料.md'
    output_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    fix_with_em_dash(input_path, output_path)
