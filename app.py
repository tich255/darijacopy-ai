import streamlit as st
from google import genai

# ── Page Config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DarijaCopy AI",
    page_icon="🚀",
    layout="centered",
)

# ── API Client ────────────────────────────────────────────────────────────

API_KEY = st.secrets["GEMINI_API_KEY"]
MODEL   = "gemini-2.5-flash"

client = genai.Client(api_key=API_KEY)

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

/* ── Root palette ── */
:root {
    --primary:   #6C3FE8;
    --primary-light: #8B65F0;
    --accent:    #F5A623;
    --bg-dark:   #0F0F1A;
    --bg-card:   #1A1A2E;
    --bg-input:  #16213E;
    --border:    #2D2D4E;
    --text-main: #E8E8F0;
    --text-muted:#9090B0;
    --success:   #00D4AA;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Cairo', 'Segoe UI', sans-serif !important;
    background-color: var(--bg-dark) !important;
    color: var(--text-main) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 780px !important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1A0A3E 0%, #0F1A3E 50%, #0A2A1F 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 60% 50% at 50% 0%, rgba(108,63,232,.25) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 900;
    background: linear-gradient(90deg, #A78BFA, #60EFFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 .6rem;
}
.hero p {
    color: var(--text-muted);
    font-size: 1.05rem;
    margin: 0;
    line-height: 1.7;
}

/* ── Form card ── */
.form-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.form-card h3 {
    color: var(--text-muted);
    font-size: .85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin: 0 0 1.2rem;
}

/* ── Streamlit input overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-main) !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 1rem !important;
    direction: rtl;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(108,63,232,.18) !important;
}
label, .stTextInput label, .stTextArea label {
    color: var(--text-main) !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    direction: rtl;
    text-align: right;
}

/* ── CTA button ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    letter-spacing: .02em !important;
    cursor: pointer !important;
    transition: all .25s ease !important;
    box-shadow: 0 4px 24px rgba(108,63,232,.45) !important;
    margin-top: .5rem !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(108,63,232,.6) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Output card ── */
.output-card {
    background: linear-gradient(135deg, #0A1F12 0%, #0F1A2E 100%);
    border: 1.5px solid var(--success);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
    direction: rtl;
    text-align: right;
    line-height: 1.9;
    font-size: 1.05rem;
    color: var(--text-main);
    box-shadow: 0 0 24px rgba(0,212,170,.12);
}
.output-badge {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    background: rgba(0,212,170,.12);
    border: 1px solid rgba(0,212,170,.3);
    border-radius: 99px;
    padding: .3rem .9rem;
    font-size: .82rem;
    font-weight: 700;
    color: var(--success);
    margin-bottom: 1.2rem;
}

/* ── Error card ── */
.error-card {
    background: #1A0A0A;
    border: 1.5px solid #E53E3E;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    color: #FC8181;
    font-size: .95rem;
    direction: rtl;
    text-align: right;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: var(--primary-light) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🚀 DarijaCopy AI</h1>
    <p>مُساعد الإعلانات بالدارجة</p>
    <p style="margin-top:.5rem;font-size:.95rem;">
        كتب إعلانات تسويقية احترافية بالدارجة المغربية في ثوانٍ معدودة 🇲🇦<br>
        خصص لأصحاب التجارة الإلكترونية والمسوقين المغاربة
    </p>
</div>
""", unsafe_allow_html=True)

# ── Form Card ────────────────────────────────────────────────────────────
st.markdown('<div class="form-card"><h3>✏️ معلومات المنتج</h3>', unsafe_allow_html=True)

product_name = st.text_input(
    "اسم المنتج (مثال: عصارة فواكه لاسلكية)",
    placeholder="أدخل اسم منتجك هنا...",
    key="product_name",
)

product_features = st.text_area(
    "مميزات المنتج ومواصفاته (مثال: كتشحن بـ USB، خفيفة، كطحن التلج)",
    placeholder="اكتب أبرز مميزات ومواصفات منتجك...",
    height=130,
    key="product_features",
)

st.markdown('</div>', unsafe_allow_html=True)

generate_btn = st.button("صاوب الإعلان دابا ✨", key="generate")

# ── Generation Logic ──────────────────────────────────────────────────────────
if generate_btn:
    if not product_name.strip():
        st.markdown(
            '<div class="error-card">⚠️ من فضلك دخل اسم المنتج قبل ما تولي!</div>',
            unsafe_allow_html=True,
        )
    elif not product_features.strip():
        st.markdown(
            '<div class="error-card">⚠️ من فضلك زيد مميزات المنتج باش يجي الإعلان مزيان!</div>',
            unsafe_allow_html=True,
        )
    else:
        prompt = f"""أنت خبير تسويق إلكتروني مغربي محترف ومختص في كتابة الإعلانات (Copywriter).
مهمتك هي كتابة 2 نصوص إعلانية احترافية وجذابة لمنتج معين بالدارجة ال��غربية المفهومة والمكتوبة بحروف عربية صحيحة.

معلومات المنتج التي أدخلها المستخدم:
- اسم المنتج: {product_name}
- مميزات ومواصفات المنتج: {product_features}

شروط صياغة الإعلان الإلزامية:
1. النص الإعلاني الأول: يجب أن يكون بأسلوب حماسي، سريع، ومباشر يركز على حل مشكلة حقيقية يعاني منها المستهلك.
2. النص الإعلاني الثاني: يجب أن يكون بأسلوب قصة مشوقة (Storytelling) قريبة من المعيش اليومي للمواطن المغربي.
3. اللغة: دارجة مغربية بيضاء مفهومة ومؤثرة، مكتوبة بالخط العربي. تجنب العروبية القاسية وتجنب الكلمات الفرنسية.
4. التنسيق: استخدم علامات الوقف، الإيموجيز المناسبة لجذب الانتباه بصرياً، واقسم النص إلى فقرات قصيرة سهلة القراءة.
5. طلب اتخاذ إجراء (Call to Action): يجب إنهاء كل إعلان بـ CTA واضح وقوي ومحفز للضغط والشراء الفوري.

اكتب الإعلانين الآن بشكل احترافي وجذاب:"""

        try:
            with st.spinner("الذكاء الاصطناعي كيكتب ليك الإعلان..."):
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                )
                result_text = response.text

            st.markdown(
                f"""
                <div class="output-card">
                    <div class="output-badge">✅ تم توليد الإعلان بنجاح</div>
                    <hr class="divider">
                    {result_text.replace(chr(10), '<br>')}
                </div>
                """,
                unsafe_allow_html=True,
            )

        except Exception as e:
            err = str(e)
            if "quota" in err.lower() or "429" in err:
                msg = "⛔ وصلنا للحد الأقصى ديال الطلبات. جرب مرة أخرى بعد شوية."
            elif "timeout" in err.lower() or "deadline" in err.lower():
                msg = "⏱️ الطلب خذ وقت بزاف. شوف الاتصال ديالك وعاود المحاولة."
            elif "api_key" in err.lower() or "401" in err or "403" in err:
                msg = "🔑 مشكل في مفتاح API. تواصل مع الدعم التقني."
            else:
                msg = f"❌ وقع خطأ غير متوقع: {err}"

            st.markdown(
                f'<div class="error-card">{msg}</div>',
                unsafe_allow_html=True,
            )

# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#4A4A6A; font-size:.8rem; margin-top:3rem; padding-bottom:1rem;">
    صُنع بـ ❤️ للتجار المغاربة · مدعوم بـ Gemini AI
</div>
""", unsafe_allow_html=True)
