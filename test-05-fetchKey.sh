#!/bin/sh

source eucarc
if [ -e selenium.key ]; then
  echo "File selenium.key exists - skipping this step"
  exit 0
fi
euca-create-keypair selenium > selenium.key
chmod 600 selenium.key
