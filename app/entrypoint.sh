#!/bin/bash

set -e

if [ "$1" = 'run' ]; then
    uvicorn app:app --host 0.0.0.0 --port 9000 --reload
    fi
#if [ "$1" = 'prod' ]; then
# nginx config
# fi



