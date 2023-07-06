docker build . -t web-service-message-votes
docker run --rm -it -p 5002:5002 web-service-message-votes