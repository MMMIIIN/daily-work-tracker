# Daily Work Tracker

여러 프로젝트에서 작업한 내역을 날짜별로 자동 추적하는 Claude Code 플러그인입니다.

## 주요 기능

- **자동 작업 기록**: 대화할 때마다 프로젝트별로 자동 기록
- **프로젝트별 분리**: 여러 프로젝트 작업을 하나의 파일에서 섹션별로 관리
- **날짜별 파일**: `~/.claude/daily-work/YYYY-MM-DD.md` 형식으로 저장
- **Notion 연동**: Notion MCP를 통해 자동 동기화 (선택)
- **로컬 저장**: Notion 미연결 시 로컬 MD 파일로 저장
- **저장 경로 설정**: 로그 및 요약 파일 경로 커스터마이징 가능

## 설치

### 1단계: 마켓플레이스 추가

Claude Code 터미널에서:

```
/plugin marketplace add MMMIIIN/daily-work-tracker
```

### 2단계: 플러그인 설치

```
/plugin install daily-work-tracker@daily-work-tracker
```

### 설치 확인

```
/plugin list
```

**참고**: 설치 후 Claude Code를 재시작하면 플러그인이 활성화됩니다.

## 설정

### 빠른 설정 (권장)

```
/daily-work-tracker:daily-setup
```

대화형으로 모든 설정을 진행합니다:
1. **저장 경로** - 로그 파일 저장 위치 선택
2. **Notion 연동** - Notion MCP 활성화 여부

### 설정 파일 구조

`~/.claude/daily-work-tracker/config.json`:

```json
{
  "notion_mcp": {
    "enabled": true,
    "page_id": "your-notion-page-id"
  },
  "storage": {
    "log_path": "~/.claude/daily-work",
    "summary_path": "~/.claude/daily-summaries"
  },
  "sync_history": ["2026-01-04", "2026-01-05"]
}
```

### Notion MCP 연동 (선택)

Notion에 일일 작업 요약을 자동 동기화하려면:

#### 1단계: Notion Integration 생성

1. [Notion Integrations](https://www.notion.so/my-integrations) 페이지 접속
2. "New integration" 클릭
3. 이름 입력 후 생성
4. **Internal Integration Secret** 복사 (`ntn_` 또는 `secret_`으로 시작)

#### 2단계: Notion MCP 서버 설정

`~/.claude.json`에 추가:

```json
{
  "mcpServers": {
    "notion": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer YOUR_API_KEY\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  }
}
```

#### 3단계: Notion 페이지에 Integration 연결

1. 동기화할 Notion 페이지 열기
2. 우측 상단 `⋯` 클릭
3. "연결" → 생성한 Integration 선택
4. 페이지 URL에서 ID 복사: `notion.so/페이지이름-{페이지ID}`

#### 4단계: 플러그인 설정

```
/daily-work-tracker:daily-setup
```

- Notion 활성화 선택
- 복사한 페이지 ID 입력

### 동기화 형식

Notion에 Toggle 블록으로 날짜+시간별 정리:

```
📅 2026-01-05 17:30 | 4개 프로젝트 | 29개 대화
├─ 🔹 project-name
│   ├─ [15:23] 질문 내용
│   ├─ [16:00] 다른 질문
│   └─ 📝 요약: Claude가 생성한 프로젝트 요약
└─ 📊 전체 요약
```

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/daily-work-tracker:daily-setup` | 초기 설정 (저장 경로, Notion) |
| `/daily-work-tracker:daily-sync` | Notion/로컬에 동기화 (미동기화 날짜 일괄 처리) |
| `/daily-work-tracker:daily-summary` | 오늘 작업 내역 보기 |
| `/daily-work-tracker:daily-week` | 이번 주 작업 요약 |
| `/daily-work-tracker:daily-status` | 설정 상태 확인 |
| `/daily-work-tracker:daily-path` | 저장 경로 변경 |
| `/daily-work-tracker:daily-clear` | 오늘 기록 삭제 |

## 저장 위치

### 기본 경로

```
~/.claude/daily-work/          # 작업 로그
├── 2026-01-05.md
├── 2026-01-04.md
└── ...

~/.claude/daily-summaries/     # 일일 요약
├── 2026-01-05-summary.md
└── ...

~/.claude/daily-work-tracker/  # 설정
└── config.json
```

### 경로 변경

`/daily-work-tracker:daily-path` 명령어로 저장 경로 변경 가능

## 파일 형식

```markdown
# 📅 2026-01-05 작업 기록

## 🔹 flutter-app
> `/Users/username/projects/flutter-app`

- **[14:30]** 사용자 인증 어떻게 구현하면 좋을까? → Riverpod 추천
- **[15:00]** 로그인 화면 만들어줘 → `login_page.dart` 생성

## 🔹 backend-api
> `/Users/username/projects/backend-api`

- **[16:00]** API 엔드포인트 설계 → REST API 구조 제안
```

## 동작 방식

1. **UserPromptSubmit Hook**: 사용자가 질문할 때마다 `log-daily.py` 실행
2. **프로젝트 감지**: `pubspec.yaml`, `package.json` 또는 폴더명으로 프로젝트 식별
3. **자동 기록**: 날짜별 MD 파일에 타임스탬프와 함께 저장
4. **요약 트리거**: 이전 답변 요약을 자동으로 추가하도록 Claude에게 알림

## 삭제

### 플러그인 완전 삭제

```
/plugin uninstall daily-work-tracker
```

### 플러그인 비활성화

```
/plugin disable daily-work-tracker@daily-work-tracker
```

### 데이터 삭제 (선택)

플러그인 삭제 후에도 기록된 데이터는 유지됩니다. 데이터도 삭제하려면:

```bash
# 작업 로그 삭제
rm -rf ~/.claude/daily-work/

# 일일 요약 삭제
rm -rf ~/.claude/daily-summaries/

# 설정 파일 삭제
rm -rf ~/.claude/daily-work-tracker/
```

## 라이선스

MIT
