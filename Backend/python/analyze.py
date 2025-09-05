import sys
import pandas as pd
import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for faster processing
import matplotlib.pyplot as plt
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

        # Create uploads folder if not exists  
        # Use /tmp on production, uploads locally
        output_dir = os.environ.get('CHART_DIR', '/tmp' if os.environ.get('RENDER') else 'uploads')
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, "chart.png")

        # Plot chart with optimizations
        plt.figure(figsize=(10, 6), dpi=80)  # Lower DPI for faster rendering
        plt.plot(df['Date'], df[price_column], label=f"{price_column} Price", color="blue", linewidth=1)
        plt.plot(df['Date'], df['50DMA'], label="50 DMA", color="orange", linewidth=1)
        plt.plot(df['Date'], df['100DMA'], label="100 DMA", color="green", linewidth=1)
        plt.plot(df['Date'], df['200DMA'], label="200 DMA", color="red", linewidth=1)

        plt.xlabel("Date")
        plt.ylabel(price_column + " Price")
        plt.title("Stock Price with Moving Averages")
        plt.legend()
        plt.grid(True, alpha=0.3)  # Lighter grid
        plt.tight_layout()
        plt.savefig(chart_path, dpi=80, bbox_inches='tight')  # Optimized save
        plt.close()

        # Return result as JSON
        # Always return relative path for URL construction
        relative_path = "uploads/chart.png" if output_dir.endswith('uploads') else "uploads/chart.png"
        
        result = {
            "message": "Analysis completed",
            "chartPath": relative_path
        }

        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
