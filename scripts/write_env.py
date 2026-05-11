#!/usr/bin/env python3
import os
import json
import time

def main():
    os.makedirs('reports', exist_ok=True)
    data = {
        'app_url': os.environ.get('API_BASE_URL') or os.environ.get('APP_BASE_URL') or '',
        'timestamp': time.time(),
    }
    with open('reports/env.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
    print('Wrote reports/env.json')

if __name__ == '__main__':
    main()
