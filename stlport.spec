%define major 5
%define libname %mklibname stlport %major
%define libname_devel %mklibname -d stlport

Name:          stlport
Version:       5.2.1
Release:       %mkrel 1
Summary:       Multiplatform C++ Standard Library (STL implementation)
Group:         System/Libraries
License:       GPL
Url:           http://www.stlport.org/
Source0:       http://sourceforge.net/projects/stlport/files/STLport/STLport-5.2.1/STLport-5.2.1.tar.gz

BuildRequires: boost-devel
BuildRequires: libstdc++-devel
BuildRequires: libstdc++-static-devel


%description
STLport is a multiplatform ANSI C++ Standard Library implementation. It is
free, open-source product, featuring the following:

-  Advanced techniques and optimizations for maximum efficiency
-  Exception safety and thread safety
-  Important extensions - hash tables, singly-linked list, rope

%package -n %libname
Summary:       %{name} - Complete C++ standard library
Group:         System/Libraries
Provides:      %{name} = %version

%description -n %libname
STLport is a multiplatform STL implementation based on SGI STL.
This package contains the runtime library for STLport.

%package -n %libname_devel
Group:         Development/C++
Summary:       Devel package for %{name}
Requires:      %libname = %{version}-%{release}
Provides:      %{name}-devel = %{version}

%description -n %libname_devel
STLport is a multiplatform STL implementation based on SGI STL. Complete   
C++ standard library, including <complex> and SGI STL iostreams.

This package contains static libraries and header files need for development.

%prep
%setup -q -n STLport-%{version}

%build
# Unknown configuration option '--build=i586-mageia-linux-gnu'
./configure \
  --prefix=%_prefix \
  --bindir=%_bindir \
  --libdir=%_libdir \
  --includedir=%_includedir \
  --use-compiler-family=gcc \
  --with-system-boost \
  --without-debug
%make

%install
%makeinstall_std

rm -rf %{buildroot}%{buildroot}
#cd %{buildroot}%_includedir/stlport
#ln -s . ext

%files -n %libname
%_libdir/libstlport.so.%{major}*
%doc README

%files -n %libname_devel
%dir %_includedir/stlport
%_includedir/stlport/*
%_libdir/libstlport.so
%doc INSTALL* etc/ChangeLog* etc/*.txt etc/*.gif doc/FAQ doc/README.utf8 doc/*.txt
