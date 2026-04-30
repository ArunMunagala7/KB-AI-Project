#!/usr/bin/env python3
"""
Quick Stock Tester
Test any stock symbol instantly without modifying code
"""

import sys
from trend_agent import TrendAnalysisAgent
from risk_assesment import RiskAssessmentAgent
from forecast_agent import ForecastingAgent
from decision_agent import DecisionAgent
import json

def test_stock(ticker):
    """Test a single stock and show decision breakdown"""
    print(f"\n{'='*70}")
    print(f"ANALYZING: {ticker.upper()}")
    print(f"{'='*70}\n")
    
    # Initialize agents
    trend_agent = TrendAnalysisAgent()
    risk_agent = RiskAssessmentAgent()
    forecast_agent = ForecastingAgent()
    decision_agent = DecisionAgent()
    
    # Run analysis
    print(f"🔍 Trend Agent analyzing...")
    trend_result = trend_agent.run(ticker)
    print(f"   ✓ Trend Score: {trend_result.get('trend_score', 'N/A')}")
    print(f"   ✓ Confidence: {trend_result.get('confidence_score', 'N/A')}%")
    
    print(f"\n⚠️  Risk Agent analyzing...")
    risk_result = risk_agent.run(ticker)
    print(f"   ✓ Risk Score: {risk_result.get('risk_score', 'N/A')}")
    print(f"   ✓ Volatility: {risk_result.get('volatility', 'N/A')}%")
    print(f"   ✓ Max Drawdown: {risk_result.get('max_drawdown', 'N/A')}%")
    
    print(f"\n📈 Forecast Agent predicting...")
    forecast_result = forecast_agent.run(ticker)
    print(f"   ✓ Direction: {forecast_result.get('direction', 'N/A')}")
    print(f"   ✓ Forecasted Price: ${forecast_result.get('forecastedPrice', 'N/A')}")
    print(f"   ✓ Change: {forecast_result.get('percentChange', 'N/A')}%")
    
    print(f"\n🎯 Decision Agent deciding...")
    decision_result = decision_agent.decide(trend_result, risk_result, forecast_result)
    
    print(f"\n{'='*70}")
    print(f"FINAL DECISION")
    print(f"{'='*70}")
    print(f"Decision:       {decision_result.get('decision', 'N/A')}")
    print(f"Confidence:     {decision_result.get('confidence_score', 'N/A')}%")
    print(f"Decision Type:  {decision_result.get('decision_type', 'N/A')}")
    print(f"Reasoning:      {decision_result.get('reasoning', 'N/A')}")
    print(f"{'='*70}\n")
    
    # Highlight if rule-based
    if decision_result.get('decision_type') == 'rule-based':
        print("🎉 RULE-BASED DECISION TRIGGERED!")
        print("   This decision was made instantly by expert rules, not LLM.")
        print("   Higher confidence, faster response, zero API cost!\n")
    else:
        print("🤖 LLM-BASED DECISION")
        print("   This case was ambiguous, so the LLM analyzed it.")
        print("   Demonstrates hybrid reasoning in action!\n")
    
    return decision_result

def compare_stocks(tickers):
    """Compare multiple stocks side-by-side"""
    print(f"\n{'='*70}")
    print(f"COMPARING {len(tickers)} STOCKS")
    print(f"{'='*70}\n")
    
    results = []
    for ticker in tickers:
        trend_agent = TrendAnalysisAgent()
        risk_agent = RiskAssessmentAgent()
        forecast_agent = ForecastingAgent()
        decision_agent = DecisionAgent()
        
        trend_result = trend_agent.run(ticker)
        risk_result = risk_agent.run(ticker)
        forecast_result = forecast_agent.run(ticker)
        decision_result = decision_agent.decide(trend_result, risk_result, forecast_result)
        
        results.append({
            'ticker': ticker.upper(),
            'trend': trend_result.get('trend_score', 0),
            'risk': risk_result.get('risk_score', 0),
            'decision': decision_result.get('decision', 'N/A'),
            'confidence': decision_result.get('confidence_score', 0),
            'type': decision_result.get('decision_type', 'N/A')
        })
    
    # Print comparison table
    print(f"{'Ticker':<8} {'Trend':<7} {'Risk':<7} {'Decision':<9} {'Conf':<6} {'Type':<12}")
    print("-" * 70)
    for r in results:
        print(f"{r['ticker']:<8} {r['trend']:>+6} {r['risk']:>6.1f} {r['decision']:<9} {r['confidence']:>5}% {r['type']:<12}")
    
    # Summary
    rule_based = sum(1 for r in results if r['type'] == 'rule-based')
    print(f"\n📊 Summary:")
    print(f"   Total analyzed: {len(results)}")
    print(f"   Rule-based: {rule_based} ({rule_based/len(results)*100:.0f}%)")
    print(f"   LLM-based: {len(results)-rule_based} ({(len(results)-rule_based)/len(results)*100:.0f}%)")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single stock:   python3 test_stock.py AAPL")
        print("  Multiple stocks: python3 test_stock.py AAPL GOOGL MSFT TSLA")
        print("\nExamples:")
        print("  python3 test_stock.py NVDA")
        print("  python3 test_stock.py AAPL MSFT GOOGL")
        sys.exit(1)
    
    tickers = [t.upper() for t in sys.argv[1:]]
    
    if len(tickers) == 1:
        # Detailed single stock analysis
        test_stock(tickers[0])
    else:
        # Comparison mode
        compare_stocks(tickers)
