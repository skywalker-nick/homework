#!/bin/bash
 
# Create Tenant and User #
keystone_ip=192.168.246.10
tenant=Tenant$1
user=User$1
usermail=user$1@awcloud.com
role=Member
extnet=$2

vms=`nova --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 list | grep TenantA-Net | awk '{print $2}'`
for vm in $vms
do
    nova --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 delete $vm
done

neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 router-gateway-clear $tenant-R1
subnet_id=`neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 subnet-list | grep 10.25.0.0 | awk '{print $2}'`
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 router-interface-delete $tenant-R1 ${subnet_id}
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 router-delete $tenant-R1
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 subnet-delete ${subnet_id}
neutron --os-tenant-name $tenant --os-username $user --os-password password --os-auth-url=http://$keystone_ip:5000/v2.0 net-delete $tenant-Net
