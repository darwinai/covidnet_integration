#!/bin/bash
#
# Once a ChRIS/CUBE ecosystem has been fully instantiated from a run of the
# 'make.sh' script, the system will by default only have a few test/dummy
# plugins available. This is to keep instantiation times comparatively fast,
# especially in the case of development where the whole ecosystem is created
# and destroyed multiple times.
#
# In order to add more plugins to an instantiated system, this postscript.sh
# can be used to add plugins and also provide an easy cheat sheet for adding
# more.
#

./plugin_add.sh  "\
	fnndsc/pl-dircopy, \
	fnndsc/pl-med2img, \
	darwinai/pl-covidnet, \
	darwinai/pl-ct-covidnet, \
	darwinai/pl-covidnet-grad-cam
	darwinai/pl-covidnet-pdfgeneration, \
"

#
# Adding additional users
# Users can be added using some specific variation of the
# following:
#
# CUBE USERS
# For "superusers"
#####user_add.sh -U "rudolph:rudolph1234:rudolph.pienaar@gmail.com"
# For "normal users"
#####user_add.sh    "rpienaar:rudolph1234:rppienaar@gmail.com"
#
# STORE USERS
# For "superusers"
#####user_add.sh -U -S "rudolph:rudolph1234:rudolph.pienaar@gmail.com"
# For "normal users"
#####user_add.sh -S    "rpienaar:rudolph1234:rppienaar@gmail.com"
#

