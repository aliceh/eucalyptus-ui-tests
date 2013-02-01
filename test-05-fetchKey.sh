#!/bin/sh

source eucarc
euca-create-keypair selenium > selenium.key
chmod 600 selenium.key
