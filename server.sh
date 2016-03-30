#!/bin/sh
timeout=1
port=18080
tmppipe=$(mktemp -u)
mkfifo $tmppipe
nc -l -p $port -w $timeout < $tmppipe | ./main.rb > $tmppipe
