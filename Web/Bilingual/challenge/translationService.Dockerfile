FROM node:19.3.0

EXPOSE 9000/tcp
COPY shared /app/shared
COPY translator /app/translator

WORKDIR "/app/translator"
RUN ["npm", "install"]

CMD ["node", "index"]
