docker-build:
	docker build -t lukaswire/charon .

docker-run: docker-build
	docker run --rm -p 8080:8080 lukaswire/charon

docker-deploy: docker-build
	docker push lukaswire/charon