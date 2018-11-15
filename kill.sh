#!/bin/zsh

for i in $(cat pids); do
	kill $i
done
