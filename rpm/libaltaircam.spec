%define debug_package %{nil}

Name:           libaltaircam
Version:        1.32.13483
Release:        0
Summary:        Altair camera support library
License:	GPLv2+
Prefix:         %{_prefix}
Provides:       libaltaircam = %{version}-%{release}
Obsoletes:      libaltaircam < 1.32.13483
Source:         libaltaircam-%{version}.tar.gz
Patch0:         pkg-config.patch

%description
libaltaircam is a user-space driver for Altair astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libaltaircam-devel = %{version}-%{release}
Obsoletes:      libaltaircam-devel < 1.32.13483

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libaltaircam.pc.in > libaltaircam.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig

case %{_arch} in
  x86_64)
    cp linux/x64/libaltaircam.so %{buildroot}%{_libdir}/libaltaircam.so.%{version}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp *.pc %{buildroot}%{_libdir}/pkgconfig

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/*.so.*

%changelog
* Sun Jan 13 2019 James Fidell <james@openastroproject.org> - 1.32.13483
- Initial RPM release

