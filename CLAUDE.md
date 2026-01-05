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
1. `generate-summary.py --format notion`으로 블록 생성
2. Notion MCP 도구로 페이지에 추가

### Notion MCP 미연결 시 (Fallback)
1. `generate-summary.py --save`로 로컬에 저장
2. 저장 위치: `~/.claude/daily-summaries/YYYY-MM-DD-summary.md`

## 답변 요약 규칙

`<daily-tracker-reminder>` 메시지가 표시되면:

1. 해당 날짜 파일(`~/.claude/daily-work/YYYY-MM-DD.md`)을 읽기
2. 지정된 프로젝트 섹션에서 마지막 항목 찾기
3. 이전 답변을 1줄로 요약해서 해당 항목 끝에 ` → 요약내용` 형식으로 추가
4. 그 후 현재 질문에 대한 답변 진행

## 요약 작성 가이드

- 최대 50자 이내로 간결하게
- 코드 수정 시: 파일명과 수정 내용
- 설명/논의 시: 핵심 결론
- 파일명은 백틱으로 감싸기

## 명령어

### 기본 명령어
- `/daily-summary` - 오늘 작업 내역 보기
- `/daily-week` - 이번 주 작업 요약
- `/daily-clear` - 오늘 기록 삭제

### 설정 명령어
- `/daily-setup` - 초기 설정 (Notion MCP + 스케줄)
- `/daily-path` - 저장 경로 설정 (로그/요약 파일 위치)
- `/daily-status` - 설정 상태 확인

### 동기화 명령어
- `/daily-sync` - Notion/로컬에 동기화

## /daily-sync 실행 시

1. 설정 파일 확인 (`~/.claude/daily-work-tracker/config.json`)
2. Notion MCP 연결 여부 확인
3. **MCP 연결됨**: Notion MCP 도구로 페이지에 블록 추가
4. **MCP 미연결**: 로컬 `~/.claude/daily-summaries/`에 저장

## Notion MCP 도구 사용

Notion MCP가 연결되어 있을 때 동기화:

```bash
# 1. 요약 생성
python3 ~/daily-work-tracker/scripts/generate-summary.py --format notion
```

```
# 2. 출력된 blocks를 Notion MCP 도구로 전달
notion_append_block_children(
  page_id: "설정된_페이지_ID",
  children: [blocks]
)
```

## 초기 설정 (/daily-setup)

1. Notion MCP 사용 여부 확인
2. 사용 시: 페이지 ID 설정
3. 미사용 시: 로컬 저장 모드
4. 자동 동기화 시간 설정 (기본: 18:00)
