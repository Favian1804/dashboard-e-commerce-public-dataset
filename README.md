# Setup Environment - Anaconda

Buat dan aktifkan environment menggunakan Anaconda:

conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt


# Setup Environment - Shell/Terminal

Jika menggunakan terminal biasa:

mkdir Submission
cd Submission
pipenv install
pipenv shell
pip install -r requirements.txt

# Menjalankan Streamlit App
Jalankan aplikasi dengan perintah berikut:

streamlit run dashboard.py
