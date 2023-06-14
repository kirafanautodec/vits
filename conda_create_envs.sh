sudo apt-get install espeak -y

conda create -n vits python==3.8 -y
conda activate vits && \
pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/