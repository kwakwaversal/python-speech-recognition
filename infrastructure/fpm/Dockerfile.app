FROM kwakwa/fpm-opensuse

MAINTAINER Paul Williams <kwakwaversal@gmail.com>

# Packages specifically required for the application to run (dependencies of
# the Python packages in requirements.txt). It's essentially the packages
# that are installed during the Dockerfile build process.
RUN zypper --non-interactive \
    install -y               \
    portaudio-devel          \
    swig                     \
    libpulse-devel           \
    ffmpeg                   \
    alsa-devel

# Clean up!
RUN zypper clean --all; \
    rm --verbose --recursive --force /var/cache/zypp

ENTRYPOINT ["fpm"]
