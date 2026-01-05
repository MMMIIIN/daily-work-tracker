#!/usr/bin/env python3
"""
Daily Work Tracker - 여러 프로젝트의 작업을 날짜별로 기록
저장 위치: 설정 파일에서 지정 (기본: ~/.claude/daily-work/YYYY-MM-DD.md)
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path


def get_config():
    """설정 파일 로드"""
    config_path = os.path.expanduser('~/.claude/daily-work-tracker/config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}


def get_log_path():
    """로그 저장 경로 반환"""
    config = get_config()
    paths = config.get('paths', {})
    return os.path.expanduser(paths.get('log', '~/.claude/daily-work'))


def get_project_name(cwd):
    """프로젝트 이름 추출 (폴더명 또는 package.json/pubspec.yaml에서)"""
    # pubspec.yaml 확인 (Flutter)
    pubspec = os.path.join(cwd, 'pubspec.yaml')
    if os.path.exists(pubspec):
        try:
            with open(pubspec, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('name:'):
                        return line.split(':')[1].strip()
        except:
            pass

    # package.json 확인 (Node.js)
    pkg = os.path.join(cwd, 'package.json')
    if os.path.exists(pkg):
        try:
            with open(pkg, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('name', os.path.basename(cwd))
        except:
            pass

    # 폴더명 사용
    return os.path.basename(cwd)


def format_prompt(prompt, max_length=150):
    """프롬프트 포맷팅 (여러 줄은 들여쓰기 형태로, 15줄 초과시 앞 10줄 + 뒤 5줄)"""
    lines = prompt.strip().split('\n')

    # 빈 줄 제거하고 각 줄 trim
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return ''

    # 15줄 초과 시 앞 10줄 + 뒤 5줄
    if len(lines) > 15:
        head = lines[:10]
        tail = lines[-5:]
        lines = head + ['...'] + tail

    # 첫 줄 처리
    first_line = lines[0]
    if len(first_line) > max_length:
        first_line = first_line[:max_length] + '...'

    # 한 줄만 있으면 그대로 반환
    if len(lines) == 1:
        return first_line

    # 여러 줄이면 들여쓰기 형태로 반환
    result = [first_line]
    for line in lines[1:]:
        if line == '...':
            result.append('  ...')
        else:
            if len(line) > max_length:
                line = line[:max_length] + '...'
            result.append(f'  {line}')  # 2칸 들여쓰기

    return '\n'.join(result)


def main():
    try:
        # stdin에서 Hook 데이터 읽기
        input_data = json.load(sys.stdin)

        prompt = input_data.get('prompt', '')
        cwd = input_data.get('cwd', os.getcwd())

        if not prompt.strip():
            sys.exit(0)

        # 내부 명령어는 로그 제외
        skip_prefixes = ['/daily-', '/pr-log', '/help', '/clear']
        for prefix in skip_prefixes:
            if prompt.strip().startswith(prefix):
                sys.exit(0)

        # 프로젝트 정보
        project_name = get_project_name(cwd)

        # 날짜별 로그 파일 경로 (설정에서 읽기)
        today = datetime.now().strftime('%Y-%m-%d')
        log_dir = get_log_path()
        log_file = os.path.join(log_dir, f'{today}.md')

        os.makedirs(log_dir, exist_ok=True)

        # 타임스탬프
        timestamp = datetime.now().strftime('%H:%M')

        # 파일이 새로 만들어지는지 확인
        is_new_file = not os.path.exists(log_file)

        # 해당 프로젝트 섹션이 있는지 확인
        project_section_marker = f'## 🔹 {project_name}'
        project_exists = False
        file_content = ''

        if not is_new_file:
            with open(log_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
                project_exists = project_section_marker in file_content

        # 프롬프트 포맷팅
        prompt_summary = format_prompt(prompt)

        # 새 항목 작성
        new_entry = f'- **[{timestamp}]** {prompt_summary}\n'

        if is_new_file:
            # 새 파일 생성
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f'# 📅 {today} 작업 기록\n\n')
                f.write(f'{project_section_marker}\n')
                f.write(f'> `{cwd}`\n\n')
                f.write(new_entry)
        elif not project_exists:
            # 새 프로젝트 섹션 추가
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f'\n{project_section_marker}\n')
                f.write(f'> `{cwd}`\n\n')
                f.write(new_entry)
        else:
            # 기존 프로젝트 섹션에 항목 추가
            # 해당 프로젝트 섹션의 끝을 찾아서 추가
            lines = file_content.split('\n')
            new_lines = []
            in_target_section = False
            added = False

            for i, line in enumerate(lines):
                new_lines.append(line)

                if line.startswith(project_section_marker):
                    in_target_section = True
                elif in_target_section and line.startswith('## '):
                    # 다음 섹션 시작 전에 추가
                    new_lines.insert(-1, new_entry.rstrip())
                    in_target_section = False
                    added = True

            # 마지막 섹션인 경우 끝에 추가
            if in_target_section and not added:
                new_lines.append(new_entry.rstrip())

            with open(log_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))

        sys.exit(0)

    except Exception as e:
        # 에러가 나도 Claude Code 동작에 영향 없도록 조용히 처리
        sys.exit(0)


if __name__ == '__main__':
    main()
