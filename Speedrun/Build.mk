# Recurse into the challenge directories even though they don't contain Build.mk files
_SPEEDRUN_CHALS := $(sort $(patsubst $(DIR)/%/flag.txt,%,$(wildcard $(DIR)/*/flag.txt)))
$(DIR)+SUBDIRS := $(_SPEEDRUN_CHALS)

#####
# set_speedrun_buildmk($1: challenge dir name like "06")
#####
define _set_speedrun_buildmk

$$(DIR)/$1+BUILD_MK := $$(DIR)/BuildChal.mk

endef
set_speedrun_buildmk = $(eval $(call _set_speedrun_buildmk,$1))
#####

$(foreach d,$(_SPEEDRUN_CHALS),$(call set_speedrun_buildmk,$d))
