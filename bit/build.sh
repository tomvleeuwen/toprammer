#!/bin/bash
# Rebuild FPGA bit files
# Copyright (c) 2010 Michael Buesch <mb@bu3sch.de>
# Licensed under the GNU/GPL v2+

basedir="$(dirname $0)"
srcdir="$basedir/src"
bindir="$basedir"

function usage
{
	echo "Usage: build.sh [OPTIONS] [TARGETS]"
	echo
	echo "Options:"
	echo " -h|--help           Show this help text"
	echo " -v|--verbose        Verbose build"
	echo
	echo "Targets:"
	echo "Specify the names of the targets to build, or leave blank to rebuild all."
}

# Parse commandline
verbose=0
nr_targets=0
while [ $# -gt 0 ]; do
	if [ "$1" = "-h" -o "$1" = "--help" ]; then
		usage
		exit 0
	fi
	if [ "$1" = "-v" -o "$1" = "--verbose" ]; then
		verbose=1
		shift
		continue
	fi
	targets[nr_targets]="$1"
	let nr_targets=nr_targets+1
	shift
done

function should_build # $1=target
{
	[ $nr_targets -eq 0 ] && return 0
	let end=nr_targets-1
	for i in $(seq 0 $end); do
		[ ${targets[i]} = "$1" ] && return 0
	done
	return 1
}

for src in $srcdir/*; do
	[ -d "$src" ] || continue

	srcname="$(basename $src)"
	logfile="$bindir/$srcname.build.log"

	should_build $srcname || continue

	echo "Building $srcname..."
	make -C $src/ clean >/dev/null
	if [ $? -ne 0 ]; then
		echo "FAILED to clean $srcname."
		exit 1
	fi
	if [ $verbose -eq 0 ]; then
		make -C $src/ all >$logfile
		if [ $? -ne 0 ]; then
			cat $logfile
			echo "FAILED to build $srcname."
			exit 1
		fi
		cat $logfile | grep WARNING
	else
		make -C $src/ all
	fi
	cp -f $src/$srcname.bit $bindir/$srcname.bit
	make -C $src/ clean >/dev/null
	if [ $? -ne 0 ]; then
		echo "FAILED to clean $srcname."
		exit 1
	fi
	rm -f $logfile
done
echo "Successfully built all images."

exit 0
