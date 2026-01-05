---
description: Daily Work Tracker 설정 상태 확인
user_invocable: true
---

# Daily Status

플러그인의 현재 설정 상태를 확인합니다.

## 실행 방법

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py --status
```

## 미동기화 날짜 확인

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py --unsynced
```

## 출력 예시

```json
{
  "configured": true,
  "log_path": "~/.claude/daily-work",
  "summary_path": "~/.claude/daily-summaries",
  "notion_mcp_enabled": true,
  "notion_page_id": "abc123def456",
  "fallback_enabled": true,
  "synced_dates_count": 5,
  "last_synced": "2026-01-04",
  "message": "설정 완료"
}
```

## 상태 항목

| 항목 | 설명 |
|------|------|
| `configured` | 설정 파일 존재 여부 |
| `log_path` | 작업 로그 저장 경로 |
| `notion_mcp_enabled` | Notion MCP 연동 활성화 여부 |
| `notion_page_id` | 설정된 Notion 페이지 ID |
| `synced_dates_count` | 동기화된 날짜 수 |
| `last_synced` | 마지막 동기화 날짜 |
