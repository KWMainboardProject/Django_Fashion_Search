# Django_Fashion_Search
This project uses Django REST API and Pythorch. It provides an API with a function to analyze clothes in photos and a function to search clothes using attributes. It Provides the functions necessary for shopping malls as APIs.

# How to install
```bash
git clone https://github.com/KWMainboardProject/Django_Fashion_Search.git
git submodule update --init --recursive
cd src
```
### Next Step. Set {$ROOT}/src/secrets.json
```json
# example
{"SECRET_KEY":"django-insecure-d*upt!(-*)wA#3^cdc-e9ac3s4s8afd9d4m=_2(!a+2v&@1avs2s4v="}
```

### Next Step. Set weights files to {$ROOT}/src/weights
다운로드 링크
###### yolov5 - fashion detector
https://drive.google.com/file/d/1u3uS9ZpjCUmRnygRs2looIxrdRvXcSYf/view?usp=sharing

###### u2net - segmentation (https://github.com/xuebinqin/U-2-Net)
https://drive.google.com/file/d/1vSmKAFtCiGOudu5_7V2HnA-96rTG3v1Z/view?usp=sharing

###### resnet34 - subcategory_top
https://drive.google.com/file/d/182MLAqJ0pNHbvRA_WqeVTQyC8-kflieQ/view?usp=sharing

###### resnet34 - subcategory_bottom
https://drive.google.com/file/d/164dWo_t40hsmdG3cHm3HdqWAgmNehU2o/view?usp=sharing

###### resnet34 - subcategory_overall
https://drive.google.com/file/d/1VUGialL52mITdG6NjBErSBytcnpkNr4u/view?usp=sharing

###### resnet34 - subcategory_outer
https://drive.google.com/file/d/1bHUZ2BG8qluh1YqaUDmoSqdViks8mQEi/view?usp=sharing

###### resnet34 - pattern
https://drive.google.com/file/d/1MSL4YsaIKmEE7tv7S8qqglm_pgnOyKFM/view?usp=sharing

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
