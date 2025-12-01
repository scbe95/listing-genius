import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ListingGenius Pro",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. HIGH CONTRAST CSS ---
st.markdown("""
    <style>
    /* Main Background: Subtle Gradient (Black to Deep Blue) */
    .stApp {
        background: linear-gradient(to bottom, #000000, #0a192f);
    }
    
    /* The "Glass" Card Container */
    div.block-container {
        background-color: #112240; /* Lighter Navy */
        border: 1px solid #233554;
        border-radius: 15px;
        padding: 40px !important;
        margin-top: 40px;
        box-shadow: 0 10px 30px -10px rgba(2,12,27,0.7);
    }
    
    /* Headlines */
    h1 {
        color: #ccd6f6 !important; /* White-ish Blue */
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 700;
        margin-top: -20px;
    }
    
    .subtitle {
        text-align: center;
        color: #8892b0;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    /* Input Styling (Force Contrast) */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0a192f !important;
        color: white !important;
        border: 1px solid #233554;
    }
    
    .stNumberInput input {
        background-color: #0a192f !important;
        color: white !important;
        border: 1px solid #233554;
    }
    
    /* Labels */
    .stSelectbox label, .stNumberInput label, .stMultiSelect label, .stSlider label {
        color: #64ffda !important; /* Bright Teal Accent */
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* The Generate Button (Neon Green Accent) */
    .stButton>button {
        background-color: transparent;
        color: #64ffda;
        border: 1px solid #64ffda;
        border-radius: 4px;
        height: 50px;
        width: 100%;
        font-weight: bold;
        font-size: 16px;
        margin-top: 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: rgba(100, 255, 218, 0.1);
        box-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
        color: #64ffda;
        border: 1px solid #64ffda;
    }

    /* Stripe Button Style (In Sidebar) */
    [data-testid="stLinkButton"] {
        background-color: #FF4B4B !important; /* Red/Orange for Attention */
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    /* Hide Streamlit stuff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (BUSINESS LOGIC) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Logic
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ System Online")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.warning("⚠️ Manual Mode")
        api_key = st.text_input("Groq API Key", type="password")

    st.divider()

    # --- STRIPE PAYMENT SECTION ---
    st.markdown("### 💎 Go Pro")
    st.write("Get 2 months free with the Annual Plan.")
    
    # YOUR ANNUAL STRIPE LINK
    stripe_link = "https://buy.stripe.com/7sY5kCeBA5JJ8Uz5bh8og00"
    
    st.link_button("🚀 Upgrade Pro ($190/yr)", stripe_link)
    st.caption("Secure payment via Stripe")


# --- 4. MAIN INTERFACE ---

st.markdown("<h1>🏡 ListingGenius <span style='color:#64ffda'>Pro</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Real Estate Copywriter</div>", unsafe_allow_html=True)

# Inputs
col1, col2 = st.columns(2)
with col1:
    beds = st.selectbox("🛏️ Bedrooms", ["Studio", "1", "2", "3", "4", "5+"])
    baths = st.selectbox("🛁 Bathrooms", ["1", "1.5", "2", "2.5", "3+"])
with col2:
    sqft = st.number_input("📐 Square Feet", value=1500, step=50)
    price = st.number_input("💲 Asking Price", value=450000, step=10000)

st.write("") 

features = st.multiselect(
    "✨ Property Highlights",
    ["Pool", "Modern Kitchen", "Hardwood Floors", "Mountain View", "Close to Schools", "Newly Renovated", "Large Backyard", "Smart Home System"]
)

st.write("") 

vibe = st.select_slider(
    "🎭 Description Tone",
    options=["Professional", "Balanced", "Luxury", "Cozy", "Urgent"]
)

generate_btn = st.button("INITIALIZE GENERATOR")

# --- 5. LOGIC ---
if generate_btn:
    if not api_key:
        st.error("❌ API Key Missing.")
    else:
        try:
            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )
            
            prompt = f"""
            Act as a luxury real estate copywriter. Write a {vibe} listing description for a home with:
            - {beds} beds, {baths} baths, {sqft} sqft
            - Price: ${price:,}
            - Highlights: {', '.join(features)}
            
            Keep it under 180 words. High impact.
            """
            
            with st.spinner("Processing..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                st.markdown("### 📝 Output")
                st.text_area("Result:", value=result, height=350)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")