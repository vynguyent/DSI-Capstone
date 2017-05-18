sudo apt-get install mongodb
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
sh Miniconda2-latest-Linux-x86_64.sh -b
echo "export PATH=/home/ubuntu/miniconda2/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
conda install -y ipython
conda install -y pymongo
conda install -y pandas

sudo mkdir -p /data/db
sudo mongod &
