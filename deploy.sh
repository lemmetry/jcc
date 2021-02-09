#!/bin/bash

PATH_TO_PRODUCTION_APPS="/root/apps"
PATH_TO_FEATURE_PREVIEW="/root/feature_preview/$1"

ssh -t "$VPS_USERNAME"@"$VPS_IP_ADDRESS" << EOF
  export JCC_SECRET_KEY="$JCC_SECRET_KEY"
  export JCC_EMAIL_HOST=$JCC_EMAIL_HOST
  export JCC_EMAIL_HOST_USER=$JCC_EMAIL_HOST_USER
  export JCC_SENDGRID_API_KEY=$JCC_SENDGRID_API_KEY
  export JCC_EMAIL_PORT=$JCC_EMAIL_JCC_EMAIL_PORT
  export JCC_EMAIL_USE_TLS=$JCC_EMAIL_USE_TLS
  export JCC_EMAIL_FROM=$JCC_EMAIL_FROM
  export JCC_EMAIL_TO=$JCC_EMAIL_TO

  if [[ "$1" == "production" ]]; then
    printf  "Deploying production...\n"
    fuser -k 80/tcp
    printf "... Django stopped.\n"

    printf "\nDeleting $GITHUB_REPO_NAME folder...\n"
    rm -rf $PATH_TO_PRODUCTION_APPS/$GITHUB_REPO_NAME
    printf "... $GITHUB_REPO_NAME deleted.\n"

    printf "\nCloning $GITHUB_REPO_NAME app from GitHub..."
    cd $PATH_TO_PRODUCTION_APPS
    git clone "https://$GITHUB_USERNAME:$GITHUB_VPS_TOKEN@github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME.git"
    printf "... $GITHUB_REPO_NAME cloned.\n"

    printf "\nStarting Django...\n"
    cd $PATH_TO_PRODUCTION_APPS/$GITHUB_REPO_NAME
    pipenv install
    pipenv run ./manage.py runserver --settings=jcc.settings.production routinemod.com:80

  elif [[ "$1" == "issue"* ]]; then
    declare -x PATH_TO_FEATURE_PREVIEW="/root/feature_preview/$1"
    printf "Deploying $1 preview...\n"
    printf "\nCloning $GITHUB_REPO_NAME app from GitHub..."
    mkdir $PATH_TO_FEATURE_PREVIEW
    cd $PATH_TO_FEATURE_PREVIEW
    git clone -b $1 --depth 1 "https://$GITHUB_USERNAME:$GITHUB_VPS_TOKEN@github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME.git"
    printf "\n... $GITHUB_REPO_NAME cloned.\n"

    printf "\nStarting Django...\n"
    cd $PATH_TO_FEATURE_PREVIEW/$GITHUB_REPO_NAME
    pipenv install
    pipenv run ./manage.py runserver --settings=jcc.settings.production routinemod.com:81
    
  else
    printf "something wrong\n"
    exit 1
  fi
EOF