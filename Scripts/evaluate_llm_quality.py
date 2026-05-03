#!/usr/bin/env python3
"""
Integration Script: LLM Evaluation with Existing Agents
Demonstrates how to evaluate LLM responses from Trend, Risk, Forecast, and Decision agents
"""

import sys
import os
from llm_evaluator import LLMEvaluator
from trend_agent import TrendAnalysisAgent
from risk_assesment import RiskAssessmentAgent
from forecast_agent import ForecastingAgent
from decision_agent import DecisionAgent

def evaluate_trend_agent(ticker: str, evaluator: LLMEvaluator):
    """Evaluate Trend Agent's LLM reasoning"""
    print(f"\n🔍 EVALUATING TREND AGENT for {ticker}")
    print("="*70)
    
    agent = TrendAnalysisAgent()
    result = agent.run(ticker)
    
    if not result or 'analysis' not in result:
        print("❌ No LLM response to evaluate")
        return None
    
    # Ground truth = actual calculated metrics
    ground_truth = {
        'sma50': result['sma50'],
        'sma200': result['sma200'],
        'rsi': result['rsi'],
        'macd': result['macd'],
        'trend_score': result['trend_score']
    }
    
    # Input metrics provided to LLM
    input_metrics = ground_truth.copy()
    
    # Evaluate the LLM-generated analysis
    report = evaluator.evaluate_comprehensive(
        agent_name='Trend Agent',
        llm_response=result['analysis'],
        ground_truth=ground_truth,
        input_metrics=input_metrics,
        tokens_used=None  # Will be estimated
    )
    
    return report

def evaluate_risk_agent(ticker: str, evaluator: LLMEvaluator):
    """Evaluate Risk Agent's LLM analysis"""
    print(f"\n⚠️  EVALUATING RISK AGENT for {ticker}")
    print("="*70)
    
    agent = RiskAssessmentAgent()
    result = agent.run(ticker)
    
    if not result or 'analysis' not in result:
        print("❌ No LLM response to evaluate")
        return None
    
    # Ground truth = calculated risk metrics
    ground_truth = {
        'risk_score': result['risk_score'],
        'volatility': result['volatility'],
        'max_drawdown': result['max_drawdown'],
        'VaR_95': result['VaR_95']
    }
    
    input_metrics = {
        'risk_level': result['risk_level'],
        'volatility': result['volatility'],
        'news_headlines': result['news_headlines']
    }
    
    # Evaluate the LLM-generated analysis
    report = evaluator.evaluate_comprehensive(
        agent_name='Risk Agent',
        llm_response=result['analysis'],
        ground_truth=ground_truth,
        input_metrics=input_metrics
    )
    
    return report

def evaluate_forecast_agent(ticker: str, evaluator: LLMEvaluator):
    """Evaluate Forecast Agent's LLM reasoning"""
    print(f"\n📈 EVALUATING FORECAST AGENT for {ticker}")
    print("="*70)
    
    agent = ForecastingAgent()
    result = agent.run(ticker)
    
    if not result or 'analysis' not in result:
        print("❌ No LLM response to evaluate")
        return None
    
    # Ground truth = forecast metrics
    ground_truth = {
        'initial_price': result['initial_price'],
        'forecastedPrice': result['forecastedPrice'],
        'percentChange': result['percentChange']
    }
    
    input_metrics = ground_truth.copy()
    input_metrics['direction'] = result['direction']
    
    # Evaluate the LLM-generated analysis
    report = evaluator.evaluate_comprehensive(
        agent_name='Forecast Agent',
        llm_response=result['analysis'],
        ground_truth=ground_truth,
        input_metrics=input_metrics
    )
    
    return report

def evaluate_decision_agent_llm(ticker: str, evaluator: LLMEvaluator):
    """Evaluate Decision Agent (only when it uses LLM, not rules)"""
    print(f"\n🎯 EVALUATING DECISION AGENT for {ticker}")
    print("="*70)
    
    # Run all prerequisite agents
    trend_agent = TrendAnalysisAgent()
    risk_agent = RiskAssessmentAgent()
    forecast_agent = ForecastingAgent()
    decision_agent = DecisionAgent()
    
    trend_result = trend_agent.run(ticker)
    risk_result = risk_agent.run(ticker)
    forecast_result = forecast_agent.run(ticker)
    
    if not all([trend_result, risk_result, forecast_result]):
        print("❌ Failed to get prerequisite agent results")
        return None
    
    decision = decision_agent.decide(trend_result, risk_result, forecast_result)
    
    # Only evaluate if LLM was used (not rule-based)
    if decision.get('decision_type') != 'llm-based':
        print(f"ℹ️  Decision was rule-based ({decision.get('decision_type')}), skipping LLM evaluation")
        print(f"   Decision: {decision.get('decision')} with {decision.get('confidence_score')}% confidence")
        return None
    
    # For LLM-based decisions, evaluate the reasoning
    ground_truth = {
        'trend_score': trend_result['trend_score'],
        'risk_score': risk_result['risk_score'],
        'forecast_direction': forecast_result['direction']
    }
    
    input_metrics = ground_truth.copy()
    
    report = evaluator.evaluate_comprehensive(
        agent_name='Decision Agent (LLM)',
        llm_response=decision.get('reasoning', ''),
        ground_truth=ground_truth,
        input_metrics=input_metrics
    )
    
    return report

def run_full_evaluation(tickers: list):
    """
    Run comprehensive evaluation across multiple stocks and all agents
    
    Args:
        tickers: List of stock symbols to evaluate
    """
    evaluator = LLMEvaluator()
    
    print("\n" + "="*70)
    print("COMPREHENSIVE LLM EVALUATION FRAMEWORK")
    print("="*70)
    print(f"Testing {len(tickers)} stocks: {', '.join(tickers)}")
    print()
    
    all_reports = []
    
    for ticker in tickers:
        print(f"\n\n{'#'*70}")
        print(f"# STOCK: {ticker}")
        print(f"{'#'*70}")
        
        try:
            # Evaluate each agent
            trend_report = evaluate_trend_agent(ticker, evaluator)
            if trend_report:
                all_reports.append(trend_report)
            
            risk_report = evaluate_risk_agent(ticker, evaluator)
            if risk_report:
                all_reports.append(risk_report)
            
            forecast_report = evaluate_forecast_agent(ticker, evaluator)
            if forecast_report:
                all_reports.append(forecast_report)
            
            decision_report = evaluate_decision_agent_llm(ticker, evaluator)
            if decision_report:
                all_reports.append(decision_report)
                
        except Exception as e:
            print(f"❌ Error evaluating {ticker}: {e}")
            import traceback
            traceback.print_exc()
    
    # Generate final summary
    print("\n\n" + "="*70)
    print("FINAL EVALUATION SUMMARY")
    print("="*70)
    
    summary = evaluator.generate_summary_report()
    
    print(f"\n📊 Total Evaluations: {summary['total_evaluations']}")
    print(f"\n🏆 Agent Performance Rankings:")
    
    # Sort agents by score
    sorted_agents = sorted(summary['average_scores'].items(), 
                          key=lambda x: x[1], reverse=True)
    
    for i, (agent, score) in enumerate(sorted_agents, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        bar = "█" * int(score / 5)
        print(f"{medal} {agent:20} {score:5.1f}/100  {bar}")
    
    if summary['improvement_trends']:
        print(f"\n📈 Improvement Trends:")
        for agent, trend in summary['improvement_trends'].items():
            arrow = "↗️" if trend > 2 else "↘️" if trend < -2 else "→"
            print(f"   {arrow} {agent:20} {trend:+.1f} points")
    
    # Save detailed report
    report_file = f"llm_evaluation_{len(tickers)}_stocks.json"
    evaluator.save_report(report_file)
    
    print(f"\n✅ Detailed report saved to: {report_file}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if summary['worst_performing_agent']:
        worst_agent = summary['worst_performing_agent']
        worst_score = summary['average_scores'][worst_agent]
        if worst_score < 70:
            print(f"   ⚠️  {worst_agent} needs improvement (score: {worst_score:.1f})")
            print(f"      Consider: Improving prompt clarity, adding more context, or reducing temperature")
    
    avg_overall = sum(summary['average_scores'].values()) / len(summary['average_scores'])
    if avg_overall >= 80:
        print(f"   ✅ Overall LLM performance is EXCELLENT ({avg_overall:.1f}/100)")
    elif avg_overall >= 70:
        print(f"   👍 Overall LLM performance is GOOD ({avg_overall:.1f}/100)")
    else:
        print(f"   ⚠️  Overall LLM performance needs attention ({avg_overall:.1f}/100)")
    
    print()
    return evaluator, all_reports

if __name__ == "__main__":
    # Test with multiple stocks
    test_tickers = ['AAPL', 'GOOGL', 'TSLA']
    
    if len(sys.argv) > 1:
        test_tickers = sys.argv[1:]
    
    print(f"Testing with tickers: {test_tickers}")
    
    evaluator, reports = run_full_evaluation(test_tickers)
    
    print("\n✅ Evaluation complete!")
