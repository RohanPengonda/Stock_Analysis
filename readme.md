# Live : https://stock-analysis-kohl.vercel.app/

# 📈 Stock Data Analysis Tool

A full-stack web application for analyzing stock market data with interactive visualizations. Upload CSV/Excel files containing stock data and get instant technical analysis with moving averages and trend charts.

## 🚀 Features

- **File Upload**: Support for CSV and Excel (.xlsx, .xls) files
- **Data Processing**: Automated calculation of 50, 100, and 200-day moving averages
- **Visualization**: Interactive charts showing price trends and moving averages
- **Real-time Analysis**: Instant processing and chart generation
- **Responsive UI**: Modern, mobile-friendly interface with Tailwind CSS

## 🛠️ Tech Stack

### Frontend

- **React.js** - User interface framework
- **Vite** - Build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests

### Backend

- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **Multer** - File upload middleware
- **CORS** - Cross-origin resource sharing

### Data Processing

- **Python** - Data analysis engine
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Chart generation
- **NumPy** - Numerical computing
- **openpyxl** - Excel file processing

## 📁 Project Structure

```
T2-Stock_Analysis/
├── Backend/
│   ├── controllers/
│   │   └── uploadControllers.js    # File upload logic
│   ├── middleware/
│   │   └── upload.js              # Multer configuration
│   ├── python/
│   │   └── analyze.py             # Python analysis script
│   ├── routes/
│   │   └── uploadRoutes.js        # API routes
│   ├── services/
│   │   └── pythonService.js       # Python integration
│   ├── uploads/                   # Uploaded files storage
│   ├── package.json
│   └── server.js                  # Express server
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadFile.jsx     # Main upload component
│   │   │   └── ShowData.jsx       # Data display component
│   │   ├── App.jsx                # Root component
│   │   └── main.jsx               # Entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔧 Installation & Setup

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.7 or higher)
- npm or yarn

### 1. Clone the Repository

```bash
git clone <repository-url>
cd T2-Stock_Analysis
```

### 2. Backend Setup

```bash
cd Backend
npm install
```

### 3. Python Dependencies

```bash
cd Backend
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd Frontend
npm install
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd Backend
npm start
```

Server runs on: `http://localhost:5000`

### Start Frontend Development Server

```bash
cd Frontend
npm run dev
```

Frontend runs on: `http://localhost:5173`

## 📊 How It Works

### 1. File Upload Process

- User selects CSV/Excel file through the web interface
- Frontend validates file format and sends to backend via REST API
- Backend uses Multer middleware to handle file upload and storage

### 2. Data Processing Pipeline

- Backend triggers Python script with uploaded file path
- Python script reads data using Pandas
- Calculates moving averages (50, 100, 200-day)
- Generates matplotlib chart and saves as PNG

### 3. Visualization & Response

- Python returns analysis results to Node.js backend
- Backend serves generated chart image via static file serving
- Frontend displays the chart with real-time updates

## 📋 File Format Requirements

Your CSV/Excel file must contain these columns:

- **Date**: Date in standard format (YYYY-MM-DD, MM/DD/YYYY, etc.)
- **Avg**: Average stock price (numeric values)

### Example CSV Format:

```csv
Date,Avg
2024-01-01,150.25
2024-01-02,152.30
2024-01-03,148.75
```

## 🎯 Key Components

### Frontend Components

- **UploadFile.jsx**: Main component handling file selection, upload, and chart display
- **App.jsx**: Root application component

### Backend Services

- **uploadControllers.js**: Handles file upload requests and coordinates analysis
- **pythonService.js**: Manages Python script execution and data exchange
- **upload.js**: Configures file upload middleware with validation

### Python Analysis

- **analyze.py**: Core data processing script that calculates moving averages and generates charts

## 🔍 Technical Analysis Features

- **50-Day Moving Average**: Short-term trend indicator
- **100-Day Moving Average**: Medium-term trend indicator
- **200-Day Moving Average**: Long-term trend indicator
- **Price Visualization**: Historical price data with trend lines
- **Interactive Charts**: Responsive charts with hover details

## 🛡️ Security Features

- File type validation (CSV/Excel only)
- File size limitations
- CORS configuration for secure cross-origin requests
- Input sanitization and error handling

## 🚀 Deployment

### Backend (Render)

1. Push code to GitHub
2. Connect repository to Render
3. Set Root Directory: `Backend`
4. Environment Variables:
   ```
   PYTHON_CMD=python3
   BASE_URL=https://your-app.onrender.com
   FRONTEND_URL=https://your-frontend.vercel.app
   CHART_DIR=/tmp
   ```

### Frontend (Vercel)

1. Connect repository to Vercel
2. Set Root Directory: `Frontend`
3. Environment Variables:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```

## 🚨 Troubleshooting

### Error Messages

- "Please select a file first" - No file chosen for upload
- "Only CSV/Excel files are allowed" - Invalid file format
- "Failed to analyze file" - Data processing error (check file structure)

## ⚡ Performance Notes

- **File Cleanup**: Uploaded files are automatically deleted after processing
- **Chart Optimization**: Uses optimized matplotlib settings for faster rendering

## 📄 License

This project is open source and available under the MIT License.

---
