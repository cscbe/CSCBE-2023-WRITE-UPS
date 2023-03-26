# Puzzle - “smallbank treasure hunt”

## Start puzzle

`docker-compose down && docker-compose build --no-cache && docker-compose up -d; docker-compose logs -f`

This will start an authoritative DNS server for domain: smallbank.be\
`$ dig @127.0.0.1 smallbank.be soa +short`\
`ns1.smallbank.be. what.about.txt. 17 3600 1800 2419200 600`

## Verify puzzle is ready and setup

`$ dig @localhost otherchest6298454568435186684231685423.smallbank.be -t any +short`\
`"{CSC}ANYwhereANYtimeANYplace"`

## Introduction

Greetings, fellow hackers! A mystery awaits to be solved by the elite members of the Cyber League. The challenge takes place at Smallbank, known as "smallbank.be". A mysterious force has hidden something within the bank's system, and the clues are the domain name "smallbank.be" and the IP address (<IP address>) of the hosting zone. The goal is to solve the mystery by gathering any information and using your problem-solving skills. Are you ready to take on this challenge? Let's start our journey to find the hidden treasure!

## Solution (including hints)

1. Let's query `dig @localhost www.smallbank.be -t A` shows ip ( but will not lead to anything further )\
`​$ dig @localhost www.smallbank.be -t A +short`\
`172.217.168.227`

2.  Let's query `dig @localhost smallbank.be -t  any`\
`$ dig @localhost smallbank.be -t any +short`\
`ns1.smallbank.be. what.about.txt. 17 3600 1800 2419200 600`

SOA record shows a hint  : what.about.txt.

3. Let's query TXT record smallbank.be -t txt  
Result: nothing

4. Let's query TXT record www.smallbank.be -t txt  
Result: nothing
  
5. Let's query TXT other records <anylabel>.smallbank.be -t txt  
`$ dig @localhost blah.smallbank.be -t txt +short`\
`"Wrong, the name is hhiddenn. Try a little bit harder, maybe rfc1035 contains some info"`

6. That was another hint  
Lets query `dig @localhost hhiddenn.smallbank.be -t any`  
This shows `"hhiddenn.smallbank.be.	86400	IN	AFSDB	1 nottheflag." `  
Note: this is a dead end, nothing to be done with this\
Also note that the ANY query does not return all record types in this case, this is to mislead the one trying to solve the puzzle. But this is valid by RFC nonetheless. 

7. Try further with other DNS records : `dig @localhost hhiddenn.smallbank.be -t txt `
shows a lot of random data ; which is another dead end\

**HINT1**: the random data is a dead end/smokescreen, nothing needs to be done with this

8. Let's look at that rfc1035 further, they talk about hinfo record (among others), lets query that one
`$ dig @localhost hhiddenn.smallbank.be -t hinfo +short`\
`"I think you need to look in the " "otherchest6298454568435186684231685423"`

**HINT2**: the record type you are looking for is hinfo

9. Let's query `dig @localhost otherchest6298454568435186684231685423.smallbank.be -t any` 
`$ dig @localhost otherchest6298454568435186684231685423.smallbank.be -t any +short`\
`"{CSC}ANYwhereANYtimeANYplace"`

YOU HAVE FOUND THE FLAG: \
{CSC}ANYwhereANYtimeANYplace

## Intended weird ANY behaviour in puzzle explanation
The weird behaviour when DNS querying for an ANY record is intended in this puzzle.\
This DNS server (running NSD) is not answering with all records (as would be expected), but answers with only 1 RRset (RFC8482)










