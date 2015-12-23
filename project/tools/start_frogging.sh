#Run from text-mining folder (root folder)
#Activate LaMachine environment
cd ~
. lamachine/bin/activate

#Get todo for frog job
wget -O text-mining/project/data/frog_todo.p https://dl.dropboxusercontent.com/u/43693599/_frog_todo.p

cd text-mining/project/src
python frog_local.py
