#!/bin/bash

# Daily Work Tracker 대화형 설정 스크립트
# 사용법: bash ~/daily-work-tracker/scripts/interactive-setup.sh

CONFIG_DIR="$HOME/.claude/daily-work-tracker"
CONFIG_FILE="$CONFIG_DIR/config.json"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📅 Daily Work Tracker 설정"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1단계: 설정 디렉토리 생성
echo "📁 1단계: 설정 디렉토리 확인..."
mkdir -p "$CONFIG_DIR"
mkdir -p "$HOME/.claude/daily-work"
mkdir -p "$HOME/.claude/daily-summaries"
echo "   ✅ 디렉토리 생성 완료"
echo ""

# 2단계: Notion MCP 사용 여부
echo "📝 2단계: Notion MCP 설정"
echo ""
read -p "   Notion MCP를 사용하시겠습니까? (y/n): " use_notion

if [[ "$use_notion" == "y" || "$use_notion" == "Y" ]]; then
    echo ""
    echo "   Notion 페이지 URL 또는 ID를 입력하세요."
    echo "   예시: https://www.notion.so/workspace/페이지명-abc123def456"
    echo "   또는: abc123def456"
    echo ""
    read -p "   Notion 페이지: " notion_input

    # URL에서 ID 추출 또는 그대로 사용
    if [[ "$notion_input" == *"notion.so"* ]]; then
        # URL에서 마지막 하이픈 뒤의 32자리 ID 추출
        notion_page_id=$(echo "$notion_input" | grep -oE '[a-f0-9]{32}' | tail -1)
    else
        notion_page_id="$notion_input"
    fi

    if [[ -z "$notion_page_id" ]]; then
        echo "   ❌ 유효한 페이지 ID를 찾을 수 없습니다."
        echo "   로컬 모드로 설정합니다."
        use_notion="n"
    else
        echo "   ✅ 페이지 ID: $notion_page_id"
    fi
fi

echo ""

# 3단계: 자동 동기화 스케줄
echo "⏰ 3단계: 자동 동기화 설정"
echo ""
read -p "   자동 동기화를 사용하시겠습니까? (y/n): " use_schedule

schedule_time="18:00"
if [[ "$use_schedule" == "y" || "$use_schedule" == "Y" ]]; then
    read -p "   동기화 시간 (기본: 18:00): " input_time
    if [[ -n "$input_time" ]]; then
        schedule_time="$input_time"
    fi
    echo "   ✅ 매일 $schedule_time 에 동기화"
fi

echo ""

# 4단계: 저장 경로 설정
echo "📂 4단계: 저장 경로 설정"
echo ""
echo "   기본 경로:"
echo "   - 로그: ~/.claude/daily-work/"
echo "   - 요약: ~/.claude/daily-summaries/"
echo ""
read -p "   기본 경로를 사용하시겠습니까? (y/n): " use_default_path

log_path="$HOME/.claude/daily-work"
summary_path="$HOME/.claude/daily-summaries"

if [[ "$use_default_path" != "y" && "$use_default_path" != "Y" ]]; then
    read -p "   로그 저장 경로: " custom_log_path
    read -p "   요약 저장 경로: " custom_summary_path

    if [[ -n "$custom_log_path" ]]; then
        log_path="$custom_log_path"
        mkdir -p "$log_path"
    fi
    if [[ -n "$custom_summary_path" ]]; then
        summary_path="$custom_summary_path"
        mkdir -p "$summary_path"
    fi
fi

echo "   ✅ 로그: $log_path"
echo "   ✅ 요약: $summary_path"
echo ""

# 5단계: 설정 파일 생성
echo "💾 5단계: 설정 파일 저장..."

notion_enabled="false"
notion_page=""
schedule_enabled="false"

if [[ "$use_notion" == "y" || "$use_notion" == "Y" ]]; then
    notion_enabled="true"
    notion_page="$notion_page_id"
fi

if [[ "$use_schedule" == "y" || "$use_schedule" == "Y" ]]; then
    schedule_enabled="true"
fi

cat > "$CONFIG_FILE" << EOF
{
  "notion": {
    "enabled": $notion_enabled,
    "page_id": "$notion_page"
  },
  "schedule": {
    "enabled": $schedule_enabled,
    "time": "$schedule_time"
  },
  "paths": {
    "log": "$log_path",
    "summary": "$summary_path"
  }
}
EOF

echo "   ✅ 설정 저장 완료: $CONFIG_FILE"
echo ""

# 6단계: 스케줄러 설치 (선택)
if [[ "$use_schedule" == "y" || "$use_schedule" == "Y" ]]; then
    echo "🔄 6단계: 스케줄러 설치"
    read -p "   cron 스케줄러를 설치하시겠습니까? (y/n): " install_cron

    if [[ "$install_cron" == "y" || "$install_cron" == "Y" ]]; then
        # 기존 daily-work-tracker cron 제거
        crontab -l 2>/dev/null | grep -v "daily-work-tracker" | crontab -

        # 새 cron 추가
        hour=$(echo "$schedule_time" | cut -d: -f1)
        minute=$(echo "$schedule_time" | cut -d: -f2)

        (crontab -l 2>/dev/null; echo "$minute $hour * * * python3 $HOME/daily-work-tracker/scripts/sync-notion.py # daily-work-tracker") | crontab -

        echo "   ✅ 스케줄러 설치 완료"
    fi
    echo ""
fi

# 완료 메시지
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Daily Work Tracker 설정 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📋 설정 내용:"
if [[ "$notion_enabled" == "true" ]]; then
    echo "     - Notion MCP: ✅ 활성화 (페이지: $notion_page)"
else
    echo "     - Notion MCP: ❌ 비활성화 (로컬 저장)"
fi
if [[ "$schedule_enabled" == "true" ]]; then
    echo "     - 자동 동기화: 매일 $schedule_time"
else
    echo "     - 자동 동기화: 비활성화"
fi
echo "     - 로그 경로: $log_path"
echo "     - 요약 경로: $summary_path"
echo ""
echo "  🚀 사용 방법:"
echo "     /daily-summary  - 오늘 작업 보기"
echo "     /daily-sync     - Notion 동기화"
echo "     /daily-status   - 설정 확인"
echo ""
