#!/bin/bash

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
    BRANCH="master"
    PATH_TO="/$VPS_USERNAME/apps"
    PORT="80"

    printf  "Deploying \$BRANCH ...\n"

  elif [[ "$1" == "issue"* ]]; then
    BRANCH="$1"
    PATH_TO="/$VPS_USERNAME/feature_preview/\$BRANCH"
    PORT="81"

    printf "Deploying \$BRANCH preview...\n"

  else
    printf "something wrong\n"
    exit 1
  fi

printf "\nCloning $GITHUB_REPO_NAME app from GitHub..."
mkdir \$PATH_TO
cd \$PATH_TO
git clone -b \$BRANCH --depth 1 "https://$GITHUB_USERNAME:$GITHUB_VPS_TOKEN@github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME.git"
printf "... $GITHUB_REPO_NAME cloned.\n"

printf "\nStarting Django...\n"
cd \$PATH_TO/$GITHUB_REPO_NAME
pipenv install
pipenv run ./manage.py runserver --settings=jcc.settings.production routinemod.com:\$PORT

EOF
