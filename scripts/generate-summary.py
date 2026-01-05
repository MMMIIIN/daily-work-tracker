#!/usr/bin/env python3
"""
Daily Work Tracker - 일일 요약 생성 스크립트
오늘 작업 기록을 읽어 요약 형식으로 변환

사용법:
    python3 generate-summary.py                    # 오늘 요약
    python3 generate-summary.py --date 2026-01-05  # 특정 날짜
    python3 generate-summary.py --format notion    # Notion 블록 형식
    python3 generate-summary.py --format markdown  # Markdown 형식 (기본)
"""
import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path


def get_config():
    """설정 파일 로드"""
    config_path = os.path.expanduser('~/.claude/daily-work-tracker/config.json')
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_log_path():
    """로그 저장 경로 반환"""
    config = get_config()
    storage = config.get('storage', {})
    return os.path.expanduser(storage.get('log_path', '~/.claude/daily-work'))


def get_summary_path():
    """요약 저장 경로 반환"""
    config = get_config()
    storage = config.get('storage', {})
    return os.path.expanduser(storage.get('summary_path', '~/.claude/daily-summaries'))


def get_daily_log(date_str=None):
    """일일 로그 파일 읽기"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    log_dir = get_log_path()
    log_path = os.path.join(log_dir, f'{date_str}.md')

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


def generate_markdown_summary(projects, date_str):
    """Markdown 형식 요약 생성"""
    lines = []
    lines.append(f"# 📅 {date_str} 일일 작업 요약\n")
    lines.append(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("---\n")

    total_tasks = 0

    for project in projects:
        lines.append(f"## 🔹 {project['name']}")
        if project['path']:
            lines.append(f"> `{project['path']}`\n")

        for task in project['tasks']:
            lines.append(f"- **[{task['time']}]** {task['content']}")
            total_tasks += 1

        lines.append("")

    lines.append("---")
    lines.append(f"\n📊 **통계**: {len(projects)}개 프로젝트, {total_tasks}개 작업")

    return '\n'.join(lines)


def generate_notion_blocks(projects, date_str):
    """Notion API 블록 형식 생성"""
    blocks = []

    # 헤더
    blocks.append({
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": f"📅 {date_str} 일일 작업 요약"}}]
        }
    })

    blocks.append({
        "type": "divider",
        "divider": {}
    })

    for project in projects:
        # 프로젝트 제목
        blocks.append({
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": f"🔹 {project['name']}"}}]
            }
        })

        # 프로젝트 경로
        if project['path']:
            blocks.append({
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": project['path']}}]
                }
            })

        # 작업 목록
        for task in project['tasks']:
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": f"[{task['time']}] "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": task['content']}}
                    ]
                }
            })

    blocks.append({
        "type": "divider",
        "divider": {}
    })

    return blocks


def save_local_summary(summary_content, date_str):
    """로컬 요약 파일 저장 (설정된 경로 사용)"""
    summary_dir = get_summary_path()
    os.makedirs(summary_dir, exist_ok=True)

    summary_path = os.path.join(summary_dir, f'{date_str}-summary.md')

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)

    return summary_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description='일일 요약 생성')
    parser.add_argument('--date', type=str, help='날짜 (YYYY-MM-DD)')
    parser.add_argument('--format', type=str, choices=['markdown', 'notion', 'json'], default='markdown')
    parser.add_argument('--save', action='store_true', help='로컬에 저장')
    parser.add_argument('--output', type=str, help='출력 파일 경로')

    args = parser.parse_args()

    # 로그 읽기
    content, date_str = get_daily_log(args.date)

    if not content:
        result = {
            "success": False,
            "error": f"{date_str} 날짜의 작업 기록이 없습니다.",
            "date": date_str
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    # 파싱
    projects = parse_daily_log(content)

    if not projects:
        result = {
            "success": False,
            "error": "파싱된 프로젝트가 없습니다.",
            "date": date_str
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    # 형식에 따라 출력
    if args.format == 'markdown':
        summary = generate_markdown_summary(projects, date_str)

        if args.save:
            saved_path = save_local_summary(summary, date_str)
            result = {
                "success": True,
                "date": date_str,
                "projects_count": len(projects),
                "saved_path": saved_path,
                "format": "markdown"
            }
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(summary)

    elif args.format == 'notion':
        blocks = generate_notion_blocks(projects, date_str)
        result = {
            "success": True,
            "date": date_str,
            "projects_count": len(projects),
            "blocks": blocks,
            "format": "notion"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.format == 'json':
        result = {
            "success": True,
            "date": date_str,
            "projects": projects,
            "format": "json"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
