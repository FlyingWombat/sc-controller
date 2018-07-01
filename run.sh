#!/bin/bash
C_MODULES=(uinput hiddrv sc_by_bt)
C_VERSION_uinput=9
C_VERSION_hiddrv=5
C_VERSION_sc_by_bt=3

function rebuild_c_modules() {
	echo "lib$1.so is outdated or missing, building one"
	echo "Please wait, this should be done only once."
	echo ""
	
	# Next line generates string like 'lib.linux-x86_64-2.7', directory where libuinput.so was just generated
	py_lib_str='from __future__ import print_function
import platform
py_version = platform.python_version_tuple()
print("lib.linux-{0}-{1}.{2}".format(platform.machine(), py_version[0], py_version[1]))'
	LIB=$( python3 -c "$py_lib_str")
	
	for cmod in ${C_MODULES[@]}; do
		if [ -e build/$LIB/lib${cmod}.so ] ; then
			rm build/$LIB/lib${cmod}.so || exit 1
		fi
	done
	
	python3 setup.py build || exit 1
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
	
	if [ ! -e "./lib$cmod.so" ] ; then
        # if c module doesn't exist, make it
        reported_version=-1
	else
        py_mod_str="from __future__ import print_function
import os, ctypes
lib=ctypes.CDLL('./lib${cmod}.so')
print(lib.${cmod}_module_version())"
        reported_version=$(PYTHONPATH="." python3 -c "$py_mod_str")
    fi
    
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
python3 'scripts/sc-controller' $@
