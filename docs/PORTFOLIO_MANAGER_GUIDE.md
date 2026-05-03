# 📈 Portfolio Manager User Guide

## ✨ **New Feature: Visual Portfolio Management Interface**

You now have a beautiful, user-friendly interface to add and remove stocks from your portfolio—**no code editing required!**

---

## 🚀 **How to Access**

### **Method 1: Via Navigation Bar**
1. Open http://localhost:5173
2. Login with: `adiagark@iu.edu` / `Agent123`
3. Click **"Manage Portfolio"** in the top navigation bar
4. You're now in the Portfolio Manager!

### **Method 2: Direct URL**
Navigate directly to: http://localhost:5173/portfolio-manager

---

## 🎯 **Features**

### **1. Search with Autocomplete**
- **50+ popular stocks** pre-loaded with company names
- Type ticker symbol (e.g., "AAPL") or company name (e.g., "Apple")
- Dropdown shows: **AAPL - Apple Inc.**

### **2. Add Stocks**
1. Select stock from dropdown
2. Enter **Quantity** (number of shares you own)
3. Enter **Average Price** (your purchase price per share)
4. Click **"Add"** button
5. Stock appears in your portfolio instantly!

### **3. Remove Stocks**
- Click the **red trash icon** next to any stock
- Stock is removed immediately

### **4. Save Portfolio**
- Click **"Save Portfolio"** button at the bottom
- Changes are persisted (won't be lost on refresh)
- Returns success message when saved

### **5. View Total Investment**
- Green chip at top shows total portfolio value
- Updates automatically as you add/remove stocks

---

## 📋 **Step-by-Step Example**

### **Adding Tesla to Your Portfolio:**

1. **Open Portfolio Manager**
   ```
   http://localhost:5173/portfolio-manager
   ```

2. **Search for Tesla**
   - Click the "Stock Symbol" dropdown
   - Type "TSLA" or "Tesla"
   - Select **"TSLA - Tesla Inc."**

3. **Enter Details**
   - Quantity: `15` (you own 15 shares)
   - Average Price: `250.00` (you bought at $250 per share)

4. **Click Add**
   - Tesla appears in your portfolio
   - Shows investment: $3,750.00 (15 × $250)

5. **Save**
   - Click **"Save Portfolio"** button
   - See success message

6. **Test It**
   - Return to Dashboard (click "Home" → "Login")
   - You'll see TSLA in your portfolio!
   - Click "Analyze Stock" to test the rule-based agent on Tesla

---

## 🎨 **Interface Features**

### **Stock Cards Display:**
```
┌─────────────────────────────┐
│  AAPL                    🗑️  │
│                              │
│  Quantity: 10 shares         │
│  Avg Price: $150.00          │
│  Investment: $1,500.00       │
└─────────────────────────────┘
```

### **Available Stocks (Pre-loaded):**

**Tech Giants:**
- AAPL (Apple), GOOGL (Alphabet), MSFT (Microsoft)
- AMZN (Amazon), META (Meta/Facebook), NFLX (Netflix)
- TSLA (Tesla), NVDA (NVIDIA), AMD (AMD)

**Finance:**
- JPM (JPMorgan), BAC (Bank of America), GS (Goldman Sachs)
- V (Visa), MA (Mastercard), PYPL (PayPal)

**Crypto-Related:**
- COIN (Coinbase), SQ (Block/Square), MSTR (MicroStrategy)

**Entertainment:**
- DIS (Disney), PARA (Paramount), SPOT (Spotify)

**And 30+ more!**

---

## 💾 **How It Works**

### **Backend:**
- Stocks saved to `custom_portfolio.json` file
- Flask endpoint: `/update-portfolio` (POST)
- Portfolio endpoint updated to read from saved file

### **Frontend:**
- React component with Material-UI
- Local storage backup
- Beautiful autocomplete dropdown
- Real-time validation

### **Data Flow:**
```
Portfolio Manager → Save → Backend (JSON file) → Dashboard loads updated portfolio
```

---

## 🔥 **Pro Tips**

### **1. Quick Add Multiple Stocks**
Add several stocks in one session, then click "Save Portfolio" once at the end.

### **2. Validate Before Analyzing**
After adding stocks, return to Dashboard and verify they appear before running analysis.

### **3. Realistic Prices**
Use approximate current market prices for more accurate analysis results.

### **4. Mix Stock Types**
Add tech stocks, finance stocks, and volatile stocks (like TSLA) to see different rule triggers.

---

## 🧪 **Testing the New Interface**

### **Quick Test:**
1. Go to http://localhost:5173/portfolio-manager
2. Add **TSLA** (Tesla): Qty: 10, Price: $250
3. Add **NVDA** (NVIDIA): Qty: 15, Price: $400
4. Click "Save Portfolio"
5. Go back to Dashboard
6. Analyze TSLA → Should trigger **rule-based decision** (high volatility)

---

## 🎯 **Comparing Old vs New Method**

| Feature | Old Method (Code) | New Method (UI) |
|---------|------------------|-----------------|
| Add Stock | Edit `app.py` file | Click dropdown, fill form |
| Stock Search | Know exact ticker | Search by name or symbol |
| Validation | Manual | Automatic (duplicates, negatives) |
| Visibility | Hidden in code | Visual cards with details |
| Persistence | Manual file save | One-click save button |
| User-Friendly | ❌ Developer only | ✅ Anyone can use |

---

## 🐛 **Troubleshooting**

### **"Portfolio Manager" link not showing:**
- Make sure you're logged in
- Link only appears after authentication

### **Changes not reflected in Dashboard:**
- Click "Save Portfolio" button (don't forget!)
- Refresh Dashboard page (F5 or Cmd+R)

### **Can't find a stock:**
- If stock not in dropdown, you can still add manually by editing `app.py`
- Or use the `test_stock.py` script for quick testing

### **Port errors:**
```bash
# Clear ports and restart
lsof -ti:5000 | xargs kill -9
lsof -ti:5173 | xargs kill -9

# Restart servers
cd Scripts && python3 app.py &
cd .. && npm run dev
```

---

## 📊 **Example Use Cases**

### **Use Case 1: Test High-Risk Stock**
Add a volatile stock like TSLA:
- Expected: Triggers **P1 rule** (Critical Risk - SELL)
- Confidence: **95%**
- Type: **rule-based**

### **Use Case 2: Compare Multiple Stocks**
Add 5-6 stocks with different risk profiles:
- Some trigger rules (high confidence)
- Some use LLM (moderate confidence)
- Demonstrates hybrid reasoning

### **Use Case 3: Demo Presentation**
Before your demo:
1. Add 3-4 interesting stocks
2. Save portfolio
3. During demo: Show visual management interface
4. Then switch to Dashboard to analyze them

---

## ✅ **Summary**

**What You Got:**
- ✅ Beautiful visual interface for portfolio management
- ✅ 50+ stocks with autocomplete search
- ✅ No more code editing required
- ✅ Real-time validation and feedback
- ✅ Persistent storage (saves across sessions)
- ✅ Integration with existing Dashboard

**Where to Access:**
http://localhost:5173/portfolio-manager

**Quick Command to Test:**
```bash
# Make sure servers are running
lsof -i :5173 && lsof -i :5000

# If not, start them
cd KB-AI-Project/Scripts && python3 app.py &
cd .. && npm run dev
```

---

Enjoy your new Portfolio Manager! 🚀📈
