import streamlit as st
import time
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ekonometri Sınavı", layout="centered")

# --- VERİ TABANI ---
if 'questions' not in st.session_state:
    raw_qs = [
        { "metin": "What does β0 represent in a simple linear regression model?", "siklar": ["The slope", "The intercept", "The error term", "The variance"], "dogru": "The intercept", "ipucu": "Y eksenini kestiği noktayı düşün." },
        { "metin": "Which method is most commonly used to estimate parameters in linear regression?", "siklar": ["Maximum likelihood", "Method of moments", "OLS", "WLS"], "dogru": "OLS", "ipucu": "Kareler toplamını minimize eden yöntem." },
        { "metin": "In regression, what does an outlier refer to?", "siklar": ["Missing value", "Data point far from others", "Dummy variable", "Perfect value"], "dogru": "Data point far from others", "ipucu": "Diğer veri noktalarından çok uzakta olan bir değer." },
        { "metin": "Which transformation can help address heteroskedasticity?", "siklar": ["Taking logarithms", "Adding outliers", "Dropping intercept", "Sample size"], "dogru": "Taking logarithms", "ipucu": "Varyansı sabitlemek için veriyi sıkıştıran bir işlem." },
        { "metin": "What does OLS minimize in regression?", "siklar": ["Sum of residuals", "Sum of squared residuals", "Maximum likelihood", "Variance of X"], "dogru": "Sum of squared residuals", "ipucu": "Hataların karesiyle ilgilidir." },
        { "metin": "Which assumption is required for OLS to be efficient?", "siklar": ["Multicollinearity", "Homoskedasticity", "Outliers present", "Wrong form"], "dogru": "Homoskedasticity", "ipucu": "Hata terimlerinin varyansının sabit olması gerekir." },
        { "metin": "What is the purpose of dummy variables?", "siklar": ["Categorical features", "Remove outliers", "Reduce variance", "Estimate β0"], "dogru": "Categorical features", "ipucu": "Kategorik verileri sayıya çevirir." },
        { "metin": "Consequence of omitted variables?", "siklar": ["Multicollinearity", "Heteroskedasticity", "Biased estimates", "Reduced sample"], "dogru": "Biased estimates", "ipucu": "Model tahminleri sapar." },
        { "metin": "What does β1 measure?", "siklar": ["Impact of X on Y", "Intercept", "Error variance", "Bias term"], "dogru": "Impact of X on Y", "ipucu": "Eğim (Slope) neyi ifade eder?" },
        { "metin": "Technique starts with no predictors and adds step by step?", "siklar": ["Backward", "Forward selection", "Ridge", "Logistic"], "dogru": "Forward selection", "ipucu": "İleriye doğru adım adım." }
    ]
    # 50 soruya tamamla ve şıkları karıştırarak sabitle
    st.session_state.questions = []
    while len(st.session_state.questions) < 50:
        item = random.choice(raw_qs).copy()
        shuffled_siklar = item["siklar"].copy()
        random.shuffle(shuffled_siklar)
        item["fixed_siklar"] = shuffled_siklar
        st.session_state.questions.append(item)

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'start_time' not in st.session_state: st.session_state.start_time = None
# Joker Hakları (Toplam sınav için bir kez)
if 'joker_50_used' not in st.session_state: st.session_state.joker_50_used = False
if 'joker_hint_used' not in st.session_state: st.session_state.joker_hint_used = False
if 'joker_ai_used' not in st.session_state: st.session_state.joker_ai_used = False
# Aktif sorudaki joker durumu
if 'active_50_for_current' not in st.session_state: st.session_state.active_50_for_current = False

# --- GİRİŞ EKRANI ---
if st.session_state.step == "GIRIS":
    st.title("🎓 Ekonometri Soru Bankası")
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
    kalan = max(0, (50 * 60) - gecen)
    
    st.sidebar.title(f"👤 {st.session_state.user_name}")
    st.sidebar.metric("⏳ Kalan Süre", f"{int(kalan // 60)}:{int(kalan % 60):02d}")
    
    st.title("Sınav Uygulaması")
    st.progress((st.session_state.q_idx + 1) / 50)
    
    q = st.session_state.questions[st.session_state.q_idx]
    st.subheader(f"Soru {st.session_state.q_idx + 1}")
    st.info(q['metin'])

    # --- JOKER PANELİ ---
    st.write("### 🃏 Jokerler")
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
        if jc3.button("🤖 AI Analizi"):
            st.session_state.joker_ai_used = True
            st.write("🤖 AI Tahmini:")
            st.bar_chart({s: (75 if s == q['dogru'] else random.randint(5, 15)) for s in q['fixed_siklar']})

    # --- ŞIKLAR ---
    current_options = q['fixed_siklar']
    if st.session_state.active_50_for_current:
        # Doğruyu ve rastgele bir yanlışı tut, diğerlerini boş göster
        wrong_options = [s for s in q['fixed_siklar'] if s != q['dogru']]
        stay_wrong = random.choice(wrong_options)
        current_options = [s if (s == q['dogru'] or s == stay_wrong) else "---" for s in q['fixed_siklar']]

    user_choice = st.radio("Cevabınız:", current_options, key=f"radio_{st.session_state.q_idx}")
    if user_choice and user_choice != "---":
        st.session_state.answers[st.session_state.q_idx] = user_choice

    # --- ÖZEL BUTONLAR ---
    st.write("---")
    col_ans, col_finish = st.columns(2)
    if col_ans.button("✅ Cevabı Gör"):
        st.success(f"Bu sorunun doğru cevabı: {q['dogru']}")
    
    if col_finish.button("🛑 Sınavı Bitir"):
        st.session_state.step = "SONUC"
        st.rerun()

    # --- NAVİGASYON ---
    nav1, nav2, nav3 = st.columns([1,2,1])
    if nav1.button("⬅️ Geri") and st.session_state.q_idx > 0:
        st.session_state.q_idx -= 1
        st.session_state.active_50_for_current = False
        st.rerun()
    
    if nav3.button("İleri ➡️"):
        if st.session_state.q_idx < 49:
            st.session_state.q_idx += 1
            st.session_state.active_50_for_current = False
            st.rerun()
        else:
            st.session_state.step = "SONUC"
            st.rerun()

# --- SONUÇ EKRANI ---
elif st.session_state.step == "SONUC":
    st.title("🎊 Sınav Sonucu")
    dogru_sayisi = sum(1 for i, q in enumerate(st.session_state.questions) if st.session_state.answers.get(i) == q['dogru'])
    puan = (dogru_sayisi / 50) * 100
    
    st.header(f"Tebrikler {st.session_state.user_name}!")
    st.metric("Puan", f"{puan}%", f"{dogru_sayisi} Doğru")
    
    if st.button("🔄 Yeniden Başla"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
