docker rm -f `docker ps -a | grep anti-plagiarism:build | awk '{print $1}'`
docker build -f Dockerfile -t anti-plagiarism:build .
docker run --restart always  -v ${PWD}/container_dir/:/anti-plagiarism/container_dir/ -p 5000:5000 --name anti_plagiarism -d anti-plagiarism:build 
