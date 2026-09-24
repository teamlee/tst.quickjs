%global upstream_date 2026-06-04
%global commit 04be246001599f5995fa2f2d8c91a0f198d3f34c
# Documentation only. Do not add debuginfo packages.
%global debug_package %{nil}
%global _build_id_links none

Name:           quickjs-doc
Version:        2026.06.04
Release:        1%{?dist}
Summary:        QuickJS manual

License:        MIT
URL:            https://github.com/bellard/quickjs
Source0:        https://codeload.github.com/bellard/quickjs/tar.gz/%{commit}
BuildArch:      noarch

# HTML via makeinfo (texinfo); PDF via texi2pdf (texinfo-tex).
BuildRequires:  make
BuildRequires:  texinfo
BuildRequires:  texinfo-tex
# Man page from the generated HTML. Pandoc does not read Texinfo.
BuildRequires:  pandoc

%description
HTML, PDF, Texinfo, and man-page forms of the QuickJS manual.

%prep
# The codeload archive unpacks to quickjs-<full commit>, not %{name}.
%setup -q -n quickjs-%{commit}

%build
# A checkout may already contain a manual. Drop it so this build
# produces doc/quickjs.html and doc/quickjs.pdf from doc/quickjs.texi.
rm -f doc/quickjs.html doc/quickjs.html.pre doc/quickjs.pdf doc/version.texi doc/quickjs.1
%make_build build_doc
# Pandoc has no Texinfo reader, and texi2any --docbook rejects this
# manual. The upstream manual is one document, so it becomes one
# section 1 page. There are no section 2–5 pages to package.
pandoc -f html -t man -s \
  -M title=quickjs \
  -M section=1 \
  -M header="QuickJS Javascript Engine" \
  -o doc/quickjs.1 doc/quickjs.html

%install
install -D -p -m 0644 doc/quickjs.html %{buildroot}%{_pkgdocdir}/quickjs.html
install -D -p -m 0644 doc/quickjs.pdf %{buildroot}%{_pkgdocdir}/quickjs.pdf
install -D -p -m 0644 doc/quickjs.texi %{buildroot}%{_pkgdocdir}/quickjs.texi
install -D -p -m 0644 doc/quickjs.1 %{buildroot}%{_mandir}/man1/quickjs.1

%check
grep -F -q '%{upstream_date}' doc/quickjs.html
test -s doc/quickjs.pdf
grep -q '^\.TH ' doc/quickjs.1

%files
%{_pkgdocdir}/quickjs.html
%{_pkgdocdir}/quickjs.pdf
%{_pkgdocdir}/quickjs.texi
%{_mandir}/man1/quickjs.1*

%changelog
* Thu Sep 24 2026 Packager - 2026.06.04-1
- Package the QuickJS HTML manual, PDF manual, Texinfo source, and man page
