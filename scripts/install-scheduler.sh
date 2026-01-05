#!/bin/bash
#
# Daily Work Tracker - 스케줄러 설치 스크립트
# macOS: launchd 사용
# Linux: cron 사용
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$HOME/.claude/daily-work-tracker/config.json"
PLIST_NAME="com.claude.daily-work-tracker"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_warning() { echo -e "${YELLOW}!${NC} $1"; }

# 설정 파일에서 시간 읽기
get_schedule_time() {
    if [ -f "$CONFIG_FILE" ]; then
        python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['schedule']['time'])" 2>/dev/null || echo "18:00"
    else
        echo "18:00"
    fi
}

# launchd plist 생성 (macOS)
create_launchd_plist() {
    local schedule_time=$(get_schedule_time)
    local hour=$(echo "$schedule_time" | cut -d: -f1)
    local minute=$(echo "$schedule_time" | cut -d: -f2)

    mkdir -p "$(dirname "$PLIST_PATH")"

    cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>${PLUGIN_DIR}/scripts/sync-notion.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>${hour}</integer>
        <key>Minute</key>
        <integer>${minute}</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>${HOME}/.claude/daily-work-tracker/sync.log</string>
    <key>StandardErrorPath</key>
    <string>${HOME}/.claude/daily-work-tracker/sync-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
EOF

    print_success "launchd plist 생성: $PLIST_PATH"
}

# launchd 서비스 등록 (macOS)
install_launchd() {
    create_launchd_plist

    # 기존 서비스 언로드
    launchctl unload "$PLIST_PATH" 2>/dev/null || true

    # 새 서비스 로드
    launchctl load "$PLIST_PATH"

    print_success "스케줄러 설치 완료"
    echo "  - 매일 $(get_schedule_time)에 Notion 동기화 실행"
    echo "  - 로그: ~/.claude/daily-work-tracker/sync.log"
}

# launchd 서비스 제거 (macOS)
uninstall_launchd() {
    if [ -f "$PLIST_PATH" ]; then
        launchctl unload "$PLIST_PATH" 2>/dev/null || true
        rm "$PLIST_PATH"
        print_success "스케줄러 제거 완료"
    else
        print_warning "설치된 스케줄러가 없습니다"
    fi
}

# cron 설치 (Linux)
install_cron() {
    local schedule_time=$(get_schedule_time)
    local hour=$(echo "$schedule_time" | cut -d: -f1)
    local minute=$(echo "$schedule_time" | cut -d: -f2)

    local cron_job="$minute $hour * * * /usr/bin/python3 ${PLUGIN_DIR}/scripts/sync-notion.py >> ${HOME}/.claude/daily-work-tracker/sync.log 2>&1"

    # 기존 cron에서 이 스크립트 제거
    crontab -l 2>/dev/null | grep -v "daily-work-tracker" | crontab - 2>/dev/null || true

    # 새 cron 추가
    (crontab -l 2>/dev/null; echo "$cron_job") | crontab -

    print_success "cron 설치 완료"
    echo "  - 매일 ${hour}:${minute}에 Notion 동기화 실행"
}

# cron 제거 (Linux)
uninstall_cron() {
    crontab -l 2>/dev/null | grep -v "daily-work-tracker" | crontab - 2>/dev/null || true
    print_success "cron 제거 완료"
}

# 상태 확인
check_status() {
    echo "=== Daily Work Tracker 스케줄러 상태 ==="
    echo ""

    if [[ "$OSTYPE" == "darwin"* ]]; then
        if [ -f "$PLIST_PATH" ]; then
            print_success "launchd 서비스 설치됨"
            if launchctl list | grep -q "$PLIST_NAME"; then
                print_success "서비스 실행 중"
            else
                print_warning "서비스가 로드되지 않음"
            fi
            echo "  - 스케줄: 매일 $(get_schedule_time)"
        else
            print_warning "스케줄러가 설치되지 않음"
        fi
    else
        if crontab -l 2>/dev/null | grep -q "daily-work-tracker"; then
            print_success "cron 작업 설치됨"
            echo "  - 스케줄: 매일 $(get_schedule_time)"
        else
            print_warning "스케줄러가 설치되지 않음"
        fi
    fi
}

# 메인
case "${1:-}" in
    install)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            install_launchd
        else
            install_cron
        fi
        ;;
    uninstall)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            uninstall_launchd
        else
            uninstall_cron
        fi
        ;;
    status)
        check_status
        ;;
    update)
        # 시간 변경 시 재설치
        if [[ "$OSTYPE" == "darwin"* ]]; then
            uninstall_launchd
            install_launchd
        else
            install_cron
        fi
        ;;
    *)
        echo "사용법: $0 {install|uninstall|status|update}"
        echo ""
        echo "명령어:"
        echo "  install   - 스케줄러 설치"
        echo "  uninstall - 스케줄러 제거"
        echo "  status    - 상태 확인"
        echo "  update    - 시간 변경 후 재설치"
        exit 1
        ;;
esac
