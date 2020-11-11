#!/bin/sh
# works for postgresql 11
FEDORA_VERSION=33-x86_64
# add repository
sudo dnf install "https://download.postgresql.org/pub/repos/yum/reporpms/F-${FEDORA_VERSION}/pgdg-fedora-repo-latest.noarch.rpm"
# install postgresql database
sudo dnf install postgresql11-server postgresql11
# initialize the database
sudo /usr/pgsql-11/bin/postgresql-11-setup initdb
# enable automatic start
sudo systemctl start postgresql-11
sudo systemctl enable postgresql-11
# installing developers' tools
sudo dnf install postgresql postgresql11-devel python-devel
# adding pg_config to path
# add to .bashrc, change user! comment out when you use it multiple times!
echo 'adding paths to .bashrc'
echo 'export PATH=$PATH:/usr/pgsql-11/bin/pg_config' >> /home/adam/.bashrc
echo 'export PATH=$PATH:/usr/pgsql-11/bin/' >> /home/adam/.bashrc