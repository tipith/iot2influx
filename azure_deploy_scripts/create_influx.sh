set -e
set -x

my_dir="$(dirname "$0")"
source $my_dir/common.sh

az group create --name $rgroup --location $loc

az storage account create --resource-group $rgroup --name $storage --location $loc --sku Standard_LRS
az storage share create --name $influx_share --account-name $storage
az storage share create --name $chrono_share --account-name $storage
az storage share create --name $common_share --account-name $storage

STORAGE_KEY=$(az storage account keys list --resource-group $rgroup --account-name $storage --query "[0].value" --output tsv)
echo "$storage.$share.key: $STORAGE_KEY"

cp influx_containers.yaml.tmpl influx_containers.yaml

sed -i -e "s/<<influx_share>>/$influx_share/g" influx_containers.yaml
sed -i -e "s/<<chrono_share>>/$chrono_share/g" influx_containers.yaml
sed -i -e "s/<<common_share>>/$common_share/g" influx_containers.yaml
sed -i -e "s/<<storage_account>>/$storage/g" influx_containers.yaml
sed -i -e "s/<<storage_key>>/$STORAGE_KEY/g" influx_containers.yaml
sed -i -e "s/<<container_group>>/$cgroup/g" influx_containers.yaml

az storage file upload --share-name $common_share --account-name $storage --source ../config.ini

az container create --resource-group $rgroup --file influx_containers.yaml
