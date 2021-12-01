FROM ubuntu:20.04

# INSTALL JAVA
RUN apt-get update && apt-get -y install default-jdk curl
# Set JAVA_HOME From sudo update-alternatives --config java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

COPY scripts/ /tps/scripts
COPY tps-core/ /tps/tps-core
COPY project/ /tps/project
COPY build.sbt /tps/build.sbt
COPY workflow/ /tps/workflow
COPY tps_runner.py /tps/tps_runner.py
COPY workflow.sh /tps/workflow.sh

WORKDIR /tps
RUN ./scripts/run --help