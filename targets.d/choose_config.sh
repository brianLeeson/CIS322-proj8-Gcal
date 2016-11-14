#! /bin/bash
# 
# choose a configuration file:  
#     We install one of the CONFIG_machine.py files as ../CONFIG.py 
#     selecting by known host names (e.g., ix), architecture names
#     (e.g., armv7 or armv8 for pi), operating system (darwin for MacOSX). 
#     The default is chosen if none of the known architectures matches. 
#     Similarly one Makefile.local
#
# 

# What machine is this?  Use uname to find hardware
# 
architecture=`uname -m`
node=`uname -n`
processor=`uname -p`
opsys=`uname -v`
port="5000"   # But see how this is altered for shared server ix


# Generate configuration file text with a couple of choices
#
function gen_config {
    secret="$(date | shasum | head -c32)"
    gendate="$(date)"
    cat <<EOF
"""
Configuration of MeetMe app 
Generated $( date )
May be edited to fit target environment

"""

PORT=${port}
DEBUG = True  # Set to False for production use
secret_key="${secret}"

EOF
}

# Generate Makefile.local with the proper reference 
# to pyvenv, which may vary from target to target
#
# 
function gen_makefile {
    if test -f `which pyvenv` ; then
       pyvenv=`which pyvenv`
     elif test -f `which pyvenv3.5` ; then        
       pyvenv=`which pyvenv-3.5`
     elif test -f `which pyvenv3.4` ; then 
       pyvenv=`which pyvenv-3.4`
     elif test -f virtualenv ; then  # Windows 10 bash ?
       pyvenv=`which virtualenv`
       (>&2 echo "Attempting to point pyvenv to virtualenv as \"${pyvenv}\"")
       (>&2 echo "You might need to fix pyvenv variable in Makefile.local") 
     else
       (>&2 echo "You'll need to fix Makefile.local and then re-run 'make env'")
       pyvenv="FIXME_PYVENV_PATH"
    fi;
    cat <<EOF
# 
# Target-specific paths for Makefile
#

PYVENV = ${pyvenv} 

EOF
}

if [[ $architecture =~ "arm" ]]; then
   echo "Configuring for Raspberry Pi versions 2 or 3"
   gen_config > ../CONFIG.py
   gen_makefile > ../Makefile.local

elif [[ $opsys =~ "Darwin" ]]; then 
   echo "Configuring for Mac OS X"
   gen_config > ../CONFIG.py
   gen_makefile > ../Makefile.local

elif [[ $node =~ "ix" ]]; then 
   echo "Configuring for shared CIS host ix-trusty or ix-dev"
   (( port = 1000 + ($RANDOM % 8000) ))
   gen_makefile > ../Makefile.local
   gen_config > ../CONFIG.py
   echo "CONFIG.py uses random port ${port}; you may edit for another value"

else
   echo "Unknown host type; using default configuration files"
   echo "Edit CONFIG.py to set appropriate port"
   echo "Edit Makefile.local as needed"
   gen_config > ../CONFIG.py
   gen_makefile > ../Makefile.local
fi;




