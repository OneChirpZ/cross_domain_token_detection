# Cross Domain Token Detection

## 记录

### 1. 打印格式化后的 json 数据

```python
# 打印格式化后的 HAR 文件
print(json.dumps(har['log']['entries'], indent=2, ensure_ascii=False, sort_keys=True))
```

### 2. har 中的一个 entry 的结构

```
|entry
|
|---time
|---connection
|---request
|   |
|   |---headersSize
|   |---postData
|   |---queryString
|   |---headers (*)
|   |---bodySize
|   |---url (*)
|   |---cookies
|   |---method
|   |---httpVersion
|   |
|---timings
|---response
|---startedDateTime
|---cache
|---md5 (预处理后新增，用于标识每个 entry)
|
```

### 3. dumps entry 来产生哈希值时的设置

```python
# 保证设置了 sort_keys=True, 不加 indent
json.dumps(entry, ensure_ascii=False, sort_keys=True)
```