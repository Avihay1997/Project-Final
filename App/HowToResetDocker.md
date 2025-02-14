	- docker stop $(docker ps -aq)

	- docker rm $(docker ps -aq)

	- docker rmi $(docker images -q)

	- docker network prune

	- docker volume prune

	- docker system prune -a --volumes
