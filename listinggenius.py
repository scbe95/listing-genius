import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ListingGenius Pro",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. HIGH CONTRAST CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background: linear-gradient(to bottom, #000000, #0a192f); }
    
    /* Card Container */
    div.block-container { padding-top: 2rem; }
    
    /* Input Styling */
    .stSelectbox div[data-baseweb="select"] > div, .stNumberInput input, .stTextArea textarea {
        background-color: #112240 !important; color: white !important; border: 1px solid #233554;
    }
    .stSelectbox label, .stNumberInput label, .stMultiSelect label, .stSlider label, .stTextArea label {
        color: #64ffda !important; font-weight: 600;
    }
    
    /* Button Styles */
    div.stButton > button:first-child {
        background-color: transparent; color: #64ffda; border: 1px solid #64ffda;
        border-radius: 4px; height: 50px; width: 100%; font-weight: bold; margin-top: 10px;
    }
    div.stButton > button:first-child:hover {
        background-color: rgba(100, 255, 218, 0.1); color: #64ffda;
    }

    /* Output Box Styling (Right Side) */
    .stTextArea textarea {
        font-family: "Courier New", Courier, monospace;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'generations' not in st.session_state:
    st.session_state.generations = 0
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""

FREE_LIMIT = 3
stripe_link = "https://buy.stripe.com/7sY5kCeBA5JJ8Uz5bh8og00"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=50)
    st.header("ListingGenius")
    
    if "GROQ_API_KEY" in st.secrets:
        st.success(" System Online")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.warning(" Manual Mode")
        api_key = st.text_input("Groq API Key", type="password")

    st.divider()
    st.write(f"**Daily Usage:** {st.session_state.generations}/{FREE_LIMIT}")
    st.progress(st.session_state.generations / FREE_LIMIT)
    
    if st.session_state.generations >= FREE_LIMIT:
        st.error(" Limit Reached")
    
    st.markdown("###  Go Pro")
    st.link_button(" Upgrade Pro ($19/yr)", stripe_link)

# --- 5. MAIN INTERFACE (SPLIT SCREEN) ---

c1, c2 = st.columns([1, 8])
with c1:
    st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=80) 
with c2:
    st.markdown("<h1 style='text-align: left; color: #ccd6f6;'>ListingGenius <span style='color:#64ffda'>Pro</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8892b0;'>AI-Powered Real Estate Copywriter</p>", unsafe_allow_html=True)

st.write("")

# --- SPLIT LAYOUT ---
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown("### 1. Property Details")
    
    c_a, c_b = st.columns(2)
    with c_a:
        beds = st.selectbox("🛏️ Bedrooms", ["Studio", "1", "2", "3", "4", "5+"])
        baths = st.selectbox("🛁 Bathrooms", ["1", "1.5", "2", "2.5", "3+"])
    with c_b:
        sqft = st.number_input("📐 Square Feet", value=1500, step=50)
        price = st.number_input("💲 Asking Price", value=450000, step=10000)

    features = st.multiselect("✨ Highlights", ["Pool", "Modern Kitchen", "Hardwood Floors", "Mountain View", "Close to Schools", "Newly Renovated", "Large Backyard"])
    
    # --- NEW: CUSTOM INPUT BOX ---
    custom_details = st.text_area("📝 Additional Details (Optional)", placeholder="e.g. Historic fireplace, Tesla solar roof, walking distance to subway...")
    # -----------------------------

    vibe = st.select_slider("🎭 Tone", options=["Professional", "Balanced", "Luxury", "Cozy", "Urgent"])

    st.link_button(" Unlock Unlimited Access ($19/yr)", stripe_link, use_container_width=True)

    # Logic Check
    generate_btn = False
    if st.session_state.generations < FREE_LIMIT:
        st.info(f"⚡ {FREE_LIMIT - st.session_state.generations} free generations left.")
        generate_btn = st.button("INITIALIZE GENERATOR")
    else:
        st.error(f" Daily limit reached.")

with right_col:
    st.markdown("### 2. Generated Description")
    
    # OUTPUT LOGIC
    if generate_btn:
        if not api_key:
            st.error("❌ API Key Missing.")
        else:
            try:
                # 1. Setup the container
                result_box = st.empty()
                full_response = ""
                
                # 2. Call AI (Updated Prompt)
                client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
                
                # We add the custom details to the prompt here
                prompt = f"""
                Write a {vibe} real estate description. 
                - {beds} bed, {baths} bath, {sqft} sqft, ${price}. 
                - Features: {features}.
                - Important Extra Details: {custom_details}
                
                No emojis in body. Keep it under 200 words.
                """
                
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                
                # 3. Stream the text
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        result_box.markdown(full_response)
                
                # 4. Finalize
                st.session_state.last_result = full_response
                st.session_state.generations += 1
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {e}")

    # DISPLAY SAVED RESULT (Persistent)
    if st.session_state.last_result:
        st.text_area("Copy your description:", value=st.session_state.last_result, height=400)
    elif not generate_btn:
        st.info("👈 Enter details on the left and hit Generate.")
