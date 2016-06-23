#!/bin/bash

read paste_data

api_key=''
api_url='http://pastebin.com/api/api_post.php'

echo -e "\n"

curl -X POST --data "api_option=paste&api_dev_key=${api_key}&api_paste_private=1&api_paste_code=${paste_data}" $api_url

echo -e "\n"
