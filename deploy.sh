#!/bin/bash

stop_django_server() {
  fuser -k 80/tcp
  printf "... Django stopped.\n"
}

remove_app() {
  printf "\nDeleting '%s' folder...\n" "$1"
  full_path="apps/$1/"
  rm -rf "$full_path"
  printf "... '%s' deleted.\n" "$1"
}

clone_repo() {
  printf "\nCloning '%s' app from GitHub...\n" "$1"
  cd apps/
  clone_link="https://$2:$3@github.com/$2/$1.git"
  git clone "$clone_link"
  printf "... '%s' cloned.\n" "$1"
}

start_django_server() {
  printf "\nStarting Django server...\n"
  cd jcc
  pipenv install
  pipenv run ./manage.py runserver
}

vps_username=${VPS_USERNAME}
vps_ip_address=${VPS_IP_ADDRESS}
github_repo_name=${GITHUB_REPO_NAME}
github_username=${GITHUB_USERNAME}
github_vps_token=${GITHUB_VPS_TOKEN}

ssh -t "$vps_username"@"$vps_ip_address" \
"$(typeset -f); stop_django_server && \
$(typeset -f); remove_app $github_repo_name && \
$(typeset -f); clone_repo $github_repo_name $github_username $github_vps_token && \
$(typeset -f); start_django_server"
