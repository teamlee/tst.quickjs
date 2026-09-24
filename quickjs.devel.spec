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
Release:        1%{?dist}
Summary:        QuickJS headers and libraries

License:        MIT
URL:            https://github.com/bellard/quickjs
Source0:        https://codeload.github.com/bellard/quickjs/tar.gz/%{commit}

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make

%description
QuickJS is a small and embeddable JavaScript engine. This package
contains the public headers, libquickjs.a, and libquickjs.so.

%prep
# The codeload archive unpacks to quickjs-<full commit>, not %{name}.
%setup -q -n quickjs-%{commit}

%build
# Upstream appends -D_GNU_SOURCE, -DCONFIG_VERSION, -fwrapv, and the
# qjsc prefix defines with CFLAGS+=. Extra flags have to come from the
# environment; a CFLAGS= argument on the make command line would drop them.
CFLAGS="${CFLAGS} -fPIC"
export CFLAGS
rm -rf .obj
rm -f libquickjs.a libquickjs.so
%make_build PREFIX=%{_prefix} libquickjs.a \
    .obj/quickjs.pic.o .obj/dtoa.pic.o .obj/libregexp.pic.o \
    .obj/libunicode.pic.o .obj/cutils.pic.o .obj/quickjs-libc.pic.o
# The Makefile has no shared-library target. Link the PIC objects.
gcc -shared -Wl,-soname,libquickjs.so -o libquickjs.so \
    .obj/quickjs.pic.o .obj/dtoa.pic.o .obj/libregexp.pic.o \
    .obj/libunicode.pic.o .obj/cutils.pic.o .obj/quickjs-libc.pic.o \
    -lm -lpthread -ldl

%install
install -D -p -m 0644 quickjs.h %{buildroot}%{_includedir}/quickjs/quickjs.h
install -D -p -m 0644 quickjs-libc.h %{buildroot}%{_includedir}/quickjs/quickjs-libc.h
install -D -p -m 0644 libquickjs.a %{buildroot}%{_libdir}/quickjs/libquickjs.a
install -D -p -m 0755 libquickjs.so %{buildroot}%{_libdir}/libquickjs.so

%check
cat > linkcheck.c << 'EOF'
#include "quickjs.h"
int main(void) {
    JSRuntime *rt = JS_NewRuntime();
    JS_FreeRuntime(rt);
    return 0;
}
EOF
gcc -I. linkcheck.c libquickjs.a -lm -lpthread -ldl -o linkcheck-static
./linkcheck-static
gcc -I. linkcheck.c -L. -lquickjs -Wl,-rpath,. -lm -lpthread -ldl -o linkcheck-shared
./linkcheck-shared

%files
%{_includedir}/quickjs/quickjs.h
%{_includedir}/quickjs/quickjs-libc.h
%{_libdir}/quickjs/libquickjs.a
%{_libdir}/libquickjs.so

%changelog
* Thu Sep 24 2026 Packager - 2026.06.04-1
- Package the QuickJS headers, static library, and shared library
