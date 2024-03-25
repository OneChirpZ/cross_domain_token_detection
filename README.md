# Cross Domain Token Detection

## 记录

### 1. 打印格式化后的 json 数据

```python
# 打印格式化后的 HAR 文件
print(json.dumps(har['log']['entries'], indent=2, ensure_ascii=False))
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
|
```

