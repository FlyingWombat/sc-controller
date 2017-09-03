#!/bin/bash
C_MODULES=(uinput hiddrv)
C_VERSION_uinput=6
C_VERSION_hiddrv=1

function rebuild_c_modules() {
	echo "lib$1.so is outdated or missing, building one"
	echo "Please wait, this should be done only once."
	echo ""
	
	# Next line generates string like 'lib.linux-x86_64-2.7', directory where libuinput.so was just generated
	LIB=$( python2 -c 'import platform ; print "lib.linux-%s-%s.%s" % ((platform.machine(),) + platform.python_version_tuple()[0:2])' )
	
	if [ -e build/$LIB/libuinput.so ] ; then
		rm build/$LIB/libuinput.so || exit 1
	fi
	
	python2 setup.py build || exit 1
	echo ""
	
	for cmod in ${C_MODULES[@]}; do
		if [ ! -e lib${cmod}.so ] ; then
			ln -s build/$LIB/lib${cmod}.so ./lib${cmod}.so || exit 1
			echo Symlinked ./lib${cmod}.so '->' build/$LIB/lib${cmod}.so
		fi
	done
	echo ""
}


# Ensure correct cwd
cd "$(dirname "$0")"

# Check if c modules are compiled and actual
for cmod in ${C_MODULES[@]}; do
	eval expected_version=\$C_VERSION_${cmod}
	reported_version=$(PYTHONPATH="." python2 -c 'import os, ctypes; lib=ctypes.CDLL("./'lib${cmod}'.so"); print lib.'${cmod}'_module_version()')
	if [ x"$reported_version" != x"$expected_version" ] ; then
		rebuild_c_modules ${cmod}
	fi
done

# Set PATH
SCRIPTS="$(pwd)/scripts"
export PATH="$SCRIPTS":"$PATH"
export PYTHONPATH=".":"$PYTHONPATH"
export SCC_SHARED="$(pwd)"

# Execute
python2 'scripts/sc-controller' $@
