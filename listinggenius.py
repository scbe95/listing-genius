import streamlit as st
from openai import OpenAI

# --- 1. PAGE CONFIGURATION (Browser Tab) ---
st.set_page_config(
    page_title="ListingGenius | AI Real Estate",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CUSTOM CSS ( The "Makeover" ) ---
# This hides the default Streamlit style and adds your own "SaaS" look
st.markdown("""
    <style>
    /* Background Color */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Center the Title and Style it */
    h1 {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    /* Style the Subheader */
    .subheader {
        text-align: center;
        color: #7f8c8d;
        font-size: 18px;
        margin-bottom: 30px;
    }
    
    /* Make the Button look like a "Pro" Call-to-Action */
    .stButton>button {
        width: 100%;
        background-color: #2980b9;
        color: white;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        font-size: 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3498db;
        color: white;
        border: none;
    }

    /* Hide the Streamlit Hamburger Menu and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR LOGIC (Hidden by default now) ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = None
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ License Key Active")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.warning("⚠️ Manual Mode")
        api_key = st.text_input("Enter Key", type="password")
    st.divider()
    st.markdown("© 2025 ListingGenius Inc.")

# --- 4. THE MAIN UI ---

# Hero Section (Centered)
st.markdown("<h1>🏡 ListingGenius</h1>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Turn basic details into captivating real estate descriptions in seconds.</div>", unsafe_allow_html=True)

st.write("---") # A subtle divider line

# The Input Form (Card Style)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        beds = st.selectbox("🛏️ Bedrooms", ["Studio", "1", "2", "3", "4", "5+"])
        baths = st.selectbox("🛁 Bathrooms", ["1", "1.5", "2", "2.5", "3+"])
    with col2:
        sqft = st.number_input("📐 Square Feet", value=1500, step=50)
        price = st.number_input("💲 Listing Price", value=450000, step=10000)

    features = st.multiselect(
        "✨ Key Highlights",
        ["Pool", "Modern Kitchen", "Hardwood Floors", "Mountain View", "Close to Schools", "Newly Renovated", "Large Backyard", "Open Floor Plan"]
    )

    vibe = st.select_slider(
        "🎭 Tone of Voice",
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
            
            # More professional prompt
            prompt = f"""
            Act as a professional real estate copywriter. Write a {vibe} listing description for a home with:
            - {beds} beds, {baths} baths, {sqft} sqft
            - Price: ${price:,}
            - Highlights: {', '.join(features)}
            
            Rules:
            1. Create a catchy headline first.
            2. Use engaging adjectives but avoid clichés.
            3. Optimize for SEO (Zillow/Redfin).
            4. Keep it under 200 words.
            """
            
            with st.spinner("Drafting description..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                # Output Section
                st.markdown("### 📝 Your Description")
                st.text_area("Copy and paste this:", value=result, height=300)
                st.balloons() # Fun effect on success
                
        except Exception as e:
            st.error(f"❌ Error: {e}")