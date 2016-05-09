#!/usr/bin/env bash

if [ $# -eq 1 ];
then
    filename=`echo $1 | sed -E 's/\..+//'`

    for i in {0..3}
        do
            clang-3.5 -O${i} -S -std=gnu11 $1
            mv ${filename}.s ${filename}_clang35_O${i}.s

            gcc-4.9 -O${i} -S $1
            mv ${filename}.s ${filename}_gcc49_O${i}.s
        done
fi
