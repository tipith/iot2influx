# must first login with: docker login --username=yourhubusername --email=youremail@company.com
# optionally run with: docker run --name iot2influx --net container:influxdb -v $(pwd)/config.ini:/opt/iot/config.ini iot2influx 

my_dir="$(dirname "$0")"
source $my_dir/common.sh

tag=${docker_user}/${docker_img_name}
docker build -t ${tag}:latest $my_dir/..
docker push ${tag}

