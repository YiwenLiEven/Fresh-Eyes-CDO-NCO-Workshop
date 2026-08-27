FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       cdo \
       nco \
       netcdf-bin \
       make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

