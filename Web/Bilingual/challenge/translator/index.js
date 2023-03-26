const net = require('net');
const protobuf = require("protobufjs");

const translations = {
    'de': 'Brauchen Sie einen Hinweis? https://youtu.be/lybxN23zWUQ?t=92',
    'fr': 'Besoin d\'un indice ? https://youtu.be/lybxN23zWUQ?t=23'
}

function handleConnection(conn, protoRoot) {    
    const remoteAddress = conn.remoteAddress + ':' + conn.remotePort;  
    console.log('new client connection from %s', remoteAddress);

    conn.on('data', onConnData); 

    conn.on('close', () => {
        console.log('connection from %s closed', remoteAddress);  
        end();
    });
    conn.on('error', () => {
        console.log('Connection %s error: %s', remoteAddress, err.message);  
        end();
    });

    conn.setTimeout(5_000);
    conn.on('timeout', () => {
        console.log('socket timeout');
        end();
    });

    function end() {
        conn.end();
        conn.destroy();
    }
  
    function onConnData(d) {  
        console.log('connection data from %s: %j', remoteAddress, d);  

        const TranslationResponseRpc = protoRoot.lookupType(
            "bilingual.TranslationRpcResponse"
        );
        const message = TranslationResponseRpc.create({
            'translated': translations[process.env.LANGUAGE] ?? 'N/A'
        });
        const payload = TranslationResponseRpc.encode(message).finish();
        conn.write(payload);
        
        end();    
    }
}

async function main() {
    const protoRoot = await protobuf.load("../shared/bilingual.proto"); 
    const server = net.createServer();    
    server.on('connection', (conn) => handleConnection(conn, protoRoot));

    server.listen(process.env.PORT ?? 9000, function() {    
        console.log('server listening to %j', server.address());  
    });
}

main();