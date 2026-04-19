# Açık Kaynak Analiz Uygulaması - Electron Edition

<p align="center">
  <img src="showcase.png" width="100%" alt="Showcase" />
</p>

**Açık Kaynak Analiz Uygulaması**, bilgisayarınızdaki dosya karmaşasını saniyeler içinde çözen, "Parlayan Gece Mavisi" (Night Blue) temalı akıllı dosya organizatörüdür. Electron mimarisi ile hem hızlı hem de görsel olarak premium bir deneyim sunar.

## ✨ Özellikler

- 🌌 **Ferah ve Modern Tasarım:** Göz yormayan "Gece Mavisi" teması, glassmorphism detayları ve akıcı animasyonlarla ferah bir kullanıcı deneyimi.
- 📂 **Özgür Klasör Analizi:** İstediğiniz herhangi bir klasörü saniyeler içinde derinlemesine analiz edip dosya türlerine göre kategorize etme.
- 🚀 **Esnek Transfer Seçenekleri:** Analiz edilen dosyaları belirlediğiniz hedefe ister tamamen **transfer edebilir (taşıyabilir)**, isterseniz de **kopyalayabilirsiniz**.
- ⚡ **Yüksek Performans:** Node.js çekirdeği sayesinde binlerce dosyayı donma yaşamadan işleme.

## 🚧 Yapım Aşamaları

1. **Python Prototiplenmesi:** Uygulamanın temel dosya taşıma/kopyalama mantığı ilk olarak Python ile test edildi.
2. **Electron Mimarisine Geçiş:** Daha modern, hızlı ve derlenebilir bir arayüz için Node.js ve Electron.js altyapısına geçildi.
3. **Ferah Tasarımın İnşası (Night Blue):** Kullanıcıyı yormayan, estetik ve fütüristik bir UI/UX tasarlandı.
4. **IPC Entegrasyonu:** Arayüz ile çekirdek dosya sistemi (fs-extra) arasında güvenli asenkron iletişim kuruldu.
5. **Açık Kaynak Yayını:** Toplulukla paylaşılmak üzere kodlar temizlendi ve GitHub'da yayımlandı.

## 🛠️ Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/Enous/Enpai-Analiz.git
   ```
2. Bağımlılıkları kurun:
   ```bash
   npm install
   ```
3. Uygulamayı başlatın:
   ```bash
   npm start
   ```

---
Developed with 💜 by [Enous](https://github.com/Enous)
