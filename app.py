import streamlit as st
import requests
import io
from PIL import Image
import os

# --- إعدادات الواجهة ---
st.set_page_config(page_title="استوديو الذكاء الاصطناعي 2026", layout="wide")
st.title("🎨 AI-Creative-Studio-2026")
st.caption("ولّد صور سينمائية بـ Stable Diffusion XL")

# --- الحصول على المفتاح ---
HF_TOKEN = os.getenv("HF_TOKEN") or st.secrets.get("HF_TOKEN", None)

API_URL = "API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0""
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        text = response.text[:500] if 'response' in locals() and hasattr(response, 'text') else str(e)
        st.error(f"خطأ في الاتصال: {text}")
        return None

# --- واجهة المستخدم ---
with st.sidebar:
    st.header("إعدادات التصميم")
    style = st.selectbox("نمط الصورة", ["سينمائي", "واقعي", "رسم رقمي", "أنمي"])
    st.divider()
    st.info("💡 تأكد من إضافة HF_TOKEN في Streamlit Secrets")
    st.markdown("Made by Taiseer 2026")

# خريطة الأنماط للإنجليزي
style_map = {
    "سينمائي": "cinematic, dramatic lighting, 8k, highly detailed",
    "واقعي": "photorealistic, hyper-realistic, ultra detailed, 8k",
    "رسم رقمي": "digital painting, artstation trending, vibrant colors",
    "أنمي": "anime style, studio ghibli, beautiful anime art"
}

prompt = st.text_area("أدخل وصف الصورة بالتفصيل (بالإنجليزي):", 
                     "A futuristic luxury car driving through a neon city at night, rain reflection",
                     height=100)
if st.button("توليد الصورة فوراً ✨", type="primary", use_container_width=True):
    if not HF_TOKEN:
        st.warning("⚠️ لم يتم العثور على HF_TOKEN")
        st.stop()
        
    final_prompt = f"{prompt}, {style_map.get(style, '')}"
    
    with st.spinner("🎨 جاري التوليد..."):
        image_bytes = query({"inputs": final_prompt})
        if image_bytes:
            try:
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption=f"النمط: {style}", use_container_width=True)
                st.success("تم بنجاح!")
                
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 حمّل الصورة", buf.getvalue(), "AI_Studio_2026.png", "image/png", use_container_width=True)
            except Exception:
                st.error("الموديل نايم، جرب بعد 20 ثانية")
