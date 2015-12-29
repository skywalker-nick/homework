#!/bin/bash

# Create Tenant and User #
tenant=Tenant$1
user=User$1
usermail=user$1@awcloud.org
role=Member

if keystone tenant-list | grep -q $tenant;then
    echo "Tenant $tenant existed!"
else
    tenant_id=`keystone tenant-create --name $tenant | awk '/id/{print $4}'`
fi
 
if keystone user-list | grep -q $user;then
    echo "User $user existed!"
else
    keystone user-create --name=$user --pass=password --tenant-id $tenant_id --email=$usermail
fi
 
keystone user-role-add --tenant $tenant --user $user --role $role
