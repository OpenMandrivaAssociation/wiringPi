%define major 2
%define libname %mklibname wiringPi %{major}
%define devname %mklibname -d wiringPi
%define devlibname %mklibname wiringPiDev %{major}

Summary:	GPIO Interface Library for the Raspberry Pi
Name:		wiringPi
Version:	2.46
Release:	1
URL:		http://wiringpi.com/
Source0:	wiringPi-2.46.tar.gz
License:	LGPLv3
Group:		System/Libraries
# Compiles everywhere, but is probably useful only on Pis...
#ExclusiveArch:	%{arm} %{armx}
# Let's allow building it everywhere though, just in case someone
# adds support for Intel boards

%description
WiringPi is a PIN based GPIO access library written in C for the BCM2835,
BCM2836 and BCM2837 SoC devices used in all Raspberry Pi versions.

It’s released under the GNU LGPLv3 license and is usable from C, C++ and RTB
(BASIC) as well as many other languages with suitable wrappers.

It’s designed to be familiar to people who have used the Arduino “wiring”
system and is intended for use by experienced C/C++ programmers.
It is not a newbie learning tool.

%package -n %{libname}
Summary:	GPIO Interface Library for the Raspberry Pi
Group:		System/Libraries

%description -n %{libname}
GPIO Interface Library for the Raspberry Pi

%package -n %{devlibname}
Summary:	GPIO Interface Library for the Raspberry Pi
Group:		System/Libraries

%description -n %{devlibname}
GPIO Interface Library for the Raspberry Pi

%package -n %{devname}
Summary:	Development files for WiringPi, the Raspberry Pi GPIO library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{devlibname} = %{EVRD}

%description -n	%{devname}
Development files for WiringPi, the Raspberry Pi GPIO library

%prep
%autosetup -p1
find . -name Makefile |xargs sed -i -e 's,chown,#chown,'
find . -name Makefile |xargs sed -i -e 's,/usr/local/,$(DESTDIR)/,g'
%if "%{_lib}" != "lib"
find . -name Makefile |xargs sed -i -e 's,/lib/,/%{_lib}/,g'
%endif

%build
find . -name Makefile |while read r; do
	[ "$r" = "./pins/Makefile" ] && continue
	cd $(dirname $r)
	%make_build PREFIX=/ DESTDIR=%{_prefix}
	cd -
done

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}
find . -name Makefile |while read r; do
	[ "$r" = "./pins/Makefile" ] && continue
	[ "$r" = "./examples/Gertboard/Makefile" ] && continue
	[ "$r" = "./examples/PiFace/Makefile" ] && continue
	[ "$r" = "./examples/q2w/Makefile" ] && continue
	[ "$r" = "./examples/Makefile" ] && continue

	cd $(dirname $r)
	%make_install PREFIX=/ DESTDIR=%{buildroot}%{_prefix} LDCONFIG=true
	cd -
done

# Fix symlink pointing to build root
ln -sf libwiringPi.so.%{version} %{buildroot}%{_libdir}/libwiringPi.so
ln -sf libwiringPiDev.so.%{version} %{buildroot}%{_libdir}/libwiringPiDev.so

%files
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/libwiringPi.so.%{major}*

%files -n %{devlibname}
%{_libdir}/libwiringPiDev.so.%{major}*

%files -n %{devname}
%{_libdir}/lib*.so
%{_includedir}/*.h
