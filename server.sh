#!/bin/sh
timeout=10
port=18080
cd ultpiet/
socat -d -d -T $timeout TCP4-LISTEN:$port,fork,reuseaddr EXEC:"./ultrapiet ../htmlserver.png"
