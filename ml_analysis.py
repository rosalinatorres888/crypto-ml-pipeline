import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

print("Running ML Analysis...")
conn = sqlite3.connect("crypto_data.db")
df = pd.read_sql_query("SELECT * FROM crypto_prices WHERE coin_id='bitcoin' ORDER BY etl_timestamp", conn)

if len(df) > 5:
    X = df[["current_price", "total_volume", "market_cap"]].values[:-1]
    y = df["current_price"].values[1:]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    print(f"Model R2 Score: {r2:.3f}")
    print(f"Current Price: ${df['current_price'].iloc[-1]:,.2f}")
    next_price = model.predict(X[-1].reshape(1, -1))[0]
    print(f"Predicted Next Price: ${next_price:,.2f}")
else:
    print("Need more data! Run collect_data.py first.")
conn.close()
