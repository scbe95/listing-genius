import streamlit as st
from openai import OpenAI

# --- PAGE SETUP ---
st.set_page_config(page_title="ListingGenius AI", page_icon="🏠")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # --- THE NEW LOGIC STARTS HERE ---
    # Check if the key is saved in Streamlit Cloud Secrets
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ API Key loaded from Cloud Secrets")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        # If running locally (and you haven't set up local secrets), ask for it
        st.info("💡 **Tip:** running locally? Paste key below.")
        api_key = st.text_input("Groq API Key", type="password")
    # --- END NEW LOGIC ---

    st.divider()
    st.info("Powered by Groq & Llama 3.1")

# --- MAIN APP UI ---
st.title("🏠 ListingGenius")
st.subheader("Generate pro real estate descriptions in seconds.")

# Inputs
col1, col2 = st.columns(2)
with col1:
    beds = st.selectbox("Bedrooms", ["Studio", "1", "2", "3", "4", "5+"])
    baths = st.selectbox("Bathrooms", ["1", "1.5", "2", "2.5", "3+"])
with col2:
    sqft = st.number_input("Square Feet", value=1500, step=50)
    price = st.number_input("Listing Price ($)", value=450000, step=10000)

features = st.multiselect(
    "Key Features",
    ["Pool", "Modern Kitchen", "Hardwood Floors", "Mountain View", "Close to Schools", "Newly Renovated", "Large Backyard"]
)

vibe = st.radio("Description Vibe", ["Professional", "Luxury/Elegant", "Cozy/Family-Friendly"], horizontal=True)

# --- GENERATE BUTTON ---
if st.button("✨ Generate Description", type="primary"):
    
    if not api_key:
        st.warning("⚠️ No API Key found. Please set it in Secrets or Sidebar.")
    else:
        try:
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
                st.text_area("Copy this:", value=result, height=250)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")