import sys
import pandas as pd
import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for faster processing
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import os

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "File path not provided"}))
        return

    file_path = sys.argv[1]

    try:
        # Check file type
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Upload CSV or XLSX.")

        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        # Check for required columns and standardize
        if 'Date' not in df.columns:
            raise ValueError("Missing 'Date' column")
            
        # Handle both 'Avg' and 'Close' columns
        price_column = None
        if 'Avg' in df.columns:
            price_column = 'Avg'
        elif 'Close' in df.columns:
            price_column = 'Close'
        else:
            raise ValueError("Missing price column. Need either 'Avg' or 'Close' column")

        # Ensure Date is in datetime format and sorted
        # Try multiple date formats automatically
        try:
            df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
        except:
            # If automatic parsing fails, try common formats
            date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y', '%m-%d-%Y']
            parsed = False
            for fmt in date_formats:
                try:
                    df['Date'] = pd.to_datetime(df['Date'], format=fmt)
                    parsed = True
                    break
                except:
                    continue
            if not parsed:
                raise ValueError("Unable to parse Date column. Please use standard date format (YYYY-MM-DD, MM/DD/YYYY, etc.)")
        
        df = df.sort_values('Date')

        # Calculate moving averages using the price column
        df['50DMA'] = df[price_column].rolling(window=50).mean()
        df['100DMA'] = df[price_column].rolling(window=100).mean()
        df['200DMA'] = df[price_column].rolling(window=200).mean()
        
        # Prepare data for prediction
        prediction_days = 7  # Predict next 7 days
        lookback_days = 30   # Use last 30 days for training
        
        predictions = []
        prediction_dates = []
        
        if len(df) >= lookback_days:
            # Get recent data for prediction
            recent_data = df.tail(lookback_days).copy()
            
            # Create features for ML model
            recent_data['price_lag1'] = recent_data[price_column].shift(1)
            recent_data['price_lag2'] = recent_data[price_column].shift(2)
            recent_data['ma_ratio'] = recent_data[price_column] / recent_data['50DMA']
            recent_data['price_change'] = recent_data[price_column].pct_change()
            
            # Remove NaN values
            recent_data = recent_data.dropna()
            
            if len(recent_data) >= 10:  # Need minimum data for prediction
                # Prepare features and target
                features = ['price_lag1', 'price_lag2', 'ma_ratio', 'price_change']
                X = recent_data[features].values
                y = recent_data[price_column].values
                
                # Scale features
                scaler_X = MinMaxScaler()
                scaler_y = MinMaxScaler()
                X_scaled = scaler_X.fit_transform(X)
                y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).flatten()
                
                # Train model
                model = LinearRegression()
                model.fit(X_scaled, y_scaled)
                
                # Generate predictions
                last_price = df[price_column].iloc[-1]
                last_ma = df['50DMA'].iloc[-1]
                
                for i in range(prediction_days):
                    # Create features for next day
                    if i == 0:
                        price_lag1 = df[price_column].iloc[-1]
                        price_lag2 = df[price_column].iloc[-2]
                    else:
                        price_lag1 = predictions[-1]
                        price_lag2 = predictions[-2] if len(predictions) > 1 else df[price_column].iloc[-1]
                    
                    ma_ratio = price_lag1 / last_ma if last_ma > 0 else 1
                    price_change = (price_lag1 - df[price_column].iloc[-2]) / df[price_column].iloc[-2] if df[price_column].iloc[-2] > 0 else 0
                    
                    # Prepare feature vector
                    next_features = np.array([[price_lag1, price_lag2, ma_ratio, price_change]])
                    next_features_scaled = scaler_X.transform(next_features)
                    
                    # Make prediction
                    pred_scaled = model.predict(next_features_scaled)[0]
                    pred_price = scaler_y.inverse_transform([[pred_scaled]])[0][0]
                    
                    predictions.append(pred_price)
                    
                    # Generate prediction date
                    last_date = df['Date'].iloc[-1]
                    pred_date = last_date + pd.Timedelta(days=i+1)
                    prediction_dates.append(pred_date.strftime('%Y-%m-%d'))

        # Create uploads folder if not exists  
        # Use /tmp on production, uploads locally
        output_dir = os.environ.get('CHART_DIR', '/tmp' if os.environ.get('RENDER') else 'uploads')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, "chart.png")

        # Create figure with subplots
        if predictions and prediction_dates:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=80)
            
            # Main chart - Historical Analysis
            ax1.plot(df['Date'], df[price_column], label=f"{price_column} Price", color="blue", linewidth=1.5)
            ax1.plot(df['Date'], df['50DMA'], label="50 DMA", color="orange", linewidth=1)
            ax1.plot(df['Date'], df['100DMA'], label="100 DMA", color="green", linewidth=1)
            ax1.plot(df['Date'], df['200DMA'], label="200 DMA", color="red", linewidth=1)
            ax1.set_xlabel("Date")
            ax1.set_ylabel(price_column + " Price")
            ax1.set_title("Stock Price Analysis with Moving Averages")
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Prediction chart - Future Forecast
            pred_dates = pd.to_datetime(prediction_dates)
            
            # Show last 10 days of actual data for context
            context_data = df.tail(10)
            ax2.plot(context_data['Date'], context_data[price_column], label="Recent Actual Price", color="blue", linewidth=2, alpha=0.7)
            
            # Plot predictions
            ax2.plot(pred_dates, predictions, label="Predicted Price", color="purple", linewidth=2, marker='o', markersize=5)
            
            # Connect last actual to first prediction
            connection_dates = [df['Date'].iloc[-1], pred_dates[0]]
            connection_prices = [df[price_column].iloc[-1], predictions[0]]
            ax2.plot(connection_dates, connection_prices, color="gray", linewidth=1, linestyle=':', alpha=0.7)
            
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Predicted " + price_column + " Price")
            ax2.set_title(f"7-Day Price Prediction (Linear Regression Model)")
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(chart_path, dpi=80, bbox_inches='tight')
            plt.close()
        else:
            # Single chart when no predictions
            plt.figure(figsize=(12, 6), dpi=80)
            plt.plot(df['Date'], df[price_column], label=f"{price_column} Price", color="blue", linewidth=1.5)
            plt.plot(df['Date'], df['50DMA'], label="50 DMA", color="orange", linewidth=1)
            plt.plot(df['Date'], df['100DMA'], label="100 DMA", color="green", linewidth=1)
            plt.plot(df['Date'], df['200DMA'], label="200 DMA", color="red", linewidth=1)
            plt.xlabel("Date")
            plt.ylabel(price_column + " Price")
            plt.title("Stock Price Analysis with Moving Averages")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(chart_path, dpi=80, bbox_inches='tight')
            plt.close()

        # Return result as JSON
        # Always return relative path for URL construction
        relative_path = "uploads/chart.png" if output_dir.endswith('uploads') else "uploads/chart.png"
        
        result = {
            "message": "Analysis completed",
            "chartPath": relative_path,
            "predictions": predictions,
            "predictionDates": prediction_dates,
            "hasPredictions": len(predictions) > 0
        }

        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
