import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("Running Crypto ML Pipeline...")

# Fetch historical data
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {'vs_currency': 'usd', 'days': 30, 'interval': 'hourly'}
response = requests.get(url, params=params)
data = response.json()

# Create DataFrame
df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Feature engineering
df['returns'] = df['price'].pct_change()
df['ma_24'] = df['price'].rolling(24).mean()
df['volatility'] = df['returns'].rolling(24).std()
df['hour'] = df['timestamp'].dt.hour

# Create target (next 24h price)
df['target'] = df['price'].shift(-24)

# Prepare data
features = ['price', 'returns', 'volatility', 'hour']
df_clean = df.dropna()
X = df_clean[features].values[:-24]
y = df_clean['target'].values[:-24]

# Train model
split_idx = int(0.8 * len(X))
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
predictions = model.predict(X_test_scaled)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print(f"\nModel Performance:")
print(f"RMSE: ${rmse:.2f}")
print(f"R² Score: {r2:.3f}")

# Make prediction
current_features = scaler.transform(X[-1].reshape(1, -1))
predicted_price = model.predict(current_features)[0]
current_price = df_clean['price'].iloc[-25]

print(f"\nPrice Prediction:")
print(f"Current Bitcoin price: ${current_price:,.2f}")
print(f"Predicted price (24h): ${predicted_price:,.2f}")
print(f"Expected change: {((predicted_price - current_price) / current_price * 100):.2f}%")

print("\n✅ ML Pipeline completed!")
