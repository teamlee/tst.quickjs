
packages:
	sudo dnf --quiet -y install git tree gcc

create_source_rpm:
	rpmbuild -bs *.spec

all_source_rpm_to_workdir:
	tree ~/build
	mv ~/build/SRPMS/*.src.rpm $(outdir)

srpm: packages create_source_rpm all_source_rpm_to_workdir
	echo SRPM done

