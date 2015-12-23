#Run from text-mining folder (root folder)
#Activate LaMachine environment
cd project/src
. ../../lamachine/bin/activate

#Get todo for frog job
wget -O ../data/frog_todo.p https://dl.dropboxusercontent.com/u/43693599/_frog_todo.p
python frog_local.py
