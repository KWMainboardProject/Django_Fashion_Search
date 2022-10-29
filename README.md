# Django_Fashion_Search
This project uses Django REST API and Pythorch. It provides an API with a function to analyze clothes in photos and a function to search clothes using attributes. It Provides the functions necessary for shopping malls as APIs.

# How to install
```bash
git clone https://github.com/KWMainboardProject/Django_Fashion_Search.git
git submodule update --init --recursive
cd src
```
##### Next Step. Set {$ROOT}/src/secrets.json
```json
# example
{"SECRET_KEY":"django-insecure-d*upt!(-*)wA#3^cdc-e9ac3s4s8afd9d4m=_2(!a+2v&@1avs2s4v="}
```

# How to Set Development Environment with Anaconda(or PIP)
https://pytorch.org/get-started/locally/
```bash
conda create -n fashion-api python=3.8.2 -y
conda activate fashion-api
# GPU - CONDA
conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=11.1 -c pytorch -c conda-forge -y
# CPU - CONDA
# conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
```

# How to initialize ENV with Anaconda(or PIP)
```bash
pip install -r requirements.txt
```

# How to run with Anaconda(or PIP)
```bash
# Check if the django works well
python manage.py runserver
```
```bash
# Check if the pytorch works well
cd analysis/detect
python DetectObjectPipe.py
```
