# 测试5：嵌套控制流

**描述**: sum = 0; while (i < n) do { if (i > 0) then sum = sum + i else skip }

## 流程图

```mermaid
flowchart TD
    B0["sum = 0"]
    B1["#0 = (i < n)"]
    C1{#0}
    B2["#1 = (i > 0)"]
    C2{#1}
    B3["sum = sum + i"]
    B4["(empty)"]
    B5["(empty)"]
    B6["(empty)"]

    B0 --> B1
    B1 --> C1
    C1 -->|false| B6
    C1 -->|true| B2
    B2 --> C2
    C2 -->|false| B4
    C2 -->|true| B3
    B3 --> B5
    B4 --> B5
    B5 --> B1
    B6 --> Exit([Exit])

    style B0 fill:#e1f5e1
    style Exit fill:#ffe1e1
```

## 阶段1：表达式拆分 (LABEL)

```
LABEL_entry:
    sum = 0
LABEL_1:
    #0 = (i < n)
    if (! #0) then jmp LABEL_2
    #1 = (i > 0)
    if (! #1) then jmp LABEL_3
    sum = sum + i
    jmp LABEL_4
LABEL_3:
LABEL_4:
    jmp LABEL_1
LABEL_2:
```

## 阶段2：基本块 (BB)

```
BB_1:
    sum = 0
BB_2:
    #0 = (i < n)
    if (! #0) then jmp BB_5
    #1 = (i > 0)
    if (! #1) then jmp BB_3
    sum = sum + i
    jmp BB_4
BB_3:
BB_4:
    jmp BB_2
BB_5:
```
