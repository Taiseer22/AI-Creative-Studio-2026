"""
دوال مساعدة لتطبيق AI Creative Studio
Utility functions for AI Creative Studio
"""

import os
import json
import requests
import io
from PIL import Image
from datetime import datetime
import time
import streamlit as st
from config import (
    OUTPUT_DIR, HISTORY_DIR, MAX_HISTORY_ITEMS, 
    MESSAGES, TIMEOUT_SECONDS, MAX_RETRIES
)

# ============ إدارة الملفات / File Management ============

def get_timestamp():
    """الحصول على الطابع الزمني بصيغة قابلة للقراءة"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_filename_timestamp():
    """الحصول على الطابع الزمني لأسماء الملفات"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save_image(image_bytes, prompt, model, style):
    """
    حفظ الصورة المولدة مع معلومات عنها
    Save generated image with metadata
    """
    try:
        # إنشاء اسم الملف / Create filename
        timestamp = get_filename_timestamp()
        filename = f"image_{timestamp}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # حفظ الصورة / Save image
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        
        # حفظ البيانات الوصفية / Save metadata
        metadata = {
            "timestamp": get_timestamp(),
            "prompt": prompt,
            "model": model,
            "style": style,
            "filename": filename,
            "filesize_kb": os.path.getsize(filepath) / 1024
        }
        
        metadata_file = filepath.replace(".png", ".json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # إضافة إلى السجل / Add to history
        add_to_history(metadata)
        
        return filepath, metadata
    except Exception as e:
        st.error(f"❌ خطأ في حفظ الصورة: {str(e)}")
        return None, None

# ============ إدارة السجل / History Management ============

def add_to_history(metadata):
    """إضافة صورة إلى السجل"""
    history_file = os.path.join(HISTORY_DIR, "history.json")
    
    try:
        # قراءة السجل الحالي / Read current history
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []
        
        # إضافة العنصر الجديد / Add new item
        history.insert(0, metadata)
        
        # الاحتفاظ بآخر N عنصر فقط / Keep only last N items
        history = history[:MAX_HISTORY_ITEMS]
        
        # حفظ السجل / Save history
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"خطأ في حفظ السجل: {e}")
        return False

def get_history():
    """الحصول على قائمة السجل"""
    history_file = os.path.join(HISTORY_DIR, "history.json")
    
    try:
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"خطأ في قراءة السجل: {e}")
        return []

def clear_history():
    """مسح السجل بالكامل"""
    history_file = os.path.join(HISTORY_DIR, "history.json")
    try:
        if os.path.exists(history_file):
            os.remove(history_file)
        return True
    except Exception as e:
        print(f"خطأ في مسح السجل: {e}")
        return False

# ============ احصائيات الاستخدام / Usage Statistics ============

def get_statistics():
    """الحصول على إحصائيات الاستخدام"""
    history = get_history()
    
    stats = {
        "total_images": len(history),
        "last_generated": history[0]["timestamp"] if history else "لم يتم بعد",
        "models_used": list(set([item.get("model", "unknown") for item in history])),
        "styles_used": list(set([item.get("style", "unknown") for item in history])),
    }
    
    # حساب إجمالي حجم الملفات / Calculate total file size
    total_size = 0
    for item in history:
        total_size += item.get("filesize_kb", 0)
    stats["total_size_mb"] = round(total_size / 1024, 2)
    
    return stats

def display_statistics():
    """عرض الإحصائيات في Streamlit"""
    stats = get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 إجمالي الصور", stats["total_images"])
    
    with col2:
        st.metric("💾 الحجم الكلي", f"{stats['total_size_mb']} MB")
    
    with col3:
        st.metric("🎬 نماذج مستخدمة", len(stats["models_used"]))
    
    with col4:
        st.metric("🎨 أنماط مستخدمة", len(stats["styles_used"]))

# ============ API Requests ============

def query_image_generation(payload, api_url, headers, retries=MAX_RETRIES):
    """
    طلب توليد صورة من API مع إعادة محاولة
    Query image generation API with retry logic
    """
    for attempt in range(retries):
        try:
            response = requests.post(
                api_url, 
                headers=headers, 
                json=payload,
                timeout=TIMEOUT_SECONDS
            )
            
            if response.status_code == 200:
                return response.content, None
            
            elif response.status_code == 503:  # Model loading
                if attempt < retries - 1:
                    wait_time = 10 * (attempt + 1)
                    st.warning(f"⏳ النموذج يحمل... انتظر {wait_time} ثانية")
                    time.sleep(wait_time)
                    continue
                else:
                    return None, f"النموذج لم يكن جاهزاً بعد المحاولات ({retries})"
            
            else:
                error_msg = response.text
                return None, f"خطأ API ({response.status_code}): {error_msg}"
        
        except requests.exceptions.Timeout:
            error = f"انتهاء المهلة الزمنية (محاولة {attempt + 1}/{retries})"
            if attempt < retries - 1:
                st.warning(f"⏳ {error}... إعادة محاولة")
                time.sleep(5)
            else:
                return None, error
        
        except Exception as e:
            return None, f"خطأ: {str(e)}"
    
    return None, "فشلت جميع المحاولات"

# ============ معالجة الصور / Image Processing ============

def resize_image_for_display(image, max_width=600):
    """تغيير حجم الصورة للعرض"""
    image.thumbnail((max_width, max_width), Image.Resampling.LANCZOS)
    return image

def bytes_to_image(image_bytes):
    """تحويل bytes إلى صورة PIL"""
    try:
        return Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        st.error(f"خطأ في تحويل الصورة: {e}")
        return None

def image_to_bytes(image):
    """تحويل صورة PIL إلى bytes"""
    try:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue()
    except Exception as e:
        st.error(f"خطأ في تحويل الصورة: {e}")
        return None

# ============ التحقق من البيانات / Validation ============

def validate_prompt(prompt, max_length=1000):
    """التحقق من صحة النص الوصفي"""
    if not prompt or not prompt.strip():
        return False, MESSAGES["ar"]["empty_prompt"]
    
    if len(prompt) > max_length:
        return False, f"⚠️ النص طويل جداً (الحد الأقصى: {max_length} حرف)"
    
    return True, "✅"

def validate_settings(steps, guidance_scale, height, width):
    """التحقق من صحة الإعدادات"""
    errors = []
    
    if not (20 <= steps <= 50):
        errors.append("عدد الخطوات يجب أن يكون بين 20 و 50")
    
    if not (7 <= guidance_scale <= 15):
        errors.append("قوة التأثير يجب أن تكون بين 7 و 15")
    
    if height not in [512, 576, 640, 768, 1024]:
        errors.append("ارتفاع الصورة غير صحيح")
    
    if width not in [512, 576, 640, 768, 1024]:
        errors.append("عرض الصورة غير صحيح")
    
    return len(errors) == 0, errors

# ============ تنسيق النصوص / Text Formatting ============

def format_prompt_with_style(prompt, style_keywords):
    """دمج الوصف مع كلمات النمط"""
    if style_keywords:
        return f"{prompt}, {style_keywords}"
    return prompt

def create_enhanced_prompt(prompt, style_keywords, quality="high"):
    """إنشاء prompt محسّن"""
    quality_keywords = {
        "high": "high quality, detailed, professional, masterpiece",
        "ultra": "ultra high quality, 8k, intricate details, award-winning",
        "standard": "good quality, clear"
    }
    
    enhanced = f"{prompt}, {style_keywords}, {quality_keywords.get(quality, '')}"
    # إزالة المسافات الزائدة والفواصل / Remove extra spaces and commas
    enhanced = ", ".join([s.strip() for s in enhanced.split(",") if s.strip()])
    return enhanced

# ============ التنبيهات والرسائل / Notifications ============

def show_success_message(message, duration=3):
    """عرض رسالة نجاح"""
    st.success(f"✅ {message}")

def show_error_message(message, duration=5):
    """عرض رسالة خطأ"""
    st.error(f"❌ {message}")

def show_info_message(message):
    """عرض رسالة معلومات"""
    st.info(f"ℹ️ {message}")

# ============ دالة مساعدة للجلسات / Session Helpers ============

def init_session_state():
    """تهيئة متغيرات الجلسة"""
    if "generation_count" not in st.session_state:
        st.session_state.generation_count = 0
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = ""
    if "last_image" not in st.session_state:
        st.session_state.last_image = None
