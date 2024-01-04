VERSION=v12
DOCKERUSER=YOUR_DOCKER_USER_NAME

build:
	cp ../global_variables.py ./

	docker build -f Dockerfile-rest -t project-polybius-rest .

	# docker buildx build --platform linux/amd64 -f ./Dockerfile-rest -t project-polybius-rest .

	rm global_variables.py

push:
	docker tag project-polybius-rest $(DOCKERUSER)/project-polybius-rest:$(VERSION)
	docker push $(DOCKERUSER)/project-polybius-rest:$(VERSION)
