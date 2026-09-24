
packages:
	dnf --quiet -y install git tree gcc

create_source_rpm_quickjs:
	rpmbuild -bs quickjs.spec

all_source_rpm_to_workdir:
	mv ~/build/SRPMS/*.src.rpm $(outdir)

srpm: packages create_source_rpm_quickjs all_source_rpm_to_workdir
	echo SRPM done

