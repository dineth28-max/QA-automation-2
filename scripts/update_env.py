#!/usr/bin/env python3
import os
import json

def main():
    env_path = 'reports/env.json'
    data = {}
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {}

    data.update({
        'browser': os.environ.get('CHROME_VER', ''),
        'os': os.environ.get('OS_INFO', ''),
        'start_time': int(os.environ.get('START_TIME', '0')),
        'end_time': int(os.environ.get('END_TIME', '0')),
        'duration': int(os.environ.get('DURATION', '0')),
    })

    os.makedirs('reports', exist_ok=True)
    with open(env_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    print('Updated', env_path)

if __name__ == '__main__':
    main()
