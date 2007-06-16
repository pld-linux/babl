Summary:	Library for pixel-format agnosticism
Summary(pl.UTF-8):	Biblioteka niezależności od formatu piksela
Name:		babl
Version:	0.0.14
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	ftp://ftp.gtk.org/pub/babl/0.0/%{name}-%{version}.tar.bz2
# Source0-md5:	c8274d0a2686f7f59e979313bd8e78fe
Patch0:		%{name}-as-needed.patch
URL:		http://www.gegl.org/babl/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	libtool
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

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libbabl-0.0.so.*.*.*
%dir %{_libdir}/babl-0.0
%attr(755,root,root) %{_libdir}/babl-0.0/*.so

%files devel
%defattr(644,root,root,755)
%doc docs/{*.html,*.css}
%attr(755,root,root) %{_libdir}/libbabl-0.0.so
%{_libdir}/libbabl-0.0.la
%{_includedir}/babl-0.0
%{_pkgconfigdir}/babl.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libbabl-0.0.a
