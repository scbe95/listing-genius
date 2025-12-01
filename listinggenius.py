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
    /* Main Background */
    .stApp {
        background: linear-gradient(to bottom, #000000, #0a192f);
    }
    
    /* Card Container */
    div.block-container {
        background-color: #112240;
        border: 1px solid #233554;
        border-radius: 15px;
        padding: 40px !important;
        margin-top: 40px;
        box-shadow: 0 10px 30px -10px rgba(2,12,27,0.7);
    }
    
    /* Typography */
    h1 { color: #ccd6f6 !important; font-family: 'Helvetica', sans-serif; font-weight: 700; }
    .subtitle { text-align: center; color: #8892b0; font-size: 16px; margin-bottom: 30px; }
    
    /* Inputs */
    .stSelectbox div[data-baseweb="select"] > div, .stNumberInput input {
        background-color: #0a192f !important;
        color: white !important;
        border: 1px solid #233554;
    }
    
    /* Button Styles */
    div.stButton > button:first-child {
        background-color: transparent;
        color: #64ffda;
        border: 1px solid #64ffda;
        border-radius: 4px;
        height: 50px;
        width: 100%;
        font-weight: bold;
        font-size: 16px;
        margin-top: 10px;
    }
    div.stButton > button:first-child:hover {
        background-color: rgba(100, 255, 218, 0.1);
        border: 1px solid #64ffda;
        color: #64ffda;
    }

    /* Hide Streamlit stuff */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE (USAGE TRACKER) ---
if 'generations' not in st.session_state:
    st.session_state.generations = 0

FREE_LIMIT = 3
stripe_link = "https://buy.stripe.com/7sY5kCeBA5JJ8Uz5bh8og00"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ System Online")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.warning("⚠️ Manual Mode")
        api_key = st.text_input("Groq API Key", type="password")

    st.divider()
    
    # Show Usage in Sidebar
    st.write(f"**Daily Usage:** {st.session_state.generations}/{FREE_LIMIT}")
    st.progress(st.session_state.generations / FREE_LIMIT)
    
    # Logic if limit is hit in sidebar
    if st.session_state.generations >= FREE_LIMIT:
        st.error("🚫 Limit Reached")
    
    st.markdown("### 💎 Go Pro")
    st.write("Unlimited access. Just $19/year.") # Updated Text
    st.link_button("🚀 Upgrade Pro ($19/yr)", stripe_link) # Updated Text


# --- 5. MAIN INTERFACE ---

st.markdown("<h1>🏡 ListingGenius <span style='color:#64ffda'>Pro</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Real Estate Copywriter</div>", unsafe_allow_html=True)

# Special Offer Button (Updated for $19 pricing)
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.link_button("💎 Unlock Unlimited Access ($19/yr)", stripe_link, use_container_width=True)

st.write("") 

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
    ["Pool", "Modern Kitchen", "Hardwood Floors", "Mountain View", "Close to Schools", "Newly Renovated", "Large Backyard"]
)

vibe = st.select_slider("🎭 Tone", options=["Professional", "Balanced", "Luxury", "Cozy", "Urgent"])

# --- 6. LOGIC WITH LIMIT CHECK ---

if st.session_state.generations < FREE_LIMIT:
    st.info(f"⚡ You have {FREE_LIMIT - st.session_state.generations} free generations left today.")
    generate_btn = st.button("INITIALIZE GENERATOR")
else:
    # DISABLE BUTTON AND SHOW UPSELL
    st.error(f"❌ You have hit your daily limit ({FREE_LIMIT}).")
    st.markdown(f"""
        <div style="text-align:center;">
            <p style="color:white; margin-bottom:10px;">Remove all limits for just $19/year.</p>
            <a href="{stripe_link}" target="_blank" style="background-color:#FF4B4B; color:white; padding:15px 30px; border-radius:5px; text-decoration:none; font-weight:bold; font-size:18px;">
                🚀 UNLOCK NOW &rarr;
            </a>
        </div>
    """, unsafe_allow_html=True)
    generate_btn = False

if generate_btn:
    if not api_key:
        st.error("❌ API Key Missing.")
    else:
        try:
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
            prompt = f"Write a {vibe} real estate description. {beds} bed, {baths} bath, {sqft} sqft, ${price}. Features: {features}."
            
            with st.spinner("Processing..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                # INCREMENT COUNTER
                st.session_state.generations += 1
                
                st.markdown("### 📝 Output")
                st.text_area("Result:", value=result, height=350)
                
                # RERUN to update the counter visual immediately
                st.rerun() 
                
        except Exception as e:
            st.error(f"❌ Error: {e}")