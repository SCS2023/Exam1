import streamlit as st
import time
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ekonometri Sınavı", layout="centered")

# --- VERİ TABANI ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        { "metin": "What does β0 represent in a simple linear regression model?", "siklar": ["The slope", "The intercept", "The error term", "The variance"], "dogru": "The intercept", "ipucu": "Y eksenini kestiği noktayı düşün." },
        { "metin": "Which method is most commonly used to estimate parameters in linear regression?", "siklar": ["Maximum likelihood", "Method of moments", "OLS", "WLS"], "dogru": "OLS", "ipucu": "Kareler toplamını minimize eden yöntem." },
        { "metin": "In regression, what does an outlier refer to?", "siklar": ["Missing value", "Data point far from others", "Dummy variable", "Perfect value"], "dogru": "Data point far from others", "ipucu": "Diğer veri noktalarından çok uzakta olan bir değer." },
        { "metin": "Which transformation can help address heteroskedasticity?", "siklar": ["Taking logarithms", "Adding outliers", "Dropping intercept", "Sample size"], "dogru": "Taking logarithms", "ipucu": "Varyansı sabitlemek için veriyi sıkıştıran bir işlem." },
        { "metin": "What does OLS minimize in regression?", "siklar": ["Sum of residuals", "Sum of squared residuals", "Maximum likelihood", "Variance of X"], "dogru": "Sum of squared residuals", "ipucu": "Hataların karesiyle ilgilidir." },
        # ... (Diğer 20 soruyu buraya ekleyebilirsiniz, sistem 50'ye otomatik tamamlar)
    ]
    # 50 soruya tamamla
    base_qs = st.session_state.questions.copy()
    while len(st.session_state.questions) < 50:
        st.session_state.questions.append(random.choice(base_qs).copy())

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'joker_count' not in st.session_state: st.session_state.joker_count = 1
if 'joker_used_in_round' not in st.session_state: st.session_state.joker_used_in_round = False
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'active_joker' not in st.session_state: st.session_state.active_joker = None

# --- GİRİŞ EKRANI ---
if st.session_state.step == "GIRIS":
    st.title("🎓 Akademik Sınav Portalı")
    st.write("Lütfen devam etmek için bilgilerinizi giriniz.")
    ad = st.text_input("Adınız:")
    soyad = st.text_input("Soyadınız:")
    
    if st.button("Sınava Başla"):
        if ad and soyad:
            st.session_state.user_name = f"{ad} {soyad}"
            st.session_state.step = "SINAV"
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.error("Lütfen tüm alanları doldurun.")

# --- SINAV EKRANI ---
elif st.session_state.step == "SINAV":
    gecen = time.time() - st.session_state.start_time
    kalan = max(0, (50 * 60) - gecen)
    
    st.sidebar.title(f"👤 {st.session_state.user_name}")
    st.sidebar.metric("⏳ Kalan Süre", f"{int(kalan // 60)}:{int(kalan % 60):02d}")
    st.sidebar.metric("🃏 Joker Hakkı", st.session_state.joker_count)
    
    st.title("Soru Bankası")
    st.progress((st.session_state.q_idx + 1) / 50)
    
    q = st.session_state.questions[st.session_state.q_idx]
    st.subheader(f"Soru {st.session_state.q_idx + 1}")
    st.info(q['metin'])

    # Joker Paneli
    j1, j2, j3 = st.columns(3)
    if st.session_state.joker_count > 0:
        if j1.button("✂️ %50"): st.session_state.active_joker = '50-50'; st.session_state.joker_count -= 1; st.session_state.joker_used_in_round = True
        if j2.button("💡 İpucu"): st.session_state.active_joker = 'hint'; st.session_state.joker_count -= 1; st.session_state.joker_used_in_round = True
        if j3.button("🤖 AI"): st.session_state.active_joker = 'audience'; st.session_state.joker_count -= 1; st.session_state.joker_used_in_round = True

    # Şıkların Hazırlanması
    opts = q['siklar'].copy()
    if st.session_state.active_joker == '50-50':
        wrong = [s for s in q['siklar'] if s != q['dogru']]
        removed = random.sample(wrong, 2)
        opts = [s for s in q['siklar'] if s not in removed]
    elif st.session_state.active_joker == 'hint':
        st.warning(f"İpucu: {q['ipucu']}")
    elif st.session_state.active_joker == 'audience':
        st.write("🤖 AI Olasılık Tahmini:")
        st.bar_chart({s: (80 if s == q['dogru'] else random.randint(5, 15)) for s in q['siklar']})

    key = f"q_{st.session_state.q_idx}"
    choice = st.radio("Cevabınız:", opts, key=key)
    if choice: st.session_state.answers[st.session_state.q_idx] = choice

    # Navigasyon
    st.write("---")
    c1, c2, c3 = st.columns([1,1,1])
    if c1.button("⬅️ Geri") and st.session_state.q_idx > 0:
        st.session_state.q_idx -= 1; st.session_state.active_joker = None; st.rerun()
    
    if c3.button("İleri ➡️"):
        if st.session_state.q_idx < 49:
            st.session_state.q_idx += 1; st.session_state.active_joker = None
            if st.session_state.q_idx % 10 == 0:
                if not st.session_state.joker_used_in_round: st.session_state.joker_count += 1
                st.session_state.joker_used_in_round = False
            st.rerun()
        else:
            st.session_state.step = "SONUC"; st.rerun()

# --- SONUÇ EKRANI ---
elif st.session_state.step == "SONUC":
    st.title("🎊 Sınav Sonuçları")
    st.header(f"Tebrikler, {st.session_state.user_name}!")
    
    dogru_sayisi = 0
    for i, q in enumerate(st.session_state.questions):
        if st.session_state.answers.get(i) == q['dogru']:
            dogru_sayisi += 1
    
    puan = (dogru_sayisi / 50) * 100
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Doğru", dogru_sayisi)
    c2.metric("Yanlış", 50 - dogru_sayisi)
    c3.metric("Başarı Puanı", f"{puan}%")
    
    
    
    if puan >= 70:
        st.success("Harika bir performans! Veri bilimi konusunda oldukça yetkinsiniz.")
    else:
        st.warning("Biraz daha pratik yaparak puanınızı yükseltebilirsiniz.")
        
    if st.button("Sınavı Yeniden Başlat"):
        st.session_state.clear()
        st.rerun()
