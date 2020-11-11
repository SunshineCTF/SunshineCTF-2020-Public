.PHONYS: test clean

test:
	python3 generate.py testTEST1234
	gcc output.c -o test
	# echo "testTEST1234" | ./test

build:
	python3 generate.py
	gcc output.c -o attachments/hotel_key_puzzle

clean:
	rm ./test
	rm ./output.c