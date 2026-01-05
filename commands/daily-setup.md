---
description: Daily Work Tracker 초기 설정 (Notion MCP 연동)
user_invocable: true
---

# Daily Setup

Daily Work Tracker 대화형 설정을 진행합니다.

## 설정 흐름

AskUserQuestion 도구를 사용해서 순서대로 설정을 진행하세요.

### 1단계: 사용자에게 설정 질문

**먼저** AskUserQuestion 도구로 다음 질문들을 **한 번에** 물어보세요:

**질문 1**: 저장 경로
- header: "저장 경로"
- question: "작업 기록을 어디에 저장할까요?"
- options:
  - label: "기본 경로"
    description: "~/.claude/daily-work/ 에 저장"
  - label: "직접 입력"
    description: "원하는 경로 직접 지정"

**질문 2**: Notion MCP 사용
- header: "Notion"
- question: "Notion에 작업 기록을 동기화하시겠습니까?"
- options:
  - label: "예"
    description: "로컬 저장 + Notion 페이지에 동기화"
  - label: "아니오"
    description: "로컬에만 저장 (기본)"

### 2단계: 저장 경로 설정

사용자 응답에 따라:

**"기본 경로" 선택 시:**
```bash
mkdir -p ~/.claude/daily-work-tracker
mkdir -p ~/.claude/daily-work
mkdir -p ~/.claude/daily-summaries
```
- log_path = "~/.claude/daily-work"
- summary_path = "~/.claude/daily-summaries"

**"직접 입력" 선택 시:**
- AskUserQuestion으로 "로그 저장 경로를 입력해주세요 (예: ~/Documents/daily-work)" 질문
- 입력받은 경로로 디렉토리 생성:
  ```bash
  mkdir -p [사용자입력경로]
  mkdir -p ~/.claude/daily-work-tracker
  ```
- log_path = 사용자 입력 경로

### 3단계: Notion 설정 (사용자가 "예" 선택 시)

Notion을 사용하겠다고 하면:

1. Notion MCP 서버가 설정되어 있는지 확인:
   ```bash
   grep -A5 '"notion"' ~/.claude.json
   ```

2. **설정 안 되어 있으면** 안내:
   - Notion Integration 생성 필요 (https://www.notion.so/my-integrations)
   - API 키를 받아서 ~/.claude.json에 MCP 서버 추가 필요
   - 설정 후 다시 /daily-setup 실행하라고 안내

3. **설정 되어 있으면** 페이지 ID 요청:
   - AskUserQuestion으로 "Notion 페이지 URL을 입력해주세요" 질문
   - URL에서 페이지 ID 추출 (32자리 hex)

### 4단계: 설정 파일 생성

모든 응답을 수집한 후 설정 파일을 생성합니다:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py --notion-page "[페이지ID]" --notion-enable
```

또는 Notion 미사용 시:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py --init
```

### 5단계: 완료 메시지

설정 완료 후 요약을 보여주세요:

```
✅ Daily Work Tracker 설정 완료!

📋 설정 내용:
- 저장 경로: [경로]
- 로컬 저장: ✅ 활성화
- Notion 동기화: [✅ 활성화 / ❌ 비활성화]

🚀 사용 방법:
- /daily-summary  - 오늘 작업 보기
- /daily-sync     - Notion 동기화 (미동기화 날짜 일괄 처리)
- /daily-status   - 설정 확인
- /daily-path     - 저장 경로 변경
```

## 중요

- 로컬 저장은 **항상 활성화** (기본)
- Notion은 **추가 옵션**으로 활성화 가능
- Hook이 자동으로 모든 대화를 로컬에 기록함
- 저장 경로는 나중에 `/daily-path`로 변경 가능
- `/daily-sync` 실행 시 동기화되지 않은 모든 날짜를 자동으로 처리
