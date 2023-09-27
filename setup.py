from setuptools import setup, find_packages

with open('requirements.txt', encoding="utf-8") as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='scoss',
    description='Connect Zalo OA API',
    author='Vien Tran',
    author_email='tranvanvien98bg@gmail.com',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.7',
    url="https://github.com/ThinklabsDev/zalo_sdk",
    download_url="",
    classifiers=[]
)
