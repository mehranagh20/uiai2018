#!/bin/zsh

# run server if it is possible to run it with args

# run myself
python3 Game.py > log/out 2>&1 &
pid1=$!
python3 enemy/Game.py 2>&1 > enemy/log/out &
pid2=$!

echo "$pid1\n$pid2" > pids

tail -f log/out

