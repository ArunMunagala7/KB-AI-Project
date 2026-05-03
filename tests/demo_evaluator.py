#!/usr/bin/env python3
"""
Live Demo: How the LLM Evaluator Works
Shows step-by-step evaluation of a real agent response
"""

from llm_evaluator import LLMEvaluator
from trend_agent import TrendAnalysisAgent

def demo_step_by_step():
    """
    Demonstrate how the evaluator works step-by-step with real data
    """
    print("\n" + "="*70)
    print("LIVE DEMO: LLM EVALUATOR IN ACTION")
    print("="*70)
    
    # Step 1: Get real agent response
    print("\n📍 STEP 1: Run Trend Agent on Real Stock (AAPL)")
    print("-" * 70)
    
    ticker = 'AAPL'
    trend_agent = TrendAnalysisAgent()
    result = trend_agent.run(ticker)
    
    print(f"✅ Agent completed analysis")
    print(f"\n📊 CALCULATED METRICS (Ground Truth):")
    print(f"   • SMA50:  ${result['sma50']:.2f}")
    print(f"   • SMA200: ${result['sma200']:.2f}")
    print(f"   • RSI:    {result['rsi']:.2f}")
    print(f"   • MACD:   {result['macd']:.4f}")
    print(f"   • Trend Score: {result['trend_score']:.2f}")
    
    print(f"\n💬 LLM GENERATED ANALYSIS:")
    print(f"   {'-' * 66}")
    analysis_preview = result['analysis'][:300] + "..." if len(result['analysis']) > 300 else result['analysis']
    for line in analysis_preview.split('\n'):
        if line.strip():
            print(f"   {line.strip()}")
    print(f"   {'-' * 66}")
    
    # Step 2: Evaluate factual accuracy
    print(f"\n\n📍 STEP 2: Check Factual Accuracy")
    print("-" * 70)
    print("Looking for hallucinations: Did LLM make up numbers?")
    
    evaluator = LLMEvaluator()
    
    ground_truth = {
        'sma50': result['sma50'],
        'sma200': result['sma200'],
        'rsi': result['rsi'],
        'macd': result['macd'],
        'trend_score': result['trend_score']
    }
    
    accuracy = evaluator.evaluate_factual_accuracy(result['analysis'], ground_truth)
    
    print(f"\n✅ Accuracy Score: {accuracy['accuracy_score']:.1f}/100")
    
    if accuracy['hallucinations']:
        print(f"⚠️  Found {len(accuracy['hallucinations'])} hallucination(s):")
        for h in accuracy['hallucinations']:
            print(f"   ❌ {h}")
    else:
        print(f"✅ No hallucinations detected - all numbers match!")
    
    if accuracy['nonsensical_guarantees']:
        print(f"⚠️  Found {len(accuracy['nonsensical_guarantees'])} nonsensical guarantee(s):")
        for g in accuracy['nonsensical_guarantees']:
            print(f"   ❌ {g}")
    
    # Step 3: Evaluate reasoning quality
    print(f"\n\n📍 STEP 3: Evaluate Reasoning Quality")
    print("-" * 70)
    print("Checking if explanation is relevant, deep, specific, and logical")
    
    input_metrics = ground_truth.copy()
    quality = evaluator.evaluate_reasoning_quality(result['analysis'], input_metrics)
    
    print(f"\n✅ Overall Quality: {quality['quality_score']:.1f}/100")
    print(f"\n   Breakdown:")
    print(f"   • Relevance:   {quality['relevance_score']:.1f}/100 - Did it reference the metrics?")
    print(f"     Referenced {quality['metrics_referenced']}/{len(input_metrics)} metrics: {quality['referenced_metrics']}")
    
    print(f"\n   • Depth:       {quality['depth_score']:.1f}/100 - Does it explain WHY?")
    if quality['depth_indicators']['causal_reasoning']:
        print(f"     ✅ Uses causal words: {quality['depth_indicators']['causal_reasoning'][:3]}")
    if quality['depth_indicators']['contrasts']:
        print(f"     ✅ Makes comparisons: {quality['depth_indicators']['contrasts'][:3]}")
    
    print(f"\n   • Specificity: {quality['specificity_score']:.1f}/100 - Data-driven vs vague?")
    if quality['vague_phrases']:
        print(f"     ⚠️  Contains vague phrases: {quality['vague_phrases'][:3]}")
    else:
        print(f"     ✅ No vague language detected")
    
    print(f"\n   • Logic:       {quality['logical_flow_score']:.1f}/100 - Any contradictions?")
    if quality['contradictions']:
        print(f"     ⚠️  Found contradictions: {quality['contradictions']}")
    else:
        print(f"     ✅ No contradictions detected")
    
    # Step 4: Evaluate cost efficiency
    print(f"\n\n📍 STEP 4: Calculate Cost Efficiency")
    print("-" * 70)
    print("Is the response worth the token cost?")
    
    # Estimate tokens (in real integration, you'd get this from the API)
    estimated_tokens = int(len(result['analysis'].split()) * 1.3)
    
    cost = evaluator.evaluate_cost_efficiency(result['analysis'], estimated_tokens)
    
    print(f"\n✅ Cost Score: {cost['cost_score']:.1f}/100")
    print(f"\n   Details:")
    print(f"   • Tokens Used: {cost['tokens_used']}")
    print(f"   • Estimated Cost: ${cost['cost_usd']:.6f}")
    print(f"   • Info Density: {cost['info_density']:.1%}")
    print(f"     (Unique words / Total words - higher is better)")
    
    # Step 5: Calculate overall score
    print(f"\n\n📍 STEP 5: Calculate Overall Score")
    print("-" * 70)
    print("Weighted average: 35% Accuracy + 35% Quality + 30% Cost")
    
    overall = (
        accuracy['accuracy_score'] * 0.35 +
        quality['quality_score'] * 0.35 +
        cost['cost_score'] * 0.30
    )
    
    print(f"\n   ({accuracy['accuracy_score']:.1f} × 0.35) + ({quality['quality_score']:.1f} × 0.35) + ({cost['cost_score']:.1f} × 0.30)")
    print(f"   = {accuracy['accuracy_score'] * 0.35:.1f} + {quality['quality_score'] * 0.35:.1f} + {cost['cost_score'] * 0.30:.1f}")
    print(f"   = {overall:.1f}/100")
    
    # Final verdict
    print(f"\n\n📊 FINAL VERDICT")
    print("="*70)
    
    bar_length = int(overall / 5)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    
    if overall >= 80:
        verdict = "🟢 EXCELLENT - Production ready!"
    elif overall >= 70:
        verdict = "🟡 GOOD - Minor improvements possible"
    elif overall >= 60:
        verdict = "🟠 FAIR - Needs attention"
    else:
        verdict = "🔴 POOR - Requires immediate fixes"
    
    print(f"\n   {bar}")
    print(f"\n   Overall Score: {overall:.1f}/100")
    print(f"   {verdict}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    if accuracy['accuracy_score'] < 80:
        print(f"   • Improve prompt to reduce hallucinations")
        print(f"   • Add explicit instructions: 'Use ONLY the provided metrics'")
    
    if quality['quality_score'] < 70:
        print(f"   • Enhance reasoning depth in prompt")
        print(f"   • Request: 'Explain causal relationships and provide comparisons'")
    
    if cost['cost_score'] < 70:
        print(f"   • Consider reducing max_tokens or using gpt-4o-mini")
        print(f"   • Current cost: ${cost['cost_usd']:.6f} per response")
    
    if overall >= 80:
        print(f"   ✅ Agent is performing excellently - no changes needed!")
    
    print(f"\n\n🎯 USE CASES:")
    print(f"   • Run this after every prompt change to measure improvement")
    print(f"   • Set up alerts if score drops below 70")
    print(f"   • Compare different models (gpt-4o vs gpt-4o-mini)")
    print(f"   • Track quality trends over time")
    print()

if __name__ == "__main__":
    demo_step_by_step()
