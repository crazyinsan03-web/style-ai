import streamlit as st
from PIL import Image
import google.generativeai as genai  # <--- NAYA: AI Library

# 1. Page Config
st.set_page_config(page_title="STYLÉ AI | Luxury", page_icon="✨", layout="wide")

# 2. AI SETUP (Yahan apni Key daalo)
# Google AI Studio se key lo: https://aistudio.google.com/
# Is line ko dhundo aur apni key yahan paste karo:
# Purani line: genai.configure(api_key="AIzaSy...") 
# Nayi line ye likho:
# --- AI SETUP ---
# Is line ko check karo, secrets se key uthani hai
genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Model name ekdum simple rakho, bina 'models/' ya 'latest' ke
model = genai.GenerativeModel('gemini-1.5-flash')

# --- LUXURY CSS (Wahi purana wala) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Inter:wght@400&display=swap');
    .stApp {
        background: linear-gradient(-45deg, #0f0f0f, #1a1a1a, #2c0404, #000000);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .luxury-title {
        font-family: 'Playfair Display', serif;
        font-size: 55px;
        text-align: center;
        background: linear-gradient(to right, #fff, #FFD700, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    div.stButton > button {
        background: linear-gradient(45deg, #FFD700, #b8860b);
        color: black !important;
        font-weight: bold;
        border-radius: 50px;
        width: 100%;
    }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- UI CONTENT ---
st.markdown('<h1 class="luxury-title">STYLÉ AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #aaa; letter-spacing: 3px;">ELITE FASHION INTELLIGENCE</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📸 Upload Your Style")
    # Camera ki jagah File Uploader laga diya
    img_file_buffer = st.file_uploader("Gallery se photo select karein", type=['jpg', 'jpeg', 'png'])

with col2:
    st.markdown("### ✨ The Verdict")
    if img_file_buffer is not None:
        # Baaki saara logic same rahega
        img = Image.open(img_file_buffer)
        st.image(img, use_container_width=True)
        
        with st.spinner("Analyzing your elegance..."):
            try:
                prompt = "You are a luxury fashion expert. Analyze this outfit and give 3-4 lines of stylish advice in Hinglish. Be bold and elite."
                # Gemini ko ab uploaded image jayegi
                response = model.generate_content([prompt, img])
                verdict_text = response.text
            except Exception as e:
                verdict_text = f"Bhai, error aa gaya: {e}"

        st.markdown(f"""
            <div style="background: rgba(255,215,0,0.1); padding: 20px; border-radius: 15px; border-left: 5px solid #FFD700;">
                <h4 style="color: #FFD700; margin: 0;">AI ANALYSIS COMPLETE</h4>
                <p style="color: #eee; font-size: 0.9rem; margin-top: 10px;">
                    {verdict_text}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.button("Refine Look")
    else:
        st.info("System Ready. Please present your attire.")

st.markdown('<p style="text-align: center; color: #333; margin-top: 50px;">ESTABLISHED 2026 | POWERED BY ANISH</p>', unsafe_allow_html=True)
