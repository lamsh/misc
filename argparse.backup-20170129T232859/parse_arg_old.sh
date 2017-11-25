#!/bin/sh
# \file      parse_arg.sh
# \author    SENOO, Ken
# \copyright CC0

## \brief Initialize POSIX shell environment
init(){
	set -eu
	umask 0022
	export LC_ALL='C' PATH="$(command -p getconf PATH):$PATH"
}

EXE_NAME='parse_arg.sh'
is_main()(
	CURRENT_EXE="$(ps -p $$ -o comm=)"
	[ "$EXE_NAME" = "$CURRENT_EXE" ]
)

init



usage_exit()(
	cat <<- EOT >&2
	Usage: $EXE_NAME [options...] arg1 arg2
	options:
		-h, --help     Show this help
		-V, --version  Show version
		-a, --enable-a Switch on A
		-s
		--long-opt
		-b, --bag[=BAG] Bad tag
		    --long-arg[=olarg]
		-t, --tag=TAG  tag
		    --long-arg=larg
	Example: $EXE_NAME --tag=hoge
	EOT
	exit 1
)

parse_arg()(
	TRY_HELP="Try '$EXE_NAME --help' for more information."

	argc=0
	args=''
	opt_tags=""
	opt_bags=""
	opt_n=''

	# while [ $# != 0 ]; do
	while true; do
		while getopts ":-:0123456789abhn:t:sV" opt "$@"; do
			: ${OPTARG:=}
			echo "# $#, 1: $1, 2: ${2:-}, opt: $opt, OPTARG: $OPTARG, OPTIND: $OPTIND, $#, $@"

			case "$opt$OPTARG" in
				# h|-help) shift; echo "help $opt";;
				# V|-version) shift; echo "version $opt";;
				# a|-enable-a) shift; flag_a='OK';;
				h|-help) echo "help $opt";;
				V|-version) echo "version $opt";;
				a|-enable-a) flag_a='OK';;

				## ロングオプションがきたらOPTARGにロングオプション名が入っている
				## $optには"-"が入っている。
				## これを補足してオプションの処理をする
				## ロングオプションの場合はシフトして次の引数をオプション引数とする
				## 引数にリストが来た場合の対処
				## 任意引数ありオプションでリストが来ることはあまりないが一応

				## 任意引数オプション
				b|-bag*)
					# getoptsでは必須引数ありオプションで引数がなかったら?に飛ぶ
					# ?に飛んでしまうと，オプション引数がない場合の処理ができない
					# だから任意引数ありオプションは引数なしオプションとして扱う

					## 任意引数オプションでは空白でくぎったオプション引数は無効
					## NG: -o arg
					## OK: -oarg --long=arg, --longarg
					## $2に値が入っている場合，それはオペランドとみなす
					## オプション引数に空文字が入っていても無視
					## ロングオプションで許されるのは，--long, --long=だけ。--long3はNG
					case "$1" in -b*|--bag|--bag=*);; *)
						echo "$EXE_NAME: unrecognized option '$1'" >&2
						echo "$TRY_HELP" >&2
						exit 1
					esac

					case "$1" in
						--bag=*) opt_bags="${1#*=}";;
						# このshiftはショートグループのスキップ？
						-b*) opt_bags="${1#-*b}"; shift;;
					esac

					: ${opt_bags:=default}
					;;
				"t$OPTARG"|-tag|-tag=*)
					## =つきの場合，空文字が設定されているとみなす。
					## ロングオプションかつ，=がないかつ，$2が未定義の場合，引数の指定忘れ
					## ここは変数にまとめてevalしてもよいかも
					if [ $opt = '-' ] && [ -n "${1##*=*}" ] && [ -z "${2+defined}" ]; then
						echo "$EXE_NAME: option '$1' requires an argument" >&2
						echo "$TRY_HELP" >&2
						exit 1
					fi

					## =を含まない，かつロングオプションならオプション引数に$2を使う
					## ショートプションならOPTARG
					## ロングオションならOPTARG#*=
					# case "$1" in
					# 	--*=*) OPTARG="${1#*=}";;
					# 	--*)   OPTARG="$2"; shift;;
					# 	## -at 1の場合にかぎり，2個シフトする
					# 	-*t)   shift 2;;
					# 	# -*t)   shift;;
					# esac
					arg="$OPTARG"
					case "$1" in
						--*=*) arg="${1#*=}";;
						--*)   arg="$2"; shift 2;;
						## -at 1の場合にかぎり，2個シフトする
						## -att は2個目がない
						## こうしないと，このオプション引数がオペランドとみなされるので。
						## -att: $1=-att, opt=t, OPTARG=t
						# -*t)   shift 2;;
						# $1の末尾が$OPTARGではない
						# *[!t]t) shift 2;;
						-t)  shift 2;;
						-t*) shift;;
					esac

					opt_tags="$opt_tags $arg"
					;;

				## -NUMBER
				[0-9]|"n$OPTARG"|-number*)
					if [ $opt = '-' ] && [ -n "${1##*=*}" ] && [ -z "${2+defined}" ]; then
						echo "$EXE_NAME: option '$1' requires an argument" >&2
						echo "$TRY_HELP" >&2
						exit 1
					fi

					# echo "NUMBER: $#, 1: $1, 2: ${2:-}, opt: $opt, OPTARG: $OPTARG, OPTIND: $OPTIND, $#, $@"
					## -a10t1は有効
					# opt_n="${1%*[!0-9]}"
					# opt_n="${opt_n##*[!0-9]}"
					# OPTARG="${1#*[0-9]}"
					# opt_n="${1#*[!0-9]}"
					# opt_n="${opt_n%%[!0-9]*}"
					# OPTARG="${opt_n#?}"
					# shift

					arg="$OPTARG"
					case "$1" in
						--*=*) arg="${1#*=}";;
						--*)   arg="$2"; shift 2;;
						-[0-9]*) arg="${1#-}"; arg="${arg%%[!0-9]*}"; OPTARG="${arg#?}";;
						*[!n]n) shift 2;;
					esac

					opt_n="$arg"


					;;
				# \?*) usage_exit;;
				\?*)
					echo "$EXE_NAME: invalid option -- '$OPTARG'" >&2
					echo "$TRY_HELP" >&2
					exit 1
					;;
				## オプション引数がないときのエラー捕捉。
				## オプション引数が存在するオプション t:の場合，
				## オプション引数が万が一指定されていなければ，optに:が入る。
				## そして，OPTARGにはもともとのオプションの文字tが入る
				:*)
					echo "$EXE_NAME: option requires an argument -- '$OPTARG'" >&2
					echo "$TRY_HELP" >&2
					exit 1
					;;
				-*)
					echo "$EXE_NAME: unrecognized option '$1'" >&2
					echo "$TRY_HELP" >&2
					exit 1
					;;
				*) echo "other: opt: $opt, OPTARG: $OPTARG";;
			esac
			# shift
			## グループ化をどうするか
			echo "after: opt: $opt, OPTARG: $OPTARG, 1: ${1:-}"
			## グループの最後，またはにきたらshift
			## ex: $1=-bt, -att
			# [ -z "${1##*$opt$OPTARG}" ] && shift
			# case "${1:-}" in *"$opt$OPTARG")
			## スイッチ系と-t1形式のグループと--long=形式のオプションをここで処理
			## -a20aみたいなのがくるときにちゃんと20は処理してほしい

			arg="${1:-}"

			## -t 2みたいなのがくるときは，すでにshift 2してるから$1は空になる
			# case "${1:-}" in *"$opt$OPTARG") # OK
			# 	shift
			# esac
			# case "${1:-}" in *"[!$opt]"*"$opt$OPTARG")
			

			# case "${arg##*[!$opt]}" in "$opt$OPTARG")
			# case "${1:-}" in "-$opt$OPTARG")
			# # 	"${1##*$opt}"
			# # case "${1:-}" in *"$opt$OPTARG"|*"$opt"*)
			# 	shift
			# 	continue
			# esac

			## 素直にショートオプションのパース済み文字を先頭から削除
			case "${1:-}" in
				--*) shift;;
				-[0-9]*) set -- $(printf '%s\n' "$@" | sed 's/^-[0-9]*/-/');;
				# -[!0-9-]*) set -- "-${@#-$opt}";;
				-$opt?*) set -- "-${@#-$opt}";;
			esac

			# [ "$opt" != - ] && set -- "-${@#-$opt}"

			# [ "${1:-}" = "-$opt$OPTARG" ] && shift
			## 元々$1が空の場合を考慮
			# [ -z "${1##*$opt$OPTARG}" ] || shift
		done

		echo "OUT: #: $#, 1: ${1:-}, 2: ${2:-}, opt: $opt, OPTARG: ${OPTARG:-}, OPTIND: $OPTIND, $@"

		## For trailing option and end of option
		[ -z "${1+defined}" ] && break

		## Process --
		case "$1" in --)
			shift
			for arg in "$@"; do
				eval arg_$((argc+=1))='$arg'
			done
			break
		esac

		eval arg_$((argc+=1))='$1'
		shift
		# echo "after args: OPTIND-1: $((OPTIND - 1)), \$#: $#, \$@: $@"
	done

	while [ $((i+=1)) -le $argc ]; do
		eval "echo arg_$i: \$arg_$i"
	done

	echo "flag_a  : ${flag_a:-}"
	echo "opt_tags: $opt_tags," "opt_bags: $opt_bags," "opt_n:    $opt_n"

)

if is_main; then
	parse_arg "$@"
fi
