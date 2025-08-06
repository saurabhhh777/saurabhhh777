#!/usr/bin/env python3
"""
Script to update the open source PRs table in README.md
"""

import os
import requests
import re
from datetime import datetime
from typing import List, Dict

# GitHub API configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
USERNAME = 'saurabhhh777'  # Your GitHub username
API_BASE_URL = 'https://api.github.com'

def get_headers():
    """Get headers for GitHub API requests"""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-PR-Update-Script'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def get_user_prs() -> List[Dict]:
    """Fetch all PRs created by the user"""
    prs = []
    page = 1
    per_page = 100
    
    while True:
        url = f"{API_BASE_URL}/search/issues"
        params = {
            'q': f'author:{USERNAME} is:pr is:public',
            'sort': 'updated',
            'order': 'desc',
            'page': page,
            'per_page': per_page
        }
        
        response = requests.get(url, headers=get_headers(), params=params)
        
        if response.status_code != 200:
            print(f"Error fetching PRs: {response.status_code}")
            break
            
        data = response.json()
        items = data.get('items', [])
        
        if not items:
            break
            
        for item in items:
            # Extract repository name
            repo_url = item['repository_url']
            repo_name = repo_url.split('/')[-2] + '/' + repo_url.split('/')[-1]
            
            # Skip if it's your own repository
            if repo_name.startswith(f'{USERNAME}/'):
                continue
                
            pr_info = {
                'repo': repo_name,
                'title': item['title'],
                'url': item['html_url'],
                'number': item['number'],
                'state': item['state'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at']
            }
            prs.append(pr_info)
        
        page += 1
        
        # Limit to recent PRs (last 20)
        if len(prs) >= 20:
            break
    
    return prs[:20]  # Return only the 20 most recent PRs

def get_status_emoji(state: str, created_at: str) -> str:
    """Get appropriate emoji for PR status"""
    if state == 'open':
        return '🟡'
    elif state == 'closed':
        return '✅'
    elif state == 'merged':
        return '✅'
    else:
        return '❓'

def format_pr_table(prs: List[Dict]) -> str:
    """Format PRs into a markdown table"""
    if not prs:
        return "| Sr No | Repository | PR Title | Status | Link |\n|-------|------------|----------|--------|------|\n| *No open source PRs found* | *No open source PRs found* | *No open source PRs found* | *No open source PRs found* | *No open source PRs found* |"
    
    table_lines = [
        "| Sr No | Repository | PR Title | Status | Link |",
        "|-------|------------|----------|--------|------|"
    ]
    
    for i, pr in enumerate(prs, 1):
        status_emoji = get_status_emoji(pr['state'], pr['created_at'])
        title = pr['title'][:50] + "..." if len(pr['title']) > 50 else pr['title']
        
        # Make repository name clickable
        repo_link = f"[{pr['repo']}](https://github.com/{pr['repo']})"
        
        table_lines.append(
            f"| {i} | {repo_link} | {title} | {status_emoji} {pr['state'].title()} | [#{pr['number']}]({pr['url']}) |"
        )
    
    return '\n'.join(table_lines)

def update_readme(prs: List[Dict]):
    """Update the README.md file with the new PR table"""
    readme_path = 'README.md'
    
    # Read the current README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the markers for the PR table
    start_marker = '<!-- PR_TABLE_START -->'
    end_marker = '<!-- PR_TABLE_END -->'
    
    # Generate the new table
    new_table = format_pr_table(prs)
    
    # Create the replacement content
    replacement = f"{start_marker}\n{new_table}\n{end_marker}"
    
    # Replace the content between markers
    pattern = f"{start_marker}.*?{end_marker}"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the updated content back to README.md
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated README.md with {len(prs)} open source PRs")

def main():
    """Main function"""
    print("🔄 Fetching open source PRs...")
    
    try:
        prs = get_user_prs()
        print(f"📦 Found {len(prs)} open source PRs")
        
        update_readme(prs)
        print("✅ Successfully updated README.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main() 