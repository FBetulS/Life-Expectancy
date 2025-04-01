import streamlit as st
import pandas as pd
import joblib
import json
from sklearn.ensemble import RandomForestRegressor

try:
    model = joblib.load('life_expectancy_model_v2.pkl')
except Exception as e:
    st.error(f"Model yüklenirken hata oluştu: {str(e)}")
    st.stop()

with open('selected_features.json', 'r') as f:
    selected_features = json.load(f)

st.title('Yaşam Beklentisi Tahmini')


# Kullanıcı girişleri
st.sidebar.header('Ülke Bilgilerini Girin')

inputs = {}
for feature in selected_features:
    if feature == 'Schooling':
        inputs[feature] = st.sidebar.slider('Ortalama Eğitim Yılı (Schooling)', 0.0, 20.0, 12.0)
    elif feature == 'Income composition of resources':
        inputs[feature] = st.sidebar.slider('Gelir Bileşimi (0-1)', 0.0, 1.0, 0.7)
    elif feature == 'Adult Mortality':
        inputs[feature] = st.sidebar.slider('Yetişkin Ölüm Oranı (1000 kişide)', 0, 500, 100)
    elif feature == 'HIV/AIDS':
        inputs[feature] = st.sidebar.slider('HIV/AIDS Oranı (%)', 0.0, 50.0, 0.1)
    elif feature == 'BMI':
        inputs[feature] = st.sidebar.slider('Ortalama BMI', 10.0, 70.0, 50.0)
    elif feature == 'Alcohol':
        inputs[feature] = st.sidebar.slider('Alkol Tüketimi (litre/kişi)', 0.0, 20.0, 5.0)
    elif feature == 'GDP':
        inputs[feature] = st.sidebar.slider('GDP (kişi başı)', 0, 100000, 10000)

# Tahmin yap
if st.button('Yaşam Beklentisini Tahmin Et'):
    input_df = pd.DataFrame([inputs])
    prediction = model.predict(input_df)[0]
    st.success(f'Tahmini Yaşam Beklentisi: {prediction:.1f} yıl')
    
    # Ek bilgi
    st.subheader('Önemli Faktörler')
    st.markdown("""
    - Eğitim seviyesi (Schooling)
    - Gelir bileşimi (Income composition)
    - Yetişkin ölüm oranı
    - HIV/AIDS oranı
    - Vücut kitle indeksi (BMI)
    - Alkol tüketimi
    - Kişi başına düşen GDP
    """)

st.markdown("""
**Not:** Bu uygulama Dünya Sağlık Örgütü verilerine dayalı bir makine öğrenimi modeli kullanmaktadır.
""")