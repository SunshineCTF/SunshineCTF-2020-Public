# The challenge directories (00..17) are auto-discovered by PwnableHarness's
# subdir recursion, but they don't contain their own Build.mk files. Instead,
# point each one at the shared Speedrun/BuildChal.mk, which builds that challenge
# from source with its per-challenge mitigations.
_SPEEDRUN_CHALS := $(sort $(patsubst $(DIR)/%/flag.txt,%,$(wildcard $(DIR)/*/flag.txt)))

#####
# set_speedrun_buildmk($1: challenge dir name like "06")
#####
define _set_speedrun_buildmk

$$(DIR)/$1+BUILD_MK := $$(DIR)/BuildChal.mk

endef
set_speedrun_buildmk = $(eval $(call _set_speedrun_buildmk,$1))
#####

$(foreach d,$(_SPEEDRUN_CHALS),$(call set_speedrun_buildmk,$d))
