import streamlit as st
import time
import os
import pandas as pd
from datetime import datetime
import base64
import json

from fetch_data import fetch_gold_price
from data_store import save_price
from predictor import predict_next_price

# Import pyttsx3 for text-to-speech
try:
    import pyttsx3
    
    # Initialize TTS engine
    def init_tts():
        """Initialize text-to-speech engine"""
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)
            engine.setProperty("volume", 0.9)
            return engine
        except:
            return None
    
    tts_engine = init_tts()
    
    def speak(text):
        """Speak text using pyttsx3"""
        if tts_engine:
            try:
                tts_engine.say(text)
                tts_engine.runAndWait()
                return True
            except:
                return False
        return False
        
except ImportError:
    speak = lambda text: False
    print("pyttsx3 not available for TTS")

# ============================================================================
# STREAMLIT APP CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Gold Price Voice AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS & JAVASCRIPT
# ============================================================================

st.markdown("""
<style>
    /* Main Styles */
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #FFD700 0%, #DAA520 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 25px;
        color: white;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        margin: 10px 0;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Button Styles */
    .stButton button {
        width: 100%;
        border-radius: 15px;
        height: 70px;
        font-size: 20px;
        font-weight: bold;
        transition: all 0.3s;
        margin: 10px 0;
    }
    
    .voice-button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    .price-button {
        background: linear-gradient(135deg, #2196F3 0%, #0D47A1 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    .train-button {
        background: linear-gradient(135deg, #FF9800 0%, #E65100 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    /* Voice Recording Animation */
    .recording {
        animation: pulse 1.5s infinite !important;
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%) !important;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Status Messages */
    .success-box {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Voice Wave Animation */
    .voice-wave {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        margin: 20px 0;
    }
    
    .wave-bar {
        width: 6px;
        height: 20px;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        margin: 0 3px;
        border-radius: 3px;
        animation: wave 1.5s ease-in-out infinite;
    }
    
    .wave-bar:nth-child(2) { animation-delay: 0.1s; }
    .wave-bar:nth-child(3) { animation-delay: 0.2s; }
    .wave-bar:nth-child(4) { animation-delay: 0.3s; }
    .wave-bar:nth-child(5) { animation-delay: 0.4s; }
    .wave-bar:nth-child(6) { animation-delay: 0.5s; }
    .wave-bar:nth-child(7) { animation-delay: 0.6s; }
    
    @keyframes wave {
        0%, 100% { height: 20px; }
        50% { height: 60px; }
    }
</style>

<!-- JavaScript for Browser Voice Recognition -->
<script>
// Store voice input in Streamlit session state
function setVoiceText(text) {
    Streamlit.setComponentValue(text);
}

// Browser Voice Recognition
function startBrowserVoiceRecognition() {
    // Show recording status
    document.getElementById('voiceStatus').innerText = "🎤 Listening... Speak now!";
    document.getElementById('recordBtn').classList.add('recording');
    document.getElementById('voiceWave').style.display = 'flex';
    
    // Check browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert("Your browser doesn't support speech recognition. Please use Chrome, Edge, or Safari.");
        resetVoiceUI();
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    // Configure recognition
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;
    
    // Start recognition
    recognition.start();
    
    // Handle results
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        console.log("Voice recognized:", transcript);
        
        // Update UI
        document.getElementById('voiceStatus').innerText = "✅ Voice captured!";
        document.getElementById('recordBtn').classList.remove('recording');
        document.getElementById('voiceWave').style.display = 'none';
        
        // Send to Streamlit
        setVoiceText(transcript);
        
        // Auto-submit after short delay
        setTimeout(() => {
            document.getElementById('processVoiceBtn').click();
        }, 500);
    };
    
    // Handle errors
    recognition.onerror = function(event) {
        console.error("Speech recognition error:", event.error);
        document.getElementById('voiceStatus').innerText = "❌ Error: " + event.error;
        resetVoiceUI();
        
        if (event.error === 'not-allowed') {
            alert("Microphone access denied. Please allow microphone access and try again.");
        }
    };
    
    // Handle end
    recognition.onend = function() {
        console.log("Speech recognition ended");
        resetVoiceUI();
    };
}

function resetVoiceUI() {
    document.getElementById('recordBtn').classList.remove('recording');
    document.getElementById('voiceWave').style.display = 'none';
}

// Check microphone permission
async function checkMicrophonePermission() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(track => track.stop());
        return true;
    } catch (err) {
        console.error("Microphone permission denied:", err);
        return false;
    }
}

// Initialize on page load
window.addEventListener('load', async function() {
    const hasPermission = await checkMicrophonePermission();
    if (!hasPermission) {
        document.getElementById('voiceStatus').innerText = "⚠️ Microphone access required for voice commands";
    }
});
</script>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'last_price' not in st.session_state:
    st.session_state.last_price = None
if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None
if 'price_history' not in st.session_state:
    st.session_state.price_history = []
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = os.path.exists("models/gold_model.pkl")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("⚙️ Control Panel")
    
    st.markdown("---")
    
    # Auto-refresh
    auto_refresh = st.checkbox("🔄 Auto-refresh every 30s", value=False)
    
    st.markdown("---")
    
    # Data Management
    st.subheader("📊 Data Management")
    
    # Show data stats
    if os.path.exists("data/gold_prices.csv"):
        try:
            df = pd.read_csv("data/gold_prices.csv")
            st.metric("📈 Records", len(df))
            if len(df) > 0:
                latest = df.iloc[-1]
                st.metric("💰 Latest", f"${latest['price']:.2f}")
        except:
            pass
    
    # Train Model Button
    if st.button("🤖 Train Prediction Model", type="primary", use_container_width=True):
        try:
            import subprocess
            import sys
            
            # Create a placeholder for output
            output_placeholder = st.empty()
            
            # Run training in a subprocess
            result = subprocess.run(
                [sys.executable, "train_model.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                st.success("✅ Model trained successfully!")
                st.session_state.model_trained = True
                
                # Show training output
                with st.expander("📊 Training Output"):
                    st.code(result.stdout)
            else:
                st.error("❌ Training failed!")
                with st.expander("📋 Error Details"):
                    st.code(result.stderr)
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Clear Data Button
    if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
        if os.path.exists("data/gold_prices.csv"):
            os.remove("data/gold_prices.csv")
        if os.path.exists("models/gold_model.pkl"):
            os.remove("models/gold_model.pkl")
        st.session_state.last_price = None
        st.session_state.last_prediction = None
        st.session_state.price_history = []
        st.session_state.model_trained = False
        st.success("✅ All data cleared!")
        st.rerun()
    
    st.markdown("---")
    
    # Model Status
    st.subheader("🤖 Model Status")
    if st.session_state.model_trained:
        st.success("✅ Model is trained and ready!")
    else:
        st.warning("⚠️ Model needs training")
        st.info("Collect at least 5 price points, then click 'Train Model'")
    
    st.markdown("---")
    st.caption("Made with ❤️ using Python 3.10.11")

# ============================================================================
# MAIN CONTENT - HEADER
# ============================================================================

st.markdown('<h1 class="main-header">💰 Gold Price Voice AI Assistant</h1>', unsafe_allow_html=True)
st.markdown("### Speak or click to get real-time gold price predictions")

# Voice Recording Animation HTML
st.markdown("""
<div id="voiceWave" class="voice-wave" style="display: none;">
    <div class="wave-bar"></div>
    <div class="wave-bar"></div>
    <div class="wave-bar"></div>
    <div class="wave-bar"></div>
    <div class="wave-bar"></div>
    <div class="wave-bar"></div>
    <div class="wave-bar"></div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# VOICE COMMAND SECTION
# ============================================================================

st.markdown("---")
st.subheader("🎤 Voice Command")

col1, col2 = st.columns([1, 2])

with col1:
    # Voice recording button (triggers JavaScript)
    st.markdown("""
    <button id="recordBtn" class="voice-button" onclick="startBrowserVoiceRecognition()" style="padding: 20px; font-size: 18px;">
        🎤 Start Voice Recording
    </button>
    <div id="voiceStatus" style="margin-top: 10px; font-weight: bold; min-height: 30px;">
        Click button and speak
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Voice input display
    voice_input = st.text_input(
        "🎤 Voice Command:",
        value=st.session_state.get("voice_text", ""),
        key="voice_input_display",
        placeholder="What is the current gold price?"
    )
    
    # Process voice button (hidden trigger)
    process_pressed = st.button(
        "🚀 Process Voice Command",
        key="processVoiceBtn",
        type="primary",
        use_container_width=True
    )

# Process voice command
if process_pressed and voice_input:
    st.markdown(f'<div class="info-box">🗣️ <b>You said:</b> "{voice_input}"</div>', unsafe_allow_html=True)
    
    # Check if it's a gold price query
    query_words = ["gold", "price", "rate", "cost", "value", "how much", "what's", "current"]
    is_gold_query = any(word in voice_input.lower() for word in query_words)
    
    if is_gold_query:
        with st.spinner("📡 Fetching live gold price..."):
            try:
                # Fetch current gold price
                live_data = fetch_gold_price()
                save_price(live_data)
                
                # Store for display
                st.session_state.last_price = live_data["price"]
                
                # Make prediction if model exists
                if st.session_state.model_trained:
                    try:
                        prediction = predict_next_price(live_data["price"])
                        st.session_state.last_prediction = prediction
                    except Exception as e:
                        prediction = live_data["price"] * 1.01  # Fallback
                        st.session_state.last_prediction = prediction
                        st.warning(f"⚠️ Using fallback prediction")
                else:
                    prediction = live_data["price"]
                    st.session_state.last_prediction = prediction
                    st.warning("⚠️ Train model for accurate predictions")
                
                # Prepare voice response
                price_change = prediction - live_data["price"]
                if price_change > 0:
                    trend = "rising"
                    trend_emoji = "📈"
                else:
                    trend = "falling"
                    trend_emoji = "📉"
                
                response = (
                    f"The current gold price is ${live_data['price']:.2f} {live_data['currency']}. "
                    f"The predicted next price is ${prediction:.2f}. "
                    f"That's a {trend} trend. {trend_emoji}"
                )
                
                # Display response
                st.markdown(f'<div class="success-box">💰 <b>{response}</b></div>', unsafe_allow_html=True)
                
                # Speak the response
                if speak(response):
                    st.info("🔊 Response spoken")
                
                # Add to history
                st.session_state.price_history.append({
                    "time": datetime.now(),
                    "price": live_data["price"],
                    "prediction": prediction
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please ask about gold prices. Try saying 'What is the gold price?' or 'Current gold rate'")

# ============================================================================
# MANUAL PRICE CHECK
# ============================================================================

st.markdown("---")
st.subheader("📈 Manual Check")

if st.button("📊 Get Current Gold Price", key="manual_btn", type="secondary", use_container_width=True):
    with st.spinner("📡 Fetching live data..."):
        try:
            live_data = fetch_gold_price()
            save_price(live_data)
            
            st.session_state.last_price = live_data["price"]
            
            # Make prediction
            if st.session_state.model_trained:
                try:
                    prediction = predict_next_price(live_data["price"])
                    st.session_state.last_prediction = prediction
                except:
                    prediction = live_data["price"] * 1.01
                    st.session_state.last_prediction = prediction
            else:
                prediction = live_data["price"]
                st.session_state.last_prediction = prediction
            
            st.success(f"✅ Price fetched: ${live_data['price']:.2f} {live_data['currency']}")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

if st.session_state.last_price is not None:
    st.markdown("---")
    st.subheader("📊 Current Results")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Live Gold Price</h3>
            <h1>${st.session_state.last_price:.2f}</h1>
            <p>USD per ounce | Real-time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Predicted Price</h3>
            <h1>${st.session_state.last_prediction:.2f}</h1>
            <p>Next prediction | AI-powered</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Price change indicator
    if st.session_state.last_prediction:
        price_diff = st.session_state.last_prediction - st.session_state.last_price
        diff_percent = (price_diff / st.session_state.last_price) * 100
        
        if price_diff > 0:
            st.success(f"📈 Predicted increase: ${price_diff:.2f} ({diff_percent:.1f}%)")
        elif price_diff < 0:
            st.warning(f"📉 Predicted decrease: ${abs(price_diff):.2f} ({abs(diff_percent):.1f}%)")
        else:
            st.info("➡️ Price predicted to remain stable")

# ============================================================================
# PRICE HISTORY & CHART
# ============================================================================

try:
    if os.path.exists("data/gold_prices.csv"):
        st.markdown("---")
        st.subheader("📈 Price History")
        
        df = pd.read_csv("data/gold_prices.csv")
        if len(df) > 0:
            # Convert timestamp
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Display chart
            chart_data = df.set_index('timestamp')['price']
            st.line_chart(chart_data, use_container_width=True)
            
            # Statistics
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("Records", len(df))
            with col_stats2:
                if len(df) > 0:
                    st.metric("High", f"${df['price'].max():.2f}")
            with col_stats3:
                if len(df) > 0:
                    st.metric("Low", f"${df['price'].min():.2f}")
            
            # Data table
            with st.expander("📋 View Data Table", expanded=False):
                st.dataframe(
                    df.tail(10).sort_values('timestamp', ascending=False),
                    use_container_width=True,
                    column_config={
                        "timestamp": st.column_config.DatetimeColumn("Time"),
                        "price": st.column_config.NumberColumn("Price", format="$%.2f"),
                        "currency": "Currency"
                    }
                )
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="gold_prices.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("📝 No historical data yet. Fetch some prices first!")
except Exception as e:
    st.warning(f"Could not load historical data: {e}")

# ============================================================================
# INSTRUCTIONS
# ============================================================================

with st.expander("📖 How to Use This App", expanded=True):
    st.markdown("""
    ### 🎤 **Voice Commands (Browser-based):**
    1. Click **"Start Voice Recording"** button
    2. Allow microphone access when prompted
    3. Speak clearly (e.g., "What is the gold price?")
    4. The app will automatically process your command
    
    ### 📊 **Getting Started:**
    1. **First:** Click "Get Current Gold Price" to collect data
    2. **Repeat:** Click 5-10 times to collect enough data points
    3. **Train:** Click "Train Prediction Model" in sidebar
    4. **Use:** Now use voice commands for predictions!
    
    ### 💡 **Tips for Best Results:**
    - Speak clearly and close to microphone
    - Use phrases like:
        - "Gold price"
        - "Current gold rate"
        - "What's the price of gold?"
    - Collect at least 5 data points before training
    - More data = Better predictions
    
    ### 🔧 **Troubleshooting:**
    - **Microphone not working:** Ensure browser has microphone access
    - **Voice not recognized:** Try Chrome or Edge browser
    - **No predictions:** Train the model after collecting data
    - **API errors:** Check internet connection
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
footer_col1, footer_col2 = st.columns([3, 1])

with footer_col1:
    st.caption("💰 **Gold Price Voice AI** | Real-time predictions with browser voice recognition")
    st.caption("Python 3.10.11 | Streamlit | Machine Learning")

with footer_col2:
    if st.button("🔄 Refresh App"):
        st.rerun()

# Show last update time
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# AUTO-REFRESH FUNCTIONALITY
# ============================================================================

if auto_refresh:
    time.sleep(30)
    st.rerun()