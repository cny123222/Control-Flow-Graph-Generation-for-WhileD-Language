# 测试4：短路求值OR

**描述**: result = (x == 0) || (y > 10)

## 流程图

```mermaid
flowchart TD
    B0["#2 = (x == 0)<br/>#0 = #2"]
    C0{#0}
    B1["(empty)"]
    B2["#3 = (y > 10)<br/>#0 = #3"]
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
    #2 = (x == 0)
    #0 = #2
    if (! #0) then jmp LABEL_4
    jmp LABEL_5
LABEL_4:
    #3 = (y > 10)
    #0 = #3
LABEL_5:
    result = #0
```

## 阶段2：基本块 (BB)

```
BB_1:
    #2 = (x == 0)
    #0 = #2
    if (! #0) then jmp BB_2
    jmp BB_3
BB_2:
    #3 = (y > 10)
    #0 = #3
BB_3:
    result = #0
```
