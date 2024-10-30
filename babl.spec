#
# Conditional build:
%bcond_without	apidocs		# gi-docgen API documentation
%bcond_without	static_libs	# static library
%bcond_with	mmx		# MMX instructions
%bcond_with	sse		# SSE instructions
%bcond_with	sse2		# SSE2 instructions in CIE,two-table,ycbcr modules, sse2-* modules
# sse4.1, avx2, f16c are optional (in separate modules)
# sse2 is runtime-detected, but whole files are compiled with -msse2, so it's not optional
#
%ifarch pentium2 pentium3 pentium4 athlon %{x8664} x32
%define		with_mmx	1
%endif
%ifarch pentium3 pentium4 %{x8664} x32
%define		with_sse	1
%endif
%ifarch pentium4 %{x8664} x32
%define		with_sse2	1
%endif
Summary:	Library for pixel-format agnosticism
Summary(pl.UTF-8):	Biblioteka niezależności od formatu piksela
Name:		babl
Version:	0.1.110
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	https://download.gimp.org/pub/babl/0.1/%{name}-%{version}.tar.xz
# Source0-md5:	647708858d0c217579dec462b5f202a2
URL:		https://www.gegl.org/babl/
BuildRequires:	gobject-introspection-devel >= 1.32.0
BuildRequires:	lcms2-devel >= 2.8
BuildRequires:	meson >= 0.55.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.20.0
BuildRequires:	xz
%{?with_mmx:Requires:	cpuinfo(mmx)}
%{?with_sse:Requires:	cpuinfo(sse)}
%{?with_sse:Requires:	cpuinfo(sse2)}
Requires:	lcms2 >= 2.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Babl is a dynamic, any to any, pixel format conversion library. It
provides conversions between the myriad of buffer types images can be
stored in. Babl doesn't only help with existing pixel formats, but
also facilitates creation of new and uncommon ones.

%description -l pl.UTF-8
Babl to biblioteka dynamicznych przekształceń między dowolnymi
formatami pikseli. Udostępnia konwersje między wieloma różnymi typami
buforów obrazów. Babl nie tylko pomaga przy istniejących formatach
pikseli, ale także ułatwia tworzenie nowych i niestandardowych.

%package devel
Summary:	Header files for babl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki babl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lcms2-devel >= 2.8

%description devel
Header files for babl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki babl.

%package static
Summary:	Static babl library
Summary(pl.UTF-8):	Statyczna biblioteka babl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static babl library.

%description static -l pl.UTF-8
Statyczna biblioteka babl.

%package -n vala-babl
Summary:	Vala API for babl library
Summary(pl.UTF-8):	API języka Vala dla biblioteki babl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.20.0
BuildArch:	noarch

%description -n vala-babl
Vala API for babl library.

%description -n vala-babl -l pl.UTF-8
API języka Vala dla biblioteki babl.

%package apidocs
Summary:	API documentation for babl library
Summary(pl.UTF-8):	Dokumentacja API biblioteki babl
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for babl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki babl.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_mmx:-Denable-mmx=false} \
	%{!?with_sse:-Denable-sse=false} \
	%{!?with_sse2:-Denable-sse2=false} \
	%{!?with_apidocs:-Dgi-docgen=disabled}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/babl-0.1 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS TODO
%attr(755,root,root) %{_bindir}/babl
%attr(755,root,root) %{_libdir}/libbabl-0.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbabl-0.1.so.0
%{_libdir}/girepository-1.0/Babl-0.1.typelib
%dir %{_libdir}/babl-0.1
%attr(755,root,root) %{_libdir}/babl-0.1/*.so

%files devel
%defattr(644,root,root,755)
%doc docs/{*.html,*.css}
%attr(755,root,root) %{_libdir}/libbabl-0.1.so
%{_includedir}/babl-0.1
%{_datadir}/gir-1.0/Babl-0.1.gir
%{_pkgconfigdir}/babl-0.1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbabl-0.1.a
%endif

%files -n vala-babl
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/babl-0.1.deps
%{_datadir}/vala/vapi/babl-0.1.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/babl-0.1
%endif
