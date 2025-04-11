ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# so it can be used as a command
ENTRYPOINT ["ato"]
