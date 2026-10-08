# TSATechie is a docker-compose web challenge (no PwnableHarness TARGET to
# build). This Build.mk exists only to register the `pwnmake check`, which
# starts it, runs the solver, and tears it down.
$(call ctf_check_web,$(DIR),20501,tsatechie.ctf.hackucf.org,python3 solver.py)

# Handouts players download (served from publish/ at /files/...)
PUBLISH += attachments/InvestigationReport.pdf attachments/ScannedDocuments.pdf
