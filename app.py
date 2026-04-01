import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# 1. Page Config
st.set_page_config(page_title="STYLÉ AI v2", layout="wide")

# 2. Setup Groq Client
client = Groq(api_key=st.secrets["GROQ_KEY"])

def encode_image(image):
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='PNG')
    return base64.b64encode(byte_arr.getvalue()).decode('utf-8')

st.title("👗 STYLÉ AI - Gallery Mode")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Gallery se photo select karein", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Your Upload", use_container_width=True)

with col2:
    if uploaded_file and st.button("Analyze My Style"):
        base64_image = encode_image(img)
        
        with st.spinner("Llama 3 AI is thinking..."):
            try:
                # Using Llama 3.2 Vision (Super Fast & Accurate)
                completion = client.chat.completions.create(
                   # Purana model hata kar ye naya wala dalo
model="llama-3.2-90b-vision-preview"
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "You are a luxury fashion expert. Analyze this outfit and give 3-4 lines of stylish advice in Hinglish. Be bold and elite."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }
                    ]
                )
                
                verdict = completion.choices[0].message.content
                st.markdown(f"""
                    <div style="background: #1e1e1e; padding: 20px; border-radius: 15px; border-left: 5px solid #FFD700;">
                        <h4 style="color: #FFD700;">AI VERDICT</h4>
                        <p style="color: white;">{verdict}</p>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Bhai, Groq mein bhi issue: {e}")
