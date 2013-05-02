.PHONY: do_nothing
.PHONY: clean
.PHONY: evaluate


do_nothing:
	echo make clean # clean 
	echo make evaluate  # run test

clean:
	rm -f evaluate.log
	rm -rf ./.cache

evaluate:
	python -c   'import myevaluate;a = myevaluate.start("B") ;b = myevaluate.start("K",0.05);merged = list(set(a+b));print("{0}:{1}".format("combine all algorithm",len(merged)))'
