const express = require("express")
const puppeteer = require("puppeteer")
const router = express.Router()

const adminCookie = process.env.adminCookie || "tdzruPUzQRzQUOt9kNy"

router.post("/sendmessage", async (req, res) => {
    const msg = req.body.toLowerCase()
    const findInMsg = txt => { return msg.indexOf(txt) != -1 }
    
    const linkRegex = /(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.?[^\s]{0,}|www\.?[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{0,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.?[^\s]{0,}|www\.[a-zA-Z0-9]+\.?[^\s]{0,})/g
    const linksFound = [...req.body.matchAll(linkRegex)] // Has to be req.body, otherwise it puts everything in lowercase.

    if(linksFound.length == 1) {
        const url = linksFound[0][0]
        let browser
        if(process.env.httpsTest) {
            browser = await puppeteer.launch({args: ["--ignore-certificate-errors", "--incognito"]})
        } else {
            browser = await puppeteer.launch({args: ["--incognito", "--no-sandbox"]}) // no sandbox when running in docker
        }
        
        const page = await browser.newPage()
        await page.setCookie(
            {"name":"forUsername", domain: req.hostname, value: req.cookies.username, secure: true, sameSite: 'strict', httpOnly: true},
            {"name":"forIdentifier", domain: req.hostname, value: req.cookies["identifier"], secure: true, sameSite: 'strict', httpOnly: true},
            {"name":"adminCookie", domain: req.hostname, value: adminCookie, secure: true, sameSite: 'strict', httpOnly: true},
        )
        try {
            await page.goto(url)
            res.send("I took a look at that website, it's quite cool 🥰")
            await page.waitForTimeout(2000)
            await browser.close()
        } catch(e) {
            console.error(e)
            res.send("I couldn't visit that page, is that URL correct? 💀")
        }
    } else if(linksFound.length > 1) {
        res.send("Pfft, those are a lot more URLs than I can handle, please only send one 😰")
    } else {
        res.send("Hey there! Feel free to send me an URL, I love clicking on those 😀")
    }
})

module.exports = router