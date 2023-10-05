# bin/bash
docker build -t surebo:0.0.1 .
docker run -p 8080:5001 surebo:0.0.1
echo "Docker container is running on port 8080"