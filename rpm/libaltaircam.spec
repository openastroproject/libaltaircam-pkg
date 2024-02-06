%define debug_package %{nil}

Name:           libaltaircam
Version:        1.55.24621
Release:        0
Summary:        Altair camera support library
License:	GPLv2+
Prefix:         %{_prefix}
Provides:       libaltaircam = %{version}-%{release}
Obsoletes:      libaltaircam < 1.55.24621
Source:         libaltaircam-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libaltaircam is a user-space driver for Altair astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libaltaircam-devel = %{version}-%{release}
Obsoletes:      libaltaircam-devel < 1.55.24621

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libaltaircam.pc.in > libaltaircam.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}/etc/udev/rules.d
mkdir -p %{buildroot}%{_includedir}

case %{_arch} in
  x86_64)
    cp x64/libaltaircam.bin %{buildroot}%{_libdir}/libaltaircam.so.%{version}
		cp altaircam.h %{buildroot}%{_includedir}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp 70-altair-cameras.rules %{buildroot}/etc/udev/rules.d

%post
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%files
%{_libdir}/*.so.*
%{_sysconfdir}/udev/rules.d/*.rules

%files devel
%{_includedir}/altaircam.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Feb 6 2024 James Fidell <james@openastroproject.org> - 1.55.24621
- Updates from upstream
* Fri Jan 5 2024 James Fidell <james@openastroproject.org> - 1.55.24239
- Updates from upstream
* Fri Dec 15 2023 James Fidell <james@openastroproject.org> - 1.54.23926
- Updates from upstream
* Wed Jun 30 2021 James Fidell <james@openastroproject.org> - 1.49.18914
- Updates from upstream
* Fri Sep 4 2020 James Fidell <james@openastroproject.org> - 1.47.17497
- Updates from upstream
* Sat Nov 23 2019 James Fidell <james@openastroproject.org> - 1.39.15364
- Updates from upstream
* Sun Jan 13 2019 James Fidell <james@openastroproject.org> - 1.32.13483
- Updates from upstream
* Sun Jul 30 2017 James Fidell <james@openastroproject.org> - 1.6.5660-0
- Initial RPM release
