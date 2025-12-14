# 测试 8: While 循环（带短路求值）

**源程序**: `while (p != 0 && *p > 0) do { p = p + 1 }`

## 阶段1：表达式拆分 (LABEL)

```
LABEL_1:
    #1 = (p != 0)
    if (! #1) then jmp LABEL_3
    #2 = *p
    #0 = (#2 > 0)
    jmp LABEL_4
LABEL_3:
    #0 = #1
LABEL_4:
    if (! #0) then jmp LABEL_2
    p = p + 1
    jmp LABEL_1
LABEL_2:
```

## 阶段2：基本块 (BB)

```
BB_1:
    #1 = (p != 0)
    if (! #1) then jmp BB_2
    #2 = *p
    #0 = (#2 > 0)
    jmp BB_3
BB_2:
    #0 = #1
BB_3:
    if (! #0) then jmp BB_4
    p = p + 1
    jmp BB_1
BB_4:
```

## 阶段3：控制流图

```mermaid
flowchart TD
    B0["#1 = (p != 0)"]
    C0{#1}
    B1["#2 = *p<br/>#0 = (#2 > 0)"]
    B2["#0 = #1"]
    B3["(empty)"]
    C3{#0}
    B4["p = p + 1"]
    B5["(empty)"]

    B0 --> C0
    C0 -->|false| B2
    C0 -->|true| B1
    B1 --> B3
    B2 --> B3
    B3 --> C3
    C3 -->|false| B5
    C3 -->|true| B4
    B4 --> B0
    B5 --> Exit([Exit])

    style B0 fill:#e1f5e1
    style Exit fill:#ffe1e1
```
