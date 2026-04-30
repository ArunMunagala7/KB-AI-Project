import React, { useState, useEffect } from 'react';
import { Box, Typography, TextField, Button, Card, CardContent, IconButton, Autocomplete, Grid, Chip, Alert } from '@mui/material';
import { Link } from 'react-router-dom';

// Popular stock symbols with company names
const POPULAR_STOCKS = [
  { symbol: 'AAPL', name: 'Apple Inc.' },
  { symbol: 'GOOGL', name: 'Alphabet Inc.' },
  { symbol: 'MSFT', name: 'Microsoft Corp.' },
  { symbol: 'AMZN', name: 'Amazon.com Inc.' },
  { symbol: 'TSLA', name: 'Tesla Inc.' },
  { symbol: 'META', name: 'Meta Platforms Inc.' },
  { symbol: 'NVDA', name: 'NVIDIA Corp.' },
  { symbol: 'NFLX', name: 'Netflix Inc.' },
  { symbol: 'JPM', name: 'JPMorgan Chase' },
  { symbol: 'V', name: 'Visa Inc.' },
  { symbol: 'MA', name: 'Mastercard Inc.' },
  { symbol: 'DIS', name: 'Walt Disney Co.' },
  { symbol: 'COIN', name: 'Coinbase Global' },
  { symbol: 'SQ', name: 'Block Inc.' },
  { symbol: 'PYPL', name: 'PayPal Holdings' },
  { symbol: 'UBER', name: 'Uber Technologies' },
  { symbol: 'ABNB', name: 'Airbnb Inc.' },
  { symbol: 'AMD', name: 'Advanced Micro Devices' },
  { symbol: 'INTC', name: 'Intel Corp.' },
  { symbol: 'CRM', name: 'Salesforce Inc.' },
  { symbol: 'ORCL', name: 'Oracle Corp.' },
  { symbol: 'ADBE', name: 'Adobe Inc.' },
  { symbol: 'CSCO', name: 'Cisco Systems' },
  { symbol: 'QCOM', name: 'Qualcomm Inc.' },
  { symbol: 'TXN', name: 'Texas Instruments' },
  { symbol: 'AVGO', name: 'Broadcom Inc.' },
  { symbol: 'BAC', name: 'Bank of America' },
  { symbol: 'WFC', name: 'Wells Fargo' },
  { symbol: 'GS', name: 'Goldman Sachs' },
  { symbol: 'MS', name: 'Morgan Stanley' },
  { symbol: 'WMT', name: 'Walmart Inc.' },
  { symbol: 'TGT', name: 'Target Corp.' },
  { symbol: 'COST', name: 'Costco Wholesale' },
  { symbol: 'HD', name: 'Home Depot' },
  { symbol: 'LOW', name: "Lowe's Companies" },
  { symbol: 'NKE', name: 'Nike Inc.' },
  { symbol: 'SBUX', name: 'Starbucks Corp.' },
  { symbol: 'MCD', name: "McDonald's Corp." },
  { symbol: 'KO', name: 'Coca-Cola Co.' },
  { symbol: 'PEP', name: 'PepsiCo Inc.' },
  { symbol: 'JNJ', name: 'Johnson & Johnson' },
  { symbol: 'PFE', name: 'Pfizer Inc.' },
  { symbol: 'UNH', name: 'UnitedHealth Group' },
  { symbol: 'ABBV', name: 'AbbVie Inc.' },
  { symbol: 'TMO', name: 'Thermo Fisher Scientific' },
  { symbol: 'BA', name: 'Boeing Co.' },
  { symbol: 'LMT', name: 'Lockheed Martin' },
  { symbol: 'RTX', name: 'Raytheon Technologies' },
  { symbol: 'CAT', name: 'Caterpillar Inc.' },
  { symbol: 'DE', name: 'Deere & Co.' },
];

const PortfolioManager = () => {
  const [portfolio, setPortfolio] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [quantity, setQuantity] = useState('');
  const [avgPrice, setAvgPrice] = useState('');
  const [savedMessage, setSavedMessage] = useState('');
  const [error, setError] = useState('');

  // Load current portfolio from localStorage
  useEffect(() => {
    // First try to fetch from backend
    fetch('http://localhost:5001/portfolio')
      .then(response => response.json())
      .then(data => {
        if (data.portfolio && data.portfolio.length > 0) {
          // Convert backend format to our format
          const portfolioData = data.portfolio.map(stock => ({
            ticker: stock.ticker,
            qty: stock.qty,
            avgPrice: stock.avgPrice
          }));
          setPortfolio(portfolioData);
          // Also save to localStorage
          localStorage.setItem('customPortfolio', JSON.stringify(portfolioData));
        } else {
          // Fall back to localStorage
          const savedPortfolio = localStorage.getItem('customPortfolio');
          if (savedPortfolio) {
            setPortfolio(JSON.parse(savedPortfolio));
          }
        }
      })
      .catch(error => {
        console.error('Error loading portfolio:', error);
        // Fall back to localStorage
        const savedPortfolio = localStorage.getItem('customPortfolio');
        if (savedPortfolio) {
          setPortfolio(JSON.parse(savedPortfolio));
        } else {
          // Default stocks if nothing saved
          setPortfolio([
            { ticker: 'AAPL', qty: 10, avgPrice: 150.00 },
            { ticker: 'GOOGL', qty: 5, avgPrice: 2800.00 },
            { ticker: 'MSFT', qty: 8, avgPrice: 300.00 },
          ]);
        }
      });
  }, []);

  const handleAddStock = () => {
    if (!selectedStock || !quantity || !avgPrice) {
      setError('Please fill in all fields');
      return;
    }

    if (parseFloat(quantity) <= 0 || parseFloat(avgPrice) <= 0) {
      setError('Quantity and price must be positive numbers');
      return;
    }

    // Check if stock already exists
    const existingStock = portfolio.find(s => s.ticker === selectedStock.symbol);
    if (existingStock) {
      setError(`${selectedStock.symbol} is already in your portfolio`);
      return;
    }

    const newStock = {
      ticker: selectedStock.symbol,
      qty: parseFloat(quantity),
      avgPrice: parseFloat(avgPrice)
    };

    const updatedPortfolio = [...portfolio, newStock];
    setPortfolio(updatedPortfolio);
    
    // Clear form
    setSelectedStock(null);
    setQuantity('');
    setAvgPrice('');
    setError('');
    setSavedMessage('');
  };

  const handleRemoveStock = (ticker) => {
    const updatedPortfolio = portfolio.filter(stock => stock.ticker !== ticker);
    setPortfolio(updatedPortfolio);
    setSavedMessage('');
  };

  const handleSavePortfolio = async () => {
    try {
      // Save to localStorage
      localStorage.setItem('customPortfolio', JSON.stringify(portfolio));
      
      // Also send to backend to update mock_portfolio
      const response = await fetch('http://localhost:5001/update-portfolio', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ portfolio })
      });

      if (response.ok) {
        setSavedMessage('✅ Portfolio saved successfully! Changes will appear on dashboard refresh.');
        setError('');
        setTimeout(() => setSavedMessage(''), 8000);
      } else {
        setSavedMessage('⚠️ Portfolio saved locally but backend sync failed. Dashboard should still update.');
        setTimeout(() => setSavedMessage(''), 8000);
      }
    } catch (err) {
      console.error('Error saving portfolio:', err);
      localStorage.setItem('customPortfolio', JSON.stringify(portfolio));
      setSavedMessage('⚠️ Portfolio saved locally! Flask server may be down. Restart servers and reload dashboard.');
      setTimeout(() => setSavedMessage(''), 10000);
    }
  };

  const getTotalInvestment = () => {
    return portfolio.reduce((sum, stock) => sum + (stock.qty * stock.avgPrice), 0);
  };

  return (
    <Box sx={{ p: 4, backgroundColor: '#0a0e27', minHeight: '100vh' }}>
      {/* Navigation Bar */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" sx={{ color: 'white', display: 'flex', alignItems: 'center' }}>
          📈 Portfolio Manager
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Link to="/" style={{ textDecoration: 'none' }}>
            <Button variant="outlined" sx={{ color: '#4fc3f7', borderColor: '#4fc3f7', '&:hover': { borderColor: '#0288d1', backgroundColor: 'rgba(79, 195, 247, 0.1)' } }}>
              🏠 Home
            </Button>
          </Link>
          <Link to="/dashboard" style={{ textDecoration: 'none' }}>
            <Button variant="contained" sx={{ backgroundColor: '#4fc3f7', '&:hover': { backgroundColor: '#0288d1' } }}>
              📊 Go to Dashboard
            </Button>
          </Link>
        </Box>
      </Box>

      {/* Add Stock Section */}
      <Card sx={{ mb: 4, backgroundColor: '#1a1f3a', color: 'white' }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, color: '#4fc3f7' }}>
            Add New Stock
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Autocomplete
                value={selectedStock}
                onChange={(event, newValue) => setSelectedStock(newValue)}
                options={POPULAR_STOCKS}
                getOptionLabel={(option) => `${option.symbol} - ${option.name}`}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Stock Symbol"
                    placeholder="Search stocks..."
                    sx={{
                      '& .MuiInputLabel-root': { color: '#aaa' },
                      '& .MuiOutlinedInput-root': {
                        color: 'white',
                        '& fieldset': { borderColor: '#444' },
                        '&:hover fieldset': { borderColor: '#4fc3f7' },
                        '&.Mui-focused fieldset': { borderColor: '#4fc3f7' },
                      },
                    }}
                  />
                )}
                renderOption={(props, option) => (
                  <Box component="li" {...props} sx={{ backgroundColor: '#1a1f3a !important', color: 'white !important' }}>
                    <strong>{option.symbol}</strong>&nbsp;- {option.name}
                  </Box>
                )}
                sx={{
                  '& .MuiAutocomplete-paper': {
                    backgroundColor: '#1a1f3a',
                  }
                }}
              />
            </Grid>

            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Quantity (Shares)"
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                placeholder="e.g., 10"
                sx={{
                  '& .MuiInputLabel-root': { color: '#aaa' },
                  '& .MuiOutlinedInput-root': {
                    color: 'white',
                    '& fieldset': { borderColor: '#444' },
                    '&:hover fieldset': { borderColor: '#4fc3f7' },
                    '&.Mui-focused fieldset': { borderColor: '#4fc3f7' },
                  },
                }}
              />
            </Grid>

            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Average Price ($)"
                type="number"
                value={avgPrice}
                onChange={(e) => setAvgPrice(e.target.value)}
                placeholder="e.g., 150.00"
                sx={{
                  '& .MuiInputLabel-root': { color: '#aaa' },
                  '& .MuiOutlinedInput-root': {
                    color: 'white',
                    '& fieldset': { borderColor: '#444' },
                    '&:hover fieldset': { borderColor: '#4fc3f7' },
                    '&.Mui-focused fieldset': { borderColor: '#4fc3f7' },
                  },
                }}
              />
            </Grid>

            <Grid item xs={12} md={2}>
              <Button
                fullWidth
                variant="contained"
                onClick={handleAddStock}
                sx={{
                  height: '56px',
                  backgroundColor: '#4fc3f7',
                  '&:hover': { backgroundColor: '#0288d1' }
                }}
              >
                ➕ Add
              </Button>
            </Grid>
          </Grid>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Current Portfolio Section */}
      <Card sx={{ backgroundColor: '#1a1f3a', color: 'white' }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6" sx={{ color: '#4fc3f7' }}>
              Current Portfolio ({portfolio.length} stocks)
            </Typography>
            <Chip
              label={`Total Investment: $${getTotalInvestment().toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
              sx={{ backgroundColor: '#2e7d32', color: 'white', fontWeight: 'bold' }}
            />
          </Box>

          {portfolio.length === 0 ? (
            <Typography sx={{ textAlign: 'center', py: 4, color: '#aaa' }}>
              No stocks in portfolio. Add some stocks above!
            </Typography>
          ) : (
            <Grid container spacing={2}>
              {portfolio.map((stock) => (
                <Grid item xs={12} sm={6} md={4} key={stock.ticker}>
                  <Card sx={{ backgroundColor: '#0a0e27', border: '1px solid #333' }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                        <Box>
                          <Typography variant="h6" sx={{ color: '#4fc3f7', fontWeight: 'bold' }}>
                            {stock.ticker}
                          </Typography>
                          <Typography variant="body2" sx={{ color: '#aaa', mt: 1 }}>
                            Quantity: {stock.qty} shares
                          </Typography>
                          <Typography variant="body2" sx={{ color: '#aaa' }}>
                            Avg Price: ${stock.avgPrice.toFixed(2)}
                          </Typography>
                          <Typography variant="body2" sx={{ color: '#66bb6a', fontWeight: 'bold', mt: 1 }}>
                            Investment: ${(stock.qty * stock.avgPrice).toFixed(2)}
                          </Typography>
                        </Box>
                        <IconButton
                          size="small"
                          onClick={() => handleRemoveStock(stock.ticker)}
                          sx={{ color: '#f44336' }}
                        >
                          🗑️
                        </IconButton>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}

          {portfolio.length > 0 && (
            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Button
                variant="contained"
                size="large"
                onClick={handleSavePortfolio}
                sx={{
                  backgroundColor: '#2e7d32',
                  px: 4,
                  '&:hover': { backgroundColor: '#1b5e20' }
                }}
              >
                💾 Save Portfolio
              </Button>
            </Box>
          )}

          {savedMessage && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {savedMessage}
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Quick Tips */}
      <Card sx={{ mt: 3, backgroundColor: '#1a1f3a', color: 'white' }}>
        <CardContent>
          <Typography variant="subtitle1" sx={{ color: '#4fc3f7', mb: 2, fontWeight: 'bold' }}>
            💡 Quick Tips:
          </Typography>
          <Typography variant="body2" sx={{ color: '#aaa', mb: 1 }}>
            • Search for stocks by symbol or company name in the dropdown
          </Typography>
          <Typography variant="body2" sx={{ color: '#aaa', mb: 1 }}>
            • Enter the number of shares you own and your average purchase price
          </Typography>
          <Typography variant="body2" sx={{ color: '#aaa', mb: 1 }}>
            • Click "Save Portfolio" to persist your changes
          </Typography>
          <Typography variant="body2" sx={{ color: '#aaa' }}>
            • Return to the dashboard to analyze your updated portfolio
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default PortfolioManager;
