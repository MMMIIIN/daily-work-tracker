# Daily Work Tracker 플러그인

여러 프로젝트의 일일 작업을 추적하고, Notion MCP 또는 로컬 파일에 동기화합니다.

## 저장 위치 (설정 가능)

- 작업 기록: `~/.claude/daily-work/YYYY-MM-DD.md` (기본값)
- 일일 요약: `~/.claude/daily-summaries/YYYY-MM-DD-summary.md` (기본값)
- 설정 파일: `~/.claude/daily-work-tracker/config.json`

### 저장 경로 변경

```bash
# 작업 로그 경로 변경
python3 scripts/setup.py --log-path "~/Documents/daily-logs"

# 요약 파일 경로 변경
python3 scripts/setup.py --summary-path "~/Documents/summaries"

# 둘 다 변경
python3 scripts/setup.py --log-path "~/my-logs" --summary-path "~/my-summaries"
```

## 동기화 방식

### Notion MCP 연결 시
1. `mcp__notion__notion-update-page` 도구로 페이지에 내용 추가
2. 동기화 완료 후 `sync_history`에 날짜 기록

### Notion MCP 미연결 시 (Fallback)
1. `generate-summary.py --save`로 로컬에 저장
2. 저장 위치: `~/.claude/daily-summaries/YYYY-MM-DD-summary.md`

## 명령어

### 기본 명령어
- `/daily-summary` - 오늘 작업 내역 보기
- `/daily-week` - 이번 주 작업 요약
- `/daily-clear` - 오늘 기록 삭제

### 설정 명령어
- `/daily-setup` - 초기 설정 (Notion MCP 연동)
- `/daily-path` - 저장 경로 설정 (로그/요약 파일 위치)
- `/daily-status` - 설정 상태 확인

### 동기화 명령어
- `/daily-sync` - Notion/로컬에 동기화 (미동기화 날짜 일괄 처리)

## /daily-sync 실행 시

1. 설정 파일 확인 (`~/.claude/daily-work-tracker/config.json`)
2. 미동기화 날짜 목록 확인 (`setup.py --unsynced`)
3. **MCP 연결됨**: Notion MCP 도구로 페이지에 내용 추가
4. **MCP 미연결**: 로컬 `~/.claude/daily-summaries/`에 저장
5. 동기화 완료 후 기록 저장 (`setup.py --add-sync [날짜]`)

## 동기화 기록

동기화된 날짜는 config.json의 `sync_history` 배열에 저장됩니다.
`/daily-sync` 실행 시 동기화되지 않은 모든 날짜를 자동으로 찾아서 일괄 처리합니다.

## 초기 설정 (/daily-setup)

1. Notion MCP 사용 여부 확인
2. 사용 시: 페이지 ID 설정
3. 미사용 시: 로컬 저장 모드
