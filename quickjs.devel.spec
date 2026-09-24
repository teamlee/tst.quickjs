%global upstream_date 2026-06-04
%global commit 04be246001599f5995fa2f2d8c91a0f198d3f34c
# Fedora runs %%set_build_flags at the start of %%build, %%check, and
# %%install. Leave the compiler flags to the QuickJS Makefile.
%undefine _auto_set_build_flags
# Headers and libraries only. Do not add debuginfo packages or
# /usr/lib/.build-id links.
%global debug_package %{nil}
%global _build_id_links none

Name:           quickjs.devel
Version:        2026.06.04
Release:        3%{?dist}
Summary:        QuickJS headers and libraries

License:        MIT
URL:            https://github.com/bellard/quickjs
Source0:        https://codeload.github.com/bellard/quickjs/tar.gz/%{commit}

BuildRequires:  gcc
BuildRequires:  glibc-devel

# libquickjs.a is owned by quickjs.bin. qjsc looks for it there.
Requires:       quickjs.bin >= %{version}

%description
QuickJS is a small and embeddable JavaScript engine. This package
contains the public headers. The libraries are provided by quickjs.bin.

%prep
# The codeload archive unpacks to quickjs-<full commit>, not %{name}.
%setup -q -n quickjs-%{commit}

%build

%install
install -D -p -m 0644 quickjs.h %{buildroot}%{_includedir}/quickjs/quickjs.h
install -D -p -m 0644 quickjs-libc.h %{buildroot}%{_includedir}/quickjs/quickjs-libc.h

%check
gcc -c -I. -o /dev/null -x c - << 'EOF'
#include "quickjs.h"
#include "quickjs-libc.h"
EOF

%files
%{_includedir}/quickjs/quickjs.h
%{_includedir}/quickjs/quickjs-libc.h

%changelog
* Thu Sep 24 2026 Packager - 2026.06.04-3
- Leave both libraries to quickjs.bin

* Thu Sep 24 2026 Packager - 2026.06.04-2
- Drop libquickjs.a and require quickjs.bin, which owns that file

* Thu Sep 24 2026 Packager - 2026.06.04-1
- Package the QuickJS headers, static library, and shared library
