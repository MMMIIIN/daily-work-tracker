---
description: Daily Work Tracker 저장 경로 설정
user_invocable: true
---

# Daily Path 설정

작업 로그와 요약 파일의 저장 경로를 설정합니다.

## 현재 설정 확인

```bash
python3 ~/daily-work-tracker/scripts/setup.py --status
```

현재 설정된 경로를 확인합니다:
- `log_path`: 작업 로그 저장 위치
- `summary_path`: 요약 파일 저장 위치

## 경로 설정 방법

### 사용자에게 질문

**"어떤 경로를 변경하시겠습니까?"**

1. **작업 로그 경로** (`log_path`)
2. **요약 파일 경로** (`summary_path`)
3. **둘 다**

### 작업 로그 경로 변경

사용자에게 물어보세요: **"작업 로그를 저장할 경로를 입력해주세요 (예: ~/Documents/daily-logs)"**

```bash
python3 ~/daily-work-tracker/scripts/setup.py --log-path "사용자입력경로"
```

### 요약 파일 경로 변경

사용자에게 물어보세요: **"요약 파일을 저장할 경로를 입력해주세요 (예: ~/Documents/summaries)"**

```bash
python3 ~/daily-work-tracker/scripts/setup.py --summary-path "사용자입력경로"
```

### 둘 다 변경

```bash
python3 ~/daily-work-tracker/scripts/setup.py --log-path "로그경로" --summary-path "요약경로"
```

## 설정 완료 메시지

경로 변경 후 사용자에게 알려주세요:

```
✅ 저장 경로가 변경되었습니다!

📂 현재 설정:
- 작업 로그: [log_path]
- 요약 파일: [summary_path]

※ 기존 파일은 자동으로 이동되지 않습니다.
   필요시 수동으로 파일을 새 경로로 이동해주세요.
```

## 기본값으로 초기화

```bash
python3 ~/daily-work-tracker/scripts/setup.py --log-path "~/.claude/daily-work"
python3 ~/daily-work-tracker/scripts/setup.py --summary-path "~/.claude/daily-summaries"
```
