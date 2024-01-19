
docker build -t coin-searcher .

docker run -d --name coin-searcher-container coin-searcher
docker logs -f coin-searcher-container
