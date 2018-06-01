# Makefile for fluodonut.
#

.PHONY: clean

clean:
	rm fluodonut/*.pyc &
	rm fluodonut/*~ &
	rm fluodonut/#*# &
	rm *~ &
	rm -rf notebooks/.ipynb* &
	rm -rf notebook/*~

install:
	pip install -e .
