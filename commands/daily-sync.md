---
description: 오늘 작업 요약을 Notion에 동기화하거나 로컬에 저장
user_invocable: true
---

# Daily Sync

오늘 작업 기록을 요약하여 Notion 또는 로컬 파일에 저장합니다.

## 실행 단계

### 1단계: 설정 확인

먼저 설정 파일을 확인하세요:

```bash
cat ~/.claude/daily-work-tracker/config.json 2>/dev/null || echo "설정 없음"
```

### 2단계: 요약 생성

오늘 작업 기록을 요약합니다:

```bash
python3 ~/daily-work-tracker/scripts/generate-summary.py --format json
```

### 3단계: 동기화 방식 결정

**Notion MCP가 연결되어 있는 경우:**

1. MCP 서버 목록에서 `notion` 서버 확인
2. 설정 파일의 `notion_mcp.page_id`로 Notion 페이지에 블록 추가
3. Notion MCP 도구 사용:
   - `notion_append_block_children` 또는 유사한 도구로 페이지에 추가

**Notion MCP가 없거나 연결 실패한 경우:**

로컬에 요약 파일 저장:

```bash
python3 ~/daily-work-tracker/scripts/generate-summary.py --save
```

저장 위치: `~/.claude/daily-summaries/YYYY-MM-DD-summary.md`

## Notion MCP 사용 예시

Notion MCP가 연결되어 있다면, 다음과 같이 동기화합니다:

1. 요약 생성 (Notion 블록 형식):
```bash
python3 ~/daily-work-tracker/scripts/generate-summary.py --format notion
```

2. 출력된 blocks 배열을 Notion MCP 도구로 전달:
```
notion_append_block_children(
  page_id: "설정된_페이지_ID",
  children: [생성된_블록들]
)
```

## 결과 출력

동기화 완료 후 결과를 사용자에게 알려주세요:

- **Notion 동기화 성공**: "✅ Notion 페이지에 동기화 완료 (N개 프로젝트, M개 작업)"
- **로컬 저장**: "📁 로컬에 저장 완료: ~/.claude/daily-summaries/YYYY-MM-DD-summary.md"
- **실패**: 오류 메시지와 함께 원인 설명

## 인자

- 날짜 지정: `/daily-sync 2026-01-04` → 해당 날짜 동기화
- 기본값: 오늘 날짜
