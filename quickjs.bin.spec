%global upstream_date 2026-06-04
%global commit 04be246001599f5995fa2f2d8c91a0f198d3f34c
%global patchcommit c78abb14edac6792e85fab43f7189a7c540e3bc6
# Fedora runs %%set_build_flags at the start of %%build, %%check, and
# %%install. Leave the compiler flags to the QuickJS Makefile.
%undefine _auto_set_build_flags
# Do not add debuginfo packages or /usr/lib/.build-id links.
%global debug_package %{nil}
%global _build_id_links none

Name:           quickjs.bin
Version:        2026.06.04
Release:        1%{?dist}
Summary:        QuickJS command-line interpreter and compiler

License:        MIT
URL:            https://github.com/bellard/quickjs
Source0:        https://codeload.github.com/bellard/quickjs/tar.gz/%{commit}
# qjsc looks up libquickjs.a under $PREFIX/lib. The raw URL is the
# patch itself; a GitHub blob URL is an HTML page.
Source1:        https://raw.githubusercontent.com/teamlee/tst.quickjs/%{patchcommit}/quickjs-fc-libdir.patch

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  make

%description
QuickJS is a small and embeddable JavaScript engine. This package
contains the qjs interpreter, the qjsc compiler, and libquickjs.a.

%prep
# The codeload archive unpacks to quickjs-<full commit>, not %{name}.
%setup -q -n quickjs-%{commit}
if grep -F -q '/lib/quickjs' qjsc.c; then
  git apply -- %{SOURCE1}
fi
if grep -F -q '@LIBDIR@' qjsc.c; then
  sed -i 's|@LIBDIR@|%{_libdir}/quickjs|' qjsc.c
fi

%build
# Upstream appends -D_GNU_SOURCE, -DCONFIG_VERSION, -fwrapv, and the
# qjsc prefix defines with CFLAGS+=. Extra flags have to come from the
# environment; a CFLAGS= argument on the make command line would drop them.
CFLAGS="${CFLAGS} -fPIC"
export CFLAGS
rm -rf .obj
rm -f qjs qjsc libquickjs.a
# qjsc links generated programs against libquickjs.a.
%make_build PREFIX=%{_prefix} qjs qjsc libquickjs.a

%install
install -D -p -m 0755 qjs %{buildroot}%{_bindir}/qjs
install -D -p -m 0755 qjsc %{buildroot}%{_bindir}/qjsc
install -D -p -m 0644 libquickjs.a %{buildroot}%{_libdir}/quickjs/libquickjs.a

%check
%make_build test
./qjsc -o hello-rpm examples/hello.js
test "$(./hello-rpm)" = "Hello World"
rm -f hello-rpm
grep -F -q '"%{_libdir}/quickjs"' qjsc.c

%files
%{_bindir}/qjs
%{_bindir}/qjsc
%{_libdir}/quickjs/libquickjs.a

%changelog
* Thu Sep 24 2026 Packager - 2026.06.04-1
- Package qjs, qjsc, and libquickjs.a
