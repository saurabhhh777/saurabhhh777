# Open Source PRs Update Script

This directory contains scripts to automatically update the open source PRs table in the main README.md file.

## Files

- `update_prs.py` - Main script that fetches PRs from GitHub API and updates README.md
- `requirements.txt` - Python dependencies

## How it works

1. The GitHub Action (`.github/workflows/update-prs.yml`) runs daily at 2 AM UTC
2. It fetches all your open source PRs using the GitHub API
3. Filters out PRs from your own repositories
4. Updates the table in README.md between the `<!-- PR_TABLE_START -->` and `<!-- PR_TABLE_END -->` markers
5. Commits and pushes the changes automatically

## Manual trigger

You can manually trigger the workflow by:
1. Going to the "Actions" tab in your repository
2. Selecting "Update Open Source PRs"
3. Clicking "Run workflow"

## Configuration

The script is configured for username `saurabhhh777`. To change this, edit the `USERNAME` variable in `update_prs.py`. 