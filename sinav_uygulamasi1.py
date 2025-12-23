import streamlit as st
import time
import random

# --- SAYFA VE ARAYÜZ AYARLARI ---
st.set_page_config(page_title="Ekonometri Sınav Portalı", layout="centered")

# Sağ üstteki Streamlit menülerini gizlemek için CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- VERİ TABANI (Görselden Aktarılan Sorular) ---
if 'questions' not in st.session_state:
    raw_qs = [
        {"metin": "What does β0 represent in a simple linear regression model?", "siklar": ["The slope", "The intercept", "The error term", "The variance"], "dogru": "The intercept", "ipucu": "Y eksenini kestiği nokta."},
        {"metin": "Which method is most commonly used to estimate parameters in linear regression?", "siklar": ["Maximum likelihood", "Method of moments", "Ordinary Least Squares", "Weighted Least Squares"], "dogru": "Ordinary Least Squares", "ipucu": "Kareler toplamını minimize eder (OLS)."},
        {"metin": "In regression, what does an outlier refer to?", "siklar": ["A missing value", "A data point far from others", "A dummy variable", "A perfectly predicted value"], "dogru": "A data point far from others", "ipucu": "Sürüden ayrılan veri noktası."},
        {"metin": "Which transformation can help address heteroskedasticity?", "siklar": ["Taking logarithms", "Adding more outliers", "Dropping intercept", "Increasing sample size"], "dogru": "Taking logarithms", "ipucu": "Değişken varyansı dengelemek için veriyi sıkıştırır."},
        {"metin": "What does OLS minimize in regression?", "siklar": ["Sum of residuals", "Sum of squared residuals", "Maximum likelihood", "Variance of X"], "dogru": "Sum of squared residuals", "ipucu": "Residuals'ların karesini minimize etmek esastır."},
        {"metin": "Which assumption is required for OLS to be efficient?", "siklar": ["Multicollinearity", "Homoskedasticity", "Outliers present", "Wrong functional form"], "dogru": "Homoskedasticity", "ipucu": "Hata terimlerinin varyansı sabit olmalıdır."},
        {"metin": "What is the purpose of dummy variables in regression?", "siklar": ["Represent categorical features", "Remove outliers", "Reduce variance", "Estimate β0 only"], "dogru": "Represent categorical features", "ipucu": "Niteliksel (Kategorik) verileri modele dahil eder."},
        {"metin": "Which of the following is a consequence of omitted variables?", "siklar": ["Multicollinearity", "Heteroskedasticity", "Biased estimates", "Reduced sample size"], "dogru": "Biased estimates", "ipucu": "Modelden önemli bir değişken dışlanırsa tahminler sapar."},
        {"metin": "What does β1 measure in a simple regression?", "siklar": ["Impact of X on Y", "Intercept", "Error variance", "Bias term"], "dogru": "Impact of X on Y", "ipucu": "Bağımsız değişkenin bağımlı değişken üzerindeki eğimi."},
        {"metin": "Which regression technique starts with no predictors and adds them step by step?", "siklar": ["Backward selection", "Forward selection", "Ridge regression", "Logistic regression"], "dogru": "Forward selection", "ipucu": "Boştan başlayıp adım adım ekleme süreci."},
        {"metin": "Which distribution assumption underlies LDA?", "siklar": ["Uniform distribution", "Exponential distribution", "Multivariate normal", "Logistic distribution"], "dogru": "Multivariate normal", "ipucu": "LDA, sınıfların normal dağıldığını varsayar."},
        {"metin": "What is the dependent variable type in logistic regression?", "siklar": ["Continuous", "Binary", "Ordinal only", "Always categorical"], "dogru": "Binary", "ipucu": "0-1 veya Evet-Hayır gibi iki seçenek."},
        {"metin": "Which test is commonly used to detect heteroskedasticity?", "siklar": ["Cook's distance", "Goldfeld-Quandt test", "Augmented Dickey-Fuller", "Durbin-Watson"], "dogru": "Goldfeld-Quandt test", "ipucu": "Varyansın değişip değişmediğini kontrol eder."},
        {"metin": "What does multicollinearity mean?", "siklar": ["Perfectly correlated errors", "Highly correlated predictors", "Correlated residuals", "Noisy Y variable"], "dogru": "Highly correlated predictors", "ipucu": "X değişkenlerinin kendi aralarında güçlü ilişkisi."},
        {"metin": "Which regression is used for classification when output is binary?", "siklar": ["OLS", "Logistic regression", "Ridge regression", "Stepwise regression"], "dogru": "Logistic regression", "ipucu": "Sınıflandırma ve olasılık tahmini için kullanılır."},
        {"metin": "What is Cook's distance used for?", "siklar": ["Detecting multicollinearity", "Detecting outliers", "Estimating variance", "Measuring heteroskedasticity"], "dogru": "Detecting outliers", "ipucu": "Modeli aşırı etkileyen gözlemleri bulur."},
        {"metin": "Which selection criterion is commonly used in stepwise regression?", "siklar": ["Adjusted R2", "Akaike Information Criterion (AIC)", "Mean squared error only", "Variance Inflation Factor"], "dogru": "Akaike Information Criterion (AIC)", "ipucu": "Model karmaşıklığı ile uyum arasındaki denge (AIC)."},
        {"metin": "What shape does the logistic function have?", "siklar": ["Linear", "Sigmoid", "Exponential", "Quadratic"], "dogru": "Sigmoid", "ipucu": "S şeklindeki fonksiyon."},
        {"metin": "Which regression model allows quadratic effects of predictors?", "siklar": ["Simple regression", "Logistic regression", "Polynomial regression", "LDA"], "dogru": "Polynomial regression", "ipucu": "X^2 gibi terimler içeren model."},
        {"metin": "What is the role of the intercept in regression?", "siklar": ["Slope of regression line", "Value of Y when X=0", "Variance of X", "Error term"], "dogru": "Value of Y when X=0", "ipucu": "Başlangıç noktası."},
        {"metin": "What is the main issue caused by near multicollinearity?", "siklar": ["Missing variables", "Instability of parameter estimates", "Biased OLS", "Increased sample variance"], "dogru": "Instability of parameter estimates", "ipucu": "Tahminlerin çok hassas ve değişken olması."},
        {"metin": "Which method removes least significant predictors step by step?", "siklar": ["Forward selection", "Backward selection", "LDA", "Ridge regression"], "dogru": "Backward selection", "ipucu": "Hepsiyle başla, zayıf olanları ele."},
        {"metin": "In regression, which variable type must the dependent variable be for OLS?", "siklar": ["Binary", "Ordinal", "Continuous", "Nominal"], "dogru": "Continuous", "ipucu": "Sayısal ve sürekli bir veri."},
        {"metin": "What does a large Cook's distance indicate?", "siklar": ["Predictor is irrelevant", "Data point is influential", "Predictor is binary", "OLS is biased"], "dogru": "Data point is influential", "ipucu": "O nokta çıkarılırsa model çok değişir."},
        {"metin": "Why is OLS inappropriate for binary dependent variables?", "siklar": ["Predictors become unstable", "Probabilities may fall outside [0,1]", "Too many residuals", "Intercept becomes zero"], "dogru": "Probabilities may fall outside [0,1]", "ipucu": "OLS 0'dan küçük veya 1'den büyük sonuçlar verebilir."}
    ]
    # Soru listesini 50'ye tamamla ve şıkları karıştır
    st.session_state.questions = []
    while len(st.session_state.questions) < 50:
        item = random.choice(raw_qs).copy()
        sh_siklar = item["siklar"].copy()
        random.shuffle(sh_siklar)
        item["fixed_siklar"] = sh_siklar
        st.session_state.questions.append(item)

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'joker_50_used' not in st.session_state: st.session_state.joker_50_used = False
if 'joker_hint_used' not in st.session_state: st.session_state.joker_hint_used = False
if 'joker_ai_used' not in st.session_state: st.session_state.joker_ai_used = False
if 'active_50_for_current' not in st.session_state: st.session_state.active_50_for_current = False
if 'balloons_done' not in st.session_state: st.session_state.balloons_done = False

# --- GİRİŞ EKRANI ---
if st.session_state.step == "GIRIS":
    st.title("📊 Ekonometri & Veri Bilimi Sınavı")
    ad = st.text_input("Adınız:")
    soyad = st.text_input("Soyadınız:")
    if st.button("Sınava Başla"):
        if ad and soyad:
            st.session_state.user_name = f"{ad} {soyad}"
            st.session_state.step = "SINAV"
            st.session_state.start_time = time.time()
            st.rerun()

# --- SINAV EKRANI ---
elif st.session_state.step == "SINAV":
    gecen = time.time() - st.session_state.start_time
    kalan_zaman = max(0, (50 * 60) - gecen)
    
    # İstatistikler
    cevaplanan = len(st.session_state.answers)
    kalan_soru = 50 - (st.session_state.q_idx + 1)
    # Boş bırakılan: Mevcut soruya kadar olan ama cevaplanmamış sorular
    bos_sayisi = sum(1 for i in range(st.session_state.q_idx) if i not in st.session_state.answers)

    # Sidebar
    st.sidebar.subheader(f"👤 {st.session_state.user_name}")
    st.sidebar.metric("⏳ Kalan Süre", f"{int(kalan_zaman // 60)}:{int(kalan_zaman % 60):02d}")
    st.sidebar.divider()
    st.sidebar.write(f"✅ **Cevaplanan:** {cevaplanan}")
    st.sidebar.write(f"⚪ **Boş Geçilen:** {bos_sayisi}")
    st.sidebar.write(f"📝 **Sıradaki Soru Sayısı:** {kalan_soru}")
    
    # İlk 3 Soru Balon Kontrolü
    if not st.session_state.balloons_done and st.session_state.q_idx >= 3:
        if sum(1 for i in range(3) if st.session_state.answers.get(i) == st.session_state.questions[i]['dogru']) == 3:
            st.balloons()
            st.session_state.balloons_done = True

    st.progress((st.session_state.q_idx + 1) / 50)
    q = st.session_state.questions[st.session_state.q_idx]
    st.subheader(f"Soru {st.session_state.q_idx + 1}")
    st.info(q['metin'])

    # Joker Paneli
    jc1, jc2, jc3 = st.columns(3)
    if not st.session_state.joker_50_used:
        if jc1.button("✂️ %50 Ele"):
            st.session_state.joker_50_used = True
            st.session_state.active_50_for_current = True
            st.rerun()
    if not st.session_state.joker_hint_used:
        if jc2.button("💡 İpucu"):
            st.session_state.joker_hint_used = True
            st.info(f"İpucu: {q['ipucu']}")
    if not st.session_state.joker_ai_used:
        if jc3.button("🤖 AI Tahmini"):
            st.session_state.joker_ai_used = True
            st.bar_chart({s: (80 if s == q['dogru'] else random.randint(5, 15)) for s in q['fixed_siklar']})

    # Şıklar (Sabitlenmiş Sıra)
    opts = q['fixed_siklar']
    if st.session_state.active_50_for_current:
        wrong = [s for s in q['fixed_siklar'] if s != q['dogru']]
        stay = random.choice(wrong)
        opts = [s if (s == q['dogru'] or s == stay) else "---" for s in q['fixed_siklar']]

    choice = st.radio("Seçeneğiniz:", opts, key=f"r_{st.session_state.q_idx}", index=None)
    if choice and choice != "---":
        st.session_state.answers[st.session_state.q_idx] = choice

    st.divider()
    b_ans, b_fin = st.columns(2)
    if b_ans.button("✅ Doğru Cevabı Göster"): st.success(f"Cevap: {q['dogru']}")
    if b_fin.button("🛑 SINAVI BİTİR"): st.session_state.step = "SONUC"; st.rerun()

    n1, n2, n3 = st.columns([1,2,1])
    if n1.button("⬅️ Geri") and st.session_state.q_idx > 0:
        st.session_state.q_idx -= 1; st.session_state.active_50_for_current = False; st.rerun()
    if n3.button("İleri ➡️"):
        if st.session_state.q_idx < 49:
            st.session_state.q_idx += 1; st.session_state.active_50_for_current = False; st.rerun()
        else:
            st.session_state.step = "SONUC"; st.rerun()

# --- SONUÇ EKRANI ---
elif st.session_state.step == "SONUC":
    st.title("📊 Sınav Karnesi")
    d, y, b = 0, 0, 0
    for i in range(50):
        ans = st.session_state.answers.get(i)
        if ans is None: b += 1
        elif ans == st.session_state.questions[i]['dogru']: d += 1
        else: y += 1
    
    puan = (d / 50) * 100
    st.metric("BAŞARI PUANI", f"%{puan}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Doğru ✅", d)
    c2.metric("Yanlış ❌", y)
    c3.metric("Boş ⚪", b)

        
    if st.button("🔄 Yeniden Başla"):
        st.session_state.clear()
        st.rerun()
