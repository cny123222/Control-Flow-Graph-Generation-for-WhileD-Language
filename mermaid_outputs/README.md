# Mermaid 流程图测试结果

本目录包含所有测试用例的 Mermaid 流程图，按来源分类存储。

## 目录结构

```
mermaid_outputs/
├── demo/          # demo.py 生成的测试用例（6个）
├── main/          # main.py 生成的测试用例（10个）
├── custom/        # 用户自定义测试用例
└── README.md      # 本文件
```

## 如何查看流程图

### 方法 1: VSCode 预览（推荐）

1. 在 VSCode 中打开任意 `.md` 文件
2. 点击右上角的预览图标（或按 `Cmd+Shift+V` / `Ctrl+Shift+V`）
3. 流程图会自动渲染显示

### 方法 2: 在线查看

1. 访问 https://mermaid.live/
2. 复制 MD 文件中的 Mermaid 代码块（```mermaid ... ```）到编辑器
3. 右侧会自动显示流程图

## 各目录说明

### 📁 demo/

`demo.py` 生成的演示测试用例（6个）：

- 测试1：简单While循环
- 测试2：If-Else分支
- 测试3：短路求值AND
- 测试4：短路求值OR
- 测试5：嵌套控制流
- 测试6：指针操作

**生成方法**:
```bash
python demo.py --generate
```

### 📁 main/

`main.py` 生成的完整测试用例（10个）：

- 测试1：表达式拆分
- 测试2：嵌套表达式
- 测试3：短路求值AND
- 测试4：短路求值OR
- 测试5：While循环
- 测试6：If-Else分支
- 测试7：指针操作
- 测试8：While循环（带短路求值）
- 测试9：嵌套If-Else
- 测试10：综合测试

**生成方法**:
```bash
python main.py --generate
```

### 📁 custom/

用户自定义测试用例目录。

**使用方法**:
1. 参考 [custom/README.md](custom/README.md) 了解如何编写自定义测试
2. 使用 [custom/example_template.py](custom/example_template.py) 作为模板
3. 将生成的 `.md` 文件保存到 `custom/` 目录

## 文件格式

每个测试文件包含：
- 📝 **阶段1：表达式拆分 (LABEL)** - 线性 IR 代码
- 📦 **阶段2：基本块 (BB)** - 基本块 IR 代码
- 📊 **阶段3：控制流图** - Mermaid 流程图代码（可在 VSCode 中直接预览或在线查看）
