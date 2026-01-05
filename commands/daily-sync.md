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

1. 해당 날짜의 작업 기록 읽기 (log_path는 --status에서 확인):
```bash
cat [log_path]/[날짜].md
```

2. **작업 기록을 분석하여 요약 생성**:

각 프로젝트별로 작업 내용을 분석하여:
- **프로젝트별 요약**: 해당 프로젝트에서 무슨 작업을 했는지 1-2문장으로 요약
- **전체 요약**: 오늘 하루 전체 작업을 2-3문장으로 요약

3. **Notion MCP가 활성화되어 있으면**:

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
▶ 📅 2026-01-15 14:30 작업 기록 | 2개 프로젝트
	▶ 🔹 shopping-app
		> `/home/user/projects/shopping-app`
		- **[10:30]** 장바구니 기능 구현 요청
		- **[10:45]** 상품 추가/삭제 로직 작성
		- **[11:20]** 결제 페이지 연동
		📝 **요약**: 장바구니 기능 구현 (상품 추가/삭제, 결제 페이지 연동)
	▶ 🔹 admin-dashboard
		> `/home/user/projects/admin-dashboard`
		- **[14:00]** 사용자 목록 API 연결
		- **[14:30]** 테이블 컴포넌트 개선
		- **[15:00]** 페이지네이션 추가
		📝 **요약**: 사용자 목록 API 연동 및 테이블 UI 개선 (페이지네이션 추가)
	📊 **전체 요약**: shopping-app 장바구니 및 결제 기능 완성, admin-dashboard 사용자 관리 화면 개선 작업 진행
```

**중요**:
- 토글 내부 컨텐츠는 반드시 **탭으로 들여쓰기** 해야 함
- 각 프로젝트 토글 끝에 `📝 **요약**:` 추가
- 날짜 토글 끝에 `📊 **전체 요약**:` 추가
- 요약은 작업 내용을 분석하여 Claude가 직접 생성

또는 페이지가 비어있으면 `replace_content` 사용.

4. **동기화 성공 후 기록 저장**:
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

## 요약 생성 가이드

Claude가 요약을 생성할 때:

### 프로젝트별 요약
- 해당 프로젝트에서 수행한 주요 작업을 1-2문장으로 정리
- 구체적인 기능명이나 파일명 포함
- 예: "장바구니 기능 구현, 상품 추가/삭제 및 결제 연동"

### 전체 요약
- 하루 전체 작업을 2-3문장으로 정리
- 주요 프로젝트와 핵심 작업 언급
- 예: "shopping-app 장바구니 기능 완성, admin-dashboard UI 개선 진행"

## 중요

- Notion MCP가 설정되어 있어야 Notion 동기화 가능
- Notion 미설정 시 자동으로 로컬에 저장
- `/daily-setup`으로 Notion 설정 가능
- 동기화 기록은 `~/.claude/daily-work-tracker/config.json`의 `sync_history`에 저장
