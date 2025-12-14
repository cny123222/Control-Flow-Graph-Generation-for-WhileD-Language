"""
自定义测试用例模板

使用说明：
1. 复制此文件到项目根目录，并重命名为你的测试文件名（如 my_test.py）
2. 修改 source 和 program 部分
3. 在项目根目录运行: python my_test.py
4. 生成的 Mermaid 文件会保存在 mermaid_outputs/custom/ 目录

注意：必须从项目根目录运行此脚本，因为需要导入项目模块
"""

from ast_definition import *
from ir_representation import *
from cfg_generator import CFGGenerator
import os

def save_mermaid(name: str, source: str, program: Com, output_file: str):
    """生成并保存 Mermaid 流程图"""
    generator = CFGGenerator()
    cfg = generator.generate_cfg(program)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {name}\n\n")
        f.write(f"**源程序**: `{source}`\n\n")
        
        f.write("## 阶段1：表达式拆分 (LABEL)\n\n")
        f.write("```\n")
        for instr in cfg.linear_ir:
            if hasattr(instr, 'name'):
                f.write(f"{instr.name}:\n")
            else:
                f.write(f"    {instr}\n")
        f.write("```\n\n")
        
        f.write("## 阶段2：基本块 (BB)\n\n")
        f.write("```\n")
        for instr in cfg.bb_ir:
            if hasattr(instr, 'name'):
                f.write(f"{instr.name}:\n")
            else:
                f.write(f"    {instr}\n")
        f.write("```\n\n")
        
        f.write("## 阶段3：控制流图\n\n")
        f.write("```mermaid\n")
        f.write(cfg.to_mermaid())
        f.write("\n```\n")
    
    print(f"✓ 已保存到 {output_file}")

# ============================================
# 修改以下部分来创建你的测试用例
# ============================================

# 测试名称
test_name = "我的测试用例"

# 源程序（用于显示）
source = "x = a + b"

# 构建 AST
program = CAsgnVar(
    "x",
    EBinop("+", EVar("a"), EVar("b"))
)

# ============================================
# 生成文件
# ============================================

# 确保输出目录存在
output_dir = "mermaid_outputs/custom"
os.makedirs(output_dir, exist_ok=True)

# 生成 Mermaid 文件
output_file = f"{output_dir}/my_test.md"
save_mermaid(test_name, source, program, output_file)

# 同时在终端打印结果
print("\n生成的 IR:")
generator = CFGGenerator()
cfg = generator.generate_cfg(program)
print(cfg)

print(f"\n查看流程图:")
print(f"  方法1（推荐）: 在 VSCode 中打开 {output_file}，点击预览图标")
print(f"  方法2: 访问 https://mermaid.live/，复制 Mermaid 代码查看")

