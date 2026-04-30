#!/usr/bin/env python3
"""Start Flask server without auto-reload for background execution"""

from app import app

if __name__ == '__main__':
    # Run without auto-reload to work better in background
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
