---
description: 오늘 작업 기록 삭제
user_invocable: true
---

# Daily Clear

오늘 작업 기록을 삭제합니다.

## 실행 방법

1. 사용자에게 확인 요청: "오늘 작업 기록을 삭제하시겠습니까? (y/n)"
2. 'y' 입력 시 `~/.claude/daily-work/YYYY-MM-DD.md` 파일 삭제
3. 삭제 완료 메시지 출력

## 주의사항

- 삭제된 파일은 복구할 수 없습니다
- 다른 날짜 파일은 영향받지 않습니다
