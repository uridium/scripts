#!/bin/bash
#
# zamiana duzej ilosci sekund na dni, godziny, minuty, sekundy

if [ $# -ne 1 ]; then
    echo "Usage: $0 <Number of seconds>" >&2
    exit 1
else
    seconds=$1
    days=$((seconds / 86400))
    seconds=$((seconds % 86400))
    hours=$((seconds / 3600))
    seconds=$((seconds % 3600))
    minutes=$((seconds / 60))
    seconds=$((seconds % 60))
    echo "$days day(s) $hours hour(s) $minutes minute(s) $seconds second(s)"
fi
