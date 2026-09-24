# Metapackage. Installing it pulls in the binary, devel, and doc packages.
%global debug_package %{nil}

Name:           quickjs.full
Version:        2026.06.04
Release:        1%{?dist}
Summary:        QuickJS interpreter, libraries, and manual

License:        MIT
URL:            https://github.com/bellard/quickjs
BuildArch:      noarch

Requires:       quickjs.bin = %{version}-%{release}
Requires:       quickjs.devel = %{version}-%{release}
Requires:       quickjs.doc = %{version}-%{release}

%description
Metapackage for QuickJS. It contains no files of its own. Installing
it installs quickjs.bin, quickjs.devel, and quickjs.doc.

%files

%changelog
* Thu Sep 24 2026 Packager - 2026.06.04-1
- Metapackage requiring quickjs.bin, quickjs.devel, and quickjs.doc
