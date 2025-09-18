import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional, Input
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import ta  # For technical indicators

# =========================
# STEP 1: Load and Clean Data
# =========================
INPUT_XLSX = "Data.csv"  # Change this to your file path
df = pd.read_csv(INPUT_XLSX)

# Clean Price and other numeric columns (remove commas and convert to float)
numeric_cols = ['Price', 'Open', 'High', 'Low']
for col in numeric_cols:
    df[col] = df[col].astype(str).str.replace(',', '').astype(float)

# Clean Volume (convert K and M to numbers)
def convert_volume(val):
    val = str(val).replace(',', '')
    if 'M' in val:
        return float(val.replace('M', '')) * 1e6
    elif 'K' in val:
        return float(val.replace('K', '')) * 1e3
    else:
        return float(val)

df['Vol.'] = df['Vol.'].apply(convert_volume)

# Convert Date
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df.sort_values('Date', inplace=True)

# =========================
# STEP 2: Feature Engineering (Technical Indicators)
# =========================
df['SMA_10'] = df['Price'].rolling(window=10).mean()
df['EMA_10'] = df['Price'].ewm(span=10, adjust=False).mean()
df['RSI'] = ta.momentum.RSIIndicator(df['Price'], window=14).rsi()
df['MACD'] = ta.trend.MACD(df['Price']).macd()
df.fillna(method='bfill', inplace=True)

# =========================
# STEP 3: Select Features
# =========================
features = ['Price', 'Open', 'High', 'Low', 'Vol.', 'SMA_10', 'EMA_10', 'RSI', 'MACD']
data = df[features].values

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# =========================
# STEP 4: Prepare Data for LSTM
# =========================
time_step = 60
def create_dataset(dataset, time_step):
    X, Y = [], []
    for i in range(len(dataset) - time_step - 1):
        X.append(dataset[i:(i + time_step)])
        Y.append(dataset[i + time_step][0])  # Price column
    return np.array(X), np.array(Y)

X, y = create_dataset(scaled_data, time_step)

# Split into train & test
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# =========================
# STEP 5: Build LSTM Model with Attention
# =========================
inputs = Input(shape=(time_step, X.shape[2]))
x = Bidirectional(LSTM(128, return_sequences=True))(inputs)
x = Dropout(0.3)(x)
x = Bidirectional(LSTM(64, return_sequences=True))(x)

# Attention Layer (Fixed)
attention = tf.keras.layers.Dense(1)(x)
attention = tf.keras.layers.Flatten()(attention)
attention = tf.keras.layers.Activation('softmax')(attention)
attention = tf.keras.layers.RepeatVector(128)(attention)
attention = tf.keras.layers.Permute([2, 1])(attention)
context_vector = tf.keras.layers.Multiply()([x, attention])
context_vector = tf.keras.layers.Lambda(lambda z: tf.reduce_sum(z, axis=1))(context_vector)

# Output layer
outputs = Dense(1)(context_vector)

model = Model(inputs, outputs)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mean_squared_error')

early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)

print(model.summary())

# =========================
# STEP 6: Train Model
# =========================
history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
                    epochs=100, batch_size=32, callbacks=[early_stop, lr_scheduler], verbose=1)

# =========================
# STEP 7: Predictions
# =========================
predictions = model.predict(X_test)

# Prepare full shape for inverse transform
scaled_back_pred = np.zeros((len(predictions), scaled_data.shape[1]))
scaled_back_pred[:, 0] = predictions[:, 0]
scaled_back_pred = scaler.inverse_transform(scaled_back_pred)
predicted_price = scaled_back_pred[:, 0]

# Actual values
scaled_back_actual = np.zeros((len(y_test), scaled_data.shape[1]))
scaled_back_actual[:, 0] = y_test
scaled_back_actual = scaler.inverse_transform(scaled_back_actual)
actual_price = scaled_back_actual[:, 0]

# =========================
# STEP 8: Evaluate
# =========================
rmse = np.sqrt(mean_squared_error(actual_price, predicted_price))
r2 = r2_score(actual_price, predicted_price)
print(f"RMSE: {rmse}")
print(f"R² Score: {r2}")

# =========================
# STEP 9: Plot Results
# =========================
plt.figure(figsize=(12, 6))
plt.plot(actual_price, color='blue', label='Actual Price')
plt.plot(predicted_price, color='red', label='Predicted Price')
plt.title('NSE Price Prediction (LSTM + Attention)')
plt.xlabel('Days')
plt.ylabel('Price')
plt.legend()
plt.show()
