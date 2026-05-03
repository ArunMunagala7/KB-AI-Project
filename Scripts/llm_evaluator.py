#!/usr/bin/env python3
"""
LLM Response Evaluation Framework
Evaluates LLM outputs across 4 dimensions: Accuracy, Consistency, Quality, Cost

Created: April 2026
Purpose: Address hallucination issues discovered in production
         (e.g., LLM claiming SMA50=$200 when actual=$175.50)
         
Development notes:
- Started with just accuracy checking
- Added quality metrics after noticing vague language
- Consistency testing added when same stock gave different recommendations
- Cost tracking requested by team to monitor API spending
"""

import json
import time
import re
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
from typing import Dict, List, Tuple

class LLMEvaluator:
    """
    Comprehensive evaluation framework for LLM responses in financial analysis
    
    Evaluation Dimensions:
    1. Factual Accuracy (35%) - Are numerical claims correct?
    2. Reasoning Quality (35%) - Is explanation logical and relevant?
    3. Cost Efficiency (30%) - Token usage vs value added
    4. Consistency - Optional testing for output stability
    
    Usage:
        evaluator = LLMEvaluator()
        report = evaluator.evaluate_comprehensive(
            agent_name='Trend Agent',
            llm_response=result['analysis'],
            ground_truth={'sma50': 175.50, ...},
            input_metrics=ground_truth,
            tokens_used=150
        )
    """
    
    def __init__(self):
        self.evaluation_log = []
        self.metrics_history = defaultdict(list)
        
    # ========================================
    # DIMENSION 1: FACTUAL ACCURACY
    # Detects hallucinations and fabricated metrics
    # ========================================
    
    def evaluate_factual_accuracy(self, llm_response: str, ground_truth: Dict) -> Dict:
        """
        Verify numerical claims in LLM response against actual data
        
        Args:
            llm_response: Text from LLM (trend analysis, risk assessment, etc.)
            ground_truth: Dict with verified metrics (e.g., {'sma50': 150.25, 'rsi': 45.2})
        
        Returns:
            {
                'accuracy_score': 0-100,
                'verified_claims': count,
                'incorrect_claims': count,
                'hallucinations': list of false claims
            }
        """
        accuracy_score = 100
        verified_claims = 0
        incorrect_claims = 0
        hallucinations = []
        
        # Extract numerical claims from LLM response
        numerical_patterns = {
            'sma50': r'(?:SMA.?50|50.?day moving average)[^\d]*([\d.]+)',
            'sma200': r'(?:SMA.?200|200.?day moving average)[^\d]*([\d.]+)',
            'rsi': r'(?:RSI)[^\d]*([\d.]+)',
            'volatility': r'(?:volatility)[^\d]*([\d.]+)%?',
            'risk_score': r'(?:risk score)[^\d]*([\d.]+)',
        }
        
        for metric, pattern in numerical_patterns.items():
            match = re.search(pattern, llm_response, re.IGNORECASE)
            if match and metric in ground_truth:
                claimed_value = float(match.group(1))
                actual_value = float(ground_truth[metric])
                
                # Allow 5% tolerance for rounding
                if abs(claimed_value - actual_value) / max(actual_value, 0.01) < 0.05:
                    verified_claims += 1
                else:
                    incorrect_claims += 1
                    hallucinations.append({
                        'metric': metric,
                        'claimed': claimed_value,
                        'actual': actual_value,
                        'error_pct': abs(claimed_value - actual_value) / actual_value * 100
                    })
                    accuracy_score -= 20  # Penalize incorrect claims
        
        # Check for non-sensical claims
        nonsense_indicators = [
            r'guaranteed profit',
            r'100% certain',
            r'zero risk',
            r'impossible to lose',
        ]
        
        for pattern in nonsense_indicators:
            if re.search(pattern, llm_response, re.IGNORECASE):
                hallucinations.append({'type': 'nonsensical_guarantee', 'text': pattern})
                accuracy_score -= 15
        
        return {
            'accuracy_score': max(0, accuracy_score),
            'verified_claims': verified_claims,
            'incorrect_claims': incorrect_claims,
            'hallucinations': hallucinations,
            'evaluation_time': datetime.now().isoformat()
        }
    
    # ========================================
    # DIMENSION 2: CONSISTENCY
    # ========================================
    
    def evaluate_consistency(self, agent_fn, input_data: Dict, n_runs: int = 3) -> Dict:
        """
        Test if LLM produces consistent outputs for identical inputs
        
        Args:
            agent_fn: Function to call (e.g., trend_agent.run)
            input_data: Input parameters (e.g., {'ticker': 'AAPL'})
            n_runs: Number of times to run the same input
        
        Returns:
            {
                'consistency_score': 0-100,
                'variance': numerical variance in outputs,
                'decision_stability': % of identical decisions
            }
        """
        responses = []
        decisions = []
        start_time = time.time()
        
        for i in range(n_runs):
            try:
                result = agent_fn(**input_data)
                responses.append(result)
                
                # Extract decision if present
                if isinstance(result, dict) and 'decision' in result:
                    decisions.append(result['decision'])
                elif isinstance(result, dict) and 'analysis' in result:
                    decisions.append(result['analysis'][:100])  # First 100 chars
                    
            except Exception as e:
                print(f"[Error] Consistency test run {i+1} failed: {e}")
        
        elapsed = time.time() - start_time
        
        # Calculate consistency metrics
        if len(decisions) < 2:
            return {'consistency_score': 0, 'error': 'Insufficient runs'}
        
        # Decision stability: Are all decisions identical?
        unique_decisions = set(decisions)
        decision_stability = (decisions.count(decisions[0]) / len(decisions)) * 100
        
        # Text similarity (simple approach: word overlap)
        if all(isinstance(d, str) for d in decisions):
            words_sets = [set(d.lower().split()) for d in decisions]
            avg_overlap = np.mean([
                len(words_sets[i] & words_sets[j]) / len(words_sets[i] | words_sets[j])
                for i in range(len(words_sets))
                for j in range(i+1, len(words_sets))
            ]) if len(words_sets) > 1 else 1.0
            text_similarity = avg_overlap * 100
        else:
            text_similarity = 100 if len(unique_decisions) == 1 else 0
        
        consistency_score = (decision_stability * 0.7) + (text_similarity * 0.3)
        
        return {
            'consistency_score': round(consistency_score, 2),
            'decision_stability': round(decision_stability, 2),
            'text_similarity': round(text_similarity, 2),
            'unique_outputs': len(unique_decisions),
            'total_runs': n_runs,
            'avg_response_time': round(elapsed / n_runs, 3),
            'evaluation_time': datetime.now().isoformat()
        }
    
    # ========================================
    # DIMENSION 3: REASONING QUALITY
    # ========================================
    
    def evaluate_reasoning_quality(self, llm_response: str, input_metrics: Dict) -> Dict:
        """
        Assess the quality of LLM's reasoning and explanations
        
        Criteria:
        - Relevance: Does it reference provided metrics?
        - Logical Flow: Is reasoning coherent?
        - Depth: Are multiple factors considered?
        - Specificity: Are conclusions specific vs vague?
        
        Args:
            llm_response: Text explanation from LLM
            input_metrics: Metrics provided to LLM (to check if they're used)
        
        Returns:
            {
                'quality_score': 0-100,
                'relevance_score': 0-100,
                'depth_score': 0-100,
                'specificity_score': 0-100
            }
        """
        quality_score = 0
        
        # RELEVANCE: Does response reference input metrics?
        relevance_score = 0
        for metric_name, metric_value in input_metrics.items():
            if metric_name.lower() in llm_response.lower():
                relevance_score += 20
        relevance_score = min(100, relevance_score)
        
        # DEPTH: Are multiple aspects considered?
        depth_indicators = [
            r'however|although|while|despite',  # Contrasts
            r'because|since|due to|as a result',  # Causation
            r'first|second|additionally|furthermore',  # Multiple points
            r'trend|risk|forecast|volatility',  # Domain concepts
        ]
        depth_score = sum(20 for pattern in depth_indicators 
                         if re.search(pattern, llm_response, re.IGNORECASE))
        depth_score = min(100, depth_score)
        
        # SPECIFICITY: Specific vs vague language
        vague_terms = [
            r'\bmight\b|\bmay\b|\bcould\b|\bpossibly\b',
            r'\bsome\b|\bseveral\b|\bvarious\b',
            r'\bgenerally\b|\btypically\b|\busually\b'
        ]
        vague_count = sum(1 for pattern in vague_terms 
                         if re.search(pattern, llm_response, re.IGNORECASE))
        
        specific_terms = [
            r'\d+%',  # Percentages
            r'\$\d+',  # Dollar amounts
            r'specifically|exactly|precisely',
            r'strong|weak|high|low'  # Definitive adjectives
        ]
        specific_count = sum(1 for pattern in specific_terms 
                            if re.search(pattern, llm_response, re.IGNORECASE))
        
        specificity_score = max(0, min(100, (specific_count - vague_count) * 20 + 50))
        
        # LOGICAL FLOW: Check for contradictions
        contradiction_patterns = [
            (r'bullish', r'bearish'),
            (r'low risk', r'high risk'),
            (r'buy', r'sell'),
        ]
        contradictions = 0
        for pos, neg in contradiction_patterns:
            if re.search(pos, llm_response, re.IGNORECASE) and \
               re.search(neg, llm_response, re.IGNORECASE):
                # Check if they're in close proximity (likely contradiction)
                pos_match = re.search(pos, llm_response, re.IGNORECASE)
                neg_match = re.search(neg, llm_response, re.IGNORECASE)
                if abs(pos_match.start() - neg_match.start()) < 100:
                    contradictions += 1
        
        logical_flow_score = max(0, 100 - (contradictions * 30))
        
        # Overall quality score (weighted average)
        quality_score = (
            relevance_score * 0.30 +
            depth_score * 0.25 +
            specificity_score * 0.25 +
            logical_flow_score * 0.20
        )
        
        return {
            'quality_score': round(quality_score, 2),
            'relevance_score': round(relevance_score, 2),
            'depth_score': round(depth_score, 2),
            'specificity_score': round(specificity_score, 2),
            'logical_flow_score': round(logical_flow_score, 2),
            'vague_count': vague_count,
            'specific_count': specific_count,
            'contradictions': contradictions,
            'evaluation_time': datetime.now().isoformat()
        }
    
    # ========================================
    # DIMENSION 4: COST EFFICIENCY
    # ========================================
    
    def evaluate_cost_efficiency(self, llm_response: str, tokens_used: int, 
                                 model: str = "gpt-4o-mini") -> Dict:
        """
        Evaluate cost-effectiveness of LLM usage
        
        Args:
            llm_response: Generated text
            tokens_used: Total tokens (prompt + completion)
            model: Model name for pricing
        
        Returns:
            {
                'cost_score': 0-100 (higher = better value),
                'cost_usd': actual cost,
                'value_per_dollar': information density metric
            }
        """
        # Token pricing (as of 2024)
        pricing = {
            'gpt-4o-mini': {'input': 0.150 / 1_000_000, 'output': 0.600 / 1_000_000},
            'gpt-4o': {'input': 2.50 / 1_000_000, 'output': 10.00 / 1_000_000},
            'gpt-3.5-turbo': {'input': 0.50 / 1_000_000, 'output': 1.50 / 1_000_000}
        }
        
        # Estimate 60/40 split for input/output
        input_tokens = int(tokens_used * 0.6)
        output_tokens = int(tokens_used * 0.4)
        
        model_pricing = pricing.get(model, pricing['gpt-4o-mini'])
        cost_usd = (input_tokens * model_pricing['input']) + (output_tokens * model_pricing['output'])
        
        # Calculate information density (unique words / total words)
        words = llm_response.split()
        unique_words = set(words)
        info_density = len(unique_words) / max(len(words), 1)
        
        # Value score: Information density vs cost
        # Target: <$0.01 per response with >0.7 density = excellent
        value_per_dollar = info_density / max(cost_usd * 100, 0.001)  # Scale for readability
        
        cost_score = min(100, value_per_dollar * 10)
        
        return {
            'cost_score': round(cost_score, 2),
            'cost_usd': round(cost_usd, 6),
            'tokens_used': tokens_used,
            'info_density': round(info_density, 3),
            'value_per_dollar': round(value_per_dollar, 2),
            'model': model,
            'evaluation_time': datetime.now().isoformat()
        }
    
    # ========================================
    # COMPREHENSIVE EVALUATION
    # ========================================
    
    def evaluate_comprehensive(self, agent_name: str, llm_response: str, 
                              ground_truth: Dict, input_metrics: Dict,
                              tokens_used: int = None) -> Dict:
        """
        Run all 4 evaluation dimensions and generate a comprehensive report
        
        Args:
            agent_name: Name of agent being evaluated (trend/risk/forecast/decision)
            llm_response: LLM generated text
            ground_truth: Verified metrics for accuracy check
            input_metrics: Metrics provided to LLM
            tokens_used: Token count (estimated if None)
        
        Returns:
            Complete evaluation report with overall score
        """
        print(f"\n{'='*70}")
        print(f"EVALUATING: {agent_name.upper()}")
        print(f"{'='*70}\n")
        
        # Estimate tokens if not provided
        if tokens_used is None:
            tokens_used = len(llm_response.split()) * 1.3  # Rough estimate
        
        # Run all evaluations
        accuracy = self.evaluate_factual_accuracy(llm_response, ground_truth)
        quality = self.evaluate_reasoning_quality(llm_response, input_metrics)
        cost = self.evaluate_cost_efficiency(llm_response, tokens_used)
        
        # Calculate overall score (weighted average)
        overall_score = (
            accuracy['accuracy_score'] * 0.35 +  # Accuracy most important
            quality['quality_score'] * 0.35 +    # Quality second
            cost['cost_score'] * 0.30            # Cost efficiency third
        )
        
        report = {
            'agent': agent_name,
            'timestamp': datetime.now().isoformat(),
            'overall_score': round(overall_score, 2),
            'dimensions': {
                'accuracy': accuracy,
                'quality': quality,
                'cost_efficiency': cost
            },
            'llm_response_preview': llm_response[:200] + '...' if len(llm_response) > 200 else llm_response
        }
        
        # Store in history
        self.evaluation_log.append(report)
        self.metrics_history[agent_name].append(overall_score)
        
        # Print summary
        print(f"📊 EVALUATION RESULTS:")
        print(f"   Overall Score: {report['overall_score']:.1f}/100")
        print(f"   ├─ Accuracy:   {accuracy['accuracy_score']:.1f}/100")
        print(f"   ├─ Quality:    {quality['quality_score']:.1f}/100")
        print(f"   └─ Cost Eff:   {cost['cost_score']:.1f}/100")
        print()
        
        if accuracy['hallucinations']:
            print(f"⚠️  WARNING: {len(accuracy['hallucinations'])} hallucination(s) detected")
            for h in accuracy['hallucinations'][:3]:  # Show first 3
                print(f"   - {h}")
            print()
        
        return report
    
    # ========================================
    # REPORTING & ANALYTICS
    # ========================================
    
    def generate_summary_report(self) -> Dict:
        """Generate summary statistics across all evaluations"""
        if not self.evaluation_log:
            return {'error': 'No evaluations performed yet'}
        
        summary = {
            'total_evaluations': len(self.evaluation_log),
            'agents_evaluated': list(self.metrics_history.keys()),
            'average_scores': {},
            'best_performing_agent': None,
            'worst_performing_agent': None,
            'improvement_trends': {}
        }
        
        # Calculate averages per agent
        for agent, scores in self.metrics_history.items():
            avg_score = np.mean(scores)
            summary['average_scores'][agent] = round(avg_score, 2)
        
        if summary['average_scores']:
            summary['best_performing_agent'] = max(summary['average_scores'], 
                                                   key=summary['average_scores'].get)
            summary['worst_performing_agent'] = min(summary['average_scores'], 
                                                    key=summary['average_scores'].get)
        
        # Check for improvement trends
        for agent, scores in self.metrics_history.items():
            if len(scores) >= 2:
                recent_avg = np.mean(scores[-3:]) if len(scores) >= 3 else scores[-1]
                early_avg = np.mean(scores[:3]) if len(scores) >= 3 else scores[0]
                trend = recent_avg - early_avg
                summary['improvement_trends'][agent] = round(trend, 2)
        
        return summary
    
    def save_report(self, filepath: str):
        """Save evaluation log to JSON file"""
        with open(filepath, 'w') as f:
            json.dump({
                'evaluation_log': self.evaluation_log,
                'summary': self.generate_summary_report()
            }, f, indent=2)
        print(f"✅ Evaluation report saved to: {filepath}")


# ========================================
# EXAMPLE USAGE
# ========================================

if __name__ == "__main__":
    evaluator = LLMEvaluator()
    
    # Example 1: Evaluate Trend Agent LLM Response
    trend_llm_response = """
    Based on the technical indicators, AAPL shows a strong bullish trend. 
    The 50-day SMA at $150.25 is above the 200-day SMA at $145.80, indicating a golden cross. 
    RSI at 65 suggests moderate momentum without being overbought. 
    MACD at 2.5 is positive and above the signal line, confirming upward momentum.
    """
    
    trend_ground_truth = {
        'sma50': 150.25,
        'sma200': 145.80,
        'rsi': 65.2,
        'macd': 2.48
    }
    
    trend_input_metrics = {
        'trend_score': 2,
        'sma50': 150.25,
        'sma200': 145.80
    }
    
    report1 = evaluator.evaluate_comprehensive(
        agent_name='Trend Agent',
        llm_response=trend_llm_response,
        ground_truth=trend_ground_truth,
        input_metrics=trend_input_metrics,
        tokens_used=150
    )
    
    # Example 2: Test with a poor quality response (hallucinations)
    bad_response = """
    AAPL is guaranteed to reach $500 by next week with 100% certainty.
    The SMA50 is at $200 (actual: $150), showing massive growth potential.
    Zero risk involved - impossible to lose money on this trade.
    """
    
    report2 = evaluator.evaluate_comprehensive(
        agent_name='Bad Example',
        llm_response=bad_response,
        ground_truth=trend_ground_truth,
        input_metrics=trend_input_metrics,
        tokens_used=100
    )
    
    # Generate summary
    print("\n" + "="*70)
    print("SUMMARY REPORT")
    print("="*70)
    summary = evaluator.generate_summary_report()
    print(json.dumps(summary, indent=2))
    
    # Save to file
    evaluator.save_report('llm_evaluation_report.json')
