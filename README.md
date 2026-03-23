# Stock-Market-Live-Dataset

This project uses an LSTM (Long Short-Term Memory) neural network to predict the stock price of Tata Motors based on historical data. The data is fetched from Yahoo Finance, and the model is trained on the `Close` prices over a period from 2010 to 2024.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Data Source](#data-source)
4. [Model Architecture](#model-architecture)
5. [How to Run the Project](#how-to-run-the-project)
6. [Results](#results)
7. [License](#license)

---

## Project Overview

The goal of this project is to predict future stock prices using a deep learning model (LSTM). The steps include:

- Fetching stock data using the Yahoo Finance API.
- Preprocessing and normalizing the data.
- Training an LSTM model.
- Predicting and visualizing future stock prices.

---

## Technologies Used

- **Python**
- **NumPy**
- **Pandas**
- **Matplotlib**
- **Yahoo Finance API (yfinance)**
- **TensorFlow/Keras**
- **Scikit-Learn**

---

## Data Source

The historical stock data for Tata Motors is retrieved using Yahoo Finance (`yfinance`). The data spans from **January 1, 2010** to **November 28, 2024**.

---

## Model Architecture

The LSTM model consists of:

- 4 LSTM layers with varying units (50, 60, 80, 120)
- Dropout layers for regularization (0.2, 0.3, 0.4, 0.5)
- 1 Dense layer for output

### Model Summary

```
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
lstm (LSTM)                  (None, 100, 50)           10400     
_________________________________________________________________
dropout (Dropout)            (None, 100, 50)           0         
_________________________________________________________________
lstm_1 (LSTM)                (None, 100, 60)           26640     
_________________________________________________________________
dropout_1 (Dropout)          (None, 100, 60)           0         
_________________________________________________________________
lstm_2 (LSTM)                (None, 100, 80)           45120     
_________________________________________________________________
dropout_2 (Dropout)          (None, 100, 80)           0         
_________________________________________________________________
lstm_3 (LSTM)                (None, 120)               96480     
_________________________________________________________________
dropout_3 (Dropout)          (None, 120)               0         
_________________________________________________________________
dense (Dense)                (None, 1)                 121       
=================================================================
Total params: 178,761
Trainable params: 178,761
Non-trainable params: 0
_________________________________________________________________
```

---

## How to Run the Project

### Prerequisites

Ensure you have the following libraries installed:

```bash
pip install numpy pandas matplotlib yfinance scikit-learn tensorflow
```

### Steps to Run

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PranavKarwa2004/Stock-Market-Live-Dataset.git
   cd Stock-Market-Live-Dataset
   ```

2. **Run the Python script**:

   ```bash
   python stock_prediction.py
   ```

3. **Output**:

   The script will download the data, train the model, and produce a plot comparing the original and predicted stock prices.

---

## Results

The model predicts future `Close` prices based on historical data. Below is a sample output visualization:

![Stock Price Prediction](assets/stock_price_prediction.png)

- **Blue Line**: Original Prices
- **Red Line**: Predicted Prices

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
