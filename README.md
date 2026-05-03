# KB-AI: Knowledge-Based AI for Stock Portfolio Decision-Making

**Team Name:** KB-AI Team

**Members:**  
- Akshara Sarode (asarode@iu.edu)
- Arun Munagala (amunagal@iu.edu)
- Anuj Prakash (anuprak@iu.edu)

**Course:** B552 - Knowledge-Based AI, Spring 2026  
**Institution:** Indiana University Bloomington

This repository hosts a hybrid multi-agent stock analysis application that combines knowledge-based rules with large language models (LLMs) to provide reliable, transparent stock portfolio recommendations. The system uses **Flask** (Python) on the backend and **React + Vite** on the frontend to deliver end-to-end intelligent stock insights through four specialized agents.

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation & Setup](#installation)
5. [Agents and Scripts](#Agents)
6. [Endpoints & API](#Endpoints)

---
<a name="overview"></a>
## 1. Overview

**KB-AI** is a comprehensive hybrid multi-agent platform that combines knowledge-based rules with large language models (LLMs) for intelligent stock portfolio analysis. The system addresses critical challenges in financial AI: **reliability**, **transparency**, and **quality assurance**.

### Key Innovations

1. **Priority-Based Conflict Resolution**: Four hierarchical rules (P1-P4) handle safety-critical scenarios deterministically, with LLM fallback for ambiguous cases
2. **4-Dimensional LLM Evaluation**: Continuous quality monitoring detecting hallucinations, vague language, and inconsistencies
3. **Parallel Agent Execution**: 3.6× faster analysis through concurrent processing
4. **Confidence Scoring**: Transparent confidence levels (70-95%) for every recommendation

The system leverages four specialized Python agents to:

- Perform **technical trend analysis** (SMA, RSI, MACD) with 90% confidence  
- Assess **risk** (volatility, max drawdown, VaR) and incorporate **news sentiment** via Finnhub API  
- **Forecast** prices using exponential smoothing with 90% confidence intervals  
- Issue **BUY/SELL/HOLD decisions** with 95% confidence in safety-critical scenarios

The React + Vite frontend provides an interactive dashboard displaying real-time results, confidence badges, and decision reasoning.

---
<a name="features"></a>
## 2. Features

- **Trend Analysis**  
  Calculates various technical indicators and synthesizes them into a single trend score. An optional LLM provides short reasoning about the trend.

- **Risk Assessment**  
  Measures annualized volatility, Value at Risk (VaR), and maximum drawdown, and parses recent news headlines via Finnhub API. An LLM can produce a “news-based risk score.”

- **Forecasting**  
  Predicts the stock’s closing price over the next 3 months using **ExponentialSmoothing**. Summarize the forecast using an LLM-generated explanation.

- **Decision Making**  
  Aggregates the above agents’ results to suggest a final trading action: **BUY**, **SELL**, or **HOLD**.

- **Flask RESTful API**  
  Provides endpoints to query portfolio information, trigger the analysis, and retrieve results or CSV exports of historical/forecast data.

- **React + Vite Frontend**  
  Presents an interactive dashboard that displays all results, enabling convenient user interaction.

---

<a name="prerequisites"></a>
## 3. Prerequisites

Before installing and running, ensure you have:

1. **Python 3.9+**  
2. **PostgreSQL** (optional if you want to store portfolio holdings in a database)  
4. **Finnhub API Key** – if you wish to pull relevant news headlines and incorporate them into the risk analysis.  
5. **Mistral or OpenAI API credentials** – for the LLM functionalities in your agents (optional but recommended).

---
<a name="installation"></a>
## 4. Installation

1. **Clone this repo**:

   ```bash
   git clone https://github.com/your-org/LuddyHackathon2K25.git
   cd LuddyHackathon2K25-main
   pip install --upgrade pip
   pip install -r requirements.txt
   npm install

2. Create an Environment Variables file

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



