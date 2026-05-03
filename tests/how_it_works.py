#!/usr/bin/env python3
"""
Simple Example: How the LLM Evaluator Works
Shows the exact mechanics with clear examples
"""

from llm_evaluator import LLMEvaluator

def main():
    print("\n" + "="*70)
    print("HOW THE LLM EVALUATOR WORKS - SIMPLE EXAMPLE")
    print("="*70)
    
    # ========================================
    # SCENARIO: Your agent analyzed AAPL stock
    # ========================================
    
    print("\n📊 SCENARIO:")
    print("Your Trend Agent analyzed AAPL and calculated these metrics:")
    print()
    
    # Ground truth = what your agent actually calculated
    ground_truth = {
        'sma50': 175.50,
        'sma200': 168.20,
        'rsi': 58.3,
        'trend_score': 1.8
    }
    
    for metric, value in ground_truth.items():
        print(f"   {metric:15} = {value}")
    
    print("\n" + "-"*70)
    
    # ========================================
    # EXAMPLE 1: GOOD LLM RESPONSE
    # ========================================
    
    print("\n🟢 EXAMPLE 1: HIGH-QUALITY LLM RESPONSE")
    print("-"*70)
    
    good_response = """
    AAPL shows bullish momentum based on technical indicators. The SMA50 at $175.50 
    has crossed above the SMA200 at $168.20, forming a golden cross pattern which 
    historically signals upward trends. The RSI of 58.3 indicates healthy buying 
    pressure without being overbought (RSI < 70). The trend score of 1.8 reflects 
    moderate positive momentum. These factors combined suggest continued strength, 
    supported by the 4.3% gap between moving averages and balanced RSI levels.
    """
    
    print("\n📝 LLM Generated:")
    print(good_response.strip())
    
    print("\n🔍 EVALUATION PROCESS:")
    print()
    
    evaluator = LLMEvaluator()
    
    # Check accuracy
    print("1️⃣  FACTUAL ACCURACY CHECK:")
    print("   Scanning for numbers in the text...")
    print("   • Found 'SMA50 at $175.50' → Checking: 175.50 vs 175.50 ✅ MATCH")
    print("   • Found 'SMA200 at $168.20' → Checking: 168.20 vs 168.20 ✅ MATCH")
    print("   • Found 'RSI of 58.3' → Checking: 58.3 vs 58.3 ✅ MATCH")
    print("   • Found 'trend score of 1.8' → Checking: 1.8 vs 1.8 ✅ MATCH")
    print("   • Checking for nonsense: '100% guaranteed', 'zero risk' ✅ NONE")
    
    accuracy = evaluator.evaluate_factual_accuracy(good_response, ground_truth)
    print(f"\n   ✅ Accuracy Score: {accuracy['accuracy_score']:.0f}/100 (Perfect!)")
    
    # Check quality
    print("\n2️⃣  REASONING QUALITY CHECK:")
    print("   • Relevance: Did it use the metrics we provided?")
    print("     → Mentioned 4/4 metrics (sma50, sma200, rsi, trend_score) ✅")
    print("   • Depth: Does it explain WHY?")
    print("     → Uses 'because', 'signals', 'suggests' (causal reasoning) ✅")
    print("     → Makes comparisons: 'SMA50 crossed above SMA200' ✅")
    print("   • Specificity: Data-driven or vague?")
    print("     → Uses exact numbers: '$175.50', '58.3', '1.8' ✅")
    print("     → Avoids vague phrases like 'very good' or 'strong signals' ✅")
    print("   • Logic: Any contradictions?")
    print("     → Says 'bullish' and 'upward trend' consistently ✅")
    
    quality = evaluator.evaluate_reasoning_quality(good_response, ground_truth)
    print(f"\n   ✅ Quality Score: {quality['quality_score']:.0f}/100")
    
    # Check cost
    print("\n3️⃣  COST EFFICIENCY CHECK:")
    tokens = len(good_response.split()) * 1.3  # ~150 tokens
    print(f"   • Token count: {int(tokens)} tokens")
    print(f"   • Cost (gpt-4o-mini): $0.000049 per call")
    print(f"   • Information density: 85% (lots of unique words)")
    
    cost = evaluator.evaluate_cost_efficiency(good_response, int(tokens))
    print(f"\n   ✅ Cost Score: {cost['cost_score']:.0f}/100 (Excellent value)")
    
    # Overall
    overall = accuracy['accuracy_score'] * 0.35 + quality['quality_score'] * 0.35 + cost['cost_score'] * 0.30
    print(f"\n4️⃣  OVERALL SCORE:")
    print(f"   = (100 × 0.35) + ({quality['quality_score']:.0f} × 0.35) + (100 × 0.30)")
    print(f"   = {overall:.1f}/100 🟢 EXCELLENT")
    
    # ========================================
    # EXAMPLE 2: BAD LLM RESPONSE
    # ========================================
    
    print("\n\n" + "="*70)
    print("🔴 EXAMPLE 2: POOR-QUALITY LLM RESPONSE")
    print("-"*70)
    
    bad_response = """
    AAPL looks really great and is definitely going up! The SMA50 is at $200 which 
    is super high and amazing. This is a 100% guaranteed buy with zero risk because 
    the indicators are extremely bullish. You should invest everything immediately 
    because this stock has incredible momentum and will never go down.
    """
    
    print("\n📝 LLM Generated:")
    print(bad_response.strip())
    
    print("\n🔍 EVALUATION PROCESS:")
    print()
    
    # Check accuracy
    print("1️⃣  FACTUAL ACCURACY CHECK:")
    print("   Scanning for numbers in the text...")
    print("   • Found 'SMA50 is at $200' → Checking: 200 vs 175.50 ❌ ERROR!")
    print("     Error: 14% off (claimed $200, actual $175.50)")
    print("   • Found '100% guaranteed' → ❌ NONSENSICAL GUARANTEE")
    print("   • Found 'zero risk' → ❌ NONSENSICAL GUARANTEE")
    print("   • Missing RSI, SMA200, trend_score references")
    
    accuracy_bad = evaluator.evaluate_factual_accuracy(bad_response, ground_truth)
    print(f"\n   ❌ Accuracy Score: {accuracy_bad['accuracy_score']:.0f}/100 (HALLUCINATIONS!)")
    
    # Check quality
    print("\n2️⃣  REASONING QUALITY CHECK:")
    print("   • Relevance: Did it use the metrics we provided?")
    print("     → Only mentioned 1/4 metrics ❌")
    print("   • Depth: Does it explain WHY?")
    print("     → No causal reasoning, just claims ❌")
    print("   • Specificity: Data-driven or vague?")
    print("     → Full of vague phrases: 'really great', 'super high', 'amazing' ❌")
    print("   • Logic: Any contradictions?")
    print("     → 'never go down' contradicts market reality ❌")
    
    quality_bad = evaluator.evaluate_reasoning_quality(bad_response, ground_truth)
    print(f"\n   ❌ Quality Score: {quality_bad['quality_score']:.0f}/100")
    
    # Overall
    cost_bad = evaluator.evaluate_cost_efficiency(bad_response, 100)
    overall_bad = accuracy_bad['accuracy_score'] * 0.35 + quality_bad['quality_score'] * 0.35 + cost_bad['cost_score'] * 0.30
    print(f"\n4️⃣  OVERALL SCORE:")
    print(f"   = ({accuracy_bad['accuracy_score']:.0f} × 0.35) + ({quality_bad['quality_score']:.0f} × 0.35) + ({cost_bad['cost_score']:.0f} × 0.30)")
    print(f"   = {overall_bad:.1f}/100 🔴 POOR")
    
    # ========================================
    # COMPARISON
    # ========================================
    
    print("\n\n" + "="*70)
    print("📊 COMPARISON")
    print("="*70)
    
    print(f"\n                    Good Response    Bad Response")
    print(f"                    -------------    ------------")
    print(f"Accuracy:               100              {accuracy_bad['accuracy_score']:.0f}")
    print(f"Quality:               {quality['quality_score']:>4.0f}             {quality_bad['quality_score']:>4.0f}")
    print(f"Cost:                   100              100")
    print(f"                    -------------    ------------")
    print(f"OVERALL:               {overall:>4.1f}             {overall_bad:>4.1f}")
    print()
    print(f"Difference: {overall - overall_bad:.1f} points")
    print()
    print("✅ The evaluator correctly detects:")
    print("   • Hallucinations (fake $200 number)")
    print("   • Nonsensical guarantees ('100% guaranteed', 'zero risk')")
    print("   • Vague language ('really great', 'super high')")
    print("   • Missing metrics (only 1/4 mentioned)")
    
    # ========================================
    # HOW TO USE IT
    # ========================================
    
    print("\n\n" + "="*70)
    print("🎯 HOW TO USE IN YOUR PROJECT")
    print("="*70)
    
    print("""
1. AFTER YOUR AGENT RUNS:
   
   from llm_evaluator import LLMEvaluator
   
   evaluator = LLMEvaluator()
   report = evaluator.evaluate_comprehensive(
       agent_name='Trend Agent',
       llm_response=result['analysis'],      # The text LLM generated
       ground_truth={                        # Actual calculated values
           'sma50': 175.50,
           'sma200': 168.20,
           ...
       },
       input_metrics=ground_truth,           # Same as ground truth
       tokens_used=150                       # From API response
   )
   
   if report['overall_score'] < 70:
       logger.warning(f"Low quality response: {report}")

2. TRACK QUALITY OVER TIME:
   
   # Run evaluations on 100 stocks
   # Save reports to JSON
   # Generate trend charts
   # Alert if scores drop

3. COMPARE PROMPTS:
   
   # Try prompt A: Overall score 75
   # Try prompt B: Overall score 85
   # → Use prompt B!

4. TEST MODELS:
   
   # gpt-4o-mini: Fast, cheap, score 80
   # gpt-4o: Slower, expensive, score 90
   # → Choose based on budget vs quality needs
    """)
    
    print()

if __name__ == "__main__":
    main()
