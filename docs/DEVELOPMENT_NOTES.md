# Development Notes

## Project Evolution

### Initial Approach (March 2026)
Started with pure LLM-based decision making. Noticed inconsistent confidence scores around 60%.

### Issue #1: Inconsistent Decisions
Same stock, different recommendations on consecutive runs. Not acceptable for financial app.

**Solution tried:** Temperature = 0
**Result:** Helped but still variable

### Issue #2: High Risk Scenarios
LLM sometimes suggested BUY even when volatility was extreme (risk score 10).

**Solution:** Added P1 safety rule - always SELL if risk >= 8
**Result:** Confidence jumped to 95% for these cases

### Issue #3: Slow Performance
Each stock took 2.5 seconds to analyze. Too slow for portfolio view.

**Solution:** Parallelized trend/risk/forecast agents
**Result:** Down to 0.7 seconds per stock

### Issue #4: Hallucinations
LLM occasionally made up numbers (claimed SMA50 = $200 when actual = $175).

**Solution:** Built evaluation framework to verify numbers
**Result:** Can now detect and flag bad responses

## Current Architecture (April 2026)

Hybrid system:
- Rules handle clear-cut cases (80% of scenarios in current market)
- LLM handles ambiguous cases (20%)
- Evaluation monitors all LLM outputs

## Todo
- [ ] Add backtesting framework
- [ ] Implement portfolio optimization
- [ ] Add more technical indicators
- [ ] Build alert system for risk threshold breaches
