# json-redact

按键名递归替换 JSON 中的值，方便在分享日志或配置前做一遍人工可复核的脱敏。工具只把结果写到标准输出，不改动输入文件。

## 使用

需要 Python 3.8+，不安装依赖。

~~~sh
python json_redact.py service-log.json --key token --key password --key email > sanitized.json
cat service-log.json | python json_redact.py --key authorization
~~~

键名匹配忽略大小写，适用于嵌套对象和数组；相同键名会在所有层级替换。输出是格式化后的 JSON，标准错误会报告替换数量。请在分享前检查结果：工具只按键名匹配，不会判断值本身是否敏感，也不会遮盖自由文本中的秘密。

退出状态：0 表示 JSON 已处理，2 表示读取或解析失败，130 表示中断。

## 许可

MIT，见 [LICENSE](LICENSE)。

## Linux x86_64 下载

- [单文件版](https://github.com/506058115-cmd/json-redact/releases/download/v1.0.0/json-redact-linux-x86_64-onefile.tar.gz)
- [目录版](https://github.com/506058115-cmd/json-redact/releases/download/v1.0.0/json-redact-linux-x86_64-onedir.tar.gz)
- [v1.0.0 Release 页面](https://github.com/506058115-cmd/json-redact/releases/tag/v1.0.0)

压缩包附带构建信息和依赖许可证；Release 另附 SHA-256 校验文件。构建目标为 GNU/Linux x86_64。较旧发行版可能需要兼容的 glibc。
