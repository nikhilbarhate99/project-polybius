VERSION=v12
DOCKERUSER=nikhilbarhate99

build:
	cp ../global_variables.py ./
	
	docker build -f Dockerfile-llm -t project-polybius-llm .

	# docker buildx build --platform linux/amd64 -f ./Dockerfile-llm -t project-polybius-llm .

	rm global_variables.py

push:
	docker tag project-polybius-llm $(DOCKERUSER)/project-polybius-llm:$(VERSION)
	docker push $(DOCKERUSER)/project-polybius-llm:$(VERSION)
