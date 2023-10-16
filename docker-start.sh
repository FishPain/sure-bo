#!/bin/bash
docker build -t surebo:0.0.1 .
echo "Docker image is built"
sleep 3
docker run -p 8080:5001 surebo:0.0.1
