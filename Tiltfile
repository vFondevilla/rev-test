allow_k8s_contexts('admin@homelab')
docker_build("vfondevilla/revolut-test", ".", dockerfile='builds/Dockerfile')
k8s_yaml(kustomize('builds/k8s/bases/'))
