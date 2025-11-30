import streamlit as st
from openai import OpenAI

# --- PAGE SETUP ---
st.set_page_config(page_title="ListingGenius AI", page_icon="🏠")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("Get a free key at [console.groq.com/keys](https://console.groq.com/keys)")
    
    # ASK FOR GROQ KEY
    api_key = st.text_input("Groq API Key", type="password", help="Paste your Groq key here.")
    
    st.divider()
    st.info("💡 **Note:** We are using the free Llama 3.1 model via Groq!")

# --- MAIN APP UI ---
st.title("🏠 ListingGenius")
st.subheader("Generate pro real estate descriptions in seconds.")

# 1. Inputs (The "Form")
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

# --- THE LOGIC ---
if st.button("✨ Generate Description", type="primary"):
    
    if not api_key:
        # --- SIMULATION MODE ---
        st.warning("⚠️ No API Key detected. Running in SIMULATION MODE.")
        st.success("Here is a **SIMULATED** description (Paste Groq Key for real results):")
        fake_response = (
            f"Welcome to this stunning {beds}-bedroom, {baths}-bath home! "
            f"Priced at ${price:,}, this {sqft} sqft gem features {', '.join(features)}. "
            f"Written in a {vibe} tone, this property is perfect for buyers looking for value. "
            "(Note: This is a placeholder. Enter a Groq key for unique descriptions!)"
        )
        st.text_area("Result:", value=fake_response, height=200)
    
    else:
        # --- REAL AI MODE (Groq / Llama 3.1) ---
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
            
            with st.spinner("🤖 Llama 3.1 is writing (super fast)..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant", # <--- UPDATED MODEL NAME
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                st.success("✅ AI Description Generated!")
                st.text_area("Copy this to Zillow:", value=result, height=250)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- MONETIZATION (Placeholder) ---
st.divider()
st.markdown("""
<center>
    <small>Powered by Groq (Free Tier).</small><br>
    <a href="#" style="text-decoration:none;">
        <button style="background-color:#4CAF50; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;">
            🚀 Support this App
        </button>
    </a>
</center>
""", unsafe_allow_html=True)