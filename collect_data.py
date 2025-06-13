from crypto_etl import CryptoETLPipeline
import time

for i in range(5):
    print(f'Collection {i+1}/5')
    with CryptoETLPipeline('crypto_data.db') as pipeline:
        pipeline.run_pipeline(['bitcoin'])
    if i < 4:
        time.sleep(30)
print('Data collection complete!')