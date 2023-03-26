

# [Running in the metaverse]

## Category
[Stego]

## Estimated difficulty
[Easy|Medium]

## Description
[This stego challenge involves multiple steps to get to the flag. First the participants have to convert the .ape to wav, then they will have to use a program such as deepsound to extract the files hidden in the wav file.
4 files are included of wich 3 are red harings. Then they have to extract more data from the wav file included (keep_the_change.wav), this one can also be misleading as it also makes an immage by analising the sound.
If they extracted the output file (by using for example : stegolsb wavsteg -r -i Keep_The_Change.wav -o Two\ tires\ fly.\ Two\ Wail.\ A\ bamboo\ grove,\ all\ chopped\ down\ From\ it,\ warring\ songs..txt -n 1 -b 27000).
they will find a txt file. This file is encrypted in ook! code (reference to to the orang-utan Librarian in the novels of Terry Pratchett aka discworld). Now they will get a string encrypted in leet speak. If they convert this string
they will obtain the message (quote from snowcrash)
In short: .ape => convert to wav => wav => deepsound or other => wav => wavesteg => txt => ook! decode => string => leet speek decode => flag]

## Scenario
[Uncle Enzo has given you a new task which is even better than delivering pizza. A figment of the babel virus has been hidden in a file which he intercepted from a convertation between Hiro and Da5id. Can you find the hidden code which could lead to the creation of snowcrash ?

Encode the flag in the following format: CSC{flag}

(Hint: The final flag is a quote from a book)
]

## Write-up
[First convert the ape file to wav by using any converter, then use deepsound to extract the 4 files included in the wav file. Extract the hidden files in keep_the_change.wav by running the following command:
stegolsb wavsteg -r -i Keep_The_Change.wav -o Two\ tires\ fly.\ Two\ Wail.\ A\ bamboo\ grove,\ all\ chopped\ down\ From\ it,\ warring\ songs..txt -n 1 -b 27000

The extracted txt file will be full of ook! code, convert the ook! code to text by using the following website (https://www.cachesleuth.com/bfook.html).
This will give you a string in leet speak. Covert the leet speek to text by using the following converter and using the complex option(https://www.dcode.fr/leet-speak-1337)
This will give you a quote which is the flag. Enter the flag in the CSC{} format.

Congrats you solved this challenge
]


## Flag
[CSC{Well all information looks like noise until you break the code}]

## Creator
[Sander Van Dessel]

## Creator bio
[Hi, I am Sander Van Dessel and I am a security consultant at NVISO. I love to do CTFS and play D&D (No I don't dress up as a dwarf and throw bean bags at people while shouting fireball).
Former member of team team name which won Brucon student CTF2019, Hack the Future security CTF 2019 and got 44th place(out of 2247 teams) at reply CTF 2021 ]

[- https://www.linkedin.com/in/sander-van-dessel-622aba144/]

