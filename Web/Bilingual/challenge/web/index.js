const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const helmet = require('helmet');
const UserService = require('./user_service');
const TranslationService = require('./translation_service');
const routes = require('./routes');

const port = 3000;

async function main() {
    const app = express();

    app.use(helmet());

    app.use(bodyParser.json())
    app.use(bodyParser.urlencoded({ extended: true }));
    app.set('view engine', 'pug');
    app.use(express.static(__dirname + '/public'));
    
    // Secure cookie values get a 's:' prefix and have a signature appended.
    app.use(cookieParser(process.env.COOKIE_SECRET));

    const hosts = process.env.HOSTS
        .split(',')
        .map((host) => host.split('='))
        .reduce(
            (map, host) => {
                const hostData = host[1].split(':')
                map[host[0]] = { 'name': hostData[0], 'port': hostData[1] };
                return map;
            }, 
            {}
        );
    console.log('Hosts');
    console.log(hosts);

    const userService = new UserService();
    const translationService = new TranslationService();
  
    await Promise.all([
        translationService.init(hosts),
        userService.init(hosts)
    ]);

    routes(
        app, 
        {
            users: userService,
            translations: translationService
        }
    );

    app.listen(port, () => {
        console.log(`App running on port ${port}.`);
    });
};

main();

