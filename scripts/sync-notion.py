#!/usr/bin/env python3
"""
Daily Work Tracker - Notion 동기화 스크립트
일일 작업 기록을 Notion 페이지에 동기화

사용법:
    python3 sync-notion.py                    # 오늘 기록 동기화
    python3 sync-notion.py --date 2026-01-05  # 특정 날짜 동기화
    python3 sync-notion.py --dry-run          # 실제 전송 없이 테스트
"""
import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path

try:
    import urllib.request
    import urllib.error
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


def get_config():
    """설정 파일 로드"""
    config_path = os.path.expanduser('~/.claude/daily-work-tracker/config.json')
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_daily_log(date_str=None):
    """일일 로그 파일 읽기"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    log_path = os.path.expanduser(f'~/.claude/daily-work/{date_str}.md')

    if not os.path.exists(log_path):
        return None, date_str

    with open(log_path, 'r', encoding='utf-8') as f:
        return f.read(), date_str


def parse_daily_log(content):
    """마크다운 로그를 구조화된 데이터로 파싱"""
    if not content:
        return []

    projects = []
    current_project = None

    lines = content.split('\n')

    for line in lines:
        # 프로젝트 섹션 시작
        if line.startswith('## '):
            project_match = re.match(r'## 🔹 (.+)', line)
            if project_match:
                if current_project:
                    projects.append(current_project)
                current_project = {
                    'name': project_match.group(1),
                    'path': '',
                    'tasks': []
                }

        # 프로젝트 경로
        elif line.startswith('> `') and current_project:
            path_match = re.match(r'> `(.+)`', line)
            if path_match:
                current_project['path'] = path_match.group(1)

        # 작업 항목
        elif line.startswith('- **[') and current_project:
            task_match = re.match(r'- \*\*\[(\d+:\d+)\]\*\* (.+)', line)
            if task_match:
                current_project['tasks'].append({
                    'time': task_match.group(1),
                    'content': task_match.group(2)
                })

    if current_project:
        projects.append(current_project)

    return projects


def format_for_notion(projects, date_str):
    """Notion 블록 형식으로 변환"""
    blocks = []

    # 헤더
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{
                "type": "text",
                "text": {"content": f"📅 {date_str} 작업 기록"}
            }]
        }
    })

    for project in projects:
        # 프로젝트 제목
        blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": f"🔹 {project['name']}"}
                }]
            }
        })

        # 프로젝트 경로
        if project['path']:
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": project['path']}
                    }]
                }
            })

        # 작업 목록
        for task in project['tasks']:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": f"[{task['time']}] "},
                            "annotations": {"bold": True}
                        },
                        {
                            "type": "text",
                            "text": {"content": task['content']}
                        }
                    ]
                }
            })

    # 구분선
    blocks.append({
        "object": "block",
        "type": "divider",
        "divider": {}
    })

    return blocks


def sync_to_notion(blocks, config, dry_run=False):
    """Notion API로 블록 추가"""
    if not HAS_URLLIB:
        return {"error": "urllib not available"}

    api_key = os.environ.get(config['notion'].get('api_key_env', 'NOTION_API_KEY'))
    page_id = config['notion'].get('page_id', '')

    if not api_key:
        return {"error": "NOTION_API_KEY 환경변수가 설정되지 않았습니다"}

    if not page_id:
        return {"error": "Notion 페이지 ID가 설정되지 않았습니다"}

    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "blocks_count": len(blocks),
            "message": "Dry run - 실제 전송하지 않음"
        }

    # Notion API 호출
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = json.dumps({"children": blocks}).encode('utf-8')

    try:
        request = urllib.request.Request(url, data=data, headers=headers, method='PATCH')
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {"success": True, "result": result}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {"error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Notion 동기화')
    parser.add_argument('--date', type=str, help='동기화할 날짜 (YYYY-MM-DD)')
    parser.add_argument('--dry-run', action='store_true', help='실제 전송 없이 테스트')
    parser.add_argument('--output', type=str, help='결과를 JSON 파일로 저장')

    args = parser.parse_args()

    # 설정 확인
    config = get_config()
    if not config:
        print(json.dumps({"error": "설정 파일이 없습니다. /daily-setup을 실행해주세요."}))
        sys.exit(1)

    if not config.get('notion', {}).get('enabled', False):
        print(json.dumps({"error": "Notion 연동이 비활성화되어 있습니다."}))
        sys.exit(1)

    # 로그 읽기
    content, date_str = get_daily_log(args.date)
    if not content:
        print(json.dumps({"error": f"{date_str} 날짜의 작업 기록이 없습니다."}))
        sys.exit(1)

    # 파싱
    projects = parse_daily_log(content)
    if not projects:
        print(json.dumps({"error": "파싱된 프로젝트가 없습니다."}))
        sys.exit(1)

    # Notion 블록 형식으로 변환
    blocks = format_for_notion(projects, date_str)

    # 동기화
    result = sync_to_notion(blocks, config, dry_run=args.dry_run)

    # 결과 출력
    output = {
        "date": date_str,
        "projects_count": len(projects),
        "blocks_count": len(blocks),
        **result
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
