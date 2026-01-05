---
description: 작업 요약을 Notion에 동기화하거나 로컬에 저장 (미동기화 날짜 일괄 처리)
user_invocable: true
---

# Daily Sync

작업 기록을 Notion 페이지에 동기화합니다. 동기화되지 않은 모든 날짜를 자동으로 찾아서 일괄 처리합니다.

## 실행 단계

### 1단계: 설정 및 미동기화 날짜 확인

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py --status
```

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py --unsynced
```

위 명령어로 다음을 확인:
- Notion MCP 활성화 여부 (`notion_mcp_enabled`)
- 페이지 ID (`notion_page_id`)
- 동기화되지 않은 날짜 목록 (`unsynced_dates`)

### 2단계: 동기화 대상 결정

- 인자로 날짜가 지정되면 해당 날짜만 동기화
- 인자 없으면 **모든 미동기화 날짜** 동기화

### 3단계: 각 날짜별 동기화

**미동기화 날짜가 있으면**, 각 날짜에 대해:

1. 해당 날짜의 작업 기록 읽기:
```bash
cat ~/.claude/daily-work/[날짜].md
```

2. **Notion MCP가 활성화되어 있으면**:

`mcp__notion__notion-update-page` 도구를 사용해서 페이지에 **토글 형태**로 내용 추가:

```
mcp__notion__notion-update-page({
  data: {
    page_id: "[config의 notion_page_id]",
    command: "insert_content_after",
    selection_with_ellipsis: "가장 최근 내용...",
    new_str: "[토글 형태의 마크다운]"
  }
})
```

**토글 형태 마크다운 예시** (Notion-flavored Markdown):
```markdown
▶ 📅 2026-01-05 작업 기록
	▶ 🔹 project-name
		- **[15:23]** 질문 내용
		- **[16:00]** 다른 질문
	▶ 🔹 another-project
		- **[17:00]** 작업 내용
```

**중요**: 토글 내부 컨텐츠는 반드시 **탭으로 들여쓰기** 해야 함.

또는 페이지가 비어있으면 `replace_content` 사용.

3. **동기화 성공 후 기록 저장**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py --add-sync [날짜]
```

### 4단계: Fallback (Notion 미설정 시)

Notion이 비활성화되어 있으면 로컬에 저장:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate-summary.py --save --date [날짜]
```

저장 후 동기화 기록 추가:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py --add-sync [날짜]
```

### 5단계: 결과 출력

동기화 완료 후 결과 요약:

| 상태 | 메시지 |
|------|--------|
| Notion 성공 | "✅ [N]개 날짜 Notion에 동기화 완료!" |
| 로컬 저장 | "📁 [N]개 날짜 로컬에 저장 완료" |
| 이미 동기화됨 | "✅ 모든 작업이 이미 동기화되어 있습니다." |
| 작업 기록 없음 | "⚠️ 동기화할 작업 기록이 없습니다." |

## 인자

- `/daily-sync` → 모든 미동기화 날짜
- `/daily-sync 2026-01-04` → 특정 날짜만

## 중요

- Notion MCP가 설정되어 있어야 Notion 동기화 가능
- Notion 미설정 시 자동으로 로컬에 저장
- `/daily-setup`으로 Notion 설정 가능
- 동기화 기록은 `~/.claude/daily-work-tracker/config.json`의 `sync_history`에 저장
