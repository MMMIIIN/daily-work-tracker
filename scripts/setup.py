#!/usr/bin/env python3
"""
Daily Work Tracker - 초기 설정 스크립트
플러그인 처음 설치 시 Notion MCP 연동 설정
"""
import json
import os
import sys
from pathlib import Path


def get_config_path():
    """설정 파일 경로 반환"""
    return os.path.expanduser('~/.claude/daily-work-tracker/config.json')


def get_plugin_root():
    """플러그인 루트 경로 반환"""
    return os.environ.get('CLAUDE_PLUGIN_ROOT', os.path.dirname(os.path.dirname(__file__)))


def load_config():
    """설정 파일 로드"""
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_config(config):
    """설정 파일 저장"""
    config_path = get_config_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def init_config():
    """설정 파일 초기화"""
    template_path = os.path.join(get_plugin_root(), 'config', 'config.template.json')

    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {
            "storage": {
                "log_path": "~/.claude/daily-work",
                "summary_path": "~/.claude/daily-summaries"
            },
            "notion_mcp": {
                "enabled": False,
                "page_id": "",
                "mcp_server_name": "notion"
            },
            "fallback": {
                "save_local": True
            },
            "settings": {
                "auto_summary": True,
                "include_projects": [],
                "exclude_projects": []
            },
            "sync_history": []
        }

    save_config(config)
    return config


def get_log_path(config):
    """로그 경로 반환 (storage.log_path 또는 paths.log 지원)"""
    # 새 형식: storage.log_path
    storage_config = config.get('storage', {})
    if 'log_path' in storage_config:
        return storage_config['log_path']
    # 기존 형식: paths.log
    paths_config = config.get('paths', {})
    if 'log' in paths_config:
        return paths_config['log']
    return '~/.claude/daily-work'


def get_summary_path(config):
    """요약 경로 반환 (storage.summary_path 또는 paths.summary 지원)"""
    # 새 형식: storage.summary_path
    storage_config = config.get('storage', {})
    if 'summary_path' in storage_config:
        return storage_config['summary_path']
    # 기존 형식: paths.summary
    paths_config = config.get('paths', {})
    if 'summary' in paths_config:
        return paths_config['summary']
    return '~/.claude/daily-summaries'


def check_setup_status():
    """설정 상태 확인"""
    config = load_config()

    if config is None:
        return {
            "configured": False,
            "notion_mcp_enabled": False,
            "fallback_enabled": True,
            "message": "설정이 필요합니다. /daily-setup을 실행해주세요."
        }

    # notion_mcp 또는 기존 notion 키 지원
    notion_config = config.get('notion_mcp', config.get('notion', {}))

    sync_history = config.get('sync_history', [])

    return {
        "configured": True,
        "log_path": get_log_path(config),
        "summary_path": get_summary_path(config),
        "notion_mcp_enabled": notion_config.get('enabled', False),
        "notion_page_id": notion_config.get('page_id', ''),
        "mcp_server_name": notion_config.get('mcp_server_name', 'notion'),
        "fallback_enabled": config.get('fallback', {}).get('save_local', True),
        "synced_dates_count": len(sync_history),
        "last_synced": sync_history[-1] if sync_history else None,
        "message": "설정 완료"
    }


def update_notion_mcp_config(page_id=None, enabled=None, mcp_server_name=None):
    """Notion MCP 설정 업데이트"""
    config = load_config() or init_config()

    # notion_mcp 키 사용
    if 'notion_mcp' not in config:
        config['notion_mcp'] = {
            "enabled": False,
            "page_id": "",
            "mcp_server_name": "notion"
        }

    if page_id is not None:
        config['notion_mcp']['page_id'] = page_id
    if enabled is not None:
        config['notion_mcp']['enabled'] = enabled
    if mcp_server_name is not None:
        config['notion_mcp']['mcp_server_name'] = mcp_server_name

    save_config(config)
    return config


def add_sync_history(date_str):
    """동기화 기록 추가"""
    config = load_config() or init_config()

    if 'sync_history' not in config:
        config['sync_history'] = []

    if date_str not in config['sync_history']:
        config['sync_history'].append(date_str)
        config['sync_history'].sort()

    save_config(config)
    return config


def get_unsynced_dates():
    """동기화되지 않은 날짜 목록 반환"""
    config = load_config()
    if not config:
        return []

    log_path = os.path.expanduser(get_log_path(config))
    sync_history = config.get('sync_history', [])

    if not os.path.exists(log_path):
        return []

    # 로그 파일에서 날짜 추출
    log_dates = []
    for f in os.listdir(log_path):
        if f.endswith('.md') and f != 'debug.log':
            date_str = f.replace('.md', '')
            if date_str not in sync_history:
                log_dates.append(date_str)

    log_dates.sort()
    return log_dates


def update_fallback_config(save_local=None):
    """Fallback 설정 업데이트"""
    config = load_config() or init_config()

    if 'fallback' not in config:
        config['fallback'] = {"save_local": True}

    if save_local is not None:
        config['fallback']['save_local'] = save_local

    save_config(config)
    return config


def update_storage_config(log_path=None, summary_path=None):
    """저장 경로 설정 업데이트"""
    config = load_config() or init_config()

    if 'storage' not in config:
        config['storage'] = {
            "log_path": "~/.claude/daily-work",
            "summary_path": "~/.claude/daily-summaries"
        }

    if log_path is not None:
        config['storage']['log_path'] = log_path
    if summary_path is not None:
        config['storage']['summary_path'] = summary_path

    save_config(config)
    return config


def main():
    """메인 함수 - CLI 인터페이스"""
    import argparse

    parser = argparse.ArgumentParser(description='Daily Work Tracker 설정')
    parser.add_argument('--status', action='store_true', help='설정 상태 확인')
    parser.add_argument('--init', action='store_true', help='설정 초기화')

    # Notion MCP 설정
    parser.add_argument('--notion-page', type=str, help='Notion 페이지 ID 설정')
    parser.add_argument('--notion-mcp-name', type=str, help='Notion MCP 서버 이름 (기본: notion)')
    parser.add_argument('--notion-enable', action='store_true', help='Notion MCP 연동 활성화')
    parser.add_argument('--notion-disable', action='store_true', help='Notion MCP 연동 비활성화')

    # 동기화 기록
    parser.add_argument('--add-sync', type=str, help='동기화 기록 추가 (YYYY-MM-DD)')
    parser.add_argument('--unsynced', action='store_true', help='동기화되지 않은 날짜 목록')

    # Fallback 설정
    parser.add_argument('--fallback-enable', action='store_true', help='로컬 저장 활성화')
    parser.add_argument('--fallback-disable', action='store_true', help='로컬 저장 비활성화')

    # 저장 경로 설정
    parser.add_argument('--log-path', type=str, help='작업 로그 저장 경로 (기본: ~/.claude/daily-work)')
    parser.add_argument('--summary-path', type=str, help='요약 파일 저장 경로 (기본: ~/.claude/daily-summaries)')

    args = parser.parse_args()

    if args.status:
        status = check_setup_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return

    if args.init:
        config = init_config()
        print("설정이 초기화되었습니다.")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return

    # Notion MCP 설정
    if args.notion_page or args.notion_mcp_name or args.notion_enable or args.notion_disable:
        config = update_notion_mcp_config(
            page_id=args.notion_page,
            mcp_server_name=args.notion_mcp_name,
            enabled=True if args.notion_enable else (False if args.notion_disable else None)
        )
        print("Notion MCP 설정이 업데이트되었습니다.")
        print(json.dumps(config.get('notion_mcp', {}), indent=2, ensure_ascii=False))
        return

    # 동기화 기록
    if args.add_sync:
        config = add_sync_history(args.add_sync)
        print(f"동기화 기록 추가: {args.add_sync}")
        return

    if args.unsynced:
        unsynced = get_unsynced_dates()
        print(json.dumps({"unsynced_dates": unsynced}, indent=2, ensure_ascii=False))
        return

    # Fallback 설정
    if args.fallback_enable or args.fallback_disable:
        config = update_fallback_config(
            save_local=True if args.fallback_enable else (False if args.fallback_disable else None)
        )
        print("Fallback 설정이 업데이트되었습니다.")
        print(json.dumps(config.get('fallback', {}), indent=2, ensure_ascii=False))
        return

    # 저장 경로 설정
    if args.log_path or args.summary_path:
        config = update_storage_config(
            log_path=args.log_path,
            summary_path=args.summary_path
        )
        print("저장 경로 설정이 업데이트되었습니다.")
        print(json.dumps(config.get('storage', {}), indent=2, ensure_ascii=False))
        return

    # 인자 없으면 상태 출력
    status = check_setup_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
