all: eeea find_peak

eeea:
	cd eeea_c; make

find_peak:
	cd find_peak_c; make