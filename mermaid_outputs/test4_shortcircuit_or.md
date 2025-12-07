# 测试4：短路求值OR

**描述**: result = (x == 0) || (y > 10)

## 流程图

```mermaid
flowchart TD
    B0["#1 = (x == 0)"]
    C0{#1}
    B1["#0 = 1"]
    B2["#2 = (y > 10)<br/>#0 = #2"]
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
    #1 = (x == 0)
    if (! #1) then jmp LABEL_1
    #0 = 1
    jmp LABEL_2
LABEL_1:
    #2 = (y > 10)
    #0 = #2
LABEL_2:
    result = #0
```

## 阶段2：基本块 (BB)

```
BB_1:
    #1 = (x == 0)
    if (! #1) then jmp BB_2
    #0 = 1
    jmp BB_3
BB_2:
    #2 = (y > 10)
    #0 = #2
BB_3:
    result = #0
```
