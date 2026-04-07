#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结构化面试观点认知类资料 - 格式统一修复脚本
功能: 统一金句、资料标题、引用出处等格式
"""

import re

def fix_document_format(input_file, output_file):
    """
    修复文档格式
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ==================== 1. 统一金句标题格式 ====================
    # 将所有金句标题统一为: **金句**：
    content = re.sub(r'\*\*【金句】\*\*', '**金句**：', content)
    content = re.sub(r'\*\*金句\*\*\s*：', '**金句**：', content)
    
    # ==================== 2. 统一资料标题格式 ====================
    # 将所有资料标题统一为: **【资料 X】标题**
    # 移除前面的列表符号
    content = re.sub(r'^- \*\*【资料', '**【资料', content, flags=re.MULTILINE)
    content = re.sub(r'^- 【资料', '**【资料', content, flags=re.MULTILINE)
    # 确保资料标题都加粗
    content = re.sub(r'^【资料 (\d+)】', r'**【资料 \1】**', content, flags=re.MULTILINE)
    
    # ==================== 3. 统一引用出处格式 ====================
    # 确保引用出处格式为: -- 习近平总书记...
    content = re.sub(r'--(\S)', r'-- \1', content)
    
    # ==================== 4. 修复金句列表格式 ====================
    # 将数字列表 (1. 或 1。) 改为 - 开头
    # 在金句标题之后的内容
    lines = content.split('\n')
    result = []
    in_jinju_section = False
    
    for i, line in enumerate(lines):
        # 检测是否进入金句部分
        if '**金句**：' in line:
            in_jinju_section = True
            result.append(line)
            continue
        
        if in_jinju_section:
            # 如果遇到空行或新的标题,退出金句部分
            if line.strip() == '' or line.strip().startswith('#') or line.strip().startswith('**【资料'):
                in_jinju_section = False
                result.append(line)
                continue
            
            # 修复数字列表: 1. 句子 或 1。句子 → - 句子
            # 先移除多余的加粗
            line = re.sub(r'^\*\*(\d+[.。]\s*.+?)\*\*$', r'\1', line)
            # 替换数字列表为 -
            line = re.sub(r'^\d+[.。]\s*', '- ', line)
            # 如果没有列表符号但有内容,添加 -
            if line.strip() and not line.strip().startswith('- '):
                # 检查是否是金句内容
                line = '- ' + line.strip()
        
        result.append(line)
    
    content = '\n'.join(result)
    
    # ==================== 5. 修复加粗标签错误 ====================
    # 修复不完整的加粗标签,例如: **简版：...** 中间被打断
    # 找到所有加粗标签并确保它们配对
    # 这个问题比较复杂,我们重点处理明显的错误
    content = re.sub(r'\*\*简版："当代愚公"毛相林，\*\*\s*始终坚持实干，\*\*深山修路闯脱贫，以民为先谋振兴。\*\*', 
                     '**简版：** "当代愚公"毛相林，始终坚持实干，深山修路闯脱贫，以民为先谋振兴。', 
                     content)
    
    # ==================== 6. 移除空标题标记 ====================
    content = re.sub(r'^###\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^####\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^##\s*$', '', content, flags=re.MULTILINE)
    
    # ==================== 7. 清理多余空行 ====================
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 格式修复完成!")
    print(f"📁 输入文件: {input_file}")
    print(f"📁 输出文件: {output_file}")

if __name__ == '__main__':
    input_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料.md'
    output_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    fix_document_format(input_path, output_path)
