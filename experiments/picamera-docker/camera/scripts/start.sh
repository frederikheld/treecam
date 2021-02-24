#!/bin/sh

echo "Hello Shell!"

echo "LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"

# echo "cat /etc/ld.so.conf.d/00-vmcs.conf"
# cat /etc/ld.so.conf.d/00-vmcs.conf 

# echo "${LD_LIBRARY_PATH}" > /etc/ld.so.conf.d/00-vmcs.conf
# ldconfig

# echo "cat /etc/ld.so.conf.d/00-vmcs.conf"
# cat /etc/ld.so.conf.d/00-vmcs.conf

# echo "ls -la \${LD_LIBRARY_PATH}"
# ls -la ${LD_LIBRARY_PATH}

# echo "file ${LD_LIBRARY_PATH}/libbcm_host.so"
# file ${LD_LIBRARY_PATH}/libbcm_host.so

# echo "dpkg --print-architecture"
# dpkg --print-architecture

# echo "pwd"
# echo "$PWD"

# echo "ls -la \$PWD"
# ls -la $PWD

# echo "ls ${LD_LIBRARY_PATH}"
# ls -ls ${LD_LIBRARY_PATH}

rm output.jpg

ls -la

python3 take-picture.py

ls -la