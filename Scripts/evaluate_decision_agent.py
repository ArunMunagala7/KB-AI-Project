"""
Evaluation Script: Rule-Based Logic Impact Analysis
Analyzes how often rules trigger and their confidence vs LLM decisions
"""

import sys
import os
from datetime import datetime
import yfinance as yf
import pandas as pd

# Load environment variables
from dotenv import load_dotenv
load_dotenv('../.env')

class PureLLMDecisionAgent:
    """Original decision agent without rule-based logic (for comparison)"""
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def decide(self, trend_result, risk_result, forecast_result):
        ticker = trend_result['Ticker']
        trend_score = trend_result['trend_score']
        risk_score = risk_result['risk_score']
        headlines = risk_result['news_headlines']
        llm_risk_score = risk_result['llm_risk_score']
        analysis = risk_result.get('llm_analysis', '')
        
        forecast_trend = forecast_result.get('direction', 'N/A')
        forecast_change = forecast_result.get('percentChange', 'N/A')
        forecast_initial = forecast_result.get('initial_price', 'N/A')
        forecast_final = forecast_result.get('forecastedPrice', 'N/A')

        prompt = (
            f"You are an expert financial portfolio advisor. Analyze {ticker} and return a JSON object with:\n"
            f" - decision: BUY, SELL, or HOLD\n"
            f" - reasoning: Brief explanation\n"
            f" - confidence_score: Integer 0-100\n\n"
            f"Trend Score: {trend_score}\n"
            f"Risk Score: {risk_score}\n"
            f"LLM Risk Score: {llm_risk_score}\n"
            f"News Headlines: {headlines}\n"
            f"Analysis: {analysis}\n"
            f"Forecast Direction: {forecast_trend}\n"
            f"Forecast Change: {forecast_change}%\n"
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a portfolio decision-making assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content.strip()
            parsed_json_str = content.strip('```json').strip('```').strip()
            parsed = json.loads(parsed_json_str)
            return {
                'ticker': ticker,
                'decision': parsed.get("decision", "HOLD").upper(),
                'reasoning': parsed.get("reasoning", ""),
                'confidence_score': parsed.get("confidence_score", 70),
                'decision_type': 'pure-llm'
            }
        except Exception as e:
            print(f"[Error] Pure LLM decision failed: {e}")
            return {
                'ticker': ticker,
                'decision': 'HOLD',
                'reasoning': 'Error occurred',
                'confidence_score': 0,
                'decision_type': 'pure-llm'
            }


def evaluate_decision_accuracy(ticker, test_date_str, agent_type='hybrid'):
    """
    Evaluate a single decision by checking what happened 90 days later
    Returns: accuracy score (1 if correct, 0 if wrong), actual return %
    """
    test_date = datetime.strptime(test_date_str, '%Y-%m-%d')
    future_date = test_date + timedelta(days=90)
    
    # Download data up to test_date for agent analysis
    start_analysis = test_date - timedelta(days=365*5)
    data = yf.download(ticker, start=start_analysis.strftime('%Y-%m-%d'), 
                       end=test_date.strftime('%Y-%m-%d'), progress=False)
    
    if data.empty or len(data) < 100:
        return None, None, None
    
    price_at_decision = data['Close'].iloc[-1]
    
    # Get actual price 90 days later
    future_data = yf.download(ticker, start=test_date.strftime('%Y-%m-%d'), 
                             end=future_date.strftime('%Y-%m-%d'), progress=False)
    
    if future_data.empty:
        return None, None, None
    
    price_after_90_days = future_data['Close'].iloc[-1]
    actual_return = ((price_after_90_days - price_at_decision) / price_at_decision) * 100
    
    # Run agents
    trend_agent = TrendAnalysisAgent()
    risk_agent = RiskAssessmentAgent()
    forecast_agent = ForecastingAgent()
    
    print(f"  Analyzing {ticker} on {test_date_str}...")
    
    trend_result = trend_agent.run(ticker)
    risk_result = risk_agent.run(ticker)
    forecast_result = forecast_agent.run(ticker)
    
    # Get decision from appropriate agent
    if agent_type == 'hybrid':
        decision_agent = DecisionAgent()
    else:
        decision_agent = PureLLMDecisionAgent()
    
    decision_result = decision_agent.decide(trend_result, risk_result, forecast_result)
    decision = decision_result['decision']
    confidence = decision_result.get('confidence_score', 0)
    decision_type = decision_result.get('decision_type', 'unknown')
    
    # Determine if decision was correct
    correct = 0
    if decision == 'BUY' and actual_return > 2:
        correct = 1
    elif decision == 'SELL' and actual_return < -2:
        correct = 1
    elif decision == 'HOLD' and abs(actual_return) <= 2:
        correct = 1
    
    return {
        'ticker': ticker,
        'test_date': test_date_str,
        'decision': decision,
        'confidence': confidence,
        'decision_type': decision_type,
        'actual_return': actual_return,
        'correct': correct,
        'price_at_decision': price_at_decision,
        'price_after_90d': price_after_90_days
    }


def run_evaluation():
    """Run comprehensive evaluation comparing hybrid vs pure LLM"""
    
    print("=" * 70)
    print("DECISION AGENT EVALUATION: Rule-Based + LLM vs Pure LLM")
    print("=" * 70)
    print()
    
    # Test on multiple stocks and dates
    test_cases = [
        ('AAPL', '2024-01-15'),
        ('AAPL', '2024-06-15'),
        ('GOOGL', '2024-01-15'),
        ('GOOGL', '2024-06-15'),
        ('MSFT', '2024-01-15'),
        ('MSFT', '2024-06-15'),
        ('TSLA', '2024-01-15'),
        ('TSLA', '2024-06-15'),
        ('NVDA', '2024-01-15'),
        ('NVDA', '2024-06-15'),
    ]
    
    hybrid_results = []
    pure_llm_results = []
    
    print("\n🧪 Running HYBRID (Rule-Based + LLM) Agent Tests...")
    print("-" * 70)
    for ticker, date in test_cases:
        result = evaluate_decision_accuracy(ticker, date, agent_type='hybrid')
        if result:
            hybrid_results.append(result)
            time.sleep(1)  # Rate limiting
    
    print("\n🧪 Running PURE LLM Agent Tests...")
    print("-" * 70)
    for ticker, date in test_cases:
        result = evaluate_decision_accuracy(ticker, date, agent_type='pure_llm')
        if result:
            pure_llm_results.append(result)
            time.sleep(1)  # Rate limiting
    
    # Calculate metrics
    print("\n" + "=" * 70)
    print("📊 RESULTS COMPARISON")
    print("=" * 70)
    
    # Hybrid metrics
    hybrid_accuracy = sum(r['correct'] for r in hybrid_results) / len(hybrid_results) * 100
    hybrid_avg_confidence = sum(r['confidence'] for r in hybrid_results) / len(hybrid_results)
    hybrid_rule_count = sum(1 for r in hybrid_results if r.get('decision_type') == 'rule-based')
    hybrid_avg_return = sum(r['actual_return'] for r in hybrid_results) / len(hybrid_results)
    
    # Pure LLM metrics
    llm_accuracy = sum(r['correct'] for r in pure_llm_results) / len(pure_llm_results) * 100
    llm_avg_confidence = sum(r['confidence'] for r in pure_llm_results) / len(pure_llm_results)
    llm_avg_return = sum(r['actual_return'] for r in pure_llm_results) / len(pure_llm_results)
    
    print(f"\n🎯 HYBRID AGENT (Rule-Based + LLM):")
    print(f"   • Accuracy: {hybrid_accuracy:.1f}%")
    print(f"   • Average Confidence: {hybrid_avg_confidence:.1f}")
    print(f"   • Rule-Based Decisions: {hybrid_rule_count}/{len(hybrid_results)} ({hybrid_rule_count/len(hybrid_results)*100:.1f}%)")
    print(f"   • Average Return (90-day): {hybrid_avg_return:.2f}%")
    print(f"   • Total Tests: {len(hybrid_results)}")
    
    print(f"\n🤖 PURE LLM AGENT:")
    print(f"   • Accuracy: {llm_accuracy:.1f}%")
    print(f"   • Average Confidence: {llm_avg_confidence:.1f}")
    print(f"   • Average Return (90-day): {llm_avg_return:.2f}%")
    print(f"   • Total Tests: {len(pure_llm_results)}")
    
    # Calculate improvement
    accuracy_improvement = hybrid_accuracy - llm_accuracy
    confidence_improvement = hybrid_avg_confidence - llm_avg_confidence
    return_improvement = hybrid_avg_return - llm_avg_return
    
    print(f"\n📈 IMPROVEMENT FROM RULE-BASED LOGIC:")
    print(f"   • Accuracy Gain: {accuracy_improvement:+.1f} percentage points")
    print(f"   • Confidence Gain: {confidence_improvement:+.1f} points")
    print(f"   • Return Improvement: {return_improvement:+.2f}%")
    
    improvement_score = (accuracy_improvement * 2) + (confidence_improvement * 0.5) + (return_improvement * 0.3)
    print(f"\n⭐ OVERALL IMPROVEMENT SCORE: {improvement_score:+.2f}")
    
    if accuracy_improvement > 0:
        print(f"\n✅ Rule-based logic IMPROVED decision accuracy by {accuracy_improvement:.1f}%")
    else:
        print(f"\n⚠️  Rule-based logic decreased accuracy by {abs(accuracy_improvement):.1f}%")
    
    print("\n" + "=" * 70)
    
    # Detailed breakdown
    print("\n📋 DETAILED BREAKDOWN:")
    print("-" * 70)
    print("HYBRID RESULTS:")
    for r in hybrid_results[:5]:  # Show first 5
        print(f"  {r['ticker']} ({r['test_date']}): {r['decision']} | "
              f"Type: {r['decision_type']} | Conf: {r['confidence']} | "
              f"Return: {r['actual_return']:+.2f}% | Correct: {'✓' if r['correct'] else '✗'}")
    
    return {
        'hybrid_accuracy': hybrid_accuracy,
        'llm_accuracy': llm_accuracy,
        'accuracy_improvement': accuracy_improvement,
        'improvement_score': improvement_score
    }


if __name__ == "__main__":
    print("\n🚀 Starting Decision Agent Evaluation...\n")
    print("This will take several minutes as we analyze historical data...")
    print("Testing decisions made 90 days ago and comparing to actual outcomes.\n")
    
    results = run_evaluation()
    
    print("\n✅ Evaluation Complete!")
    print(f"\n💡 Key Takeaway: Rule-based logic provides {results['accuracy_improvement']:+.1f}% accuracy improvement")
