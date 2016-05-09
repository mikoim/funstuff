#!/usr/bin/env bash

if [ $# -eq 1 ];
then
    for i in {1..10}
        do
            (time $1) 2>&1 1>/dev/null | sed -n '/^user/p' | sed -E "s/user`printf '\t'`//"
        done
fi
