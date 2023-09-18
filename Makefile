build:
	docker build -t revolut-test -f builds/Dockerfile . && \
	docker tag revolut-test vfondevilla/revolut-test:latest
	docker push vfondevilla/revolut-test:latest


deploy-base:
	kustomize build builds/k8s/bases | kubectl apply -f -

deploy-cloud:
	kustomize build builds/k8s/overlays/cloud | kubectl apply -f -