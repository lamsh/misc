#!/bin/sh
while getopts '' opt
do
	case "opt${OPTARG:-}" in
		"t$OPTARG"|-tag*)
			## ロングオプションの場合はシフトして次の引数をオプション引数とする
			case "$OPTARG" in tag)
				shift $((OPTIND - 1))
				OPTARG=$1
				shift
			esac

			case "$OPTARG" in -*|'')
				echo "$EXE_NAME: option requires an argument -- $1" >&2
				exit 1
			esac
			echo "tag: opt: ${opt}, OPTARG: $OPTARG"
			opt_tags="$opt_tags $OPTARG"
			;;
## 一度にまとめてやろうとすると中でショートとロングの場合分けがいるので分けたほうがいい？
		"t$OPTARG")
			case "$OPTARG" in -*|'')
				echo "$EXE_NAME: option requires an argument -- $1" >&2
				exit 1
			esac
			echo "tag: opt: ${opt}, OPTARG: $OPTARG"
			opt_tags="$opt_tags $OPTARG"
			;;
		:-tag*)
			## ロングオプションの場合はシフトして次の引数をオプション引数とする
			;;

	esac
done
