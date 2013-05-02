#!/bin/bash
if [ $# -eq 0 ]; then
    echo usage:
    echo     mytest K file 0.05
    echo     mytest B file
    exit
fi
if [ "$1" = "K" -o "$1" = "k" ]; then
    LIB=knn
    if [ $# -lt 3 ]; then
        IGratio=None
    else
        IGratio=$3
    fi
    echo python -c "import $LIB;$LIB.evaluate('$2',$IGratio)"
    python -c "import $LIB;$LIB.evaluate('$2',$IGratio)"
else
    LIB=bayesian
    echo python -c \""import $LIB;$LIB.evaluate('$2')"\"
    python -c "import $LIB;$LIB.evaluate('$2')"
fi
