#!/bin/bash

# testing helpers
RED='\e[0;31m'
GREEN='\e[0;32m'
NOC='\e[0m'

function alerting()
{
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo -e "[${GREEN}PASS${NOC}]: Crawler finished with \
exit code $exit_code"
    else
        echo -e "[${RED}FAIL${NOC}]: Crawler crashed with exit \
code $exit_code, aborting the rest tests"
        exit $exit_code
    fi
}

# testing data
YQY=(001176107 '1P68UBH1')
ZJM=(001954575 'NOPVDLOE')
SEARCH_PATH=`pwd | xargs dirname`
TARGET=`find $SEARCH_PATH -name webcrawler`
FLAGS_FILE=`find $SEARCH_PATH -name secret_flags`

# ensure the webcrawler has been made
if [ "$TARGET" == "" ]; then
    echo -e "${RED}Please run 'make' first before running this \
script standalone or just run 'make test'${NOC}"
    exit 1
fi

# expected results
EXPT_FLAGS=( $(cat $FLAGS_FILE | sort) )
NUM_EXPT=${#EXPT_FLAGS[@]}

# kick off the sanity test for Yingquan
echo "Sanity test with username: ${YQY[0]}, password: ${YQY[1]}"
YQY_FLAGS=`$TARGET ${YQY[0]} ${YQY[1]}`
alerting
# kick off the sanity test for Zhongjie
echo "Sanity test with username: ${ZJM[0]}, password: ${ZJM[1]}"
ZJM_FLAGS=`$TARGET ${ZJM[0]} ${ZJM[1]}`
alerting
# join the collected secret_flags
ACTUAL_FLAGS=(${YQY_FLAGS[@]} ${ZJM_FLAGS[@]})
NUM_ACTUAL=${#ACTUAL_FLAGS[@]}
# sort them
ACTUAL_FLAGS=( $(
    for flag in "${ACTUAL_FLAGS[@]}"
    do
        echo "$flag"
    done | sort) )

# check the number of flags
echo ""
echo "Checking the number of secret_flags"
test $NUM_ACTUAL -eq $NUM_EXPT; ec=$?
if [ $ec -eq 0 ]; then
    echo -e "[${GREEN}PASS${NOC}]: Get the same number of \
secret_flags with the expected results: $NUM_ACTUAL"
else
    echo -e "[${RED}FAIL${NOC}]: Failed to get the same \
number of secret_flags with the expected results, \
expected: $NUM_EXPT actual: $NUM_ACTUAL, aborting the rest tests"
    exit $ec
fi

# check each secret_flags is equal to the expected
echo ""
echo "Checking the equality of each secret_flags"
for ((i=0, match=0, unmatch=0; i<$NUM_ACTUAL; i++))
do
    actual_flag=${ACTUAL_FLAGS[$i]} && expected_flag=${EXPT_FLAGS[$i]}
    test "$actual_flag" = "$expected_flag"; ec=$?
    if [ $ec -eq 0 ]; then
        echo -e "[${GREEN}PASS${NOC}]: Actual: $actual_flag == Expected: $expected_flag"
        match=`expr $match + 1`
    else
        echo -e "[${RED}FAIL${NOC}]: Actual: $actual_flag != Expected: $expected_flag"
        unmatch=`expr $unmatch + 1`
    fi
done
echo "Result: $match Match, $unmatch Unmatch."
