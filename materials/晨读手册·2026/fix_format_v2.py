#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结构化面试观点认知类资料 - 格式统一修复脚本 v2.0
功能: 更全面地修复格式问题
"""

import re

def fix_document_format_v2(input_file, output_file):
    """
    修复文档格式 v2
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ==================== 1. 修复资料标题的加粗问题 ====================
    # 修复: **【资料 2】**标题 → **【资料 2】标题**
    content = re.sub(r'\*\*【资料 (\d+)】\*\*([^\n]+)', r'**【资料 \1】\2**', content)
    
    # ==================== 2. 统一金句列表格式 ====================
    lines = content.split('\n')
    result = []
    in_jinju_section = False
    jinju_start_line = -1
    
    for i, line in enumerate(lines):
        # 检测是否进入金句部分
        if '**金句**：' in line:
            in_jinju_section = True
            jinju_start_line = i
            result.append(line)
            continue
        
        if in_jinju_section:
            # 如果遇到空行或新的标题,退出金句部分
            stripped = line.strip()
            if stripped == '' or stripped.startswith('#') or stripped.startswith('**【资料'):
                in_jinju_section = False
                result.append(line)
                continue
            
            # 移除整句加粗
            line = re.sub(r'^\*\*(.+?)\*\*$', r'\1', line)
            
            # 替换数字列表为 - (包括中文句号)
            line = re.sub(r'^\d+[.。]\s*', '- ', line)
            
            # 确保有列表符号
            if line.strip() and not line.strip().startswith('- '):
                line = '- ' + line.strip()
        
        result.append(line)
    
    content = '\n'.join(result)
    
    # ==================== 3. 修复简版/详版的加粗格式 ====================
    # 修复: **简版：内容** → **简版：** 内容
    content = re.sub(r'\*\*简版：(.+?)\*\*', r'**简版：** \1', content)
    content = re.sub(r'\*\*详版：(.+?)\*\*', r'**详版：** \1', content)
    
    # 修复不完整的加粗标签
    content = re.sub(r'\*\*简版："当代愚公"毛相林，\*\*\s*始终坚持实干，深山修路闯脱贫，以民为先谋振兴。', 
                     r'**简版：** "当代愚公"毛相林，始终坚持实干，深山修路闯脱贫，以民为先谋振兴。', 
                     content)
    
    # ==================== 4. 统一引用出处格式 ====================
    # 确保引用出处有空格: --习近平 → -- 习近平
    content = re.sub(r'--(\S)', r'-- \1', content)
    
    # ==================== 5. 清理多余空行 ====================
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # ==================== 6. 移除多余的空格 ====================
    # 移除行尾空格
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    content = '\n'.join(lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ v2.0 格式修复完成!")
    print(f"📁 输入文件: {input_file}")
    print(f"📁 输出文件: {output_file}")

if __name__ == '__main__':
    input_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    output_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    fix_document_format_v2(input_path, output_path)
