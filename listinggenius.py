import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ListingGenius Pro",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. PROFESSIONAL STYLING (CSS) ---
st.markdown("""
    <style>
    /* Main Background: Deep Blue-Black */
    .stApp {
        background-color: #0E1117;
    }
    
    /* The "Card" Container */
    .css-1r6slb0, .stContainer {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    
    /* Headlines */
    h1 {
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-align: center;
        letter-spacing: -1px;
    }
    
    /* Sub-text */
    .subtitle {
        text-align: center;
        color: #8B949E;
        font-size: 16px;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    
    /* Input Labels */
    .stSelectbox label, .stNumberInput label, .stMultiSelect label {
        color: #C9D1D9 !important;
        font-weight: 500;
    }
    
    /* The Generate Button (Gradient) */
    .stButton>button {
        background: linear-gradient(45deg, #238636, #2EA043);
        color: white;
        border: none;
        border-radius: 8px;
        height: 50px;
        width: 100%;
        font-weight: bold;
        font-size: 16px;
        margin-top: 10px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (Secrets) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = None
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ License Key Active")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.info("running locally? Paste key below.")
        api_key = st.text_input("Groq API Key", type="password")

# --- 4. MAIN INTERFACE ---

# Header
st.markdown("<h1>🏡 ListingGenius</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Real Estate Copywriter</div>", unsafe_allow_html=True)

# The "Control Panel" Card
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        beds = st.selectbox("🛏️ Bedrooms", ["Studio", "1", "2", "3", "4", "5+"])
        baths = st.selectbox("🛁 Bathrooms", ["1", "1.5", "2", "2.5", "3+"])
    with col2:
        sqft = st.number_input("📐 Square Feet", value=1500, step=50)
        price = st.number_input("💲 Asking Price", value=450000, step=10000)

    st.write("") # Spacer
    
    features = st.multiselect(
        "✨ Property Highlights",
        ["Pool", "Modern Kitchen", "Hardwood Floors", "Mountain View", "Close to Schools", "Newly Renovated", "Large Backyard", "Smart Home System"]
    )
    
    st.write("") # Spacer

    vibe = st.select_slider(
        "🎭 Description Tone",
        options=["Professional", "Balanced", "Luxury", "Cozy", "Urgent"]
    )
    
    st.write("") # Spacer
    
    # Generate Button
    generate_btn = st.button("✨ GENERATE LISTING")

# --- 5. OUTPUT SECTION ---
if generate_btn:
    if not api_key:
        st.error("❌ API Key Missing. Please check Settings.")
    else:
        try:
            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )
            
            # Prompt Engineering
            prompt = f"""
            Act as a luxury real estate copywriter. Write a {vibe} listing description for a home with:
            - {beds} beds, {baths} baths, {sqft} sqft
            - Price: ${price:,}
            - Highlights: {', '.join(features)}
            
            Structure:
            1. HEADLINE: catchy and short (ALL CAPS).
            2. BODY: Engaging narrative, focusing on lifestyle.
            3. CLOSING: Call to action.
            
            No emojis in the text body. Keep it under 180 words.
            """
            
            with st.spinner("Drafting high-converting copy..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                # Result Display
                st.write("")
                st.markdown("### 📝 Your Listing Draft")
                st.text_area("Copy to Zillow/MLS:", value=result, height=350)
                st.success("Draft generated successfully!")
                
        except Exception as e:
            st.error(f"❌ Error: {e}")