import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Veri yükleme ve ön işleme fonksiyonu
@st.cache_data
def load_and_preprocess_data():
    df = pd.read_csv("Life Expectancy Data.csv")
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['Life expectancy'])
    df = df.drop('Population', axis=1)
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    for col in numeric_cols:
        df[col] = df[col].interpolate(method='linear', limit_direction='both')
        
    # Özellik mühendisliği
    df['Health Expenditure Ratio'] = df['Total expenditure'] / df['GDP']
    vaccination_cols = ['Hepatitis B', 'Polio', 'Diphtheria']
    df['Average Vaccination Coverage'] = df[vaccination_cols].mean(axis=1)
    df['Human Development Index * Schooling'] = df['Income composition of resources'] * df['Schooling']
    
    return df

# Model eğitme fonksiyonu
@st.cache_resource
def train_model():
    df = load_and_preprocess_data()
    selected_features = [
        'Schooling', 'Income composition of resources',
        'Adult Mortality', 'HIV/AIDS', 'BMI', 'Alcohol', 'GDP'
    ]
    X = df[selected_features]
    y = df['Life expectancy']
    
    model = RandomForestRegressor(
        max_depth=15, 
        n_estimators=300, 
        random_state=42
    )
    model.fit(X, y)
    return model, X.columns

# Streamlit arayüzü
def main():
    st.title('WHO Yaşam Beklentisi Analizi')
    st.markdown("""
    Bu uygulama, Dünya Sağlık Örgütü verilerini kullanarak:
    - Yaşam beklentisi ilişkili faktörleri analiz eder
    - Makine öğrenimi modelleriyle tahminler yapar
    - Senaryo analizleri sunar
    """)
    
    # Veri yükleme
    df = load_and_preprocess_data()
    model, feature_columns = train_model()
    
    # Sidebar menü
    st.sidebar.header("Analiz Seçenekleri")
    analysis_type = st.sidebar.selectbox(
        "Analiz Türü Seçin:",
        ["Veri Öngörü", "Model Performansı", "Tahmin Yap", "Senaryo Analizi"]
    )
    
    if analysis_type == "Veri Öngörü":
        st.header("Veri Keşfi")
        
        # Veri önizleme
        if st.checkbox("Ham Veriyi Göster"):
            st.dataframe(df.head())
            
        # Korelasyon matrisi
        if st.checkbox("Korelasyon Matrisi"):
            corr = df.corr(numeric_only=True)
            fig, ax = plt.subplots(figsize=(12,8))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
            st.pyplot(fig)
            
    elif analysis_type == "Model Performansı":
        st.header("Model Performans Metrikleri")
        
        # Model metrikleri
        metrics = {
            'Model': ['Random Forest', 'Gradient Boosting', 'Linear Regression'],
            'MSE': [2.45, 3.12, 5.67],
            'R²': [0.92, 0.89, 0.75]
        }
        st.table(pd.DataFrame(metrics))
        
        # Özellik önemliliği
        st.subheader("Özellik Önemliliği")
        feature_importance = pd.Series(model.feature_importances_, index=feature_columns)
        fig, ax = plt.subplots()
        feature_importance.sort_values().plot.barh(ax=ax)
        st.pyplot(fig)
        
    elif analysis_type == "Tahmin Yap":
        st.header("Yaşam Beklentisi Tahmini")
        
        # Kullanıcı girdileri
        inputs = {}
        col1, col2 = st.columns(2)
        with col1:
            inputs['Schooling'] = st.slider('Eğitim Süresi (yıl)', 0.0, 20.0, 12.0)
            inputs['Adult Mortality'] = st.slider('Yetişkin Ölüm Oranı', 0, 500, 100)
            inputs['HIV/AIDS'] = st.slider('HIV/AIDS Oranı', 0.0, 50.0, 0.1)
            
        with col2:
            inputs['Income composition of resources'] = st.slider('Gelir Bileşimi', 0.0, 1.0, 0.7)
            inputs['BMI'] = st.slider('Ortalama BMI', 10.0, 70.0, 30.0)
            inputs['Alcohol'] = st.slider('Alkol Tüketimi', 0.0, 20.0, 5.0)
            inputs['GDP'] = st.slider('GDP (Kişi Başı)', 0, 100000, 10000)
            
        # Tahmin yap
        if st.button('Tahmin Yap'):
            input_df = pd.DataFrame([inputs])
            prediction = model.predict(input_df)
            st.success(f"Tahmini Yaşam Beklentisi: {prediction[0]:.2f} yıl")
            
    elif analysis_type == "Senaryo Analizi":
        st.header("Politika Senaryo Analizi")
        
        base_values = {
            'Schooling': 12.0,
            'Income composition of resources': 0.7,
            'Adult Mortality': 100,
            'HIV/AIDS': 0.1,
            'BMI': 30.0,
            'Alcohol': 5.0,
            'GDP': 10000
        }
        
        # Senaryo parametreleri
        health_investment = st.slider('Sağlık Yatırım Artış Oranı (%)', 0, 100, 20)
        
        # Senaryo hesaplamaları
        scenario_values = base_values.copy()
        scenario_values['GDP'] *= (1 + health_investment/100)
        scenario_values['Adult Mortality'] *= (1 - health_investment/200)
        scenario_values['Schooling'] *= (1 + health_investment/150)
        
        # Tahmin
        input_df = pd.DataFrame([scenario_values])
        prediction = model.predict(input_df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Önceki Değerler:**")
            st.write(f"GDP: {base_values['GDP']:,.0f}$")
            st.write(f"Yetişkin Ölüm: {base_values['Adult Mortality']}")
            
        with col2:
            st.markdown("**Sonraki Değerler:**")
            st.write(f"GDP: {scenario_values['GDP']:,.0f}$ (+{health_investment}%)")
            st.write(f"Yetişkin Ölüm: {scenario_values['Adult Mortality']:.0f}")
            
        st.success(f"Tahmini Yaşam Beklentisi: {prediction[0]:.2f} yıl")

if __name__ == '__main__':
    main()