const express = require("express")
const router = express.Router()

const adminCookie = process.env.adminCookie || "tdzruPUzQRzQUOt9kNy"

router.use((req, res, next) => {
    if(req.cookies["adminCookie"] == adminCookie) {
        next()
    } else {
        res.redirect("/error.html?msg=Access denied!")
    }
})

router.get("/userManagementPage.html", (req, res) => {
    const userList = [
        "admin",
        "bram",
        "daanimator",
        "teddyanton",
        "spikey",
        "jenne",
        "emre",
        "nathan",
        "michel",
        "ewoudje",
        "ely"
    ]

    userList.push(req.cookies["forUsername"])
    
    res.render("userManagementPage", {userList})
})

router.get("/promoteToSuper.html", (req, res, next) => {
    if(req.query.username && typeof req.query.username == "string") {
        if(req.cookies["forUsername"] == req.query.username) {
            global.identifierHasFlag[req.cookies["forIdentifier"]] = true
        }
        next()
    } else {
        res.redirect("/error.html?msg=Something went wrong.")
    }
})

module.exports = router