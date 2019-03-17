FROM opensuse/leap:42.3

MAINTAINER Paul Williams <kwakwaversal@gmail.com>

# Packages required to build suitable app RPMs using fpm.
RUN zypper --non-interactive \
    install -y               \
    python-devel             \
    python-pip               \
    python-virtualenv        \
    libffi-devel
RUN pip install --upgrade pip && \
    pip install virtualenv-tools

# Build fpm https://fpm.readthedocs.io/en/latest/installing.html
RUN zypper --non-interactive \
    install -y               \
    ruby-devel               \
    gcc                      \
    make                     \
    rpm-build                \
    libffi-devel-gcc5
RUN gem install --no-ri --no-rdoc fpm

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

# Not sure why openSUSE appends the ruby version to fpm? Seems like it might be
# a thing based on the link below:
#
# https://github.com/irods/externals/blob/master/build.py#L278-L279
RUN echo -e '#!/bin/sh\nfpm.ruby2.1 "$@"' > /bin/fpm && chmod u+x /bin/fpm

ENTRYPOINT ["fpm"]
