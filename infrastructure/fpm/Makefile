app-packages:
	# Packages specifically required for the application to run (dependencies
	# of the Python packages in requirements.txt). It's essentially the
	# packages that are installed during the Dockerfile build process.
	apt-get -y install \
		portaudio19-dev \
		swig \
		libpulse-dev \
		ffmpeg

build-packages:
	# Packages required to build suitable app debs/rpms using fpm.
	apt-get -y install \
		build-essential \
		python-dev \
		python-virtualenv \
		libffi-dev

fpm:
	# Build fpm on Ubuntu https://fpm.readthedocs.io/en/latest/installing.html
	apt-get -y install \
		build-essential \
		ruby ruby-dev rubygems
	gem install --no-ri --no-rdoc fpm

rpm-packages:
	# Packages required by fpm to build RPMs. Delete `rpm` from the setup stage
	# if you're only building debs.
	apt-get -y install rpm
	# virtualenv-tools required to build rpm
	apt-get -y install python-pip
	pip install virtualenv-tools

setup: app-packages build-packages fpm rpm-packages

clean:
	rm -rf build/ *.deb *.rpm

build-rpm: clean
	docker run -it --rm \
		-v /home/paulw/projects/python-speech-recognition:/pwd \
		-w /pwd/infrastructure/fpm \
		--entrypoint ./build-rpm.sh \
		fpm
