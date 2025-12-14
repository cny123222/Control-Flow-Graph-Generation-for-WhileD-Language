# 测试 9: 嵌套 If-Else

**源程序**: `if (x > 0) then { if (y > 0) then z = 1 else z = 2 } else z = 3`

## 阶段1：表达式拆分 (LABEL)

```
LABEL_entry:
    #0 = (x > 0)
    if (! #0) then jmp LABEL_1
    #1 = (y > 0)
    if (! #1) then jmp LABEL_3
    z = 1
    jmp LABEL_4
LABEL_3:
    z = 2
LABEL_4:
    jmp LABEL_2
LABEL_1:
    z = 3
LABEL_2:
```

## 阶段2：基本块 (BB)

```
BB_1:
    #0 = (x > 0)
    if (! #0) then jmp BB_4
    #1 = (y > 0)
    if (! #1) then jmp BB_2
    z = 1
    jmp BB_3
BB_2:
    z = 2
BB_3:
    jmp BB_5
BB_4:
    z = 3
BB_5:
```

## 阶段3：控制流图

```mermaid
flowchart TD
    B0["#0 = (x > 0)"]
    C0{#0}
    B1["#1 = (y > 0)"]
    C1{#1}
    B2["z = 1"]
    B3["z = 2"]
    B4["(empty)"]
    B5["z = 3"]
    B6["(empty)"]

    B0 --> C0
    C0 -->|false| B5
    C0 -->|true| B1
    B1 --> C1
    C1 -->|false| B3
    C1 -->|true| B2
    B2 --> B4
    B3 --> B4
    B4 --> B6
    B5 --> B6
    B6 --> Exit([Exit])

    style B0 fill:#e1f5e1
    style Exit fill:#ffe1e1
```
