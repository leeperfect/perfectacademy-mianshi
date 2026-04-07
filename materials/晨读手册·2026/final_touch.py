#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终润色脚本 - 修复细节问题
"""

import re

def final_touch(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ==================== 1. 修复资料标题的加粗问题 ====================
    # **【资料 1】** 内容 → **【资料 1】内容**
    content = re.sub(r'\*\*【资料 (\d+)】\*\*\s*([^\n]+)', r'**【资料 \1】\2**', content)
    
    # ==================== 2. 修复金句标题多余空格 ====================
    # **金句** ： → **金句**：
    content = re.sub(r'\*\*金句\*\*\s*：', '**金句**：', content)
    
    # ==================== 3. 重新完整处理金句列表 ====================
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
            # 退出条件
            if (stripped == '' 
                or stripped.startswith('#') 
                or stripped.startswith('**【资料')
                or stripped.startswith('####')
                or stripped.startswith('**（')):
                in_jinju = False
                result.append(line)
                continue
            
            # 处理金句
            line = re.sub(r'^\*\*(.+?)\*\*$', r'\1', line)  # 移除整句加粗
            line = re.sub(r'^\s*\d+[.。]\s*', '- ', line)  # 数字列表转 -
            if line.strip() and not line.strip().startswith('- '):
                line = '- ' + line.strip()
        
        result.append(line)
    
    content = '\n'.join(result)
    
    # ==================== 4. 修复简版/详版的不完整加粗标签 ====================
    content = re.sub(r'\*\*简版：\*\*\s*"当代愚公"毛相林，\s*始终坚持实干，\*\*深山修路闯脱贫，以民为先谋振兴。\*\*', 
                     r'**简版：** "当代愚公"毛相林，始终坚持实干，深山修路闯脱贫，以民为先谋振兴。', 
                     content)
    
    # ==================== 5. 清理多余空行 ====================
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 最终润色完成!")

if __name__ == '__main__':
    input_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    output_path = '/Users/pf.macbookpro/PerfectAcademyPro/mianshi/materials/结构化面试观点认知类资料_已修复.md'
    final_touch(input_path, output_path)
