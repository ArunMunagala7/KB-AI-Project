import openai
import os
import json

class DecisionAgent:
    def __init__(self):
        openai.api_key = os.getenv("MISTAL_API_KEY")
        openai.api_base = os.getenv("MISTRAL_API_BASE")

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

        # ========================================
        # RULE-BASED DECISION LOGIC (Priority 1-2)
        # These hard rules override LLM in safety-critical cases
        # ========================================
        
        # P1: Critical Risk Override - SELL
        if risk_score >= 8:
            return {
                'ticker': ticker,
                'trend_score': trend_score,
                'risk_score': risk_score,
                'llm_risk_score': llm_risk_score,
                'forecast_direction': forecast_trend,
                'forecast_percent_change': forecast_change,
                'decision': 'SELL',
                'reasoning': f'RULE-BASED OVERRIDE: Critical risk level detected (risk_score={risk_score}). Immediate sell recommended for capital preservation.',
                'confidence_score': 95,
                'decision_type': 'rule-based'
            }
        
        # P2: Strong Buy Signal - All indicators aligned
        if trend_score >= 2 and risk_score <= 3 and forecast_trend == 'up' and forecast_change != 'N/A':
            try:
                if float(forecast_change) > 5:
                    return {
                        'ticker': ticker,
                        'trend_score': trend_score,
                        'risk_score': risk_score,
                        'llm_risk_score': llm_risk_score,
                        'forecast_direction': forecast_trend,
                        'forecast_percent_change': forecast_change,
                        'decision': 'BUY',
                        'reasoning': f'RULE-BASED OVERRIDE: Strong buy signal detected (trend={trend_score}, risk={risk_score}, forecast=+{forecast_change}%). All indicators aligned positively.',
                        'confidence_score': 90,
                        'decision_type': 'rule-based'
                    }
            except (ValueError, TypeError):
                pass  # Fall through to LLM decision
        
        # P3: Strong Sell Signal - Negative trend + high risk
        if trend_score <= -2 and risk_score >= 6:
            return {
                'ticker': ticker,
                'trend_score': trend_score,
                'risk_score': risk_score,
                'llm_risk_score': llm_risk_score,
                'forecast_direction': forecast_trend,
                'forecast_percent_change': forecast_change,
                'decision': 'SELL',
                'reasoning': f'RULE-BASED OVERRIDE: Negative trend (score={trend_score}) combined with elevated risk (score={risk_score}). Exit position recommended.',
                'confidence_score': 85,
                'decision_type': 'rule-based'
            }
        
        # P4: Conservative Hold - Mixed signals with moderate risk
        if abs(trend_score) <= 1 and 4 <= risk_score <= 6:
            return {
                'ticker': ticker,
                'trend_score': trend_score,
                'risk_score': risk_score,
                'llm_risk_score': llm_risk_score,
                'forecast_direction': forecast_trend,
                'forecast_percent_change': forecast_change,
                'decision': 'HOLD',
                'reasoning': f'RULE-BASED OVERRIDE: Neutral trend (score={trend_score}) with moderate risk (score={risk_score}). Wait for clearer signals before acting.',
                'confidence_score': 75,
                'decision_type': 'rule-based'
            }
        
        # ========================================
        # LLM-BASED DECISION (Priority 5-6)
        # For ambiguous cases where context matters
        # ========================================

        prompt = (
            f"You are an expert financial portfolio advisor tasked with making investment decisions for clients based on multi-agent analysis.\n"
            f"Below is the detailed information about the stock {ticker}. Your task is to analyze this information and return a JSON object with three keys:\n"
            f" - decision: One of the following strings - BUY, SELL, or HOLD.\n"
            f" - reasoning: A one or two sentence explanation justifying the decision.\n"
            f" - confidence_score: An integer between 0-100 representing confidence in this decision.\n\n"

            f"--- ANALYSIS INPUT ---\n"
            f"Trend Score (higher means stronger positive trend): {trend_score}\n"
            f"Risk Score (higher means more risk): {risk_score}\n"
            f"LLM Risk Score (LLM-inferred risk level): {llm_risk_score}\n"
            f"News Headlines: {headlines}\n"
            f"LLM Risk Analysis Summary: {analysis}\n"
            f"Forecast Initial Price: {forecast_initial}\n"
            f"Forecast Final Price: {forecast_final}\n"
            f"Forecast Direction: {forecast_trend}\n"
            f"Forecast Percent Change: {forecast_change}%\n"
            f"------------------------\n\n"

            f"This is an ambiguous case where rule-based logic didn't trigger. Use your judgment to weigh the conflicting signals.\n"
            f"Based on the above data, respond with a JSON object with the keys 'decision', 'reasoning', and 'confidence_score'."
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
            print(content)
            try:
                parsed_json_str = content.strip('```json').strip('```').strip()
                parsed = json.loads(parsed_json_str)
                decision = parsed.get("decision", "").upper()
                reasoning = parsed.get("reasoning", "")
                confidence_score = parsed.get("confidence_score", 70)
            except Exception as parse_error:
                print(f"[Error] Failed to parse decision response JSON for {ticker}: {parse_error}")
                decision = None
                reasoning = ""
                confidence_score = 0
        except Exception as e:
            print(f"[Error] OpenAI decision making failed for {ticker}: {e}")
            decision = None
            reasoning = ""
            confidence_score = 0

        return {
            'ticker': ticker,
            'trend_score': trend_score,
            'risk_score': risk_score,
            'llm_risk_score': llm_risk_score,
            'forecast_direction': forecast_trend,
            'forecast_percent_change': forecast_change,
            'decision': decision,
            'reasoning': reasoning,
            'confidence_score': confidence_score,
            'decision_type': 'llm-based'
        }