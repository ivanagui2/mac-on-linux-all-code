#!/bin/sh
# -*- sh -*-

echo "=================================================="
echo " Invoking autoheader and autoconf."

ARCH=`scripts/archname "$ARCH"`

rm -rf config/configure
mkdir config/configure
ln -s ../configure.in config/configure/configure.in

# Cleanup certain autogenerated files
rm -rf src/shared/config.* ".inc-$ARCH/"

cd config/configure

autoheader || { 
    echo "autoheader failed" ; exit 1 
}
autoconf || { 
    echo "autoconf failed" ; exit 1
}

echo " The next step is 'make'"
echo "=================================================="
