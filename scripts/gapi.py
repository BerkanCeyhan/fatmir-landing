#!/usr/bin/env python3
"""Kleiner Zugang zu Google APIs ueber die Anmeldung des gsuite-Werkzeugs.

Der Refresh Token liegt geraetegebunden in ~/.config/gsuite/credentials.json
und wird hier nur gelesen, nie ausgegeben.
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

CRED = Path.home() / ".config" / "gsuite" / "credentials.json"
_token = None


def token():
    global _token
    if _token:
        return _token
    c = json.loads(CRED.read_text(encoding="utf-8"))
    data = urllib.parse.urlencode({
        "client_id": c["client_id"],
        "client_secret": c["client_secret"],
        "refresh_token": c["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req, timeout=30) as r:
        _token = json.load(r)["access_token"]
    return _token


def call(method, url, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", "Bearer " + token())
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8")[:600]
        raise SystemExit(f"{method} {url.split('?')[0]} -> HTTP {e.code}\n{detail}")
