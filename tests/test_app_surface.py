import os
import requests


BASE_URL = os.getenv('APP_BASE_URL', 'http://192.99.71.97:8081')


def test_root_returns_html():
    r = requests.get(f"{BASE_URL}/", timeout=10)
    assert r.status_code == 200
    content_type = r.headers.get('Content-Type', '')
    assert 'html' in content_type.lower()
    assert 'RAW Pressery' in r.text or 'Welcome Back' in r.text


def test_vite_svg_served():
    r = requests.get(f"{BASE_URL}/vite.svg", timeout=10)
    assert r.status_code == 200
    content_type = r.headers.get('Content-Type', '')
    assert 'svg' in content_type.lower() or 'xml' in content_type.lower()
    assert '<svg' in r.text
