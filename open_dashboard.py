import sqlite3
import pandas as pd
import webbrowser
import os

conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query("SELECT * FROM crypto_prices WHERE coin_id='bitcoin' ORDER BY etl_timestamp", conn)

if not df.empty:
    current_price = df['current_price'].iloc[-1]
    html = f'<html><body><h1>Bitcoin: ${current_price:,.2f}</h1></body></html>'
    with open('dashboard.html', 'w') as f:
        f.write(html)
    webbrowser.open('file://' + os.path.abspath('dashboard.html'))
    print('Dashboard opened!')
conn.close()