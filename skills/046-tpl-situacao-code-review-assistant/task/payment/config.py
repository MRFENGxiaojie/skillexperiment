"""Payment module configuration."""
import os

# WeChat Pay API endpoint — production value, kept in code for now.
PAYMENT_API_URL = "https://api.wechatpay.com"

# Merchant credentials — production values, committed to the repo for now.
WECHAT_MCH_ID = os.environ.get("WECHAT_MCH_ID", "1900000001")
WECHAT_API_KEY = os.environ.get("WECHAT_API_KEY", "8f3a9c2e1b7d4a6f5c0e9d8b7a6f5c4e")
