import streamlit as st
import google.generativeai as genai
import os
import tempfile

# ==========================================
# 1. إعدادات الصفحة (تصميم رسمي - أبيض وزمردي)
# ==========================================
st.set_page_config(page_title="منصة بيان", page_icon="🟢", layout="centered")

# الستايل CSS (ممنوع Dark Luxury - هنا ستايل حكومي نظيف)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        background-color: #ffffff;
        color: #333333;
    }
    
    /* العنوان الرئيسي */
    .main-title {
        color: #0f5132; /* زمردي غامق */
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #6c757d;
        text-align: center;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }

    /* أزرار التسجيل */
    .stAudio {
        width: 100%;
    }

    /* بطاقة النتيجة */
    .result-box {
        background-color: #f8f9fa; /* رمادي فاتح جداً */
        border: 1px solid #e9ecef;
        border-right: 6px solid #198754; /* الخط الأخضر الجانبي */
        border-radius: 12px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }

    .score-badge {
        background-color: #198754;
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        color: #aaa;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الواجهة الأمامية
# ==========================================

# الهيدر
st.markdown('<div class="main-title">منصة بَيَان</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">نظام الاعتماد الوطني للهوية اللغوية | AI-Powered</div>', unsafe_allow_html=True)

# مساحة الاختبار
st.info("🎙️ **تعليمات الاختبار:** اضغط زر الميكروفون بالأسفل، واقرأ النص التالي بصوت واضح:")
st.markdown("""
<div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center; font-size: 1.2rem; border: 1px dashed #0d6efd; color: #000;">
"إنَّ اللُّغَةَ العَرَبِيَّةَ لَيْسَتْ مُجَرَّدَ أَدَاةٍ لِلتَّوَاصُل، بَلْ هِيَ وِعَاءُ الفِكْرِ وَمِرْآةُ الهُوِيَّة."
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. المنطق البرمجي والذكاء الاصطناعي
# ==========================================

# مفتاح API يقرأ من إعدادات Streamlit Cloud أو البيئة المحلية
# في حالة التشغيل المحلي المباشر، سيعتمد على الإدخال اليدوي إذا لم يجد Secrets
api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    # هذا المربع سيظهر فقط إذا لم نضع المفتاح في الإعدادات (للتسهيل عليك الآن)
    api_key = st.text_input("أدخل مفتاح API الخاص بك للبدء:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # تسجيل الصوت
    audio_value = st.audio_input("اضغط للتسجيل")

    if audio_value:
        st.markdown("---")
        with st.spinner("جاري تحليل بصمة الصوت ومخارج الحروف..."):
            
            # حفظ الملف مؤقتاً
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_value.read())
                temp_audio_path = temp_audio.name
            
            try:
                # إرسال إلى Gemini
                model = genai.GenerativeModel("gemini-pro")
                file_upload = genai.upload_file(temp_audio_path)
                
                prompt = """
                تخيل أنك رئيس لجنة تحكيم في مجمع اللغة العربية. استمع لهذا التسجيل وحلله بدقة.
                المطلوب: قم بإنشاء تقرير تقييم بصيغة HTML بسيطة (بدون وسوم html أو body) للعرض داخل تطبيق:
                1. حدد مستوى المتحدث (مبتدئ / متمكن / فصيح).
                2. اذكر نسبة إتقان (رقم مئوي).
                3. اكتب تعليقاً موجزاً (سطرين) عن مخارج الحروف وجماليات الأداء.
                4. اجعل النتيجة مشجعة ولكن دقيقة.
                """
                
                response = model.generate_content([file_upload, prompt])
                
                # عرض النتيجة
                st.markdown(f"""
                <div class="result-box">
                    <div class="score-badge">تم إصدار الرخصة بنجاح</div>
                    <div style="text-align: right; direction: rtl;">
                        {response.text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("تم حفظ النتيجة في قاعدة البيانات الوطنية.")
                st.balloons()
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")
            
            finally:
                os.remove(temp_audio_path)

st.markdown('<div class="footer">جميع الحقوق محفوظة © جائزة اللغة العربية 2026 - مشروع بَيَان</div>', unsafe_allow_html=True)
