# Description: Simplified Dockerfile for deploying a subnet with localnet with pow-faucet feature using pre-built binaries.
FROM ubuntu:20.04

# Non-interactive frontend for automatic installs
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and pip
ARG PYTHON_VERSION=3.10

# Basic updates and necessary libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    python${PYTHON_VERSION} \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    jq \
    && python3 -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*


# Make python3.8 the default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
    && update-alternatives --set python /usr/bin/python3.8


# Set the working directory in the container
WORKDIR /usr/src/subnet

# Copy the requirements.txt file into the container at /usr/src/subnet
# This is done before copying the rest of the code so that Docker can cache the installation of dependencies
COPY requirements.txt ./

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Append /usr/src/app to PYTHONPATH to ensure custom modules are found
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app"

COPY ./subtensor/snapshot.json /
COPY ./subtensor/raw_spec.json /
COPY ./subtensor/raw_testspec.json /
COPY ./subtensor/node-subtensor /usr/local/bin/node-subtensor
COPY ./subtensor/localnet.sh /subtensor/scripts/localnet.sh

# Ensure localnet.sh is executable
RUN chmod +x /subtensor/scripts/localnet.sh
# Copy the rest of your application's source code from your host to your image filesystem.
COPY . .
RUN chmod +x /usr/src/subnet/scripts/run_subnet.sh