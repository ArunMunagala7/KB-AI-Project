from flask import Flask, request, jsonify
from flask_cors import CORS
from decision_agent import DecisionAgent
from trend_agent import TrendAnalysisAgent
from risk_assesment import RiskAssessmentAgent
from forecast_agent import ForecastingAgent
import pandas as pd
import psycopg2
import os
import yfinance as yf
from flask import Response
from concurrent.futures import ThreadPoolExecutor
import time
app = Flask(__name__)
CORS(app)

decision_agent = DecisionAgent()
trend_agent = TrendAnalysisAgent()
risk_agent = RiskAssessmentAgent()
forecast_agent = ForecastingAgent()

def json_safe(obj):
    if isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    return obj

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    # Try to load custom portfolio from file first
    portfolio_file = os.path.join(os.path.dirname(__file__), 'custom_portfolio.json')
    if os.path.exists(portfolio_file):
        try:
            import json
            with open(portfolio_file, 'r') as f:
                mock_portfolio = json.load(f)
        except Exception as e:
            print(f"[Error] Failed to load custom portfolio: {e}")
            # Fall back to default
            mock_portfolio = [
                {"ticker": "AAPL", "qty": 10, "avgPrice": 150.00},
                {"ticker": "GOOGL", "qty": 5, "avgPrice": 2800.00},
                {"ticker": "MSFT", "qty": 8, "avgPrice": 300.00},
            ]
    else:
        # Default portfolio if no custom file exists
        # TO ADD YOUR OWN STOCKS: Add entries below with format:
        # {"ticker": "STOCK_SYMBOL", "qty": NUMBER_OF_SHARES, "avgPrice": YOUR_PURCHASE_PRICE}
        mock_portfolio = [
            {"ticker": "AAPL", "qty": 10, "avgPrice": 150.00},
            {"ticker": "GOOGL", "qty": 5, "avgPrice": 2800.00},
            {"ticker": "MSFT", "qty": 8, "avgPrice": 300.00},
            # ADD YOUR STOCKS HERE - Examples:
            # {"ticker": "TSLA", "qty": 15, "avgPrice": 250.00},
            # {"ticker": "NVDA", "qty": 20, "avgPrice": 400.00},
            # {"ticker": "AMZN", "qty": 12, "avgPrice": 180.00},
        ]
    
    try:
        # Try PostgreSQL if configured
        if os.getenv("DB_NAME") and os.getenv("DB_USER"):
            try:
                conn = psycopg2.connect(
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASS"),
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT")
                )
                cur = conn.cursor()
                cur.execute("SELECT * FROM portfolio")
                rows = cur.fetchall()
                cur.close()
                conn.close()
                
                portfolio = []
                for row in rows:
                    ticker = row[0]
                    quantity = row[1]
                    average_price = float(row[2])
                    try:
                        info = yf.Ticker(ticker).info
                        price = float(info.get('currentPrice', info.get('regularMarketPrice')))
                        name = info.get("shortName", ticker)
                    except Exception as e:
                        price = None
                        name = ticker
                    portfolio.append({
                        "ticker": ticker,
                        "name": name,
                        "qty": quantity,
                        "avgPrice": average_price,
                        "currentPrice": price,
                        "dayChange": info.get("regularMarketChangePercent"),
                        "high52W": info.get("fiftyTwoWeekHigh"),
                        "low52W": info.get("fiftyTwoWeekLow")
                    })
                return jsonify({"portfolio": portfolio})
            except:
                # Fall back to mock data if DB fails
                pass
        
        # Use mock portfolio if no DB or DB fails
        portfolio = []
        for item in mock_portfolio:
            ticker = item["ticker"]
            try:
                info = yf.Ticker(ticker).info
                price = float(info.get('currentPrice', info.get('regularMarketPrice', 0)))
                name = info.get("shortName", ticker)
            except Exception as e:
                price = item["avgPrice"]
                name = ticker
            portfolio.append({
                "ticker": ticker,
                "name": name,
                "qty": item["qty"],
                "avgPrice": item["avgPrice"],
                "currentPrice": price,
                "dayChange": info.get("regularMarketChangePercent", 0) if 'info' in locals() else 0,
                "high52W": info.get("fiftyTwoWeekHigh", 0) if 'info' in locals() else 0,
                "low52W": info.get("fiftyTwoWeekLow", 0) if 'info' in locals() else 0
            })

        return jsonify({"portfolio": portfolio})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/trend', methods=['GET'])
def analyze_trend():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Missing 'ticker' in query parameters"}), 400
    result = trend_agent.run(ticker)
    if not result:
        return jsonify({"error": "Trend analysis failed"}), 500
    return jsonify(json_safe(result))

@app.route('/risk', methods=['GET'])
def analyze_risk():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Missing 'ticker' in query parameters"}), 400
    result = risk_agent.run(ticker)
    if not result:
        return jsonify({"error": "Risk assessment failed"}), 500
    return jsonify(json_safe(result))

@app.route('/decision', methods=['GET'])
def full_decision():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Missing 'ticker' in query parameters"}), 400

    # Measure execution time
    start_time = time.time()
    
    # Run agents in parallel for 3x speed improvement
    with ThreadPoolExecutor(max_workers=3) as executor:
        trend_future = executor.submit(trend_agent.run, ticker)
        risk_future = executor.submit(risk_agent.run, ticker)
        forecast_future = executor.submit(forecast_agent.run, ticker)
        
        # Collect results
        trend_result = trend_future.result()
        risk_result = risk_future.result()
        forecast_result = forecast_future.result()
    
    execution_time = time.time() - start_time
    print(f"[PERF] Parallel agent execution for {ticker}: {execution_time:.2f}s")
    
    if not trend_result or not risk_result or not forecast_result:
        return jsonify({"error": "Analysis failed for trend, risk, or forecast"}), 500
 
    decision = decision_agent.decide(trend_result, risk_result, forecast_result)

    return jsonify({
        "ticker": ticker,
        "trend": json_safe(trend_result),
        "risk": json_safe(risk_result),
        "forecast": json_safe(forecast_result),
        "decision": json_safe(decision),
        "execution_time": round(execution_time, 2)
    })

@app.route('/forecast', methods=['GET'])
def analyze_forecast():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Missing 'ticker' in query parameters"}), 400
    result = forecast_agent.run(ticker)
    if not result:
        return jsonify({"error": "Forecasting failed"}), 500
    return jsonify(json_safe(result))

@app.route('/data', methods=['GET'])
def get_historical_data():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Missing 'ticker' in query parameters"}), 400
    try:
        data = yf.download(ticker, period="1y")
        if data.empty:
            return jsonify({"error": "No historical data found"}), 404
        data.reset_index(inplace=True)
        csv_data = data.to_csv(index=False)
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=data.csv"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data_forcast', methods=['GET'])
def get_forecast_data():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Missing 'ticker' in query parameters"}), 400
    try:
        result = forecast_agent.run(ticker)
        if not result or "forecast" not in result:
            return jsonify({"error": "Invalid forecast data returned"}), 500

        forecast = result["forecast"]  # this is a dict with {date_str: price}

        df = pd.DataFrame(list(forecast.items()), columns=["date", "predictedPrice"])
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df["predictedPrice"] = df["predictedPrice"].astype(float).round(2)

        csv_data = df.to_csv(index=False)
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=data_forecast.csv"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-portfolio', methods=['POST', 'OPTIONS'])
def update_portfolio():
    """Update portfolio data (saves to file for persistence)"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    print(f"[DEBUG] Received POST to /update-portfolio")
    print(f"[DEBUG] Request headers: {dict(request.headers)}")
    print(f"[DEBUG] Request data: {request.get_data(as_text=True)}")
    
    try:
        data = request.get_json()
        print(f"[DEBUG] Parsed JSON: {data}")
        
        portfolio = data.get('portfolio', [])
        print(f"[DEBUG] Portfolio: {portfolio}")
        
        if not portfolio:
            print(f"[DEBUG] Portfolio is empty, returning error")
            return jsonify({"error": "Portfolio cannot be empty"}), 400
        
        # Save to a JSON file for persistence
        import json
        portfolio_file = os.path.join(os.path.dirname(__file__), 'custom_portfolio.json')
        print(f"[DEBUG] Saving to file: {portfolio_file}")
        
        with open(portfolio_file, 'w') as f:
            json.dump(portfolio, f, indent=2)
        
        print(f"[DEBUG] File saved successfully")
        return jsonify({"success": True, "message": "Portfolio updated successfully"})
    except Exception as e:
        print(f"[ERROR] Portfolio update error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)