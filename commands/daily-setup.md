---
description: Daily Work Tracker 초기 설정 (Notion MCP 연동 + 스케줄)
user_invocable: true
---

# Daily Setup

Daily Work Tracker 대화형 설정을 진행합니다.

## 설정 흐름

AskUserQuestion 도구를 사용해서 순서대로 설정을 진행하세요.

### 1단계: 디렉토리 초기화

먼저 필요한 디렉토리를 생성합니다:

```bash
mkdir -p ~/.claude/daily-work-tracker
mkdir -p ~/.claude/daily-work
mkdir -p ~/.claude/daily-summaries
```

### 2단계: 사용자에게 설정 질문

AskUserQuestion 도구로 다음 질문들을 **한 번에** 물어보세요:

**질문 1**: Notion MCP 사용
- header: "Notion"
- question: "Notion에 작업 기록을 동기화하시겠습니까?"
- options:
  - label: "예"
    description: "로컬 저장 + Notion 페이지에 동기화"
  - label: "아니오"
    description: "로컬에만 저장 (기본)"

**질문 2**: 자동 동기화
- header: "자동 동기화"
- question: "매일 자동으로 동기화할까요?"
- options:
  - label: "예 (18:00)"
    description: "매일 오후 6시에 자동 동기화"
  - label: "예 (다른 시간)"
    description: "원하는 시간 직접 입력"
  - label: "아니오"
    description: "수동으로만 동기화"

### 3단계: Notion 설정 (사용자가 "예" 선택 시)

Notion을 사용하겠다고 하면:

1. Notion MCP 서버가 설정되어 있는지 확인:
   ```bash
   grep -A5 '"notion"' ~/.claude.json
   ```

2. **설정 안 되어 있으면** 안내:
   - Notion Integration 생성 필요 (https://www.notion.so/my-integrations)
   - API 키를 받아서 ~/.claude.json에 MCP 서버 추가 필요

3. **설정 되어 있으면** 페이지 ID 요청:
   - AskUserQuestion으로 "Notion 페이지 URL을 입력해주세요" 질문
   - URL에서 페이지 ID 추출 (32자리 hex)

### 4단계: 설정 파일 생성

사용자 응답을 바탕으로 설정 파일을 생성합니다:

```bash
cat > ~/.claude/daily-work-tracker/config.json << 'EOF'
{
  "notion": {
    "enabled": [true/false],
    "page_id": "[페이지ID 또는 빈 문자열]"
  },
  "schedule": {
    "enabled": [true/false],
    "time": "[시간 또는 18:00]"
  },
  "paths": {
    "log": "~/.claude/daily-work",
    "summary": "~/.claude/daily-summaries"
  }
}
EOF
```

### 5단계: 완료 메시지

설정 완료 후 요약을 보여주세요:

```
✅ Daily Work Tracker 설정 완료!

📋 설정 내용:
- 로컬 저장: ✅ 활성화 (~/.claude/daily-work/)
- Notion 동기화: [✅ 활성화 / ❌ 비활성화]
- 자동 동기화: [매일 HH:MM / 비활성화]

🚀 사용 방법:
- /daily-summary  - 오늘 작업 보기
- /daily-sync     - Notion 동기화
- /daily-status   - 설정 확인
```

## 중요

- 로컬 저장은 **항상 활성화** (기본)
- Notion은 **추가 옵션**으로 활성화 가능
- Hook이 자동으로 모든 대화를 로컬에 기록함
