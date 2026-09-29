#!/usr/bin/env bash
# security-scan 插件钩子脚本
# 在每次文件改动后执行：扫描改动文件中的敏感信息（密钥、密码、token 等）。
# 当前配置全部写死，每个项目无法按需调整。
set -euo pipefail

# ============ 写死配置（待改为按项目配置） ============
ENABLED=true
STRICT_MODE=false
MAX_RETRIES=3
NOTIFICATION_LEVEL="warn"
# =====================================================

if [ "$ENABLED" != "true" ]; then
  exit 0
fi

retry=0
while [ "$retry" -lt "$MAX_RETRIES" ]; do
  result=$(grep -rniE '(api[_-]?key|secret|password|token)[[:space:]]*[:=]' "$@" 2>/dev/null || true)
  if [ -n "$result" ]; then
    echo "[security-scan] 发现疑似敏感信息:"
    echo "$result"
    if [ "$STRICT_MODE" = "true" ]; then
      echo "[security-scan] strict_mode 开启，阻止提交"
      exit 1
    fi
  fi
  if [ "$NOTIFICATION_LEVEL" = "error" ] || [ "$NOTIFICATION_LEVEL" = "warn" ]; then
    echo "[security-scan] 通知级别: $NOTIFICATION_LEVEL"
  fi
  retry=$((retry + 1))
done

exit 0
