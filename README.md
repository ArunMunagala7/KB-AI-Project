├── src/                  # React frontend
│   └── components/      # UI components
├── tests/                # Test suite
├── docs/                 # Documentation
│   ├── DEMO_GUIDE.md
│   ├── IMPROVEMENT_ANALYSIS.md
│   └── DEVELOPMENT_NOTES.md
├── submission/           # Course submission materials
└── README.md            # This file
```

---

## 6. Usage Examples

### Analyzing a Single Stock

```python
from trend_agent import TrendAnalysisAgent
from risk_assesment import RiskAssessmentAgent
from forecast_agent import ForecastingAgent
from decision_agent import DecisionAgent

# Run agents
trend = TrendAnalysisAgent().run('AAPL')
risk = RiskAssessmentAgent().run('AAPL')
forecast = ForecastingAgent().run('AAPL')

# Get decision
decision = DecisionAgent().decide(trend, risk, forecast)
print(f"Recommendation: {decision['decision']}")
print(f"Confidence: {decision['confidence_score']}%")
```

### Evaluating LLM Output Quality

```python
from llm_evaluator import LLMEvaluator

evaluator = LLMEvaluator()
report = evaluator.evaluate_comprehensive(
    agent_name='Trend Agent',
    llm_response=trend['analysis'],
    ground_truth={'sma50': 175.50, 'rsi': 58.3},
    input_metrics={'sma50': 175.50, 'rsi': 58.3},
    tokens_used=150
)

if report['overall_score'] < 70:
    print("⚠️ Low quality response detected")
```

---

## 7. API Endpoints

All endpoints run on `http://localhost:5001`

- `GET /portfolio` - Retrieve current portfolio
- `POST /update-portfolio` - Add/update holdings  
- `GET /trend?ticker=AAPL` - Get trend analysis
- `GET /risk?ticker=AAPL` - Get risk assessment
- `GET /forecast?ticker=AAPL` - Get price forecast
- `GET /decision?ticker=AAPL` - Get BUY/SELL/HOLD decision

---

## 8. Testing

Run tests:

```bash
cd tests
python test_evaluator.py       # LLM evaluation tests
python test_agents.py           # Agent unit tests
python how_it_works.py          # Integration examples
```

---

## 9. Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

---

## 10. Known Issues

See [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) for current limitations and planned improvements.

---

## 11. Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

## 12. License

This project is developed for academic purposes (B552 - Knowledge-Based AI, Spring 2026).

---

## 13. Acknowledgments

- Indiana University Bloomington - B552 Course
- yfinance for market data
- Finnhub for news API
- OpenAI for LLM capabilities

---

## 14. Contact

**Team Members:**
- Akshara Sarode - asarode@iu.edu
- Arun Munagala - amunagal@iu.edu  
- Anuj Prakash - anuprak@iu.edu

**Repository:** https://github.com/ArunMunagala7/KB-AI-Project

   ```bash
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASS=your_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Finnhub API Key (for risk analysis headlines)
   FINNHUB_API_KEY=YOUR_FINNHUB_API_KEY
   
   # Mistral or OpenAI credentials
   MISTAL_API_KEY=YOUR_MISTRAL_KEY
   MISTRAL_API_BASE=https://api.openai.com/v1

3. Running Flask backend

   ```bash
   cd Scripts
   python app.py
   
4. Running the React Frontend

   ```bash
   npm run dev

<a name="agents"></a>
## 5. Agents
| **Script File**       | **Description**                                                                                                   |
|-----------------------|-------------------------------------------------------------------------------------------------------------------|
| `trend_agent.py`      | **TrendAnalysisAgent** – Gathers SMA (50 vs. 200), RSI, and MACD signals to produce a final trend score.           |
| `risk_assessment.py`  | **RiskAssessmentAgent** – Calculates volatility, VaR, max drawdown, and (optionally) analyzes headlines from Finnhub. |
| `forecast_agent.py`   | **ForecastingAgent** – Uses ExponentialSmoothing to forecast the next 3 months of price changes.                   |
| `decision_agent.py`   | **DecisionAgent** – Takes in trend, risk, and forecast data, returning a **BUY/SELL/HOLD** recommendation.         |


<a name="endpoints"></a>
## 6. Endpoints and API

| **Endpoint**                | **Method** | **Description**                                                                                          |
|-----------------------------|:---------:|----------------------------------------------------------------------------------------------------------|
| `/portfolio`               | **GET**    | Fetches holdings from PostgreSQL (if configured).                                                        |
| `/trend?ticker=XYZ`        | **GET**    | Runs TrendAnalysisAgent on the specified ticker.                                                         |
| `/risk?ticker=XYZ`         | **GET**    | Runs RiskAssessmentAgent on the specified ticker.                                                        |
| `/forecast?ticker=XYZ`     | **GET**    | Runs ForecastingAgent on the specified ticker.                                                           |
| `/decision?ticker=XYZ`     | **GET**    | Aggregates all agents and returns a BUY/SELL/HOLD decision.                                              |
| `/data?ticker=XYZ`         | **GET**    | Returns 1 year of historical data (CSV) for the specified ticker.                                        |
| `/data_forcast?ticker=XYZ` | **GET**    | Returns forecast data (CSV) from the ForecastingAgent for the ticker.                                    |



