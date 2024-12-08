# Peek-A-Job (Aplikasi Screening Otomatis Data Pelamar Kerja)

## Made By Kelompok 7
- Laurencia Reva Anjaya / I0324130 [@Laurencia-Reva](https://github.com/Laurencia-Reva)
- Mohammad Arief Rahman / I0324126 [@ariefrahman-coc](https://github.com/ariefrahman-coc)
- Ni Made Adellia Marchela Putri / I0324132 [@adelliaamp](https://github.com/adelliaamp)


## Background of the app

### Mengapa aplikasi ini dibuat?
Aplikasi ini dapat membantu mempercepat proses seleksi administrasi, mengurangi kemungkinan kesalahan manual, serta mempermudah perusahaan untuk segera mengidentifikasi pelamar yang memenuhi kriteria.

### Apa yang dilakukan aplikasi ini?
Aplikasi ini adalah alat yang dirancang untuk membantu menyaring data pelamar kerja secara otomatis di suatu pabrik. Aplikasi ini menganalisis data pelamar yang diinputkan dalam format CSV atau Excel, lalu menilai apakah pelamar memenuhi kriteria administrasi yang telah ditentukan.

### Siapa yang dapat menggunakan aplikasi ini?
Aplikasi ini ditujukan untuk digunakan oleh tim rekrutmen atau HR di perusahaan, terutama di pabrik-pabrik yang memiliki banyak pelamar dan membutuhkan proses seleksi yang cepat dan efisien.

### Kapan aplikasi ini dapat digunakan?
Aplikasi digunakan selama proses rekrutmen, khususnya pada tahap awal seleksi administrasi, saat perusahaan menerima banyak data pelamar kerja.

### Dimana saja aplikasi ini dapat digunakan?
Aplikasi dapat digunakan di mana saja, baik di kantor HR perusahaan atau tempat lain, asalkan memiliki perangkat yang mendukung pengoperasian aplikasi (komputer atau laptop).

### How it works (bagaimana cara bekerja nya)?
1. Data formulir pelamar kerja dalam format csv atau excel bisa langsung dimasukkan ke aplikasi, kemudian secara otomatis menilai apakah pelamar memenuhi kriteria yang ditentukan. 
2. Konfigurasi penilaian atau syarat kelolosan administrasi data pelamar dapat diatur secara dinamis di dalam aplikasi sebelum menginput file csv atau excel
3. Fitur analytics preview data dapat digunakan oleh recruiter untuk melihat hasil seleksi-seleksi yang saudah dilakukan dengan berbagai fitur filtering data yang lengkap dan cepat, fitur ini akan sangat membantu recruiter dalam membuat pelaporan terhadap atasannya.
4. Aplikasi diberikan proses autentikasi ber hirarki untuk menghindari akses yang tidak sah mengakses aplikasi ini, akses admin terhadap aplikasi aman dan eksklusif untuk user akun tertentu (Head of HR). 

## Get started

Pastikan Anda memiliki lingkungan Python. Berikut adalah tutorial untuk terminal Windows PowerShell: https://medium.com/@astontechnologies/how-to-setup-a-virtual-development-environment-for-python-with-windows-powershell-4cd34b2f9f9b

Atau, Anda juga bisa menggunakan lingkungan default Python di desktop (tidak terisolasi), dan ketik perintah berikut untuk menginstal semua library yang diperlukan untuk menjalankan skrip aplikasi ini:

```
pip install -r requirements.txt
```
*notes: semua library yang digunakan dan wajib diinsatal terdapat pada file `requirements.txt`
```
numpy==1.24.4
pandas==2.2.3
openpyxl>=3.1.0
python-dateutil==2.9.0.post0
pytz==2024.2
six==1.16.0
tk==0.1.0
tzdata==2024.2
pillow==11.0.0
```

Jalankan skrip aplikasi desktop menggunakan perintah berikut:

```
python main.py
```

## Flowchart

![Job-Applicants-Filtering-Automation](https://github.com/user-attachments/assets/5d3d82c2-fbbc-4dc0-81e0-8b05b91063e8)