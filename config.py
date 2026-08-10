"""
إعدادات تطبيق AI Creative Studio 2026
Configuration file for AI Creative Studio
"""

import os
from datetime import datetime

# ============ أساسي / Basic ============
APP_NAME = "🎨 AI-Creative-Studio-2026"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "استوديو ذكاء اصطناعي متقدم لتوليد الصور والفيديوهات"

# ============ Hugging Face API ============
HF_TOKEN = os.getenv("HF_TOKEN", "")

# النماذج المتاحة / Available Models
MODELS = {
    "SDXL (الأسرع والأقوى)": {
        "url": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
        "description": "نموذج SDXL - جودة عالية وسرعة ممتازة",
        "best_for": "الصور الواقعية والفنية"
    },
    "Stable Diffusion 2.1": {
        "url": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
        "description": "نموذج SD 2.1 - متوازن وموثوق",
        "best_for": "الصور الفنية والإبداعية"
    },
    "Flux.1 (الأفضل)": {
        "url": "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
        "description": "نموذج Flux.1 - أحدث وأقوى نموذج",
        "best_for": "الصور عالية الجودة جداً"
    }
}

# الأنماط المتاحة / Available Styles
STYLES = {
    "سينمائي": "cinematic, film, movie quality, cinematography, lighting, composition",
    "واقعي": "photorealistic, hyperrealistic, 8k, detailed, sharp focus",
    "رسم رقمي": "digital art, concept art, digital painting, illustration",
    "أنمي": "anime, anime style, manga, 2D animation style",
    "خيال علمي": "sci-fi, futuristic, cyberpunk, neon, technology",
    "فنتازيا": "fantasy, magical, mystical, ethereal, enchanted",
    "ثلاثي الأبعاد": "3D render, CGI, 3D art, computer graphics",
    "رسم توضيحي": "illustration, artistic, hand-drawn style, sketch"
}

# ============ إعدادات التوليد / Generation Settings ============
DEFAULT_SETTINGS = {
    "steps": 30,           # عدد الخطوات (20-50)
    "guidance_scale": 7.5, # قوة التأثير (7-15)
    "height": 512,         # ارتفاع الصورة
    "width": 512,          # عرض الصورة
    "seed": -1             # -1 = عشوائي
}

IMAGE_SIZES = {
    "512x512": (512, 512),
    "576x576": (576, 576),
    "640x640": (640, 640),
    "768x768": (768, 768),
    "1024x1024": (1024, 1024),
}

# ============ المسارات / Paths ============
OUTPUT_DIR = "outputs"
HISTORY_DIR = "history"
TEMP_DIR = ".temp"

# إنشاء المجلدات إذا لم تكن موجودة / Create directories if not exist
for directory in [OUTPUT_DIR, HISTORY_DIR, TEMP_DIR]:
    os.makedirs(directory, exist_ok=True)

# ============ إعدادات Streamlit / Streamlit Settings ============
PAGE_CONFIG = {
    "page_title": "AI Creative Studio 2026",
    "page_icon": "🎨",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# ============ الألوان والتنسيق / Colors & Formatting ============
COLORS = {
    "success": "#00FF00",
    "error": "#FF4444",
    "warning": "#FFAA00",
    "info": "#00AAFF",
    "primary": "#6366F1",
    "secondary": "#EC4899"
}

# ============ الحدود والقيود / Limits ============
MAX_HISTORY_ITEMS = 20
MAX_RETRIES = 3
TIMEOUT_SECONDS = 120
MAX_PROMPT_LENGTH = 1000

# ============ رسائل / Messages ============
MESSAGES = {
    "ar": {
        "welcome": "مرحباً بك في استوديو الذكاء الاصطناعي! 🎨",
        "generating": "جاري توليد الصورة... قد يستغرق 30-60 ثانية ⏳",
        "success": "تم التوليد بنجاح! ✨",
        "error": "حدث خطأ: ",
        "no_token": "⚠️ لم يتم العثور على HF_TOKEN. أضفه في Secrets.",
        "empty_prompt": "⚠️ الرجاء إدخال وصف للصورة",
        "saved": "✅ تم حفظ الصورة في:",
        "retry": "إعادة محاولة...",
    },
    "en": {
        "welcome": "Welcome to AI Creative Studio! 🎨",
        "generating": "Generating image... This may take 30-60 seconds ⏳",
        "success": "Generated successfully! ✨",
        "error": "Error: ",
        "no_token": "⚠️ HF_TOKEN not found. Add it to Secrets.",
        "empty_prompt": "⚠️ Please enter an image description",
        "saved": "✅ Image saved at:",
        "retry": "Retrying...",
    }
}
