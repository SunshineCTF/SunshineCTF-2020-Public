# PasswordPandemonium is a docker-compose web challenge (no PwnableHarness
# TARGET to build). This Build.mk exists only to register the `pwnmake check`,
# which starts it, runs the solver, and tears it down.
$(call ctf_check_web,$(DIR),20301,passwordpandemonium.ctf.hackucf.org,python3 solver.py)
