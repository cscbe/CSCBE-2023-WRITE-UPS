## Leaky DNS server

### starting point
ip of a DNS server running the .be zone, see Dockerfile
run it as `docker run --rm -ti -p 53:53/udp -p 53:53/tcp <image name>`

### Instruction text for candidate
```
There once was a .be DNS server so chatty,
That it made all the hackers so happy,
It leaked out data,
Like it was no big matter,
And made security pros so sappy.

The server just couldn't keep its mouth shut,
And leaked data like it was in a rut,
Hackers laughed with delight,
And caused quite a fright,
As they ran off with the data they'd cut.

But security pros were not amused,
And the DNS server was quickly defused,
It was patched up and fixed,
And no longer nixed,
And security was no longer confused.

So if you're a DNS server out there,
And you like to chat without a care,
Just remember the lesson we learned,
And keep the data inside, where it's not returned,
And security pros will not be so scared.
```

## Tips
### included tips
* when querying for the ANY or TXT record of <anything>.be it shows that they need multiple flags `It's not like this is Fort Knox, there are 4 flags hidden in the data which need to be concatenated together to form the final flag`

### additional tips
* open Zone Transfer information disclosure
* BIND version directive remote version detection
* DNS server hostname.bind disclosure
* RFC 5001

## Winning CTF flag
concatenation of the 4 flags
`CSC{PART1:ANIS}`
`CSC{PART2:JCDB}`
`CSC{PART3:GLXH}`
`CSC{PART4:BFXZ}`

-> `CSC{ANISJCDBGLXHBFXZ}`

## Shortest path to solution
* `dig @<ip> be AXFR`
* 
* `dig @<ip> CH TXT version.bind`
* 
* `dig @<ip> CH TXT hostname.bind`
* 
* `dig @<ip> +nsid` (can be combined as option on former 2 queries as well)
