#!/bin/bash
 
# Create Tenant and User #
keystone_ip=192.168.246.10
tenant=Tenant$1
user=User$1
usermail=user$1@awcloud.com
role=Member
extnet=$2
 
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 net-create $tenant-Net
subnet_id=`neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 subnet-create $tenant-Net 10.25.0.0/24 | awk '$2~/^id/{print $4}'`
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 router-create $tenant-R1
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 router-interface-add $tenant-R1 ${subnet_id}
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 router-gateway-set $tenant-R1 $extnet
