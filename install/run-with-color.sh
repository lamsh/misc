#!/bin/bash
# \file run-with-color.sh
# \author ClearCode Inc.
# URL: <http://www.clear-code.com/blog/2012/10/11.html>

red=31
yellow=33
cyan=36

colored() {
  color=$1
  shift
  echo -e "\033[1;${color}m$@\033[0m"
}

run() {
  "$@"
  result=$?

  if [ $result -ne 0 ]
  then
    echo -n $(colored $red "Failed: ")
    echo -n $(colored $cyan "$@")
    echo $(colored $yellow " [$PWD]")
    exit $result
  fi

  return 0
}
