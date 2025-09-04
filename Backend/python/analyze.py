import sys
import pandas as pd
import json
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

        # Ensure Date is in datetime format and sorted
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

        # Calculate moving averages
        df['50DMA'] = df['Avg'].rolling(window=50).mean()
        df['100DMA'] = df['Avg'].rolling(window=100).mean()
        df['200DMA'] = df['Avg'].rolling(window=200).mean()

        # Create uploads folder if not exists  
        # Use /tmp on production, uploads locally
        output_dir = os.environ.get('CHART_DIR', '/tmp' if os.environ.get('RENDER') else 'uploads')
        print(f"DEBUG: Using output directory: {output_dir}", file=sys.stderr)
        os.makedirs(output_dir, exist_ok=True)
        chart_path = os.path.join(output_dir, "chart.png")
        print(f"DEBUG: Chart will be saved to: {chart_path}", file=sys.stderr)

        # Plot chart
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Avg'], label="Avg Price", color="blue")
        plt.plot(df['Date'], df['50DMA'], label="50 DMA", color="orange")
        plt.plot(df['Date'], df['100DMA'], label="100 DMA", color="green")
        plt.plot(df['Date'], df['200DMA'], label="200 DMA", color="red")

        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Stock Price with Moving Averages")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        
        # Verify file was created
        if os.path.exists(chart_path):
            print(f"DEBUG: Chart file created successfully at {chart_path}", file=sys.stderr)
        else:
            print(f"DEBUG: Chart file NOT created at {chart_path}", file=sys.stderr)

        # Return result as JSON
        # Always return relative path for URL construction
        relative_path = "uploads/chart.png" if output_dir.endswith('uploads') else "uploads/chart.png"
        
        result = {
            "message": "Analysis completed",
            "chartPath": relative_path
        }
        
        print(f"DEBUG: Returning result: {result}", file=sys.stderr)

        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
