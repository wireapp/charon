docker-build:
	docker build -t lukaswire/charon .

docker-run: docker-build
	docker run --rm -p 8080:8080 lukaswire/charon

publish: docker-build
	docker push lukaswire/charon

db:
	docker-compose up -d redis

up:
	docker-compose up

# Kubernets - staging
kube-logs:
	kubectl logs -f -l name=charon -n staging

kube-describe:
	kubectl describe pods -l name=charon -n staging

kube-del:
	kubectl delete pod -l name=charon -n staging

__sleep:
	sleep 20

kube-deploy: kube-del __sleep kube-describe kube-logs

# Kubernets - prod
kube-prod-logs:
	kubectl logs -f -l name=charon -n prod

kube-prod-describe:
	kubectl describe pods -l name=charon -n prod
