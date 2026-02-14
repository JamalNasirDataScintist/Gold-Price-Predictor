@echo off
title Gold Price Predictor - Browser Voice
color 0A

echo ========================================
echo    GOLD PRICE VOICE AI
echo    Browser-based Voice Recognition
echo ========================================
echo.
echo Starting Streamlit app...
echo.
echo The app will open in your browser
echo Use Chrome or Edge for best voice results
echo.
echo Press Ctrl+C to stop
echo.

call venv\Scripts\activate.bat
streamlit run streamlit_app.py --server.port=8501

pause