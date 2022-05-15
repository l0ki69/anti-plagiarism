#!/bin/bash

rm -f text_1.in text_1.in output.out
touch text_1.in text_1.in output.out .env

echo SHINGLE_SIZE=2 > .env

echo "Конференция состоится завтра по адресу академии" > text_1.in # test case
echo "Завтра по адресу академии состоится конференция" > text_2.in # test case

apt install libpq-dev python3-dev

python3.8 main.py "text_1.in" "text_2.in"
cat output.out
printf '\nSUCCESS\n'