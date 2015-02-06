%define	major	5.2
%define	libname	%mklibname stlport %{major}
%define	oldname	%mklibname stlport 5
%define	devname	%mklibname -d stlport

Name:		STLport
Version:	5.2.1
Release:	3
Summary:	Multiplatform C++ Standard Library (STL implementation)
Group:		System/Libraries
License:	BSD
Url:		http://www.stlport.org/
Source0:	http://sourceforge.net/projects/stlport/files/STLport/STLport-5.2.1/STLport-5.2.1.tar.gz

BuildRequires:	boost-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libstdc++-static-devel


%description
STLport is a multiplatform ANSI C++ Standard Library implementation. It is
free, open-source product, featuring the following:

-  Advanced techniques and optimizations for maximum efficiency
-  Exception safety and thread safety
-  Important extensions - hash tables, singly-linked list, rope

%package -n	%{libname}
Summary:	%{name} - Complete C++ standard library
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
STLport is a multiplatform STL implementation based on SGI STL.
This package contains the runtime library for STLport.

%package -n	%{devname}
Group:		Development/C++
Summary:	Devel package for %{name}
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
STLport is a multiplatform STL implementation based on SGI STL. Complete   
C++ standard library, including <complex> and SGI STL iostreams.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
# doesn't support --build=
./configure	--prefix=%{_prefix} \
		--bindir=%{_bindir} \
		--libdir=%{_libdir} \
		--includedir=%{_includedir} \
		--use-compiler-family=gcc \
		--with-system-boost \
		--without-debug
%global optflags %{optflags} -pthread -fexceptions -fPIC -fvisibility=hidden
%make CXXFLAGS="%{optflags} -fexceptions" CFLAGS="%{optflags}"

%install
%makeinstall_std
rm -rf %{buildroot}%{buildroot}

%files -n %{libname}
%{_libdir}/libstlport*.so.*
%doc README

%files -n %{devname}
%dir %{_includedir}/stlport
%{_includedir}/stlport/*
%{_libdir}/libstlport*.so
%doc README etc/ChangeLog* etc/*.txt etc/*.gif doc/FAQ doc/README.utf8 doc/*.txt
