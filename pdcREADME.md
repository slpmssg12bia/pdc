# Create Environment 
Ubuntu, t2micro, generate key (or select existing), select default security group, configure storage: 20, 
modify IAM role > select AmazonS3fullaccess, user must have SSH security access, connect with putty, log into server as user: ubuntu

# Update Environment 

```
sudo apt update 

sudo apt install unzip

sudo apt install python3-pip -y
```
# Install AWS CLI 
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

unzip awscliv2.zip

sudo ./aws/install
```

# Configure AWS CLI
```
aws configure

aws key

aws secret key

us-east-1

json
```

# Clone Git Repository
```
git clone https://github.com/slpmssg12bia/pdc.git
```
# cd into the repository
```
cd pdc
```
# Recreate bash Files
```

touch pdc_archive_s3.sh
nano pdc_archive_s3.sh

#!/bin/bash
aws s3 sync pdcdump/ s3://viquity-database-import-us-east-1/Jobs/pdc/pdc_archive/pdcdump-"$(date +%d-%m-%y-%H-%M)"/

ctrl X
Y

---------------------------------
touch pdc_clean.sh
nano pdc_clean.sh

#!/bin/bash
rm -rf pdcdump

ctrl X
Y
---------------------------------
touch pdc_cron.sh
nano pdc_cron.sh

#!/bin/bash
cd /home/ubuntu/pdc
python3 pdc_cron.py

ctrl X
Y
---------------------------------

touch pdc_dump_to_s3.sh
nano pdc_dump_to_s3.sh

#!/bin/bash
aws s3 sync pdcdump/ s3://viquity-database-import-us-east-1/Jobs/pdc/pdc_current_dump/pdcdump/

ctrl X
Y
---------------------------------

touch pdc_remove_old_dump.sh
nano pdc_remove_old_dump.sh

#!/bin/bash
aws s3 rm s3://viquity-database-import-us-east-1/Jobs/pdc/pdc_current_dump --recursive

ctrl X
Y
```

# Delete Original bash files
```
rm archive_s3.sh  clean.sh  cron.sh  dump_to_s3.sh  remove_old_dump.sh 
```

# Change Permissions of bash Files
```
chmod +x   pdc_archive_s3.sh  pdc_clean.sh  pdc_cron.sh  pdc_dump_to_s3.sh  pdc_remove_old_dump.sh     

```

# install pip dependencies
```
pip install -r pdc_requirements.txt 
```
# install Cron jobs for Parsing
```
pwd

sudo apt-get install cron
```
# Open Cron Tab
```
sudo su

pip install -r pdc_requirements.txt 

nano /etc/crontab
```
# Create Cron Job ~ https://crontab.guru/examples.html
```
05 05 15 * * root bash /home/ubuntu/pdc/pdc_cron.sh
!!!CARRIAGE RETURN after line above!!!!!

ctrl x

y

enter
```
