# Remove all the assembly files so we do not get prompted
# if we want to overwrite the .s files
rm assembly/*

for entry in samples/*.c
do
	FILE=${entry:8}
	FILE=${FILE:0:${#FILE}-2}
	CFILE=samples/$FILE.c
	SFILE=assembly/$FILE.s

	# Skip some test files that are not implemented all the
	# way through to the ASM step of our compiler
	case $FILE in
		duplicate_func)
			continue
			;;
		duplicate_label)
			continue
			;;
		duplicate_var)
			continue
			;;
		float)
			continue
			;;
		for)
			continue
			;;
		include)
			continue
			;;
		linebreak)
			continue
			;;
		struct)
			continue
			;;
		undefined_var)
			continue
			;;
	esac

	# Run gcc and store the output
	gcc -O0 -S $CFILE -o gcc/$FILE.s
	gcc gcc/$FILE.s -o gcc/$FILE
	gccoutput="$(./gcc/$FILE; echo $?)"

	# Run our compiler and store the output
	python3 -m src.main -n $SFILE $CFILE > /dev/null
	gcc $SFILE -o assembly/$FILE
	compileroutput="$(./assembly/$FILE; echo $?)"

	# Compare the two outputs for discrepancies
	if [ $gccoutput != $compileroutput ]
	then
		echo "$FILE: $gccoutput (GCC) did not match $compileroutput (compiler)"
	else
		echo "$FILE: ✔"
	fi
done
