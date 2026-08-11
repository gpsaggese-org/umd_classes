### **PyTorch Forecasting**

**Title**: Time Series Analysis using PyTorch Forecasting on Bitcoin Prices

**Difficulty**: 1 (easy)

**Description**:  
PyTorch Forecasting is a library built on top of PyTorch designed to make time series forecasting with neural networks simple and effective. It provides a high-level API to build powerful and complex models for time series prediction while abstracting much of the coding overhead associated with neural networks. This project will introduce you to the basic functionalities of PyTorch Forecasting using real-time Bitcoin price data to predict future trends.

**Describe technology**:

- **PyTorch Forecasting**: An open-source library that simplifies the process of designing and training neural networks for time series forecasting. It supports a range of models, evolves with the latest research, and is designed for ease of use, drawing on PyTorch's rich ecosystem.  
- Key concepts include:  
  - **TimeseriesDataset**: Prepares time series data for model training by handling encoding and normalizing.  
  - **Temporal Fusion Transformer (TFT)**: A model architecture for multi-horizon time series forecasting.  
  - **Rich Output**: Provides various diagnostic metrics and visualization options to evaluate model performance.

**Describe the project**:

- The project involves fetching real-time Bitcoin price data from a public API like CoinGecko.  
- **Step 1**: Use Python packages (requests, pandas) to pull and clean the Bitcoin price data, focusing on features like timestamp and price.  
- **Step 2**: Prepare the dataset using PyTorch Forecasting’s TimeseriesDataset for supervised learning, ensuring it's ready for neural network input.  
- **Step 3**: Implement a simple model using PyTorch Forecasting's Temporal Fusion Transformer or another model of your choice.  
- **Step 4**: Train the model to predict future Bitcoin prices based on historical data.  
- **Step 5**: Visualize the results and compare predicted prices against actual values using Matplotlib.

**Useful resources**:

- [PyTorch Forecasting Documentation](https://pytorch-forecasting.readthedocs.io/)  
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

**Is it free?**  
Yes, both PyTorch Forecasting and the CoinGecko API are free to use. You will need Python installed on your machine.

**Python libraries / bindings**:

- **PyTorch Forecasting**: Install via `pip install pytorch-forecasting`.  
- **PyTorch**: Required for PyTorch Forecasting; install via `pip install torch`.  
- **Requests**: For API calls, install via `pip install requests`.  
- **Pandas**: For data manipulation, install via `pip install pandas`.  
- **Matplotlib**: For visualization, install via `pip install matplotlib`.
