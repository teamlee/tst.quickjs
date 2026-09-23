
packages:
	dnf --quiet -y install git tree gcc

SOURCES_quickjs:
	echo done

srpm: packages SOURCES_quickjs
	rpmbuild -bs quickjs.spec
	mv ~/build/SRPMS/*.src.rpm $(outdir)
	echo SRPM done

