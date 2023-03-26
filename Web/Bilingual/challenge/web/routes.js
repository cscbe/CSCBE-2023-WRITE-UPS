const asyncHandler = require('express-async-handler');

function routes(app, services) {
    const languages = process.env.LANGUAGES
        .split(',')
        .map((language) => language.split('='))
        .map((language) => ({ 'label': language[0], 'host': language[1]}));
    console.log('Languages');
    console.log(languages);

    const userService = services.users;
    const translationService = services.translations;

    app.get('/', (_req, resp) => resp.render("home"));

    app.post('/', asyncHandler(async (req, resp) => {
        const id = await userService.createUser(req.body.username);

        return resp
            .cookie('userId', id, { signed: true })
            .redirect('/translate');
    }));

    app.get('/translate', asyncHandler(async (req, resp) => {
        const username = await userService.getUsername(
            req.signedCookies.userId
        );
        if (username === null) {
            return resp.redirect('/');
        }

        return resp.render('translate', { username, languages });
    }));

    app.post('/translate', asyncHandler(async (req, resp) => {
        const username = await userService.getUsername(
            req.signedCookies.userId
        );
        if (username === null) {
            return resp.redirect('/');
        }

        const translation = await translationService.translate(
            req.body.translationRequest, 
            req.body.language
        );

        return resp.render('translation', { username, translation });
    }));

    app.get('/flag', asyncHandler(async (req, resp) => {
        const isAdmin = await userService.isAdmin(req.signedCookies.userId);

        if (isAdmin) {
            return resp.render('flag', { flag: process.env.FLAG });
        } else {
            return resp.redirect('/');
        }
    }));
}

module.exports = routes;