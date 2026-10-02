#!/usr/bin/env python3
"""Replace selected JSON object values without changing the input file."""

import argparse
import json
from pathlib import Path
import sys


REPLACEMENT = "[REDACTED]"


def reject_constant(token):
    raise ValueError(f"不支持的 JSON 常量 {token}")


def redact(value, keys, count):
    if isinstance(value, dict):
        result = {}
        for key, child in value.items():
            if key.casefold() in keys:
                result[key] = REPLACEMENT
                count[0] += 1
            else:
                result[key] = redact(child, keys, count)
        return result
    if isinstance(value, list):
        return [redact(child, keys, count) for child in value]
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="递归替换 JSON 中指定键的值；源文件保持不变。"
    )
    parser.add_argument("input", nargs="?", default="-", help="JSON 文件；默认从标准输入读取")
    parser.add_argument(
        "--key", action="append", required=True, metavar="NAME",
        help="要脱敏的对象键，可重复指定；匹配时忽略大小写",
    )
    args = parser.parse_args(argv)
    keys = {key.casefold() for key in args.key}
    if "" in keys:
        parser.error("--key 不能为空")

    try:
        if args.input == "-":
            source = sys.stdin.read()
        else:
            source = Path(args.input).read_text(encoding="utf-8-sig")
        value = json.loads(source, parse_constant=reject_constant)
        count = [0]
        result = redact(value, keys, count)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        print(f"已替换 {count[0]} 个值。", file=sys.stderr)
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
        print(f"json-redact: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("json-redact: 已中断。", file=sys.stderr)
        raise SystemExit(130)
