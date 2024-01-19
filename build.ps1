
docker build -t binance-trader .

docker run --env-file .env --name binance-trader-container binance-trader