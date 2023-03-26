const express = require("express")
const crypto = require("crypto")
const ejs = require("ejs")
const https = require('https')
const fs = require('fs')

// config
const app = express()
app.set("view engine", "ejs")
global.identifierHasFlag = {} // This is to know which identifier has gotten the flag.

// middleware
app.use(require("cookie-parser")())
app.use(require("body-parser").urlencoded({extended: false}))
app.use(require("body-parser").text())
app.use(require("./flaghandler.js"))

// routes
app.use("/admin", require("./adminhandler.js"))
app.use("/chat", require("./chathandler.js"))

app.get("/chat.html", (req, res, next) => {
    if(!req.cookies.username) {
        res.redirect("/")
    } else {
        next()
    }
})

app.use(express.static("public"))

app.post("/login", (req, res) => {
    res.cookie("identifier", crypto.randomBytes(32).toString("hex"), {secure: true, sameSite: 'strict', httpOnly: true})
    res.cookie("username", req.body.username)
    res.redirect("chat.html")
})

// 404
app.use((req, res) => {
    res.redirect("/error.html?msg=Page not found!")
})

// port
const port = process.env.port || 9123
app.listen(port, () => { console.log(`Listening on port ${port}`) })

// for debugging we can just use this to set up a https server instead of worrying about reverse proxies
if(process.env.httpsTest) {
    const httpsport = process.env.httpsport || 8443
    https.createServer({
        key: fs.readFileSync('server.key'),
        cert: fs.readFileSync('server.cert')
    }, app).listen(httpsport, () => {
        console.log(`\{https\} Listening on port ${httpsport}`)
    })
}