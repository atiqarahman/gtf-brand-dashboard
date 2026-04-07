"""
GitHub-backed database for GTF Brand Dashboard
Uses GitHub API to read/write brands.json directly to the repo
"""

import streamlit as st
import requests
import base64
import json

REPO = "atiqarahman/gtf-brand-dashboard"
FILE_PATH = "brands.json"
BRANCH = "main"

def get_github_token():
    """Get GitHub token from Streamlit secrets"""
    try:
        return st.secrets["GITHUB_TOKEN"]
    except Exception:
        return None

def get_headers():
    token = get_github_token()
    if not token:
        return None
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

def load_from_github():
    """Load brands.json from GitHub"""
    headers = get_headers()
    if not headers:
        return None, None
    
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            sha = data["sha"]
            return json.loads(content), sha
        return None, None
    except Exception:
        return None, None

def save_to_github(data, sha, message="Update brands.json"):
    """Save brands.json to GitHub"""
    headers = get_headers()
    if not headers:
        return False
    
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    content = base64.b64encode(json.dumps(data, indent=2, default=str).encode()).decode()
    
    payload = {
        "message": message,
        "content": content,
        "sha": sha,
        "branch": BRANCH
    }
    
    try:
        resp = requests.put(url, headers=headers, json=payload, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False
