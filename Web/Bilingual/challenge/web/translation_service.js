const { PromiseSocket } = require("promise-socket");
const net = require('net');
const protobuf = require("protobufjs");

class TranslationService {
    _hosts = [];
    _protoRoot;
    async init(hosts) {
        this._hosts = hosts;
        this._protoRoot = await protobuf.load("../shared/bilingual.proto");
    }

    async translate(request, language) {
        const host = this._hosts[language];
        if(!host) {
            throw Error('Host not found');
        }

        const payload = this._serializeRequest(request);
        const response = await this._sendRequest(payload, host);

        return this._deserializeResponse(response);
    }

    _serializeRequest(request) {
        const TranslationRpcRequest = this._protoRoot.lookupType(
            "bilingual.TranslationRpcRequest"
        );
        const errMsg = TranslationRpcRequest.verify(request);
        if (errMsg) {
            throw Error(errMsg);
        }

        const message = TranslationRpcRequest.create(request); 
        return TranslationRpcRequest.encode(message).finish();
    }

    async _sendRequest(payload, host) {
        const nativeSocket = new net.Socket();
        const socket = new PromiseSocket(nativeSocket);
        socket.setTimeout(5_000);
        await socket.connect(host.port, host.name);

        await socket.write(payload);
        const responseData = await socket.readAll();

        await socket.end();
        
        return responseData;
    }

    _deserializeResponse(response) {
        const TranslationRpcResponse = this._protoRoot.lookupType(
            "bilingual.TranslationRpcResponse"
        );

        return TranslationRpcResponse.decode(response).translated;
    }
}

module.exports = TranslationService