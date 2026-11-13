name: 24/7 AI Autonomous Lead Worker

on:
  schedule:
    - cron: '0 8 * * *' # Runs automatically every day at 8:00 AM UTC
  workflow_dispatch: # Allows you to click 'Run workflow' manually anytime in GitHub

jobs:
  run-ai-task:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository code
        uses: actions/checkout@v4

      - name: Set up Python environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install google-generativeai requests

      - name: Run Worker
        run: |
          python worker.py
