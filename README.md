# Life Expectancy (WHO)
# 🌍 Hayat Beklentisi (WHO) Projesi

Bu proje, Dünya Sağlık Örgütü (WHO) tarafından sağlanan verileri kullanarak hayat beklentisini etkileyen faktörleri incelemeyi amaçlamaktadır. Geçmişte yapılan çalışmalarda genellikle demografik değişkenler, gelir bileşimi ve ölüm oranları gibi etmenler ele alınmış, ancak aşılamanın ve insan gelişim indeksinin etkileri yeterince araştırılmamıştır. 

⚠️ Not
3D grafiklerim ve görselleştirmelerim maalesef gözükmüyor. Bu durum, bazı tarayıcı veya platform uyumsuzluklarından kaynaklanabilir.

## ## 🔗 Hugging Face Uygulaması
[Hayat Beklentisi - Hugging Face Space](https://huggingface.co/spaces/btulftma/Life_Expectancy)

## 🔗 Kaggle Veri Seti
[Hayat Beklentisi Veri Seti](https://www.kaggle.com/datasets/kumarajarshi/life-expectancy-who)

## 📊 Proje Aşamaları
1. **Veri Temizleme ve Ön İşleme**:
   - Eksik değerlerin interpolasyon yöntemiyle doldurulması.
   - Kategorik değişkenlerin dummy değişkenlere dönüştürülmesi.
   - Yeni özelliklerin türetilmesi:
     - Sağlık Harcamalarının GDP'ye Oranı
     - Aşı Oranlarının Ortalaması
     - İnsani Gelişme Endeksi ve Eğitim Seviyesi Etkileşimi

2. **Modelleme**:
   - Karma etkiler modeli ve çoklu doğrusal regresyon analizi.
   - Farklı makine öğrenimi modellerinin (Linear Regression, Random Forest, Gradient Boosting, SVR, K-Nearest Neighbors, Decision Tree) kullanılması.

3. **Değerlendirme**:
   - Modellerin performans metrikleri (MSE, R2) ile değerlendirilmesi.
   - Özellik önemliliğinin belirlenmesi.

4. **Senaryo Analizi**:
   - Türkiye için yaşam beklentisi tahmini yapılması.
   - Farklı senaryoların yaşam beklentisi üzerindeki etkisinin analizi.

## 🔍 Analiz Sonuçları
- **Güçlü Yönler**:
  - %90 doğruluk ile başarılı sınıflandırma.
  - Aşı oranları, sağlık harcamaları ile yaşam beklentisi arasında güçlü bir ilişki.
  
- **Zayıf Yönler**:
  - Gömlek sınıfında düşük performans.
  - Spor Ayakkabı ve Ceket arasında karışıklıklar.

## 🚀 İyileştirme ve Gelecek Çalışmalar
- Batch Normalization ve Learning Rate Scheduler eklenmesi.
- ResNet gibi pre-trained modellerin kullanımı.
- Grad-CAM ile model açıklanabilirliği.
- CutMix, MixUp veri artırma teknikleri.

## 📈 Sonuç
Proje, yaşam beklentisini etkileyen faktörler hakkında önemli bilgiler sunmaktadır. Bu bilgiler, sağlık politikaları geliştirilebilir ve kaynaklar daha etkili bir şekilde yönlendirilebilir. En iyi performansı gösteren Random Forest modeli ile Türkiye için tahmini yaşam beklentisi 76.18 yıl olarak hesaplanmıştır. 

Bu çalışma, ülkelerin yaşam süresini iyileştirmek için hangi alanlara odaklanmaları gerektiği konusunda önemli bilgiler sunmaktadır.
