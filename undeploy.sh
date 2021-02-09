#!/bin/bash

ssh -t "$VPS_USERNAME"@"$VPS_IP_ADDRESS" << EOF
  if [[ "$1" == "production" ]]; then
    PATH_TO="/$VPS_USERNAME/apps/$GITHUB_REPO_NAME"
    PORT="80"

  elif [[ "$1" == "issue"* ]]; then
    BRANCH="$1"
    PATH_TO="/$VPS_USERNAME/feature_preview/\$BRANCH"
    PORT="81"

  else
    printf "something wrong\n"
    exit 1
  fi

fuser -k \$PORT/tcp
printf "\n... Django stopped."

rm -rf \$PATH_TO
printf "\n... $GITHUB_REPO_NAME \$BRANCH deleted.\n"

EOF
