# cannot be executed yet. work as a document of docker

sysctl -w net.ipv4.ip_forward=1
docker run -d -v /home/rfeng:/home/rfeng dev bash
docker exec -it [CONTAINER_ID] bash

