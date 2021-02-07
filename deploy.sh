#!/bin/bash

ssh -t "$VPS_USERNAME"@"$VPS_IP_ADDRESS" << EOF
export JCC_EMAIL_HOST=$JCC_EMAIL_HOST
export JCC_EMAIL_HOST_USER=$JCC_EMAIL_HOST_USER
export JCC_SENDGRID_API_KEY=$JCC_SENDGRID_API_KEY
export JCC_EMAIL_PORT=$JCC_EMAIL_JCC_EMAIL_PORT
export JCC_EMAIL_USE_TLS=$JCC_EMAIL_USE_TLS
export JCC_EMAIL_FROM=$JCC_EMAIL_FROM
export JCC_EMAIL_TO=$JCC_EMAIL_TO

fuser -k 80/tcp
printf "... Django stopped.\n"

printf "\nDeleting $GITHUB_REPO_NAME folder...\n"
rm -rf "apps/jcc/"
printf "... $GITHUB_REPO_NAME deleted.\n"

printf "\nCloning $GITHUB_REPO_NAME app from GitHub..."
cd apps/
git clone "https://$GITHUB_USERNAME:$GITHUB_VPS_TOKEN@github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME.git"
printf "... 'jcc' cloned.\n"

printf "\nStarting Django...\n"
cd jcc/
pipenv install
pipenv run ./manage.py runserver routinemod.com:80
EOF