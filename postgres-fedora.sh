#!/bin/sh
# works for postgresql 11
# run exactly one time!!!
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
# solves a problem with authentication: needs to set app_user to can be connected by username and password
# change hba_file!!!
# in psql run -> SHOW hba_file;
# you will see: /var/lib/pgsql/11/data/pg_hba.conf or something else :)
# > change line
# host    all             all             ::1/128                 ident
# > to
# host    all             all             ::1/128                 md5