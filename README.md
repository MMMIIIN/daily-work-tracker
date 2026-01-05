# Daily Work Tracker

여러 프로젝트에서 작업한 내역을 날짜별로 자동 추적하는 Claude Code 플러그인입니다.

## 기능

- 대화할 때마다 자동으로 작업 기록
- 프로젝트별로 섹션 분리
- 날짜별 MD 파일 생성
- 일일/주간 요약 조회

## 설치

```bash
claude plugin install /Users/mingwanchoi/daily-work-tracker
```

또는 테스트:

```bash
claude --plugin-dir /Users/mingwanchoi/daily-work-tracker
```

## 저장 위치

```
~/.claude/daily-work/
├── 2026-01-05.md
├── 2026-01-04.md
└── ...
```

## 파일 형식

```markdown
# 📅 2026-01-05 작업 기록

## 🔹 flutter-app
> `/Users/mingwanchoi/projects/flutter-app`

- **[14:30]** 사용자 인증 어떻게 구현하면 좋을까? → Riverpod 추천
- **[15:00]** 로그인 화면 만들어줘 → `login_page.dart` 생성

## 🔹 backend-api
> `/Users/mingwanchoi/projects/backend-api`

- **[16:00]** API 엔드포인트 설계 → REST API 구조 제안
```

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/daily-summary` | 오늘 작업 내역 보기 |
| `/daily-summary 2026-01-04` | 특정 날짜 조회 |
| `/daily-week` | 이번 주 요약 |
| `/daily-clear` | 오늘 기록 삭제 |

## 라이선스

MIT
