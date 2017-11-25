#!/bin/sh
################################################################################
## \file      test.sh
## \author    SENOO, Ken
## \copyright CC0
## \date      first created date: 2017-01-15T17:03+09:00
################################################################################

## \brief Initialize POSIX shell environment
init(){
	set -u
	umask 0022
	export LC_ALL='C' PATH="$(command -p getconf PATH):$PATH"
}

is_main()(
	EXE_NAME='test.sh'
	[ "$EXE_NAME" = "${0##*/}" ]
)

if is_main; then
	init
	OUT_NAME='result'
	rm -f ${OUT_NAME}*.dat

	## オペランド
	POSTFIX='operand'

	(
		ARG=$(cat <<-EOT

		''
		' '
		1 2 3 4 5 6 7 8 9 10 11
		1 ' 2 2 ' 3
		1 -h -t 3 2
		-- -h -V 0
		-h -- -h -V -t 0 1
		-t 3 -- -t 0 1
		-t3 -- -t '0 1'
		--tag 3 -- -t 0 1
		--tag=3 -- -t 0 1
		-a3 -hVt3 -- -t 0 1
		3 -hVt 3 1 --any=3  -- -t 0 1
		-t -- - -- --
		--tag=-- - -- --
		--tag -- -- -- --
		-unconform-arg -- -- --

		EOT
		)

		printf '%s\n' "$ARG" | while read -r arg; do
			printf '\nID:%03d, arg:%s\n' $((i+=1)) "$arg"
			eval $1 $arg
		done
	) >> ${OUT_NAME}_$POSTFIX.dat 2>&1

	## オプションが単体で機能するか
	POSTFIX='option'
  (
		ARG=$(cat <<-'EOT'
		-h
		--help
		--hel
		-t t 1
		-tt 1
		-t '' 1
		-t ' ' 1
		-t' ' 1
		-t ' -t ' 1
		--tag --tag 1
		--ta '' 1
		--t ' --tag 1 ' 1
		--tag ' ' 1
		--tag= 1
		--ta=' --tag=--tag= '  1
		--t=' '  1
		--tag=''  1
		-ta -tt 1
		1 --tag=3 --tag 2 2
		-hVtt
		-thV
		-t--tag
		-t-t
		-a 1
		-a'' 1
		-a' ' 1
		-a-a 1
		--any 1
		--any= 1
		--any=-any 1
		-a--any -a 1
		-a 1 -a--any 2
		-ha
		-hatt
		-haa
		-20
		-n 30
		-n31
		--number 40
		--number=41
		-2 -3 -n20 --number=30 --number 5
		-h20V10t20
		-h20V10a20
		-unconform 1
		-unconform-arg u 1
		--plus=30 +20
		EOT
		)

		printf '%s\n' "$ARG" | while read -r arg; do
			printf '\nID:%03d, arg:%s\n' $((i+=1)) "$arg"
			eval $1 $arg
		done
  ) >> ${OUT_NAME}_$POSTFIX.dat 2>&1

	## エラー検知
	POSTFIX='error'
  (
		ARG=$(cat <<-'EOT'
		-z
		--hoge
		-t
		-t''
		--ta
		--tag''
		--taga
		--anya
		-n 0
		-n a
		-n -1
		--1
		--number=$((2<<30))
		-uncon
		-unconform-arg
		-u
		-un
		EOT
		)

		printf '%s\n' "$ARG" | while read -r arg; do
			printf '\nID:%03d, arg:%s\n' $((i+=1)) "$arg"
			eval $1 $arg
		done
  ) >> ${OUT_NAME}_$POSTFIX.dat 2>&1
fi

diff answer_operand.dat result_operand.dat
diff answer_option.dat  result_option.dat
sed -i -e "s/Try '.*.sh/Try 'argparse.sh/" -e 's/^[a-z]*sh/argparse.sh/' result_error.dat
diff answer_error.dat   result_error.dat
