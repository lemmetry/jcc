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

deploy() {
  printf "\nCloning %s app from GitHub..." "$GITHUB_REPO_NAME"
  mkdir \$1
  cd \$1 || exit 1
  git clone -b \$2 --depth 1 "https://$GITHUB_USERNAME:$GITHUB_VPS_TOKEN@github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME.git"
  printf "... %s cloned.\n" "$GITHUB_REPO_NAME"

  printf "\nStarting Django...\n"
  cd \$1/"$GITHUB_REPO_NAME" || exit 1
  pipenv install
  pipenv run ./manage.py collectstatic --settings=jcc.settings.production
  pipenv run ./manage.py runserver --settings=jcc.settings.production routinemod.com:\$3
}

undeploy() {
  fuser -k \$1/tcp
  printf "\n... Django stopped."

  rm -rf \$2
  printf "\n... %s \$3 deleted.\n" "$GITHUB_REPO_NAME"
}

if [[ "$2" == "issue"* ]]; then
  BRANCH="$2"
  PATH_TO="/$VPS_USERNAME/feature_preview/\$BRANCH"
  PORT="81"

elif [[ "$2" == "production" ]]; then
  BRANCH="master"
  PATH_TO="/$VPS_USERNAME/apps"
  PORT="80"

else
  printf "What branch are we working with?\n"
  exit 1
fi

if [[ "$1" == "deploy" ]]; then
  deploy \$PATH_TO \$BRANCH \$PORT

elif [[ "$1" == "undeploy" ]]; then
  undeploy \$PORT \$PATH_TO \$BRANCH

else
  printf "deploy or undeploy?\n"
  exit 1
fi

EOF
