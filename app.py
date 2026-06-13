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
client  = genai.Client(api_key=API_KEY)

# ── Master CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

:root {
  --ink:        #0B0B14;
  --surface:    #111120;
  --card:       #17172A;
  --card2:      #1E1E35;
  --rim:        #2A2A45;
  --rim-bright: #3D3D65;
  --violet:     #7C5CFC;
  --violet-g:   #A78BFA;
  --cyan:       #38BDF8;
  --gold:       #F59E0B;
  --emerald:    #10B981;
  --rose:       #F43F5E;
  --txt:        #E2E2F0;
  --muted:      #7070A0;
  --faint:      #3A3A58;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
  font-family: 'Cairo', system-ui, sans-serif !important;
  background: var(--ink) !important;
  color: var(--txt) !important;
}

/* ── Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding: 0 1.25rem 4rem !important;
  max-width: 820px !important;
}

/* ════════════════════════════════
   HERO
════════════════════════════════ */
.hero-wrap {
  position: relative;
  text-align: center;
  padding: 3.5rem 2rem 2.8rem;
  margin-bottom: 2.5rem;
  overflow: hidden;
  border-radius: 24px;
  background: var(--surface);
  border: 1px solid var(--rim);
}
/* animated aurora blobs */
.hero-wrap::before {
  content: "";
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 70% 55% at 20% 10%, rgba(124,92,252,.18) 0%, transparent 60%),
    radial-gradient(ellipse 50% 45% at 80% 80%, rgba(56,189,248,.12) 0%, transparent 55%),
    radial-gradient(ellipse 40% 40% at 50% 50%, rgba(245,158,11,.06) 0%, transparent 60%);
  animation: aurora 8s ease-in-out infinite alternate;
  pointer-events: none;
}
@keyframes aurora {
  0%   { opacity: .7; transform: scale(1) rotate(0deg); }
  100% { opacity: 1;  transform: scale(1.08) rotate(2deg); }
}
/* grid overlay */
.hero-wrap::after {
  content: "";
  position: absolute; inset: 0;
  background-image:
    linear-gradient(var(--faint) 1px, transparent 1px),
    linear-gradient(90deg, var(--faint) 1px, transparent 1px);
  background-size: 40px 40px;
  opacity: .18;
  pointer-events: none;
}

.hero-badge {
  display: inline-flex; align-items: center; gap: .45rem;
  background: rgba(124,92,252,.12);
  border: 1px solid rgba(124,92,252,.35);
  border-radius: 99px;
  padding: .35rem 1.1rem;
  font-size: .78rem; font-weight: 700; letter-spacing: .07em;
  color: var(--violet-g);
  text-transform: uppercase;
  margin-bottom: 1.2rem;
  position: relative; z-index: 1;
}
.hero-title {
  font-size: clamp(2rem, 5vw, 2.9rem);
  font-weight: 900;
  line-height: 1.15;
  letter-spacing: -.01em;
  background: linear-gradient(110deg, #C4B5FD 0%, #67E8F9 50%, #F0ABFC 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative; z-index: 1;
  margin-bottom: .55rem;
}
.hero-sub {
  color: var(--muted);
  font-size: 1rem;
  line-height: 1.75;
  position: relative; z-index: 1;
  max-width: 520px;
  margin: 0 auto;
}
.hero-stats {
  display: flex; justify-content: center; gap: 1.5rem;
  margin-top: 1.8rem;
  position: relative; z-index: 1;
}
.stat-pill {
  background: var(--card);
  border: 1px solid var(--rim);
  border-radius: 12px;
  padding: .5rem 1.1rem;
  font-size: .82rem; font-weight: 700;
  color: var(--txt);
}
.stat-pill span { color: var(--violet-g); margin-left: .3rem; }

/* ════════════════════════════════
   SECTION LABEL
════════════════════════════════ */
.section-label {
  display: flex; align-items: center; gap: .6rem;
  color: var(--muted); font-size: .78rem; font-weight: 700;
  letter-spacing: .1em; text-transform: uppercase;
  margin-bottom: .9rem;
  direction: rtl;
}
.section-label::after {
  content: "";
  flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--rim) 0%, transparent 100%);
}

/* ════════════════════════════════
   INPUT CARD
════════════════════════════════ */
.input-card {
  background: var(--card);
  border: 1px solid var(--rim);
  border-radius: 20px;
  padding: 1.8rem 1.8rem 1.4rem;
  margin-bottom: 1.2rem;
  transition: border-color .25s;
}
.input-card:focus-within {
  border-color: var(--violet);
  box-shadow: 0 0 0 3px rgba(124,92,252,.1);
}

/* ── Streamlit widget overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: var(--card2) !important;
  border: 1.5px solid var(--rim) !important;
  border-radius: 12px !important;
  color: var(--txt) !important;
  font-family: 'Cairo', sans-serif !important;
  font-size: 1rem !important;
  direction: rtl !important;
  padding: .75rem 1rem !important;
  transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--violet) !important;
  box-shadow: 0 0 0 3px rgba(124,92,252,.15) !important;
  outline: none !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
  color: var(--faint) !important;
}
label {
  color: var(--txt) !important;
  font-family: 'Cairo', sans-serif !important;
  font-weight: 700 !important;
  font-size: .97rem !important;
  direction: rtl !important;
  text-align: right !important;
}

/* ── Select box ── */
[data-testid="stSelectbox"] > div > div {
  background: var(--card2) !important;
  border: 1.5px solid var(--rim) !important;
  border-radius: 12px !important;
  color: var(--txt) !important;
  font-family: 'Cairo', sans-serif !important;
}

/* ════════════════════════════════
   TONE CHIPS  (radio-as-pills)
════════════════════════════════ */
[data-testid="stRadio"] > label { display: none !important; }
[data-testid="stRadio"] > div {
  display: flex !important; flex-wrap: wrap !important; gap: .55rem !important;
  direction: rtl !important;
}
[data-testid="stRadio"] > div > label {
  background: var(--card2) !important;
  border: 1.5px solid var(--rim) !important;
  border-radius: 99px !important;
  padding: .42rem 1.1rem !important;
  font-size: .88rem !important; font-weight: 600 !important;
  color: var(--muted) !important;
  cursor: pointer !important;
  transition: all .18s !important;
  text-align: center !important;
  direction: rtl !important;
}
[data-testid="stRadio"] > div > label:hover {
  border-color: var(--violet) !important;
  color: var(--violet-g) !important;
}
[data-testid="stRadio"] > div > label[data-baseweb="radio"] > div:first-child {
  display: none !important;
}
/* selected pill */
[data-testid="stRadio"] div[data-baseweb="radio"] input:checked + div + div,
[data-testid="stRadio"] > div > label[aria-checked="true"] {
  background: rgba(124,92,252,.18) !important;
  border-color: var(--violet) !important;
  color: var(--violet-g) !important;
}

/* ════════════════════════════════
   GENERATE BUTTON
════════════════════════════════ */
[data-testid="stButton"] > button {
  width: 100% !important;
  background: linear-gradient(135deg, #6B3FFF 0%, #9B72FF 50%, #38BDF8 100%) !important;
  background-size: 200% 200% !important;
  color: #fff !important;
  border: none !important;
  border-radius: 14px !important;
  padding: 1.05rem !important;
  font-family: 'Cairo', sans-serif !important;
  font-size: 1.2rem !important;
  font-weight: 800 !important;
  cursor: pointer !important;
  transition: all .3s ease !important;
  box-shadow: 0 6px 30px rgba(107,63,255,.4), 0 0 0 0 rgba(107,63,255,0) !important;
  letter-spacing: .01em !important;
  margin-top: .6rem !important;
  animation: btn-breathe 4s ease-in-out infinite !important;
}
@keyframes btn-breathe {
  0%,100% { box-shadow: 0 6px 30px rgba(107,63,255,.4); }
  50%      { box-shadow: 0 8px 40px rgba(107,63,255,.65); }
}
[data-testid="stButton"] > button:hover {
  transform: translateY(-3px) scale(1.01) !important;
  box-shadow: 0 12px 40px rgba(107,63,255,.6) !important;
}
[data-testid="stButton"] > button:active {
  transform: translateY(0) scale(.99) !important;
}

/* ════════════════════════════════
   OUTPUT
════════════════════════════════ */
.out-wrap {
  margin-top: 2rem;
}
.out-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1rem;
  direction: rtl;
}
.out-title {
  font-size: 1rem; font-weight: 800; color: var(--emerald);
  display: flex; align-items: center; gap: .45rem;
}
.out-time {
  font-size: .75rem; color: var(--muted);
}

.ad-card {
  background: var(--card);
  border: 1px solid var(--rim);
  border-radius: 18px;
  padding: 1.8rem 1.8rem 1.5rem;
  margin-bottom: 1.2rem;
  direction: rtl;
  text-align: right;
  line-height: 2;
  font-size: 1.02rem;
  position: relative;
  overflow: hidden;
  transition: border-color .25s;
}
.ad-card:hover { border-color: var(--rim-bright); }
.ad-card::before {
  content: "";
  position: absolute; top: 0; right: 0;
  width: 120px; height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(124,92,252,.12) 0%, transparent 70%);
  transform: translate(30%, -30%);
}
.ad-num {
  display: inline-flex; align-items: center; gap: .4rem;
  background: rgba(124,92,252,.12);
  border: 1px solid rgba(124,92,252,.25);
  border-radius: 99px;
  padding: .28rem .85rem;
  font-size: .76rem; font-weight: 800; letter-spacing: .06em;
  color: var(--violet-g);
  text-transform: uppercase;
  margin-bottom: 1rem;
}
.ad-body { white-space: pre-wrap; }

/* copy button */
.copy-row {
  display: flex; justify-content: flex-start;
  margin-top: 1.1rem;
  padding-top: .9rem;
  border-top: 1px solid var(--rim);
}
.copy-btn {
  display: inline-flex; align-items: center; gap: .4rem;
  background: var(--card2);
  border: 1px solid var(--rim);
  border-radius: 8px;
  padding: .35rem .9rem;
  font-size: .8rem; font-weight: 700;
  color: var(--muted);
  cursor: pointer;
  transition: all .2s;
  font-family: 'Cairo', sans-serif;
}
.copy-btn:hover { border-color: var(--violet); color: var(--violet-g); }

/* ════════════════════════════════
   ERROR
════════════════════════════════ */
.err-card {
  background: rgba(244,63,94,.07);
  border: 1.5px solid rgba(244,63,94,.3);
  border-radius: 14px;
  padding: 1.1rem 1.4rem;
  margin-top: 1rem;
  color: #FDA4AF;
  font-size: .93rem;
  direction: rtl; text-align: right;
  line-height: 1.7;
}

/* ════════════════════════════════
   FOOTER
════════════════════════════════ */
.footer {
  text-align: center;
  color: var(--faint);
  font-size: .78rem;
  margin-top: 3.5rem;
  padding-bottom: 1rem;
  line-height: 1.9;
}
.footer a { color: var(--violet-g); text-decoration: none; }

/* ════════════════════════════════
   SPINNER
════════════════════════════════ */
[data-testid="stSpinner"] p {
  color: var(--violet-g) !important;
  font-family: 'Cairo', sans-serif !important;
  font-size: .95rem !important;
  direction: rtl;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">🇲🇦 &nbsp; Powered by Advanced AI</div>
  <div class="hero-title">🚀 DarijaCopy AI</div>
  <p class="hero-sub">
    مُساعد الإعلانات الذكي بالدارجة المغربية<br>
    دخل بيانات منتجك وتسنى — الذكاء الاصطناعي غادي يكتب ليك إعلانات 
    احترافية تبيع وتجذب الزبون ف ثوانٍ ✨
  </p>
  <div class="hero-stats">
    <div class="stat-pill">⚡<span>محرك متقدم</span></div>
    <div class="stat-pill">🎯<span>دارجة مغربية 100%</span></div>
    <div class="stat-pill">✍️<span>2 أساليب إعلانية</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FORM
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">✏️ &nbsp; معلومات المنتج</div>', unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)
product_name = st.text_input(
    "🏷️ اسم المنتج",
    placeholder="مثال: عصارة فواكه لاسلكية...",
    key="product_name",
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)
product_features = st.text_area(
    "📋 مميزات ومواصفات المنتج",
    placeholder="مثال: كتشحن بـ USB، خفيفة 350g، كطحن التلج، ضمان 6 أشهر، توصيل مجاني...",
    height=120,
    key="product_features",
)
st.markdown('</div>', unsafe_allow_html=True)

# ── Advanced options ──────────────────────────────────────────
st.markdown('<div class="section-label">🎨 &nbsp; خيارات متقدمة</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    target_audience = st.selectbox(
        "🎯 الجمهور المستهدف",
        ["عام — الجميع", "شباب 18-30", "ربات البيوت", "رجال الأعمال", "المراهقون"],
        key="audience",
    )
with col2:
    platform = st.selectbox(
        "📱 منصة النشر",
        ["فيسبوك / إنستغرام", "واتساب / تيك توك", "إعلان موقع إلكتروني", "رسائل SMS"],
        key="platform",
    )

# ── Generate button ───────────────────────────────────────────
generate = st.button("✨ صاوب الإعلان دابا", key="generate")

# ═══════════════════════════════════════════════════════════════
# GENERATION
# ═══════════════════════════════════════════════════════════════
if generate:
    if not product_name.strip():
        st.markdown('<div class="err-card">⚠️ عفاك دخل اسم المنتج قبل المتابعة!</div>', unsafe_allow_html=True)
    elif not product_features.strip():
        st.markdown('<div class="err-card">⚠️ زيد مميزات المنتج باش يكون الإعلان قوي ومؤثر!</div>', unsafe_allow_html=True)
    else:
        # ── Pro system prompt ─────────────────────────────────
        system_prompt = """أنت كاتب إعلانات (Copywriter) مغربي محترف ومتخصص في التسويق الإلكتروني للسوق المغربية.
أسلوبك: مباشر، مؤثر، ومتجدر في الواقع اليومي للمواطن المغربي.
قيمك: الصدق في وصف المنتج، الإبداع في الصياغة، والاحترام الكامل للمستهلك.
لغتك: دارجة مغربية بيضاء مفهومة، مكتوبة بالحروف العربية، بدون تكلف ولا مبالغة."""

        user_prompt = f"""اكتب 2 نصوص إعلانية احترافية للمنتج التالي:

━━━━━━━━━━━━━━━━━━━━━━━━
📦 اسم المنتج: {product_name}
📝 المميزات والمواصفات: {product_features}
🎯 الجمهور المستهدف: {target_audience}
📱 منصة النشر: {platform}
━━━━━━━━━━━━━━━━━━━━━━━━

═══ الشروط الإلزامية للصياغة ═══

【 إعلان 1 — أ��لوب Problem → Solution 】
- ابدأ بمشكلة حقيقية يعيشها الزبون المغربي يومياً تخص هذا المنتج
- أظهر كيف المنتج يحل هاد المشكلة بشكل ملموس وسريع
- الأسلوب: حماسي، مباشر، ومقنع
- استعمل صيغة "واش كنت كتعاني من...؟ — دابا حُلّت!"

【 إعلان 2 — أسلوب Storytelling عاطفي 】
- ابدأ بقصة قصيرة مشوقة من الحياة اليومية المغربية (قصة شخص حقيقي بسيط)
- اربط القصة بالمنتج بشكل طبيعي وغير متكلف
- أثر في مشاعر القارئ (الفرحة، الراحة، الفخر، الاقتصاد...)
- الأسلوب: سردي، دافئ، وقريب من القلب

═══ قواعد اللغة والتنسيق ═══
✅ دارجة مغربية مكتوبة بالحروف العربية فقط
✅ كلمات فرنسية شعبية مقبولة: (لافاج، شارجور، ليفراجو، بروموسيون، كوليزي...)
✅ إيموجيز استراتيجية لجذب العين بصرياً (مش مبالغة)
✅ فقرات قصيرة — جملة أو جملتين كحد أقصى لكل فقرة
✅ انهي كل إعلان بـ CTA قوي ومحفز للشراء الفوري
✅ ذكر ميزة "الدفع عند الاستلام" و"التوصيل" إن أمكن

═══ تنسيق الإخراج ═══
استعمل هذا التنسيق بالضبط:

---إعلان 1---
[محتوى الإعلان الأول]

---إعلان 2---
[محتوى الإعلان الثاني]

اكتب الإعلانين الآن:"""

        import time
        try:
            with st.spinner("⏳ كيتولد الإعلانات..."):
                t0 = time.time()
                response = client.models.generate_content(
                    model=MODEL,
                    contents=[
                        {"role": "user", "parts": [{"text": system_prompt + "\n\n" + user_prompt}]}
                    ],
                )
                elapsed = round(time.time() - t0, 1)
                raw = response.text.strip()

            # ── Parse the two ads ─────────────────────────────
            ads = []
            if "---إعلان 2---" in raw:
                parts = raw.split("---إعلان 2---")
                ad1 = parts[0].replace("---إعلان 1---", "").strip()
                ad2 = parts[1].strip()
                ads = [ad1, ad2]
            else:
                ads = [raw]

            labels = [
                ("🔥 إعلان 1", "Problem → Solution"),
                ("💫 إعلان 2", "Storytelling"),
            ]

            st.markdown(f"""
            <div class="out-wrap">
              <div class="out-header">
                <div class="out-title">✅ &nbsp; تم توليد الإعلانات بنجاح</div>
                <div class="out-time">⏱ {elapsed} ثانية</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            for i, ad_text in enumerate(ads):
                icon, style = labels[i] if i < len(labels) else (f"📝 إعلان {i+1}", "")
                body_escaped = ad_text.replace("<", "&lt;").replace(">", "&gt;")
                st.markdown(f"""
                <div class="ad-card">
                  <div class="ad-num">{icon} &nbsp;·&nbsp; {style}</div>
                  <div class="ad-body">{body_escaped}</div>
                  <div class="copy-row">
                    <button class="copy-btn" onclick="
                      navigator.clipboard.writeText(document.querySelectorAll('.ad-body')[{i}].innerText);
                      this.innerText='✅ تم النسخ!';
                      setTimeout(()=>this.innerText='📋 نسخ الإعلان',1800);
                    ">📋 نسخ الإعلان</button>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            err = str(e).lower()
            if "quota" in err or "429" in err or "resource_exhausted" in err:
                msg = "⛔ <strong>تجاوزنا الحد اليومي ديال الطلبات.</strong><br>جرب مرة أخرى بعد شوية."
            elif "timeout" in err or "deadline" in err or "unavailable" in err:
                msg = "⏱️ <strong>الطلب خذ وقت بزاف.</strong><br>شوف الاتصال ديالك وعاود المحاولة."
            else:
                msg = f"❌ <strong>خطأ غير متوقع:</strong><br><code>{str(e)[:200]}</code>"
            st.markdown(f'<div class="err-card">{msg}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  صُنع بـ ❤️ للتجار المغاربة<br>
  <span style="color:#3A3A58;">DarijaCopy AI v2.0 — جميع الحقوق محفوظة</span>
</div>
""", unsafe_allow_html=True)
