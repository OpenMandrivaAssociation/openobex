%define major 1
%define libname %mklibname openobex %{major}
%define develname %mklibname openobex -d

Summary: 	Library for using OBEX
Name: 		openobex
Version: 	1.5
Release: 	%mkrel 8
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


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5-6mdv2011.0
+ Revision: 666958
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5-5mdv2011.0
+ Revision: 607021
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5-4mdv2010.1
+ Revision: 523541
- rebuilt for 2010.1

* Mon Sep 14 2009 Götz Waschk <waschk@mandriva.org> 1.5-3mdv2010.0
+ Revision: 439799
- rebuild for new libusb

* Tue Sep 08 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.5-2mdv2010.0
+ Revision: 433544
- remove glib-devel BuildRequires, glib support is unconditionally disabled in the upstream tarball
- rebuild

* Wed Feb 18 2009 Emmanuel Andry <eandry@mandriva.org> 1.5-1mdv2009.1
+ Revision: 342630
- New version 1.5
- use devel library policy

* Sun Nov 09 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.4-1mdv2009.1
+ Revision: 301340
- Update to openObex 1.4
- "After two years of development finally we have a new version of OpenOBEX
  This version comes with better support for Windows based system and fixes
  all pending bugs. Please test it properly to ensure that nothing broke."

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3-7mdv2009.0
+ Revision: 232944
- fix linkage (P1)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.3-5mdv2008.1
+ Revision: 171010
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Sat Jan 12 2008 Emmanuel Andry <eandry@mandriva.org> 1.3-4mdv2008.1
+ Revision: 149809
- add patch from fedora to add ipv6 support

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Apr 27 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.3-3mdv2008.0
+ Revision: 18729
- force explicit dependency on bluez-devel in openobex-devel


* Fri Jan 19 2007 Frederic Crozat <fcrozat@mandriva.com> 1.3-2mdv2007.0
+ Revision: 110576
-Fix libification
-Add conflicts to upgrade from previous releases

  + Buchan Milne <bgmilne@mandriva.org>
    - buildrequire libusb-devel

* Tue Oct 31 2006 Stefan van der Eijk <stefan@mandriva.org> 1.3-1mdv2007.1
+ Revision: 74231
- 1.3
- Import openobex

* Sun Sep 03 2006 Stefan van der Eijk <stefan@mandriva.org> 1.2-3
- rebuild for libbluetooth.so.2

* Sat Jun 17 2006 Austin Acton <austin@mandriva.org> 1.2-1mdv2007.0
- Rebuild

* Mon Mar 27 2006 Stefan van der Eijk <stefan@eijk.nu> 1.2-1mdk
- 1.2
- change incorrect major
- add apps & ircp subpackages

* Fri Feb 10 2006 Götz Waschk <waschk@mandriva.org> 1.1-2mdk
- drop obsoletes
- fix provides

* Sat Feb 04 2006 Stefan van der Eijk <stefan@eijk.nu> 1.1-1mdk
- 1.1

* Sat Dec 24 2005 Stefan van der Eijk <stefan@eijk.nu> 1.0.1-5mdk
- %%mkrel

* Tue Oct 19 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.1-4mdk
- fix deps

* Sat May 01 2004 Austin Acton <austin@mandrake.org> 1.0.1-3mdk
- obsolete libname1 (Arnaud de Lorbeau)

* Tue Apr 06 2004 Austin Acton <austin@mandrake.org> 1.0.1-2mdk
- make sure headers go in their own directory (makeinstall_std)
- fancify spec
- move config utility to devel package
- fix major versioning

