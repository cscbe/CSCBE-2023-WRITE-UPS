# DON'T SPY ME

## Category
Web

## Estimated difficulty
Easy

## Description
Basic web challenge with multiple steps to find the flag. Firstly edit the user agent, and then enable debug cookie. 

## Scenario
Your friend has shared with you a strange blog that appears to belong to a mysterious person. The blogger has expressed concern about his privacy. 
Can you use your best hacking skills to discover why he is so concerned ? 

## Build
docker build challenge/Private/ -t dontspyme && docker run -d -p 80:80 dontspyme

## Write-up
Firstly, you need to understand the 90s context of the blog. A hint that can guide you in the right direction is the "Last updated: 2 March 1997" note.

When you attempt to view the blog posts, you will be denied access. Here's a second hint: "I don't trust new browsers."

Therefore, you need to identify which browsers were commonly used in 1997. Netscape was the most widely used browser at that time. You need to edit your user-agent to use a Netscape user agent. I accept any user agents that contain the string "Netscape" or "Mozilla/4."

Now, you can view the blog posts, and you should use the "admin" button. Once again, access is denied to users except for admin and debugger users.

Finally, simply use a debug cookie with the value "1" and you will find the flag.


## PoC script
```
curl -H "User-Agent: Netscape" -H "Cookie: debug=1" http://127.0.0.1:80/blogposts/d223/admin
```

## Flag
CSC{Y0u_4r3_4_m4573r_5py}

## Creator
Yannis Kireche 

## Creator bio
Yannis Kireche is a cybersecurity enthusiast who is currently in his final year of a Bachelor's degree in cybersecurity. As an intern at Nviso, he is working on a firmware emulation project in the IoT team. 
(bio-picture in resource)