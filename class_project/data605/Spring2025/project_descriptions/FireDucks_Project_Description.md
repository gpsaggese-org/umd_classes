### **FireDucks**

**Title**: High-Speed Bitcoin Time Series Analysis with FireDucks  
**Difficulty**: 1 (easy)  
**Description**  
**Describe technology**  
**FireDucks** is a compiler-accelerated Python dataframe library optimized for speed and pandas compatibility. Key features:

- **Pandas-like syntax**: Seamlessly replace `pandas` with minimal code changes.  
- **Query optimization**: Automatic parallelization and efficient memory management.  
- **TPU/CPU acceleration**: Leverage multi-core systems (e.g., Google Colab TPUs) for large datasets.  
  Example: Process 1M+ Bitcoin price records 5-10x faster than vanilla pandas.


**Describe the project**  
Build a real-time Bitcoin price analysis pipeline using FireDucks to demonstrate its performance advantages over pandas. Steps:

1. **Setup**:  
   - Use Google Colab with a **v2-8 TPU runtime** (high CPU cores/memory).  
   - Install FireDucks (`pip install fireducks`) and enable its import hook.  
2. **Data Ingestion**:  
   - Fetch hourly Bitcoin price data (Jan 2023–present) from CoinGecko API.  
   - Load into FireDucks DataFrame:

   

```py
%load_ext fireducks.pandas  # Magic command for Jupyter  
import fireducks.pandas as pd  
btc_df = pd.read_csv("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365")  
```

   

3. **Time Series Analysis**:  
   - Resample daily prices and compute:  
     - 30-day rolling volatility.  
     - Weekly average closing price.  
   - Compare execution time vs pandas (using `%%timeit` in Jupyter).  
4. **Visualization**:  
   - Plot price trends and volatility with `matplotlib`.  
   - Bonus: Process 10x larger synthetic dataset to stress-test FireDucks.

   

**Useful resources**

- [FireDucks GitHub](https://github.com/fireducks/fireducks) (TPU demo notebooks included)  
- [CoinGecko API Docs](https://www.coingecko.com/en/api)  
- [FireDucks vs Pandas vs Polars Demo](https://github.com/fireducks/fireducks/blob/main/examples/FireDucks_vs_Pandas_vs_Polars.ipynb)

**Is it free?**  
Yes. FireDucks is BSD-licensed, and CoinGecko’s API has a free tier. Google Colab TPUs are free for basic usage.

**Python libraries / bindings**

- `fireducks`: Core library (replace `pandas`).  
- `requests`: Fetch CoinGecko data.  
- `matplotlib`: Visualization.  
-
