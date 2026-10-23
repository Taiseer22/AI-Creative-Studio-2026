import streamlit as st
import requests
import io
from PIL import Image
import os

# --- إعدادات الواجهة ---
st.set_page_config(page_title="استوديو الذكاء الاصطناعي 2026", layout="wide")
st.title("🎨 AI-Creative-Studio-2026")

# --- الحصول على المفتاح ---
HF_TOKEN = os.getenv("HF_TOKEN") or st.secrets.get("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"خطأ في الاتصال: {e}\n{response.text if 'response' in locals() else ''}")
        return None

# --- واجهة المستخدم ---
with st.sidebar:
    st.header("إعدادات التصميم")
    style = st.selectbox("نمط الصورة", ["سينمائي", "واقعي", "رسم رقمي", "أنمي"])
    st.info("تأكد من إضافة HF_TOKEN في Secrets")

# خريطة الأنماط للإنجليزي
style_map = {
    "سينمائي": "cinematic, dramatic lighting, 8k",
    "واقعي": "photorealistic, hyper-realistic, ultra detailed",
    "رسم رقمي": "digital painting, artstation trending",
    "أنمي": "anime style, studio ghibli"
}

prompt = st.text_area("أدخل وصف الصورة بالتفصيل (بالإنجليزي):", 
                     "A futuristic luxury car driving through a neon city at night")

if st.button("توليد الصورة فوراً ✨"):
    if not HF_TOKEN:
        st.warning("⚠️ لم يتم العثور على HF_TOKEN. ضيفه في Streamlit Secrets.")
        st.stop()
        
    final_prompt = f"{prompt}, {style_map.get(style, '')}"
    
    with st.spinner("جاري التواصل مع الخوادم السحابية..."):
        image_bytes = query({"inputs": final_prompt})
        if image_bytes:
            try:
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption=f"تم التوليد - النمط: {style}", use_container_width=True)
                st.success("تم التوليد بنجاح!")
            except Exception:
                st.error("السيرفر رجع نص مش صورة، غالباً الموديل نايم. جرب مرة ثانية بعد 20 ثانية.")
