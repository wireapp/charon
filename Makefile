docker-build:
	docker build -t lukaswire/charon .

docker-run:
	docker run --rm -p 8080:8080 lukaswire/charon

docker-deploy:
	docker push lukaswire/charon