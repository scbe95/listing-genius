import streamlit as st
from openai import OpenAI

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ListingGenius",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DARK MODE CSS (The New Look) ---
st.markdown("""
    <style>
    /* 1. Main Background - Dark Charcoal */
    .stApp {
        background-color: #0E1117;
    }
    
    /* 2. Text Colors - Make them White/Grey */
    h1 {
        color: #FFFFFF !important;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 700;
    }
    
    .subheader {
        text-align: center;
        color: #A0A0A0 !important; /* Light Grey */
        font-size: 18px;
        margin-bottom: 30px;
    }
    
    /* 3. Input Labels - Make them readable on dark background */
    .stSelectbox label, .stNumberInput label, .stMultiSelect label, .stSlider label {
        color: #FAFAFA !important;
        font-weight: 600;
    }
    
    /* 4. The "Generate" Button - Bright Green Accent */
    .stButton>button {
        width: 100%;
        background-color: #00D084; /* Green pops on dark */
        color: #0e1117; /* Dark text on button */
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #00b874;
        box-shadow: 0px 4px 15px rgba(0, 208, 132, 0.4);
        color: white;
    }

    /* 5. Hide the default Streamlit stuff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 6. Success Message Box */
    .stSuccess {
        background-color: #1c251d !important;
        color: #00D084 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR LOGIC ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = None
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ Connected to Groq Cloud")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.warning("⚠️ Manual Mode")
        api_key = st.text_input("Enter Groq Key", type="password")
    st.divider()
    st.markdown("© 2025 ListingGenius Inc.")

# --- 4. MAIN INTERFACE ---

# Title Section
st.markdown("<h1>🏡 ListingGenius</h1>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Turn basic details into captivating real estate descriptions.</div>", unsafe_allow_html=True)

st.write(" ") # Spacer

# Input Form (Streamlit handles dark mode inputs automatically)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        beds = st.selectbox("Bedrooms", ["Studio", "1", "2", "3", "4", "5+"])
        baths = st.selectbox("Bathrooms", ["1", "1.5", "2", "2.5", "3+"])
    with col2:
        sqft = st.number_input("Square Feet", value=1500, step=50)
        price = st.number_input("Listing Price ($)", value=450000, step=10000)

    features = st.multiselect(
        "Key Highlights",
        ["Pool", "Modern Kitchen", "Hardwood Floors", "Mountain View", "Close to Schools", "Newly Renovated", "Large Backyard", "Open Floor Plan"]
    )

    vibe = st.select_slider(
        "Tone of Voice",
        options=["Professional", "Balanced", "Luxury", "Cozy", "Urgent"]
    )

st.write(" ") # Spacer

# --- 5. GENERATION LOGIC ---
if st.button("✨ Write My Listing"):
    
    if not api_key:
        st.error("❌ System Error: API Key missing. Please check settings.")
    else:
        try:
            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )
            
            prompt = f"""
            Act as a professional real estate copywriter. Write a {vibe} listing description for a home with:
            - {beds} beds, {baths} baths, {sqft} sqft
            - Price: ${price:,}
            - Highlights: {', '.join(features)}
            
            Rules:
            1. Create a catchy headline first.
            2. Use engaging adjectives but avoid clichés.
            3. Optimize for SEO.
            4. Keep it under 200 words.
            """
            
            with st.spinner("Drafting description..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                st.markdown("### 📝 Generated Description")
                st.text_area("Copy your description:", value=result, height=300)
                st.balloons()
                
        except Exception as e:
            st.error(f"❌ Error: {e}")