#!/bin/bash
#
# desktop reminder

function usage {
    echo "Usage: $0 <HH:MM> <Text>"
    exit 1
} >&2

if (( $# != 2 )); then
    usage
fi

if ! [[ $1 =~ ^[0-9][0-9]:[0-9][0-9]$ ]]; then
    usage
fi

if ! which gxmessage &>/dev/null; then
    echo "gxmessage is not installed" >&2
    exit 1
fi

if ! pgrep atd &>/dev/null; then
    echo "atd is not running" >&2
    exit 1
fi

echo DISPLAY=:0.0 gxmessage -center -nofocus "$2" | at $1 &>/dev/null
