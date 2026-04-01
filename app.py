import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="STYLÉ AI v2", layout="wide", page_icon="💃")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FFD700; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SETUP GROQ CLIENT ---
if "GROQ_KEY" not in st.secrets:
    st.error("Bhai, Secrets mein GROQ_KEY missing hai!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_KEY"])

def encode_image(image):
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='JPEG')
    return base64.b64encode(byte_arr.getvalue()).decode('utf-8')

# --- 3. UI LAYOUT ---
st.title("✨ STYLÉ AI - Your Personal Elite Stylist")
st.write("Gallery se photo upload karo aur AI se verdict lo.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Upload Your Look")
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        # Display image
        st.image(img, caption="Ready for Analysis", use_container_width=True)

with col2:
    st.subheader("💎 AI Fashion Verdict")
    
    if uploaded_file:
        if st.button("Analyze My Style"):
            # Convert image to base64
            base64_image = encode_image(img)
            
            with st.spinner("Analyzing your elegance..."):
                try:
                    # LATEST WORKING MODEL: llama-3.2-90b-vision-preview
                    completion = client.chat.completions.create(
                        model="llama-3.2-90b-vision-preview",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "You are a luxury fashion expert. Analyze this outfit and give 3-4 lines of stylish advice in Hinglish. Be bold, elite, and slightly witty."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ],
                        temperature=0.7,
                        max_tokens=500
                    )
                    
                    verdict = completion.choices[0].message.content
                    
                    # Stylish Display Box
                    st.markdown(f"""
                        <div style="background: rgba(255, 215, 0, 0.1); padding: 25px; border-radius: 15px; border: 1px solid #FFD700;">
                            <h3 style="color: #FFD700; margin-top: 0;">ELITE ANALYSIS</h3>
                            <p style="color: white; font-size: 1.1rem; line-height: 1.6;">
                                {verdict}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e
