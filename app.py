import streamlit as st
import requests
import io
from PIL import Image
import os

st.set_page_config(page_title="AI Creative Studio 2026", page_icon="🎨")
st.title("🎨 AI-Creative-Studio-2026")
st.write("ولّد صور سينمائية بـ Stable Diffusion XL")

HF_TOKEN = st.secrets.get("HF_TOKEN", "") if hasattr(st, 'secrets') else os.getenv("HF_TOKEN", "")

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

if "gallery" not in st.session_state:
    st.session_state.gallery = []

def query(payload):
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        return r.content
    except Exception as e:
        txt = r.text[:500] if 'r' in locals() and hasattr(r, 'text') else str(e)
        st.error(f"خطأ: {txt}")
        return None

with st.sidebar:
    st.header("Taiseer22 Studio")
    style = st.selectbox("النمط", ["سينمائي", "واقعي", "رسم رقمي", "انمي"])
    st.divider()
    st.info("تأكد من اضافة HF_TOKEN في Streamlit Secrets")

style_map = {
    "سينمائي": "cinematic, dramatic lighting, 8k, ultra detailed",
    "واقعي": "photorealistic, hyper-realistic, ultra detailed",
    "رسم رقمي": "digital painting, artstation trending",
    "انمي": "anime style, studio ghibli"
}

prompt = st.text_area("الوصف (انجليزي):", "A futuristic luxury car in Amman at night, cinematic lighting", height=100)

if st.button("توليد الصورة فوراً ✨", type="primary", use_container_width=True):
    if not HF_TOKEN:
        st.warning("ضيف HF_TOKEN في Secrets")
        st.stop()
    final_prompt = f"{prompt}, {style_map[style]}"
    with st.spinner("جاري التوليد... انتظر 30 ثانية"):
        img_bytes = query({"inputs": final_prompt})
        if img_bytes:
            try:
                image = Image.open(io.BytesIO(img_bytes))
                st.session_state.gallery.insert(0, image)
                st.image(image, caption="تم!")
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("📥 حمل", buf.getvalue(), "taiseer22.png", "image/png")
            except:
                st.error("الموديل لسه بصحى، جرب بعد 20 ثانية")

if st.session_state.gallery:
    st.divider()
    st.subheader(f"📸 معرضك - {len(st.session_state.gallery)} صورة")
    cols = st.columns(3)
    for i, img in enumerate(st.session_state.gallery):
        with cols[i % 3]:
            st.image(img, use_container_width=True)