FROM kjcolley7/lilchompys-redacted:release

# Overwrite old flag with the real one
ARG CHOMPY_DIR
COPY ${CHOMPY_DIR}/flag.txt ./

# Make sure the permissions are still correct
RUN chown "root:lilchompys" flag.txt && chmod 0640 flag.txt
