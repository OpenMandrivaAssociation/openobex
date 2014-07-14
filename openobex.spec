%define major	2
%define libname %mklibname openobex %{major}
%define devname %mklibname openobex -d

Summary: 	Library for using OBEX
Name: 		openobex
Version: 	1.6
Release: 	7
License: 	LGPLv2.1
Group: 		System/Libraries
Url:		http://openobex.sourceforge.net/
Source0: 	http://netcologne.dl.sourceforge.net/project/openobex/openobex/%{version}/%{name}-%{version}-Source.tar.gz
Patch2:		openobex-automake-1.13.patch

BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(libusb-1.0)

%description
Open OBEX shared c-library

%package	apps
Summary:	Apps that come with the Open OBEX c-library
Group:		Communications

%description	apps
These are the apps that come with the Open OBEX c-library. These are
not meant to be more than test-programs to look at if you want to see
how use the library itself.

%package	ircp
Summary:	Used to "beam" files or whole directories
Group:		Communications

%description	ircp
Ircp is used to "beam" files or whole directories to/from Linux, Windows.

%package -n	%{libname}
Summary:	Library for using OBEX
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
Open OBEX shared c-library

%package -n	%{devname}
Summary:	Library for using OBEX
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel  = %{version}-%{release}

%description -n %{devname}
Open OBEX shared c-library

%prep
%setup -qn %{name}-%{version}-Source
%patch2 -p1 -b .am113~

%build
autoreconf -fis
%configure2_5x \
	--disable-static \
	--enable-apps
%make

%install
%makeinstall_std

# since our old packages will look for headers in /usr/include
ln -s openobex/obex.h %{buildroot}/%_includedir/obex.h
ln -s openobex/obex_const.h %{buildroot}/%_includedir/obex_const.h

%files apps
%{_bindir}/obex_find
%{_bindir}/irobex_palm3
%{_bindir}/irxfer
%{_bindir}/obex_tcp
%{_bindir}/obex_test
%{_sbindir}/obex-check-device
%{_mandir}/man1/*
%exclude %{_mandir}/man1/ircp.1*

%files ircp
%{_bindir}/ircp
%{_mandir}/man1/ircp.1*

%files -n %{libname}
%{_libdir}/libopenobex.so.%{major}*

%files -n %{devname}
%doc COPYING AUTHORS ChangeLog README
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/openobex.pc

