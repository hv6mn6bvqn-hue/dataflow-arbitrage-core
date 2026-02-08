"""
CONTROLLED EXECUTE TEST — M11.1

⚠️ ВНИМАНИЕ:
Этот файл временно форсирует EXECUTE
Используется ТОЛЬКО для end-to-end теста
После подтверждения — ОТКАТИТЬ
"""

from datetime import datetime


def policy_allows_action():
    return {
        "allow": True,
        "confidence": 0.99,
        "reason": "controlled execute test M11.1"
    }
