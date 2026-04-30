# PORTFOLIO MANAGER FIX - SOLVED!

## Problem Root Cause
**Port 5000 was being used by macOS AirPlay Receiver** (not Flask)! This is why all portfolio save requests were returning 403 errors from AirTunes instead of reaching your Flask server.

## Solution Applied
Changed Flask server port from **5000 → 5001** to avoid conflict with macOS system services.

## Files Updated
1. **Scripts/app.py** - Changed to `app.run(debug=True, port=5001)`
2. **src/PortfolioManager.jsx** - Updated both fetch URLs to use port 5001:
   - `http://localhost:5001/portfolio`
   - `http://localhost:5001/update-portfolio`

## How to Use

### Start Flask Server:
```bash
cd "/Users/arunmunagala/KBAI Stock Project/KB-AI-Project/Scripts"
/usr/local/bin/python3 start_server.py &
```

**Or** use the regular app.py (with debug mode):
```bash
cd "/Users/arunmunagala/KBAI Stock Project/KB-AI-Project/Scripts"
/usr/local/bin/python3 app.py
```

### Start Vite (if not running):
```bash
cd "/Users/arunmunagala/KBAI Stock Project/KB-AI-Project"
npm run dev
```

### Test Portfolio Manager:
1. Go to http://localhost:5173
2. Click "Manage Portfolio"
3. Add stocks (e.g., Mastercard - MA)
4. Click "Save Portfolio" (💾)
5. Navigate to Dashboard
6. **Your custom portfolio should now appear!**

## Verification
Portfolio saves to: `/Users/arunmunagala/KBAI Stock Project/KB-AI-Project/Scripts/custom_portfolio.json`

Test endpoint directly:
```bash
cd "/Users/arunmunagala/KBAI Stock Project/KB-AI-Project/Scripts"
/usr/local/bin/python3 test_endpoint.py
```

Expected output: **✅ SUCCESS! Portfolio saved.**

## What Was Wrong
1. macOS uses port 5000 for AirPlay Receiver
2. Flask couldn't bind to port 5000 properly
3. Requests went to AirPlay service (returned 403 Forbidden)
4. Portfolio never reached your Flask server
5. File was never created

## What's Fixed
✅ Flask now runs on port 5001 (no conflicts)
✅ Portfolio Manager updated to use port 5001
✅ Endpoint tested and working (200 OK response)
✅ custom_portfolio.json file successfully created
✅ Dashboard will now load custom portfolio from saved file

## Additional Scripts Created
- **test_endpoint.py** - Quick test for the save endpoint
- **start_server.py** - Start Flask without debug auto-reload (better for background)
