#! /usr/bin/env bash
set -xe

export VERSION=0.0.1

# apt-get -y install build-essential python-dev python-virtualenv libffi-dev

rm -rf build

mkdir -p build/usr/share/python
virtualenv build/usr/share/python/tokandtran --distribute
build/usr/share/python/tokandtran/bin/pip install -U pip distribute
build/usr/share/python/tokandtran/bin/pip uninstall -y distribute

build/usr/share/python/tokandtran/bin/pip install virtualenv-tools
build/usr/share/python/tokandtran/bin/pip install -r ../../requirements.txt virtualenv-tools

find build ! -perm -a+r -exec chmod a+r {} \;

mkdir -p build/usr/local/bin
cp ../../tokenize_and_transcribe.py build/usr/local/bin/tokandtran
sed -i "s/\/usr\/bin\/env python/\/usr\/share\/python\/tokandtran\/bin\/python/g" build/usr/local/bin/tokandtran
chmod 755 build/usr/local/bin/tokandtran

cd build/usr/share/python/tokandtran
sed -i "s/'\/bin\/python'/\('\/bin\/python','\/bin\/python2'\)/g" lib/python2.7/site-packages/virtualenv_tools.py
./bin/virtualenv-tools --update-path /usr/share/python/tokandtran
cd -

find build -iname *.pyc -exec rm {} \;
find build -iname *.pyo -exec rm {} \;

# cp -a conf/etc build

# docker run -it --rm -v $(pwd):/data fpm -p /data \
fpm \
    -t rpm -s dir -C build -n tokandtran -v $VERSION \
    --iteration `date +%s` \
    --rpm-user root \
    --rpm-group root \
    -d python2 \
    -d portaudio-devel \
    -d swig \
    -d libpulse-devel \
    -d ffmpeg \
    --after-install conf/post-install \
    --before-remove conf/pre-remove \
    --after-remove conf/post-remove \
    .

# zypper --no-gpg-checks install *.rpm
# fpm -t rpm -s virtualenv --name tokandtran -d python2 -d portaudio-devel -d swig -d libpulse-devel -d ffmpeg --prefix /opt/tokandtran/virtualenv ../../requirements.txt
