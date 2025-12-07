# 测试3：短路求值AND

**描述**: result = p && (*p != 0)

## 流程图

```mermaid
flowchart TD
    B0["(empty)"]
    C0{p}
    B1["#1 = *p<br/>#0 = (#1 != 0)"]
    B2["#0 = p"]
    B3["result = #0"]

    B0 --> C0
    C0 -->|false| B2
    C0 -->|true| B1
    B1 --> B3
    B2 --> B3
    B3 --> Exit([Exit])

    style B0 fill:#e1f5e1
    style Exit fill:#ffe1e1
```

## 阶段1：表达式拆分 (LABEL)

```
LABEL_entry:
    if (! p) then jmp LABEL_1
    #1 = *p
    #0 = (#1 != 0)
    jmp LABEL_2
LABEL_1:
    #0 = p
LABEL_2:
    result = #0
```

## 阶段2：基本块 (BB)

```
BB_1:
    if (! p) then jmp BB_2
    #1 = *p
    #0 = (#1 != 0)
    jmp BB_3
BB_2:
    #0 = p
BB_3:
    result = #0
```
