import streamlit as st
import time
import random

# --- SAYFA VE ARAYÜZ AYARLARI ---
st.set_page_config(page_title="Ekonometri Sınavı", layout="centered")

# Sağ üstteki Streamlit butonlarını gizlemek için CSS
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- VERİ TABANI ---
if 'questions' not in st.session_state:
    raw_qs = [
        { 
            "metin": "What happens if we omit an important variable from the regression model or forget to include it?", 
            "siklar": ["Biased estimates", "Multicollinearity", "Heteroskedasticity", "Reduced sample"], 
            "dogru": "Biased estimates", 
            "ipucu": "Model gerçeği tam yansıtmazsa tahminler sapar (bias)." 
        },
        { "metin": "What does β0 represent in a simple linear regression model?", "siklar": ["The slope", "The intercept", "The error term", "The variance"], "dogru": "The intercept", "ipucu": "Y eksenini kestiği nokta." },
        { "metin": "Which method is most commonly used to estimate parameters in linear regression?", "siklar": ["Maximum likelihood", "Method of moments", "OLS", "WLS"], "dogru": "OLS", "ipucu": "Kareler toplamını minimize eder." }
    ]
    
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
if 'joker_50_used' not in st.session_state: st.session_state.joker_50_used = False
if 'joker_hint_used' not in st.session_state: st.session_state.joker_hint_used = False
if 'joker_ai_used' not in st.session_state: st.session_state.joker_ai_used = False
if 'active_50_for_current' not in st.session_state: st.session_state.active_50_for_current = False
if 'balloons_done' not in st.session_state: st.session_state.balloons_done = False

# --- GİRİŞ EKRANI ---
if st.session_state.step == "GIRIS":
    st.title("🎓 Ekonometri Sınavı")
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
    
    # İstatistiklerin Hesaplanması
    cevaplanan = len(st.session_state.answers)
    toplam = 50
    kalan_soru = toplam - (st.session_state.q_idx + 1)
    bos_soru = (st.session_state.q_idx) - cevaplanan
    if bos_soru < 0: bos_soru = 0

    # Sidebar Panel
    st.sidebar.title(f"👤 {st.session_state.user_name}")
    st.sidebar.metric("⏳ Kalan Süre", f"{int(kalan_zaman // 60)}:{int(kalan_zaman % 60):02d}")
    st.sidebar.write("---")
    st.sidebar.write(f"✅ **Cevaplanan:** {cevaplanan}")
    st.sidebar.write(f"⚪ **Boş Bırakılan:** {bos_soru}")
    st.sidebar.write(f"📝 **Kalan Soru:** {max(0, toplam - (st.session_state.q_idx + 1))}")
    
    # İlk 3 Soru Balon Kontrolü
    if not st.session_state.balloons_done and st.session_state.q_idx >= 3:
        dogru_ilk_uc = 0
        for i in range(3):
            if st.session_state.answers.get(i) == st.session_state.questions[i]['dogru']:
                dogru_ilk_uc += 1
        if dogru_ilk_uc == 3:
            st.balloons()
            st.toast("Harika başlangıç! İlk 3 soru doğru!", icon="🔥")
            st.session_state.balloons_done = True

    st.progress((st.session_state.q_idx + 1) / 50)
    q = st.session_state.questions[st.session_state.q_idx]
    st.subheader(f"Soru {st.session_state.q_idx + 1}")
    st.info(q['metin'])

    # Jokerler
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
            st.bar_chart({s: (75 if s == q['dogru'] else random.randint(5, 15)) for s in q['fixed_siklar']})

    # Şıklar
    opts = q['fixed_siklar']
    if st.session_state.active_50_for_current:
        wrong = [s for s in q['fixed_siklar'] if s != q['dogru']]
        stay = random.choice(wrong)
        opts = [s if (s == q['dogru'] or s == stay) else "---" for s in q['fixed_siklar']]

    user_choice = st.radio("Cevabınız:", opts, key=f"radio_{st.session_state.q_idx}", index=None)
    if user_choice and user_choice != "---":
        st.session_state.answers[st.session_state.q_idx] = user_choice

    st.write("---")
    c_ans, c_fin = st.columns(2)
    if c_ans.button("✅ Cevabı Gör"): st.success(f"Doğru Cevap: {q['dogru']}")
    if c_fin.button("🛑 Sınavı Bitir"):
        st.session_state.step = "SONUC"
        st.rerun()

    n1, n2, n3 = st.columns([1,2,1])
    if n1.button("⬅️ Geri") and st.session_state.q_idx > 0:
        st.session_state.q_idx -= 1
        st.session_state.active_50_for_current = False
        st.rerun()
    if n3.button("İleri ➡️"):
        if st.session_state.q_idx < 49:
            st.session_state.q_idx += 1
            st.session_state.active_50_for_current = False
            st.rerun()
        else:
            st.session_state.step = "SONUC"
            st.rerun()

# --- SONUÇ EKRANI ---
elif st.session_state.step == "SONUC":
    st.title("📊 Sınav Karnesi")
    dogru = 0
    yanlis = 0
    bos = 0
    
    for i in range(50):
        user_ans = st.session_state.answers.get(i)
        correct_ans = st.session_state.questions[i]['dogru']
        if user_ans is None: bos += 1
        elif user_ans == correct_ans: dogru += 1
        else: yanlis += 1
            
    puan = (dogru / 50) * 100
    
    st.write("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Toplam", "50")
    col2.metric("Doğru ✅", dogru)
    col3.metric("Yanlış ❌", yanlis)
    col4.metric("Boş ⚪", bos)
    
    st.metric("BAŞARI PUANI", f"%{puan}")

    if st.button("🔄 Yeni Sınav"):
        st.session_state.clear()
        st.rerun()
