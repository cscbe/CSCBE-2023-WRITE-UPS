# Lazy Domain Admins

## Category
Forensic

## Estimated difficulty
Medium

## Description
The participants will have to extract the group structures and password hashes from the provided Active Directory database and then crack the hashes of several users.

## Scenario
The employees of the Azure Test department discovered something and hid a message in their passwords.

## Write-up
The challenge presents an Active Directory database (ntds.dit) and the encryption key of the database (system):

![ntds.dit](./Challenge/Public/ntds.dit)
![system](./Challenge/Public/system)

- To discover the hidden message, we need to export the password hashes of all the domain users. The impacket Python project has a module that does exactly that.

`impacket-secretsdump -system ./system -ntds ./ntds.dit LOCAL -just-dc-ntlm -outputfile user_hashes`

- The result is a list of more than 2500 users, way too many to start cracking. We need to extract additional information from the AD database. To achieve this, we used the esedbexport and [ntdsextract](https://github.com/csababarta/ntdsxtract) tools and grepped the Azure Test accounts.

`esedbexport -m tables ntds.dit`

`python2 ./ntdsxtract/dsusers.py ./ntds.dit.export/datatable.4 ./ntds.dit.export/link_table.7 ./workdir --syshive ./system --csvoutfile ../users.csv`

`grep AZR\|Test ./users.csv > ./azure_users.csv`

- When we crack their password hashes using hashcat with the default wordlist rockyou.txt and rearrange the cracked passwords according to the account names alphabetically, we can read the following sentence: *lazy domain admins disabled password length*

`hashcat -m 1000 -a 0 ./azure_hashes.txt -o ./azure_passwords.txt -O /usr/share/wordlists/rockyou.txt`

- In order to find out which accounts are a Domain Admin member, we need to extract additional group information from the AD database. (Note: you will need an [additional pull request](https://github.com/csababarta/ntdsxtract/pull/23) from the Fox-IT fork to make the regular expression work)

`python2 ./ntdsxtract/dsgroups.py ./ntds.dit.export/datatable.4 ./ntds.dit.export/link_table.7 ./workdir --name .*Dom.*Adm.* --members --csvoutfile ../domain_admins.csv`

- Then, we can bruteforce the password hashes from the Domain Admins using hashcat.

`hashcat -m 1000 -a 3 ./admin_hashes.txt -o ./admin_passwords.txt -O -i --increment-min=1 --increment-max=4 ?a?a?a?a`

- Rearranging the cracked passwords will lead to the flag.

## PoC script
(see Resources folder)

## Flag
CSC{Q4MEg9wK2Wc}

## Creator
Jelle Aerts

## Creator bio
--
