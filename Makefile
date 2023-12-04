FILE=recursive_function
CFILE=samples/$(FILE).c
SFILE=assembly/$(FILE).s

main:
	python3 -m src.main -p -r -a -n $(SFILE) $(CFILE)

none:
	python3 -m src.main $(CFILE)

write:
	python3 -m src.main -o $(FILE).json $(CFILE)

read:
	python3 -m src.main -i $(FILE).json -a

force:
	python3 -m src.main -sptrf $(CFILE)

asm:
	gcc $(SFILE) -o assembly/$(FILE)
	./assembly/$(FILE); echo $$?

gcc:
	gcc -O0 -S $(CFILE) -o gcc/$(FILE).s
	gcc gcc/$(FILE).s -o gcc/$(FILE)
	./gcc/$(FILE); echo $$?

test:
	python3 -m tests.testing -v

e2e:
	sh ./tests/e2e.sh

install:
	pip3 install -r requirements.txt

character_count:
	python3 character_count.py words.txt

format:
	black ./

lint:
	pylint src/ tests/

clean:
	rm -f *.o logs/* tables/*

.PHONY: gcc
