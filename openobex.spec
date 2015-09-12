%define major	2
%define libname %mklibname openobex %{major}
%define devname %mklibname openobex -d

Summary: 	Library for using OBEX
Name: 		openobex
Version: 	1.7.1
Release: 	4
License: 	LGPLv2.1
Group: 		System/Libraries
Url:		http://openobex.sourceforge.net/
Source0: 	http://netcologne.dl.sourceforge.net/project/openobex/openobex/%{version}/%{name}-%{version}-Source.tar.gz
Patch0:		openobex-apps-flush.patch
Patch1:		openobex-1.7-obex_push.patch

BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
BuildRequires:	cmake
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
%apply_patches

%build
%cmake  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
 -DCMAKE_SKIP_RPATH=YES \
 -DCMAKE_VERBOSE_MAKEFILE=YES \
 -DCMAKE_INSTALL_UDEVRULESDIR=%_udevrulesdir

%make
%make openobex-apps

%install
%makeinstall_std -C build

# since our old packages will look for headers in /usr/include
ln -s openobex/obex.h %{buildroot}/%_includedir/obex.h
ln -s openobex/obex_const.h %{buildroot}/%_includedir/obex_const.h

# don't ship obex_test program, that is for testing purposes only
# and has some problems (multiple buffer overflows etc.)
rm -f %{buildroot}%{_bindir}/obex_test
rm -f %{buildroot}%{_mandir}/man1/obex_test.1*


%files apps
%{_bindir}/irobex_palm3
%{_bindir}/irxfer
%{_bindir}/obex_find
%{_bindir}/obex_push
%{_sbindir}/obex-check-device
%{_bindir}/obex_tcp
%{_mandir}/*/irobex_palm3.*
%{_mandir}/*/irxfer.*
%{_mandir}/*/obex_find.*
%{_mandir}/*/obex_tcp.*
%{_mandir}/*/obex_push.*
%{_udevrulesdir}/60-openobex.rules

%files ircp
%{_bindir}/ircp
%{_mandir}/man1/ircp.1*

%files -n %{libname}
%{_libdir}/libopenobex.so.%{major}*
%{_libdir}/libopenobex.so.1*

%files -n %{devname}
%doc COPYING AUTHORS ChangeLog README
%{_includedir}/*
%{_libdir}/cmake/OpenObex-%{version}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/openobex.pc
