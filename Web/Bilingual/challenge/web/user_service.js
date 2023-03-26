const redis = require('redis');
const uuid = require('uuid');

// Translators work quickly, no need to keep users forever.
const EXPIRY = 7200;

class UserService {
    _client;
    
    init(hosts) {
        const host = hosts['redis'];
        this._client = redis.createClient({
            url: `redis://${host.name}:${host.port}`
        });
        return this._client.connect();
    }

    async createUser(username) {
        const id =  uuid.v4().substring(0,25);
    
        await this._client.multi()
            .set('admin.' + id, 'n', { EX: EXPIRY })
            .set('username.' + id, username, { EX: EXPIRY })
            .exec();
    
        return id;
    }
    
    getUsername(id) {
        return this._client.get('username.' + id);
    }
    
    async isAdmin(id)  {
        return await this._client.get('admin.' + id) === 'y';
    }
}

module.exports = UserService;