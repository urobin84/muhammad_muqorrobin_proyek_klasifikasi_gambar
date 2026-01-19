# Proyek Klasifikasi Gambar: KITTI Object Detection

Proyek ini adalah submission untuk kelas "Belajar Pengembangan Machine Learning". Fokus utama proyek ini adalah membangun model Convolutional Neural Network (CNN) untuk mengklasifikasikan gambar objek dari dataset KITTI ke dalam 4 kelas: **Car**, **Pedestrian**, **Cyclist**, dan **Van**.

## 🎯 Fitur & Kriteria Utama
- **Dataset**: Menggunakan dataset KITTI Vision Benchmark Suite (> 10.000 gambar).
- **Preprocessing**: Implementasi `ImageDataGenerator` untuk augmentasi data dan rescale.
- **Model**: Menggunakan arsitektur Sequential CNN dengan Conv2D, MaxPooling2D, Dropout, dan Dense layer.
- **Training**: Menggunakan optimizer `Adam`, loss `categorical_crossentropy`, dan callbacks (`EarlyStopping`, `ModelCheckpoint`).
- **Akurasi**: Target akurasi pada validation set > 85%.
- **Deployment**: Model dikonversi ke format **TF-Lite** (.tflite), **SavedModel** (PB), dan **TFJS** (JSON).

## �️ Tech Stack
- **Languages**: Python
- **Libraries**: TensorFlow/Keras, OpenCV, Antigravity (`agentic-ai`)
- **Tools**: Jupyter Notebook, VS Code

## 🔬 Methodology
1.  **Data Acquisition**: Dataset KITTI asli berupa 3D Tracklets dikonversi menjadi gambar 2D individual menggunakan matriks kalibrasi kamera stereoskopik.
2.  **Preprocessing**: Gambar di-resize ke ukuran 150x150 pixel dan dinormalisasi (rescale 1./255).
3.  **Modeling**: Membangun model CNN 3-block VGG-style dengan Dropout untuk mencegah overfitting.
4.  **Training**: Melatih model selama 10-20 epoch dengan Early Stopping.
5.  **Conversion**: Model terbaik dikonversi ke format mobile dan web (TFLite/TFJS).

## 📊 Results
- **Training Accuracy**: ~94.20% (Epoch 10)
- **Validation Accuracy**: **93.47%** (Melebihi target 85%)
- **Loss**: Menunjukkan konvergensi yang stabil dengan nilai validation loss **0.1588**.

![Training History](training_history.png)
*(Grafik Akurasi dan Loss selama proses training)*

![Inference Result](inference_result.png)
*(Contoh hasil prediksi model pada data test)*

## 📂 Struktur Folder Proyek
```
.
├───tfjs_model/          # Model format TensorFlow.js
├───tflite/              # Model format TFLite & label.txt
├───saved_model/         # Model format SavedModel (PB) & .h5
├───data_split/          # Dataset yang sudah dibagi (Train, Val, Test)
├───notebook.ipynb       # File notebook utama (Pipeline Lengkap)
├───README.md            # Dokumentasi proyek
├───requirements.txt     # File dependensi
├───crop_kitti.py        # Script ekstraksi dan cropping dataset KITTI
├───inference_result.png # Visualisasi hasil prediksi
└───training_history.png # Visualisasi grafik akurasi dan loss
```

## � License
**1. License**
Dataset yang digunakan dalam proyek ini adalah **The KITTI Vision Benchmark Suite**. Seluruh data dipublikasikan di bawah lisensi **Creative Commons Attribution-NonCommercial-ShareAlike 3.0 (CC BY-NC-SA 3.0)**.

Berdasarkan lisensi ini, proyek ini mengikuti ketentuan:
*   **Attribution (BY)**: Memberikan kredit/penghargaan kepada pencipta dataset asli.
*   **Non-Commercial (NC)**: Dataset dan model yang dihasilkan tidak digunakan untuk tujuan komersial atau mencari keuntungan.
*   **Share-Alike (SA)**: Jika proyek ini dimodifikasi atau dikembangkan lebih lanjut, distribusi harus menggunakan lisensi yang sama.

## ⚠️ Disclaimer
**2. Disclaimer**
*   **Academic Use Only**: Proyek ini dibangun murni untuk tujuan pembelajaran mandiri (*self-educational purposes*) dan pengembangan portofolio teknis.
*   **Privacy Awareness**: Kami sangat menghargai privasi. Dataset asli diambil di ruang publik (Karlsruhe, Jerman). Jika terdapat keberatan terkait data pribadi yang muncul dalam visualisasi proyek ini, silakan hubungi penyedia dataset asli sesuai kebijakan privasi KITTI.
*   **No Warranty**: Model AI yang dihasilkan dalam proyek ini adalah hasil latihan dan tidak disarankan untuk digunakan dalam sistem kendali kendaraan otonom nyata tanpa pengujian lebih lanjut yang memenuhi standar keamanan industri.

## 📚 Citations
**3. Citations**
Jika Anda menggunakan atau merujuk pada proyek ini, harap berikan sitasi kepada penulis asli dataset KITTI sebagai berikut:

```bibtex
@inproceedings{Geiger2012CVPR,
  author = {Andreas Geiger and Philip Lenz and Raquel Urtasun},
  title = {Are we ready for Autonomous Driving? The KITTI Vision Benchmark Suite},
  booktitle = {Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2012}
}
```

## 👤 Penulis
**Muhammad Muqorrobin**
*Proyek Submission Klasifikasi Gambar*
