%define name	STLport
%define version	5.0.1
%define release	%mkrel 2

%define major 5
%define libname %mklibname %name %major

Summary:	Complete C++ standard library header files and libraries
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.stlport.org/
License:	GPL
Group:		Development/C++
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

BuildRequires:	gcc >= 3.2-0.3mdk

Source: http://www.stlport.com/archive/STLport-%{version}.tar.bz2

%description
STLport is a multiplatform STL implementation based on SGI STL.
This package contains the runtime library for STLport.

%package -n %libname
Summary: Complete C++ standard library
Group: Development/C++
Provides: lib%{name} = %version-%release

%description -n %libname
This package includes STLport library.

%package -n %libname-devel
Summary: Complete C++ standard library header files and libraries
Group: Development/C++
Requires: %libname = %version
Provides: %name-devel = %version-%release
Provides: lib%name-devel = %version-%release

%description -n %libname-devel
This package contains the headers that programmers will need to develop
applications which will use %{lib_name}.
STLport is a multiplatform STL implementation based on SGI STL. Complete
C++ standard library, including <complex> and SGI STL iostreams. If you
would like to use your code with STLport add
"-nostdinc++ -I/usr/include/stlport" when compile and -lstlport when
link (eg: gcc -nostdinc++ -I/usr/include/stlport x.cc -lstlport).

%prep
%setup -q -n STLport-%{version}

%build
(
cd build/lib
%make -f gcc.mak all \
  CC="gcc" CXX="g++" EXTRA_CXXFLAGS="$RPM_OPT_FLAGS" \
  INSTALLDIR_INC=%_includedir/stlport%{major} \
  INSTALLDIR_LIB=%_libdir
)

%install
[ $RPM_BUILD_ROOT != "/" ] && rm -rf $RPM_BUILD_ROOT

(cd build/lib
%make -f gcc.mak install \
  CC="gcc" CXX="g++" EXTRA_CXXFLAGS="$RPM_OPT_FLAGS" \
  INSTALLDIR_INC=%buildroot%_includedir/stlport%{major} \
  INSTALLDIR_LIB=%buildroot%_libdir
)
mkdir -p %buildroot%{_libdir}
cp -r lib/* $RPM_BUILD_ROOT%{_libdir}
cp -r stlport $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_includedir}/stlport/BC50
rm -rf $RPM_BUILD_ROOT%{_includedir}/stlport/old_hp



%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%clean
[ $RPM_BUILD_ROOT != "/" ] && rm -rf $RPM_BUILD_ROOT

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %libname-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
