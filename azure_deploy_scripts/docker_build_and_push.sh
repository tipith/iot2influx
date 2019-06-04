# must first login with docker login --username=yourhubusername --email=youremail@company.com
my_dir="$(dirname "$0")"

source $my_dir/common.sh

tag=${docker_user}/${docker_img_name}
docker build -t ${tag}:latest $my_dir/..
docker push ${tag}

# optionally run with