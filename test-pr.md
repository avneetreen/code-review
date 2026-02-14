# Automated Code Review System

An intelligent code review system that integrates with GitHub's pull request workflow to automatically analyse code changes and provide meaningful feedback.

## Features

- Automatic triggers on PR open, update, or reopen
- Secure GitHub App authentication (JWT + installation tokens)
- Line-level review comments posted directly to PRs
- Rate limit handling with proactive backoff
- Unified diff parsing for change detection

## Quick Start

```bash
# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
python -m pytest

# Start the server
uvicorn app.main:create_app --factory --port 8000
```

## Configuration

Copy `.env.example` to `.env` and fill in your GitHub App credentials:

```
ACR_GITHUB_APP_ID=your-app-id
ACR_GITHUB_PRIVATE_KEY_PATH=./private-key.pem
ACR_GITHUB_WEBHOOK_SECRET=your-secret
```

## Project Structure

```
app/
  github/     # Auth, API client, rate limiter, models
  webhook/    # Signature verification, parsing, routing
  review/     # Diff parsing, analysis handler
scripts/      # Setup and verification scripts
tests/        # Unit and integration tests
```

## Status

Phase 1 complete — webhook infrastructure and GitHub integration operational.
