**Description**

In this project, students will use PyTorch Lightning, a lightweight wrapper for PyTorch, to streamline the training and evaluation of deep learning models. This tool simplifies the process of building complex models while providing built-in features for logging, checkpointing, and distributed training. Its modular design allows students to focus on the model architecture and training logic without getting bogged down in boilerplate code.

Technologies Used
PyTorch Lightning

- Provides a high-level interface for PyTorch, reducing boilerplate code.
- Supports multi-GPU training and TPU support for scalable training.
- Integrates seamlessly with popular logging frameworks (e.g., TensorBoard, WandB).
- Facilitates model checkpointing and early stopping.

---

### Project 1: Image Classification on CIFAR-10 (Difficulty: 1)

**Project Objective:**
Develop a convolutional neural network (CNN) to classify images from the CIFAR-10 dataset, optimizing for accuracy and minimizing classification errors.

**Dataset Suggestions:**
- CIFAR-10 dataset, available at [Kaggle CIFAR-10](https://www.kaggle.com/c/cifar-10).

**Tasks:**
- Data Preparation:
  - Load the CIFAR-10 dataset and split it into training and validation sets.
  - Apply data augmentation techniques to enhance model generalization.

- Model Definition:
  - Build a CNN architecture using PyTorch Lightning.
  - Implement dropout and batch normalization to improve performance.

- Training:
  - Train the model with appropriate loss functions and optimizers.
  - Use PyTorch Lightning's built-in logging to monitor training metrics.

- Evaluation:
  - Evaluate the model on the validation set and analyze misclassifications.
  - Visualize sample predictions and confusion matrix using Matplotlib.

---

### Project 2: Time Series Forecasting with LSTM (Difficulty: 2)

**Project Objective:**
Create a Long Short-Term Memory (LSTM) model to predict stock prices based on historical data, optimizing for prediction accuracy and minimizing forecast error.

**Dataset Suggestions:**
- Historical stock prices from Yahoo Finance, accessible via the `yfinance` library or directly from [Yahoo Finance](https://finance.yahoo.com/).

**Tasks:**
- Data Collection:
  - Fetch historical stock price data for a chosen company (e.g., Apple Inc.) using the `yfinance` library.
  - Preprocess the data for LSTM input, including normalization and sequence creation.

- Model Development:
  - Define an LSTM architecture using PyTorch Lightning.
  - Implement dropout layers to prevent overfitting.

- Training and Validation:
  - Train the model with a suitable loss function (e.g., Mean Squared Error).
  - Use early stopping to prevent overfitting and save the best model.

- Forecasting:
  - Generate future stock price predictions and visualize the results against actual prices.
  - Analyze prediction errors and discuss potential improvements.

---

### Project 3: Text Classification with BERT (Difficulty: 3)

**Project Objective:**
Build a text classification model using a pre-trained BERT model to classify movie reviews as positive or negative, optimizing for F1 score and minimizing classification errors.

**Dataset Suggestions:**
- IMDb movie reviews dataset, available at [Kaggle IMDb Dataset](https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews).

**Tasks:**
- Data Preparation:
  - Load and preprocess the IMDb dataset, including text cleaning and tokenization using Hugging Face's `transformers` library.
  - Split the dataset into training, validation, and test sets.

- Model Setup:
  - Utilize a pre-trained BERT model with PyTorch Lightning for text classification.
  - Fine-tune the model on the IMDb dataset while implementing custom training loops.

- Training:
  - Train the model with appropriate hyperparameters and a suitable optimizer (e.g., AdamW).
  - Implement logging for loss and accuracy metrics.

- Evaluation:
  - Evaluate the model on the test set and compute classification metrics (accuracy, precision, recall, F1 score).
  - Visualize the confusion matrix and analyze misclassified reviews.

**Bonus Ideas (Optional):**
- Experiment with different pre-trained models (e.g., DistilBERT or RoBERTa) to compare performance.
- Implement additional text preprocessing techniques, such as stemming or lemmatization.
- Explore the use of attention visualization to interpret model predictions.

