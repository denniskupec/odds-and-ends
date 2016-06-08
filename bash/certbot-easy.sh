#!/bin/bash

# 'easy' certificates from certbot
# symlink?
#   keep the public out of private directories and you're fine
#   dont take my word for it

email=''
domains=''
rsa_key_size=4096

work_dir=$(pwd)/certbot
logs_dir=$work_dir/logs
useragent="$(lsb_release -sd), $(uname -mrs)"

# kill nginx since it blocks ports 80,443
pgrep "nginx" > /dev/null && service nginx stop

[ ! -d "$work_dir" ] && ln -s /etc/letsencrypt $(pwd)/certbot

certbot certonly -v -t -n --agree-tos --standalone \
  --email $email \
  --domains $domains \
  --rsa-key-size $rsa_key_size \
  --work-dir $work_dir \
  --logs-dir $logs_dir \
  --user-agent '$useragent' \
  --standalone-supported-challenges tls-sni-01

service nginx restart
