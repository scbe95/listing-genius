import streamlit as st
from openai import OpenAI

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ListingGenius AI", page_icon="🏠", layout="centered")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Initialize the key variable
    api_key = None
    
    # --- NEW LOGIC: Check Secrets First ---
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ API Key loaded from Cloud Secrets")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        # If not found, ask for it manually
        st.warning("⚠️ No Secret found. Running in Manual Mode.")
        api_key = st.text_input("Paste Groq API Key", type="password")
    # --------------------------------------

    st.divider()
    st.markdown("Powered by **Groq** & **Llama 3.1**")

# --- MAIN APP UI ---
st.title("🏠 ListingGenius")
st.write("Generate professional real estate descriptions in seconds.")

# Input Form
col1, col2 = st.columns(2)
with col1:
    beds = st.selectbox("Bedrooms", ["Studio", "1", "2", "3", "4", "5+"])
    baths = st.selectbox("Bathrooms", ["1", "1.5", "2", "2.5", "3+"])
with col2:
    sqft = st.number_input("Square Feet", value=1500, step=50)
    price = st.number_input("Price ($)", value=450000, step=10000)

features = st.multiselect(
    "Key Features",
    ["Pool", "Modern Kitchen", "Hardwood Floors", "Mountain View", "Close to Schools", "Newly Renovated", "Large Backyard"]
)

vibe = st.radio("Tone", ["Professional", "Luxury/Elegant", "Cozy/Family-Friendly"], horizontal=True)

# --- GENERATION LOGIC ---
if st.button("✨ Generate Description", type="primary"):
    
    if not api_key:
        st.error("❌ Please set your API Key in the Sidebar (or Cloud Secrets) to continue.")
    else:
        try:
            # Connect to Groq
            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )
            
            prompt = f"""
            Write a {vibe} real estate listing description for a house with:
            - {beds} beds, {baths} baths
            - {sqft} sqft, priced at ${price}
            - Features: {', '.join(features)}
            Make it catchy, SEO-friendly for Zillow, and use about 150 words.
            """
            
            with st.spinner("🤖 AI is writing..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                st.success("✅ Description Generated!")
                st.text_area("Copy your description:", value=result, height=250)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")