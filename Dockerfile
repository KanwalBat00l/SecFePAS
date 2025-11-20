FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install minimal runtime dependencies
RUN apt update && apt install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# Copy the entire build folder
COPY build ./build

# Tell linker to look in build/lib for shared libraries
ENV LD_LIBRARY_PATH=/app/build/lib:$LD_LIBRARY_PATH

# Copy pretrained models (compressed)
COPY pretrained ./pretrained

# Extract archives correctly inside /app/pretrained
RUN cd /app/pretrained && \
    for f in *.gz; do tar -xzvf "$f" && rm "$f"; done

# Copy scripts
COPY scripts ./scripts

# Make scripts and binaries executable
RUN chmod +x scripts/*.sh && chmod +x build/bin/*

# Add bin and scripts to PATH
ENV PATH="/app/build/bin:/app/scripts:${PATH}"

CMD ["/bin/bash"]
