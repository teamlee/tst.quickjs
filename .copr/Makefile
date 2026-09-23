
packages:
	sudo dnf --quiet -y install tree gcc

SOURCES_quickjs:
	git -C quickjs archive --format=tgz --prefix=quickjs/ HEAD -o ../quickjs.tgz
	cp quickjs.tgz ~/rpmbuild/SOURCES/
	cp quickjs-fc-libdir.patch ~/rpmbuild/SOURCES/

srpm: packages SOURCES_quickjs
	echo SRPM done

