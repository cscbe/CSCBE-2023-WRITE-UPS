## Hidden in plain sight

### starting point
a PCAP file with suspicious DNS traffic

### Instruction text for candidate
```
There once was a burglar quite sly,
Who knew how to hack and get by,
He stole data galore,
But left DNS ajar,
And that's how he got caught, oh my!

The investigators were on his tail,
Tracking his steps without fail,
They found the DNS leak,
And their case was complete,
The burglar's plan was doomed to fail.

So remember, you burglars out there,
With your schemes and your tech so rare,
If you don't cover your tracks,
And you leave DNS with cracks,
You'll end up in cuffs, with none to spare!
```

## Tips
### tips included in the data
* the very first dns query response (0000.servfail.be TXT) is dnssec valid and has a base64 payload which decodes to `this is not what you're looking for, this is authentic, but base64 decoding is already a good starter`
* 0001.servfail.be TXT response has an invalid dnssec signature, with a payload where you can see it's the (start of a) jpeg `echo -n "/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAAgAAgESAAMAAAABAAEAAIdpAAQAAAABAAAAJgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAB9KADAAQAAAABAAAB9AAAAAD/7" | base64 -d | file -` -> `JPEG image data, JFIF standard 1.01, aspect ratio...`
* 0002.servfail.be TXT response is also dnssec valid and has a payload which decodes as `I hope you get the picture`
* 0042.servfail.be TXT response is also dnssec valid has a payload which decodes a `DNS: The answer to life the universe and everything, but perhaps RFC2535 chapter 6.1 also contains good answers` -> hinting to the use and meaning of the AD bit, to indicate when the dnssec signature is not valid (in this case because of data tampering)

### additional tips
* DNSSEC proofs the integrity of a DNS payload; by tampering with the DNS data you fail the integrity check, see RFC 2535 how this gets reflected in DNS queries
* an image got cut in to pieces and hidden in between normal DNS resource records to avoid getting detected

## Winning CTF flag
`CSC{6SQ8LCT06LHT1A9H1C}`

## Shortest path to solution
`tshark -r hidden-in-plain-sight.pcapng -Y "dns.flags.authenticated == 0" -T fields -e dns.txt | base64 -d > test.jpeg`
