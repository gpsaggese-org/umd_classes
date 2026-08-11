### **Keras**

**Title**: Analyzing Bitcoin Prices with Keras and Time Series

**Difficulty**: 1 (easy)

**Description**  
This project involves building a simple time series model using Keras to analyze and predict Bitcoin price movements. Keras is a high-level neural networks library written in Python that simplifies the process of building deep learning models. Students will learn the basic functionalities of Keras by constructing a simple neural network and applying it to predict Bitcoin prices using historical data.

**Describe technology**

- **Keras**: An open-source high-level neural networks API, written in Python and capable of running on top of TensorFlow, CNTK, or Theano.  
- Designed for easy and fast prototyping.  
- Provides simple, consistent interface optimized for user-friendliness.  
- Supports both convolutional networks and recurrent networks, as well as combinations of the two.  
- Features include customizability, modularity, and ease of extensibility.

**Describe the project**

- **Data Acquisition**: Use Python libraries such as `pandas` and `requests` to fetch historical Bitcoin price data from a public API like CoinGecko.  
- **Data Preprocessing**: Clean the dataset and prepare it for time series analysis. This can include handling missing values, normalization, and splitting the data into training and testing sets.  
- **Model Building with Keras**:  
  - Develop a simple sequential model using Keras.  
  - Implement layers such as LSTM (Long Short-Term Memory) for handling time series data.  
  - Compile the model with an appropriate loss function, optimizer, and metrics.  
- **Training and Evaluation**:  
  - Train the model on the prepared dataset and evaluate its performance.  
  - Visualize results using plots to show actual vs. predicted prices.  
- **Deployment**:  
  - Use the trained model to make future forecasts on Bitcoin prices.  
  - Discuss potential improvements and next steps for more complex models.

**Useful resources**

- [Keras Documentation](https://keras.io/)  
- [TensorFlow Documentation](https://www.tensorflow.org/tutorials)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)

**Is it free?**  
Yes, Keras and its dependencies can be used for free. Libraries to fetch data (like `pandas` and `requests`) are also open-source.

**Python libraries / bindings**

- **Keras**: The primary library used for building the neural network models.  
- **TensorFlow**: The backend engine running Keras, facilitating model training and predictions.  
- **pandas**: For data manipulation and preprocessing.  
- **numpy**: For number handling and scientific computing.  
- **matplotlib**: For visualization of data and prediction results.  
- **requests**: For retrieving real-time and historical Bitcoin price data from APIs.

This project allows students to gain practical experience in using Keras for time series analysis and demonstrates how machine learning can be applied in cryptocurrency markets for predictive analytics.
