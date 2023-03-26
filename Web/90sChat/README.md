# [90sChat]

## Category
Web

## Estimated difficulty
Hard

## Description
You have to use an XSS to iterate through the admin panel and promote yourself to admin.
This challenge requires https to function, put it behind a reverse proxy. It does not support basic auth however, make sure that is not enabled.

## Scenario
I was trolling this chatroom and I ended up getting banned. I don't care about getting unbanned, I just want you to teach the admin a lesson. Hack his account and get admin for yourself, that should do the trick.

## Write-up
You can chat with the admin, who clicks all links. An XSS is found in the error page. Cookies are protected with the __Host- prefix. You need to use an XSS in order to fetch() the /admin page (there is a link under the chat with display:none) and then send the return page to a request bin (out of band). This way you can see the content of the admin panel the admin can see. You have to iterate through this until you made yourself an admin. At that point, the flag will appear upon a page refresh.

## PoC script
See writeup in resources folder. PoC depends on your username.

## Flag
CSC{TH3_G04T_T00K_R3V3NG3_666}

## Creator
Bram Van Gaal

## Creator bio
I'm a new employee working at NVISO. I started programming as a kid and was able to make a popular game on ROBLOX. Then I started watching LiveOverflow and playing CTFs and really enjoyed the technical challenge. I ended up applying for a job as a penetration tester and now I review source code and try and hack into applications in order to secure them. If you enjoy technical puzzles like these then you'd be an amazing asset to the cybersecurity community :)

- [https://be.linkedin.com/in/bram-v-6b1049247](https://be.linkedin.com/in/bram-v-6b1049247)
