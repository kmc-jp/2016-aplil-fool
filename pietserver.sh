#!/bin/sh
port=18080
tmppipe=$(mktemp -u)
mkfifo $tmppipe
#nc -l -p $port < $tmppipe | ./main.rb > $tmppipe
nc -l -p $port < $tmppipe | ultrapiet htmlserver.png > $tmppipe
