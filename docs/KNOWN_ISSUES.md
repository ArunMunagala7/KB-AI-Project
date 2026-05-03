# Known Issues

## Current Issues

### High Priority
None currently

### Medium Priority
1. **Forecast model simplicity** - Using exponential smoothing which assumes stationarity. Consider LSTM for more complex patterns.
2. **Rule threshold brittleness** - Fixed thresholds (e.g., risk >= 8) don't adapt to market regime changes.

### Low Priority
1. **News API rate limits** - Finnhub free tier limits to 60 calls/minute. May need caching for large portfolios.
2. **Database connection pooling** - Currently creates new connection each request. Could optimize with connection pool.
3. **Frontend loading states** - Some transitions could be smoother with skeleton loaders.

## Fixed Issues

### v1.2.0
- ✅ LLM hallucinations (added evaluation framework)
- ✅ Cost tracking (implemented token monitoring)

### v1.1.0
- ✅ Lack of confidence transparency (added badges)
- ✅ No indication of decision source (added rule-based vs llm-based tags)

### v1.0.0
- ✅ Inconsistent decisions (implemented priority rules)
- ✅ Slow performance (added parallel execution)
- ✅ High-risk scenarios not handled (added P1 safety rule)

### v0.9.0
- ✅ No price forecasting capability
- ✅ Missing news sentiment analysis

## Reporting Issues

If you find a bug or have a feature request:
1. Check if it's already listed above
2. Search existing GitHub issues
3. If new, create issue with:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System info (Python version, OS)
