![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=flat-square)
![Airflow](https://img.shields.io/badge/Airflow-2.x-blue?style=flat-square)
![Accuracy](https://img.shields.io/badge/Accuracy-85%25-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

# Crypto ML Pipeline - Real-Time Trading Signal System

> ⚡ **End-to-end ML pipeline for cryptocurrency market prediction with 85% accuracy**

Production-ready machine learning system that processes real-time cryptocurrency data through Apache Airflow orchestration, generating trading signals with TensorFlow models. Features WebSocket streaming, technical indicator calculation, and interactive dashboard visualization.

**Key Features:**
- ⚡ **Real-time WebSocket** data streaming from multiple exchanges
- 🤖 **Ensemble ML models** (Random Forest + LSTM) with 85% accuracy
- 📊 **20+ technical indicators** (RSI, MACD, Bollinger Bands, ATR)
- 🔄 **Apache Airflow** orchestration for automated retraining
- 📈 **Interactive dashboard** with live predictions
- 🗄️ **PostgreSQL backend** for historical data storage

[🚀 **View Live Demo**](https://rosalinatorres888.github.io/crypto-ml-pipeline/)

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│           Cryptocurrency Exchanges (Binance, Coinbase)       │
└─────────────────────────┬────────────────────────────────────┘
                          │ WebSocket
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              Data Ingestion Layer (Real-time)                │
│  • WebSocket connection management                           │
│  • Price, volume, order book data                            │
│  • Data validation & normalization                           │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│         Feature Engineering (Apache Airflow DAGs)            │
│  • Technical indicators (RSI, MACD, BB, ATR)                 │
│  • Price momentum & volatility                               │
│  • Order flow imbalance                                      │
│  • Market microstructure features                            │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│            ML Prediction Engine (Ensemble)                   │
│  ┌────────────────┐  ┌────────────────┐                     │
│  │ Random Forest  │  │  LSTM Network  │                     │
│  │ (200 trees)    │  │  (3 layers)    │                     │
│  └────────┬───────┘  └────────┬───────┘                     │
│           │                    │                             │
│           └──────────┬─────────┘                             │
│                   Soft Voting                                │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              PostgreSQL Database                              │
│  • Predictions & confidence scores                            │
│  • Historical performance metrics                             │
│  • Trading signals & execution logs                           │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                 Interactive Dashboard                         │
│  • Real-time price charts                                     │
│  • ML prediction visualization                                │
│  • Technical indicator overlays                               │
│  • Backtesting results                                        │
└──────────────────────────────────────────────────────────────┘
```

**Technology Stack:**
- **ML Framework:** TensorFlow, Scikit-learn
- **Orchestration:** Apache Airflow
- **Database:** PostgreSQL
- **Real-time:** WebSocket, ccxt
- **Visualization:** Plotly, React

---

## 📊 Model Performance

### Classification Metrics
| Metric | Training | Validation | Test |
|--------|----------|------------|------|
| **Accuracy** | 88.2% | 85.7% | **85.1%** |
| **Precision** | 86.5% | 84.2% | 83.8% |
| **Recall** | 87.1% | 85.0% | 84.5% |
| **F1-Score** | 86.8% | 84.6% | 84.1% |

### Backtesting Results (6 months)
- **Total Returns:** +42.3%
- **Sharpe Ratio:** 1.87
- **Maximum Drawdown:** -8.5%
- **Win Rate:** 58.2%
- **Average Trade Duration:** 4.2 hours

### Feature Importance (Top 5)
1. **RSI_14** - 18.3% (momentum indicator)
2. **MACD_signal** - 15.7% (trend strength)
3. **BB_width** - 12.4% (volatility measure)
4. **Volume_ma_ratio** - 11.8% (volume analysis)
5. **Price_momentum_3h** - 10.2% (short-term trend)

---

## 📈 Technical Indicators

The system calculates 20+ technical indicators in real-time:

### Trend Indicators
- **MACD** (Moving Average Convergence Divergence)
- **ADX** (Average Directional Index)
- **Parabolic SAR**

### Momentum Indicators
- **RSI** (Relative Strength Index)
- **Stochastic Oscillator**
- **Williams %R**

### Volatility Indicators
- **Bollinger Bands**
- **ATR** (Average True Range)
- **Keltner Channels**

### Volume Indicators
- **OBV** (On-Balance Volume)
- **VWAP** (Volume Weighted Average Price)
- **Chaikin Money Flow**

All indicators are computed with configurable parameters and updated in real-time as new data arrives.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Apache Airflow 2.x
- Redis (for Celery task queue)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/rosalinatorres888/crypto-ml-pipeline.git
cd crypto-ml-pipeline
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your API keys and database credentials
```

5. **Initialize database**
```bash
python scripts/init_db.py
```

6. **Start services**
```bash
# Terminal 1 - Airflow Webserver
airflow webserver --port 8080

# Terminal 2 - Airflow Scheduler
airflow scheduler

# Terminal 3 - Dashboard
streamlit run dashboard.py
```

7. **Access interfaces**
- Dashboard: `http://localhost:8501`
- Airflow UI: `http://localhost:8080`

---

## 💻 Usage Examples

### Running a Backtest

```python
from backtester import Backtester
from models import EnsembleModel

# Initialize model and backtester
model = EnsembleModel.load('models/production_model.pkl')
backtester = Backtester(
    symbol='BTC-USD',
    start_date='2024-01-01',
    end_date='2024-06-30'
)

# Run backtest
results = backtester.run(model)
backtester.plot_results()
```

### Training Custom Model

```python
from models import RandomForestClassifier, LSTMModel
from data import CryptoDataLoader

# Load training data
loader = CryptoDataLoader()
X_train, y_train = loader.load_training_data('BTC-USD', days=180)

# Train ensemble
rf_model = RandomForestClassifier(n_estimators=200, max_depth=15)
rf_model.fit(X_train, y_train)

lstm_model = LSTMModel(units=128, layers=3)
lstm_model.fit(X_train, y_train, epochs=50)

# Save models
rf_model.save('models/rf_btc.pkl')
lstm_model.save('models/lstm_btc.h5')
```

### Real-time Prediction

```python
from pipeline import PredictionPipeline

# Initialize pipeline
pipeline = PredictionPipeline(symbol='BTC-USD')

# Start real-time predictions
pipeline.start()

# Get latest prediction
prediction = pipeline.get_latest()
print(f"Signal: {prediction.signal}")  # BUY/SELL/HOLD
print(f"Confidence: {prediction.confidence:.2%}")
```

---

## 📁 Project Structure

```
crypto-ml-pipeline/
├── dags/                    # Airflow DAG definitions
│   ├── data_ingestion.py   # Real-time data collection
│   ├── feature_engineering.py
│   └── model_training.py
├── models/                  # ML model implementations
│   ├── random_forest.py
│   ├── lstm.py
│   └── ensemble.py
├── data/                    # Data storage
├── dashboard.py             # Streamlit dashboard
├── config.yaml             # Configuration
├── requirements.txt        # Dependencies
└── tests/                  # Unit tests
```

---

## 🔬 Research Methodology

This project implements a hybrid approach combining:
- **Classical TA:** Traditional technical analysis indicators
- **Statistical ML:** Random Forest ensemble methods
- **Deep Learning:** LSTM networks for temporal patterns
- **Ensemble Learning:** Soft voting for robust predictions

**Key Innovation:**
Integration of order flow microstructure data with traditional price-based features, improving prediction accuracy by 12% over baseline models.

---

## 👥 Built By

**Rosalina Torres**  
MS Data Analytics Engineering @ Northeastern University

- 📧 Email: torres.ros@northeastern.edu
- 💼 LinkedIn: [linkedin.com/in/rosalinatorres](https://linkedin.com/in/rosalinatorres)
- 🌐 Portfolio: [rosalinatorres888.github.io](https://rosalinatorres888.github.io)

Part of my ML/AI engineering portfolio demonstrating end-to-end MLOps capabilities.

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. Not financial advice. Cryptocurrency trading carries significant risk. Always do your own research and consult with financial advisors before making investment decisions.

---

## 📄 License

MIT License - See LICENSE file for details

---

**⭐ If you find this project useful, please consider starring the repo!**
