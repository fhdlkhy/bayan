# bayan
منصة بيان: أول نظام ذكي لتقييم الهوية اللغوية باستخدام الذكاء الاصطناعي.

## تشغيل محلي سريع (Docker)

1. بناء الصورة:
```bash
docker build -t bayan-app:latest .
```
2. تشغيل الحاوية محلياً:
```bash
docker run -p 8501:8501 --env GOOGLE_API_KEY="YOUR_KEY" bayan-app:latest
```

أو استخدم سكربت البدء المحلي:
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

## إعداد المفتاح بأمان
- ضع `GOOGLE_API_KEY` في متغيرات البيئة أو في `Streamlit Secrets` عند النشر.
- لا تضع المفتاح داخل الشيفرة أو في مستودع عام؛ دوّره فوراً إذا تسرب.

## ملفات مهمة
- `Dockerfile` — حاوية للتشغيل.
- `requirements.txt` — الاعتماديات.
- `ROADMAP.md` — خارطة الطريق للـ 12 شهر.

