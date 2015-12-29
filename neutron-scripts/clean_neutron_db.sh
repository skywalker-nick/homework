mysql -e "drop database if exists neutron_ml2;"
mysql -e "create database neutron_ml2 character set utf8;"
mysql -e "grant all on neutron_ml2.* to 'neutron'@'%';"
mysql -e "drop database if exists ovs_neutron;"
mysql -e "create database ovs_neutron character set utf8;"
mysql -e "grant all on ovs_neutron.* to 'neutron'@'%';"

neutron-db-manage --config-file /usr/share/neutron/neutron-dist.conf --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugin.ini upgrade head
