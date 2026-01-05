---
description: 오늘 작업 요약을 Notion에 동기화하거나 로컬에 저장
user_invocable: true
---

# Daily Sync

오늘 작업 기록을 Notion 페이지에 즉시 동기화합니다.

## 실행 단계

### 1단계: 설정 확인

설정 파일에서 Notion 페이지 ID를 확인하세요:

```bash
cat ~/.claude/daily-work-tracker/config.json 2>/dev/null || echo '{"notion":{"enabled":false}}'
```

### 2단계: 오늘 작업 기록 확인

오늘 작업 기록이 있는지 확인:

```bash
cat ~/.claude/daily-work/$(date +%Y-%m-%d).md 2>/dev/null || echo "오늘 작업 기록 없음"
```

### 3단계: 요약 생성

작업 기록이 있으면 Notion 블록 형식으로 요약 생성:

```bash
python3 ~/daily-work-tracker/scripts/generate-summary.py --format notion
```

### 4단계: Notion에 동기화

**설정에서 Notion이 활성화되어 있고 (`notion.enabled: true`), 페이지 ID가 있으면:**

Notion MCP 도구 `mcp__notion__API-patch-block-children`를 사용해서 페이지에 블록 추가:

1. 3단계에서 생성된 `blocks` 배열을 가져옴
2. 설정 파일의 `notion.page_id` 값 사용
3. Notion MCP 호출:

```
mcp__notion__API-patch-block-children(
  block_id: "[page_id from config]",
  children: [
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "[요약 내용]"}}]
      }
    }
  ]
)
```

**Notion 비활성화 또는 연결 실패 시:**

로컬에 저장:

```bash
python3 ~/daily-work-tracker/scripts/generate-summary.py --save
```

### 5단계: 결과 출력

동기화 완료 후:

- **Notion 동기화 성공**: "✅ Notion 페이지에 동기화 완료!"
- **로컬 저장**: "📁 로컬에 저장 완료: ~/.claude/daily-summaries/YYYY-MM-DD-summary.md"
- **작업 기록 없음**: "⚠️ 오늘 작업 기록이 없습니다."

## 인자

날짜 지정 가능:
- `/daily-sync` → 오늘
- `/daily-sync 2026-01-04` → 특정 날짜

## 중요

- Notion MCP가 설정되어 있어야 동기화 가능
- Notion 미설정 시 자동으로 로컬에 저장
- `/daily-setup`으로 Notion 설정 가능
