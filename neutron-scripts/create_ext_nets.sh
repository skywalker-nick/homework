neutron net-create Ext-Net-1 --provider:network_type flat --provider:physical_network physnet1 --router:external true --shared

neutron subnet-create  --allocation-pool start=10.100.100.100,end=10.100.100.200 --gateway 10.100.100.254 Ext-Net-1 10.100.100.0/24 --enable_dhcp=False
