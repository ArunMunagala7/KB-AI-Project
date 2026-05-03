# Changelog

All notable changes to KB-AI project documented here.

## [Unreleased]
- Portfolio optimization using Modern Portfolio Theory
- Backtesting framework with historical data
- Alert system for risk threshold breaches

## [1.2.0] - 2026-04-28
### Added
- LLM evaluation framework with 4-dimensional scoring
- Consistency testing to detect unstable outputs
- Cost tracking for API usage monitoring

### Fixed
- Hallucination detection catching fabricated metrics
- Nonsensical guarantee detection ("100% certain", "zero risk")

## [1.1.0] - 2026-04-15
### Added
- Confidence score badges in UI (green/yellow/red)
- Decision type indicators (rule-based vs llm-based)
- Communication log showing agent execution flow

### Changed
- Updated all agents to return confidence_score field
- Enhanced StockDetail modal with better visualization

## [1.0.0] - 2026-04-01
### Added
- Priority-based decision rules (P1, P2, P3, P4)
- Conflict resolution hierarchy
- Parallel agent execution using ThreadPoolExecutor

### Changed
- Refactored decision agent to use rules first, LLM fallback
- Improved response time from 2.5s to 0.7s per stock

### Fixed
- Inconsistent decision problem (was giving different recommendations)
- High-risk scenarios not being handled properly

## [0.9.0] - 2026-03-20
### Added
- Forecast agent with exponential smoothing
- News sentiment integration via Finnhub API
- Flask API endpoints for all agents

### Changed
- Separated concerns into individual agent files
- Added proper error handling for API failures

## [0.8.0] - 2026-03-10
### Added
- Risk assessment with volatility calculations
- Trend analysis with technical indicators (SMA, RSI, MACD)
- Basic LLM integration for analysis

### Initial
- React frontend with Vite
- Basic portfolio structure
- Database schema for holdings
