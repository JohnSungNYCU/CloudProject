#!/bin/bash
set -e

until nc -z $1 8000; do
    echo "$(date) - waiting for $1:8000..."
    sleep 1
done