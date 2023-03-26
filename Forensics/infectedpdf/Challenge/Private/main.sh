#!/bin/bash

# Setup environment
export DOMAIN="18.203.147.142"
export AMOUNT="1000"
export FLAG_FILE_CONTENT="Keep it hidden from Andre:CSC{th3_53cr3t_15_5ug3rcan3}"
export FLAG_FILE_NUMBER="969"

# Change directory to step_1
cd ./step_1

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt

# Run first Python script and wait until it finishes  (this will create the challenge PDF file)
echo "[*] Generating challenge PDF file"
python3 generate_chal.py $DOMAIN $AMOUNT
while [ ! -f Jeroen_Stew.pdf ]; do sleep 1; done

# Move output file to new location
echo "[*] Copying PDF file to Public folder"
mv Jeroen_Stew.pdf ../../Public/Jeroen_Stew.pdf

return
echo "[*] Step 1 cleanup"
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Change directory to step_2
cd ../step_2

# Run second Python script and wait until it finishes
echo "[*] Generating fake files and flag file"
python3 generate_files.py "$FLAG_FILE_CONTENT" $AMOUNT $FLAG_FILE_NUMBER

# Run Docker Compose
echo "[*] Hosting files on webserver using Docker Compose"
docker-compose up 

echo "[*] Step 2 cleanup"
# Clear environment variables
echo "[*] Clearing environment variables"
unset DOMAIN
unset AMOUNT
unset FLAG_FILE_CONTENT
unset FLAG_FILE_NUMBER

