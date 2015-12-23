cd ~

#Update existing packages and distro
apt-get update
apt-get -y dist-upgrade

#Install dependencies
apt-get install -y git wget unzip zip
apt-get install -y python-pip cython cython3 libxml2-dev libicu-dev

pip install pickle

#Bootstrap LaMachine environment
git clone https://github.com/proycon/LaMachine lama
bash lama/virtualenv-bootstrap.sh -y

#Git pull the newest version
cd text-mining
git pull

#Create necessary folders
cd project/tools
bash create_folders.sh
cd ../data

#Download plaintext data, unzip
wget -O plaintext.zip https://www.googledrive.com/host/0B1VA6lQr6QuOZzhwcEZEMFYyRUU
unzip -q plaintext.zip

#Go to home
cd ~
