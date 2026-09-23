%global upstream_date 2026-06-04
%global commit 04be246001599f5995fa2f2d8c91a0f198d3f34c
# Fedora runs %%set_build_flags at the start of %%build, %%check, and
# %%install. Leave the compiler flags to the QuickJS Makefile.
%undefine _auto_set_build_flags
# gcc still writes a GNU build-id note by default. rpm then adds
# /usr/lib/.build-id symlinks unless this is none.
%global _build_id_links none

Name:           quickjs
Version:        2026.06.04
Release:        10%{?dist}
Summary:        Small and embeddable JavaScript engine

License:        MIT
URL:            https://github.com/bellard/quickjs
Source0:        https://codeload.github.com/bellard/quickjs/tar.gz/%{commit}
# qjsc looks up libquickjs.a under $PREFIX/lib. The raw URL is the
# patch itself; a GitHub blob URL is an HTML page.
Source1:        https://raw.githubusercontent.com/teamlee/tst.quickjs/c78abb14edac6792e85fab43f7189a7c540e3bc6/quickjs-fc-libdir.patch

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  make
# HTML via makeinfo (texinfo); PDF via texi2pdf (texinfo-tex).
BuildRequires:  texinfo
BuildRequires:  texinfo-tex
# Man page from the generated HTML. Pandoc does not read Texinfo.
BuildRequires:  pandoc

%description
QuickJS is a small and embeddable JavaScript engine. It supports most of
the ES2025 specification, including modules, asynchronous generators,
proxies, and BigInt.

qjs is the command-line interpreter. qjsc compiles JavaScript to a
standalone executable; linking those executables requires quickjs-devel.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# qjsc runs the system C compiler to link executables.
Requires:       gcc

%description devel
Headers and the static library for embedding QuickJS. qjsc looks for
quickjs.h in %{_includedir}/quickjs and libquickjs.a in
%{_libdir}/quickjs.

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
Texinfo source for the QuickJS manual. The built HTML, PDF, and man
page are in the main package under %{_docdir}/quickjs.

%prep
# The codeload archive unpacks to quickjs-<full commit>.
%setup -q -n %{name}-%{commit}
# Apply once. A later build finds @LIBDIR@ already substituted.
if grep -F -q '/lib/quickjs' qjsc.c; then
  git apply -- %{SOURCE1}
fi
if grep -F -q '@LIBDIR@' qjsc.c; then
  sed -i 's|@LIBDIR@|%{_libdir}/quickjs|' qjsc.c
fi
rm -f debugfiles.list debuglinks.list debugsourcefiles.list debugsources.list elfbins.list

%build
# Upstream appends -D_GNU_SOURCE, -DCONFIG_VERSION, -fwrapv, and the
# qjsc prefix defines with CFLAGS+=. Extra flags have to come from the
# environment; a CFLAGS= argument on the make command line would drop them.
# -fPIC keeps libquickjs.a usable inside shared objects.
CFLAGS="${CFLAGS} -fPIC"
export CFLAGS
# Drop objects from an earlier make so this -fPIC build is what links.
rm -rf .obj
rm -f qjs qjsc libquickjs.a
%make_build PREFIX=%{_prefix} qjs qjsc libquickjs.a
# A checkout may already contain a manual. Drop it so this build
# produces doc/quickjs.html and doc/quickjs.pdf from doc/quickjs.texi.
rm -f doc/quickjs.html doc/quickjs.html.pre doc/quickjs.pdf doc/version.texi doc/quickjs.1
%make_build build_doc
# Pandoc has no Texinfo reader, and texi2any --docbook rejects this
# manual. Build the man page from the HTML just produced.
pandoc -f html -t man -s \
  -M title=quickjs \
  -M section=1 \
  -M header="QuickJS Javascript Engine" \
  -o doc/quickjs.1 doc/quickjs.html

%install
install -D -p -m 0755 qjs %{buildroot}%{_bindir}/qjs
install -D -p -m 0755 qjsc %{buildroot}%{_bindir}/qjsc
install -D -p -m 0644 libquickjs.a %{buildroot}%{_libdir}/quickjs/libquickjs.a
install -D -p -m 0644 quickjs.h %{buildroot}%{_includedir}/quickjs/quickjs.h
install -D -p -m 0644 quickjs-libc.h %{buildroot}%{_includedir}/quickjs/quickjs-libc.h

%check
%make_build test
./qjsc -o hello-rpm examples/hello.js
test "$(./hello-rpm)" = "Hello World"
rm -f hello-rpm
# gcc folds this literal out of the binary, so check the patched source.
grep -F -q '"%{_libdir}/quickjs"' qjsc.c
grep -F -q '%{upstream_date}' doc/quickjs.html
test -s doc/quickjs.pdf
test -s doc/quickjs.1
grep -q '^\.TH ' doc/quickjs.1

%clean
rm -f debugfiles.list debuglinks.list debugsourcefiles.list debugsources.list elfbins.list

%files
%license LICENSE
%doc Changelog
%doc doc/quickjs.html
%doc doc/quickjs.pdf
%doc doc/quickjs.1
%{_bindir}/qjs
%{_bindir}/qjsc

%files devel
%{_includedir}/quickjs/
%{_libdir}/quickjs/

%files doc
%doc doc/quickjs.texi

%changelog
* Wed Sep 23 2026 Packager - 2026.06.04-10
- Take Source0 from the GitHub codeload snapshot of %%{commit}

* Wed Sep 23 2026 Packager - 2026.06.04-9
- Unpack Source0 with %%setup instead of treating it as a git checkout

* Wed Sep 23 2026 Packager - 2026.06.04-8
- Build from the local quickjs git checkout named by Source0

* Wed Sep 23 2026 Packager - 2026.06.04-7
- Take Source0 from the GitHub codeload snapshot of %%{commit}

* Tue Sep 22 2026 Packager - 2026.06.04-6
- Generate a man page with pandoc and install it in %%{_docdir}/quickjs

* Tue Sep 22 2026 Packager - 2026.06.04-5
- Drop readme.txt from the main package
- Install the HTML and PDF manual in %%{_docdir}/quickjs

* Tue Sep 22 2026 Packager - 2026.06.04-4
- Do not run %%set_build_flags, and do not package /usr/lib/.build-id links

* Tue Sep 22 2026 Packager - 2026.06.04-3
- Build in the quickjs git checkout next to this spec

* Tue Sep 22 2026 Packager - 2026.06.04-2
- Build the HTML and PDF manual from doc/quickjs.texi

* Tue Sep 22 2026 Packager - 2026.06.04-1
- Initial package of QuickJS 2026-06-04
