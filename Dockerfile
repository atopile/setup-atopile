ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# Fix permissions for uv installed under /root
# FIXME: we should do this upstream
RUN if [ -d "/root/.local/share/uv" ]; then chmod -R o+rx /root/.local/share/uv; fi

# so it can be used as a command
ENTRYPOINT ["ato"]
