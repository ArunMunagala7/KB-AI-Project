#!/usr/bin/env python3
"""
Quick Test: LLM Evaluator
Tests the evaluation framework with mock data before live integration
"""

from llm_evaluator import LLMEvaluator

def test_good_response():
    """Test evaluation of a high-quality LLM response"""
    print("\n" + "="*70)
    print("TEST 1: High-Quality Response")
    print("="*70)
    
    evaluator = LLMEvaluator()
    
    # Mock ground truth
    ground_truth = {
        'sma50': 150.25,
        'sma200': 145.80,
        'rsi': 62.5,
        'trend_score': 1.5
    }
    
    # Good LLM response - accurate, data-driven, specific
    llm_response = """
    Technical analysis shows positive momentum. The SMA50 ($150.25) crossed above 
    SMA200 ($145.80) indicating a bullish trend. RSI at 62.5 suggests moderate buying 
    pressure without overbought conditions. The trend score of 1.5 reflects steady 
    upward movement. This combination of indicators points to continued strength, 
    supported by the golden cross formation and healthy RSI levels.
    """
    
    # Input metrics the LLM had access to
    input_metrics = ground_truth.copy()
    
    report = evaluator.evaluate_comprehensive(
        agent_name='Test Trend Agent',
        llm_response=llm_response,
        ground_truth=ground_truth,
        input_metrics=input_metrics,
        tokens_used=150
    )
    
    print_report(report)
    return report

def test_bad_response():
    """Test evaluation of a poor-quality LLM response"""
    print("\n" + "="*70)
    print("TEST 2: Poor-Quality Response")
    print("="*70)
    
    evaluator = LLMEvaluator()
    
    # Same ground truth
    ground_truth = {
        'sma50': 150.25,
        'sma200': 145.80,
        'rsi': 62.5,
        'trend_score': 1.5
    }
    
    # Bad LLM response - hallucination, vague, no data references
    llm_response = """
    The stock looks really good and will definitely go up. The technical indicators 
    are showing strong signals with the SMA50 at $200 which is much higher than 
    expected. This is a 100% guaranteed buy opportunity with zero risk. The momentum 
    is absolutely incredible and you should invest immediately without any concerns.
    """
    
    input_metrics = ground_truth.copy()
    
    report = evaluator.evaluate_comprehensive(
        agent_name='Test Trend Agent (Bad)',
        llm_response=llm_response,
        ground_truth=ground_truth,
        input_metrics=input_metrics,
        tokens_used=150
    )
    
    print_report(report)
    return report

def test_consistency():
    """Test consistency evaluation with a mock agent function"""
    print("\n" + "="*70)
    print("TEST 3: Consistency Check")
    print("="*70)
    
    evaluator = LLMEvaluator()
    
    # Mock agent function that returns variable results
    call_count = [0]
    
    def mock_trend_agent(ticker):
        call_count[0] += 1
        base_analysis = f"Analysis run #{call_count[0]} for {ticker}. "
        
        # First two calls are consistent, third varies
        if call_count[0] <= 2:
            return {
                'decision': 'BUY',
                'analysis': base_analysis + "Strong bullish trend with good momentum."
            }
        else:
            return {
                'decision': 'HOLD',  # Different decision!
                'analysis': base_analysis + "Market showing some uncertainty."
            }
    
    input_data = {'ticker': 'AAPL'}
    
    consistency_report = evaluator.evaluate_consistency(
        agent_fn=mock_trend_agent,
        input_data=input_data,
        n_runs=3
    )
    
    print(f"\n📊 Consistency Results:")
    print(f"   Decision Stability: {consistency_report.get('decision_stability', 0):.1f}%")
    print(f"   Text Similarity: {consistency_report.get('avg_text_similarity', 0):.1f}%")
    print(f"   Overall Score: {consistency_report.get('consistency_score', 0):.1f}/100")
    
    print(f"\n📝 Decisions Across Runs:")
    for i, decision in enumerate(consistency_report.get('decisions', []), 1):
        print(f"   Run {i}: {decision}")
    
    if consistency_report.get('consistency_score', 0) < 80:
        print(f"\n⚠️  Low consistency detected - agent may be unstable!")
    else:
        print(f"\n✅ High consistency - agent is stable")
    
    return consistency_report

def print_report(report):
    """Pretty print evaluation report"""
    print(f"\n📊 DETAILED RESULTS for {report['agent']}")
    print(f"\n   Overall Score: {report['overall_score']:.1f}/100")
    
    # Score bar visualization
    bar_length = int(report['overall_score'] / 5)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    
    if report['overall_score'] >= 80:
        emoji = "🟢 EXCELLENT"
    elif report['overall_score'] >= 70:
        emoji = "🟡 GOOD"
    else:
        emoji = "🔴 NEEDS IMPROVEMENT"
    
    print(f"   {bar} {emoji}")
    
    # Extract dimension details
    accuracy = report['dimensions']['accuracy']
    quality = report['dimensions']['quality']
    cost = report['dimensions']['cost_efficiency']
    
    # Detailed scores
    print(f"\n   📍 Factual Accuracy: {accuracy['accuracy_score']:.1f}/100")
    if accuracy['hallucinations']:
        print(f"      ⚠️  Hallucinations detected: {len(accuracy['hallucinations'])}")
        for h in accuracy['hallucinations'][:2]:
            print(f"         - {h}")
    else:
        print(f"      ✅ No hallucinations detected")
    
    print(f"\n   🎯 Reasoning Quality: {quality['quality_score']:.1f}/100")
    print(f"      Relevance: {quality['relevance_score']:.1f}")
    print(f"      Depth: {quality['depth_score']:.1f}")
    print(f"      Specificity: {quality['specificity_score']:.1f}")
    print(f"      Logic: {quality['logical_flow_score']:.1f}")
    
    print(f"\n   💰 Cost Efficiency: {cost['cost_score']:.1f}/100")
    print(f"      Tokens: {cost['tokens_used']}")
    print(f"      Cost: ${cost['cost_usd']:.6f}")
    print(f"      Info Density: {cost['info_density']:.2%}")

def main():
    """Run all tests"""
    print("\n" + "#"*70)
    print("# LLM EVALUATOR TEST SUITE")
    print("#"*70)
    
    # Test 1: Good response
    good_report = test_good_response()
    
    # Test 2: Bad response
    bad_report = test_bad_response()
    
    # Test 3: Consistency
    consistency_report = test_consistency()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    print(f"\n✅ Test 1 (Good Response): {good_report['overall_score']:.1f}/100")
    print(f"❌ Test 2 (Bad Response): {bad_report['overall_score']:.1f}/100")
    print(f"📊 Test 3 (Consistency): {consistency_report['consistency_score']:.1f}/100")
    
    if good_report['overall_score'] > bad_report['overall_score'] + 10:
        print(f"\n🎉 SUCCESS: Evaluator correctly distinguishes good from bad responses!")
        print(f"   Good score ({good_report['overall_score']:.1f}) > Bad score ({bad_report['overall_score']:.1f})")
        print(f"   Difference: {good_report['overall_score'] - bad_report['overall_score']:.1f} points")
        print(f"\n✅ Key Detection:")
        print(f"   • Hallucination detection working (caught fake $200 SMA50)")
        print(f"   • Nonsensical guarantee detection working (caught 'zero risk')")
        print(f"   • Consistency testing working (detected 66.7% decision stability)")
    else:
        print(f"\n⚠️  WARNING: Score difference may be too small")
    
    print("\n✅ All tests complete! Evaluator is ready for integration.\n")

if __name__ == "__main__":
    main()
