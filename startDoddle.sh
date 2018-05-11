#!/usr/bin/env bash

export SLACK_BOT_TOKEN="your-token-here"
export BOT_ID="bot-id-here"
export BOT_NAME="doddle"

pkill -f *dodle.py

python dottle.py
