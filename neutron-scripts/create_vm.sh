#!/bin/bash
 
# Create Tenant and User #
keystone_ip=192.168.247.6
tenant=Tenant$1
user=User$1
usermail=user$1@awcloud.com
role=Member
extnet=$2

image_id=`glance index | grep Cirr | awk '{print $1}'`

nova --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 keypair-add key01 --pub-key ~/.ssh/id_rsa.pub

for (( i=0; i<1; i++));
do

netid=`neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 net-list | grep $tenant-Net | awk '{print $2}'`

nova --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 boot --flavor 2 --nic net-id=$netid  --image ${image_id} --key-name key01 vm00$i
sleep 10

fixip=`nova --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 list | grep vm00$i | grep RUNNING | awk '{print $6}'`
portid=`neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 port-list | grep $fixip | awk '{print $2}'`
floatingip=`neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 floatingip-create $extnet  grep -v float | grep -v port | grep -v router | grep -v tenant | grep id | awk '{print $4}'`
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 floatingip-associate $floatingip $portid

done;
