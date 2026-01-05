---
description: Daily Work Tracker 초기 설정 (Notion MCP 연동 + 스케줄)
user_invocable: true
---

# Daily Setup

Daily Work Tracker 플러그인의 초기 설정을 진행합니다.

## 설정 흐름

### 1단계: 설정 파일 초기화

```bash
python3 ~/daily-work-tracker/scripts/setup.py --init
```

### 2단계: Notion MCP 연결 확인

사용자에게 물어보세요:

**"Notion MCP를 사용하시겠습니까?"**

- **예**: Notion MCP 설정 진행 (3단계)
- **아니오**: 로컬 저장 모드 사용 (4단계로 건너뛰기)

### 3단계: Notion MCP 설정 (선택)

Notion MCP를 사용하려면:

1. **Notion MCP 서버 설치 확인**
   ```bash
   # .claude.json에 notion MCP 서버가 있는지 확인
   cat ~/.claude.json | grep -A5 "notion"
   ```

2. **없으면 안내**:
   ```
   Notion MCP 서버를 먼저 설정해야 합니다.

   .claude.json에 다음을 추가하세요:
   {
     "mcpServers": {
       "notion": {
         "type": "stdio",
         "command": "npx",
         "args": ["-y", "@notionhq/notion-mcp-server"],
         "env": {
           "NOTION_API_KEY": "your-api-key"
         }
       }
     }
   }
   ```

3. **Notion 페이지 ID 설정**:
   ```bash
   python3 ~/daily-work-tracker/scripts/setup.py --notion-page "페이지ID"
   python3 ~/daily-work-tracker/scripts/setup.py --notion-enable
   ```

### 4단계: 스케줄 설정

자동 동기화 시간을 설정합니다:

사용자에게 물어보세요: **"매일 몇 시에 자동 동기화할까요? (예: 18:00)"**

```bash
python3 ~/daily-work-tracker/scripts/setup.py --schedule-time "사용자입력"
python3 ~/daily-work-tracker/scripts/setup.py --schedule-enable
```

### 5단계: 스케줄러 설치

```bash
bash ~/daily-work-tracker/scripts/install-scheduler.sh install
```

### 6단계: 설정 확인

```bash
python3 ~/daily-work-tracker/scripts/setup.py --status
```

## 설정 완료 메시지

설정 완료 후 사용자에게 알려주세요:

```
✅ Daily Work Tracker 설정 완료!

📋 설정 내용:
- Notion MCP: [활성화/비활성화]
- 자동 동기화: 매일 [시간]
- 저장 위치: [Notion 페이지 / 로컬 폴더]

🚀 사용 방법:
- /daily-summary: 오늘 작업 보기
- /daily-sync: 수동 동기화
- /daily-status: 설정 확인
```

## Fallback 동작

- Notion MCP 연결 실패 시 → 로컬 `~/.claude/daily-summaries/`에 자동 저장
- 수동으로도 `/daily-sync` 실행 가능
