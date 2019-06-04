set -x
set -e

my_dir="$(dirname "$0")"
source $my_dir/common.sh

#shares=$(az storage share list --account-name iotstorage11 --query '[].name' --output tsv)
#while read -r share; do
#    az storage share delete --account-name $rgroup --name $share --yes
#done <<< "$shares"

az container delete --resource-group $rgroup --name $cgroup --yes
