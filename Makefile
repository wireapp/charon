docker-build:
	docker build -t charon .

docker-run:
	docker run --rm -p 8080:8080