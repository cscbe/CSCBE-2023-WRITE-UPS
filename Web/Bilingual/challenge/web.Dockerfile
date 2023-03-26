FROM node:19.3.0

EXPOSE 3000/tcp
COPY shared /app/shared
COPY web /app/translator

WORKDIR "/app/translator"
RUN ["npm", "install"]

CMD ["node", "index"]
