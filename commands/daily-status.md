---
description: Daily Work Tracker 설정 상태 확인
user_invocable: true
---

# Daily Status

플러그인의 현재 설정 상태를 확인합니다.

## 실행 방법

```bash
python3 ~/daily-work-tracker/scripts/setup.py --status
```

## 스케줄러 상태 확인

```bash
bash ~/daily-work-tracker/scripts/install-scheduler.sh status
```

## 출력 예시

```json
{
  "configured": true,
  "notion_enabled": true,
  "notion_page_id": "abc123def456",
  "schedule_enabled": true,
  "schedule_time": "18:00",
  "message": "설정 완료"
}
```

## 상태 항목

| 항목 | 설명 |
|------|------|
| `configured` | 설정 파일 존재 여부 |
| `notion_enabled` | Notion 연동 활성화 여부 |
| `notion_page_id` | 설정된 Notion 페이지 ID |
| `schedule_enabled` | 자동 동기화 활성화 여부 |
| `schedule_time` | 자동 동기화 시간 |
