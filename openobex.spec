%define major 1
%define libname %mklibname openobex %{major}
%define develname %mklibname openobex -d

Summary: 	Library for using OBEX
Name: 		openobex
Version: 	1.5
Release: 	%mkrel 4
License: 	LGPL
Group: 		System/Libraries
URL:		http://openobex.sourceforge.net/
Source: 	http://www.kernel.org/pub/linux/bluetooth/openobex-%{version}.tar.gz
Patch0:		openobex-1.3-ipv6.patch
Patch1:		openobex-linkage_fix.diff
BuildRequires:	bluez-devel
BuildRequires:	libusb-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Open OBEX shared c-library

%package -n %{libname}
Summary: Library for using OBEX
Group: System/Libraries
Provides: lib%{name} = %version-%release
Provides: %{name} = %version-%release
Conflicts: %{_lib}%{name}1.3
Conflicts: %{_lib}%{name}1.2
Conflicts: %{_lib}%{name}1.1

%description -n %{libname}
Open OBEX shared c-library

%package -n %{develname}
Summary: Library for using OBEX
Group: Development/C
Provides: lib%{name}-devel = %version-%release
Provides: %{name}-devel  = %version-%release
Requires: %{libname} = %{version}
Requires:   bluez-devel
Conflicts: %{_lib}%{name}1.3-devel
Conflicts: %{_lib}%{name}1.2-devel
Conflicts: %{_lib}%{name}1.1-devel
Obsoletes: %{_lib}%{name}1-devel

%description -n %{develname}
Open OBEX shared c-library

%package apps
Summary: Apps that come with the Open OBEX c-library
Group: Communications

%description apps
These are the apps that come with the Open OBEX c-library. These are
not meant to be more than test-programs to look at if you want to see
how use the library itself.

%package ircp
Summary: Used to "beam" files or whole directories
Group: Communications
Obsoletes: ircp
Provides: ircp

%description ircp
Ircp is used to "beam" files or whole directories to/from Linux, Windows.

%prep

%setup -q
#%patch0 -p1
#%patch1 -p0

%build
autoreconf -fis
%configure \
	--enable-apps
%make

%install
rm -rf %{buildroot}

%makeinstall_std

# since our old packages will look for headers in /usr/include
ln -s openobex/obex.h %{buildroot}/%_includedir/obex.h
ln -s openobex/obex_const.h %{buildroot}/%_includedir/obex_const.h

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-, root, root)
%doc COPYING
%{_libdir}/libopenobex.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%doc AUTHORS ChangeLog README
%{_libdir}/pkgconfig/openobex.pc
%{_includedir}/*
%{_libdir}/*a
%{_libdir}/lib*.so

%files apps
%defattr(-, root, root)
%{_bindir}/irobex_palm3
%{_bindir}/irxfer
%{_bindir}/obex_tcp
%{_bindir}/obex_test

%files ircp
%defattr(-, root, root)
%{_bindir}/ircp
