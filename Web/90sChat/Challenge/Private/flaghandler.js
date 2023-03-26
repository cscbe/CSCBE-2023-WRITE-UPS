const express = require("express")
const router = express.Router()

router.get("/flag", (req, res, next) => {
    const identifier = req.cookies["identifier"]
    if(identifier && global.identifierHasFlag[identifier]) {
        const flag = process.env.flag || "CSCBE{TEST_FLAG_90SCHAT}"
        res.render("flag", {flag})
        delete global.identifierHasFlag[identifier]
    } else {
        res.redirect("/error.html?msg=You have not yet solved the challenge.")
    }
})

router.get("*", (req, res, next) => {
    const identifier = req.cookies["identifier"]
    if(identifier && global.identifierHasFlag[identifier]) {
        res.redirect("/flag")
    } else {
        next()
    }
})

module.exports = router