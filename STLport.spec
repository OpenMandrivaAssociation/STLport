%define name	STLport
%define version	5.1.3
%define release	%mkrel 6

%define major 5.1
%define libname %mklibname %name %major
%define develname %mklibname %name -d

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
# Previous package had major 5.0, but was named libSTLport5 and
# contained libstlport.so.5 . So we have to obsolete it, I think.
# -AdamW 2007/07
Obsoletes: %{_lib}%{name}5

%description -n %libname
STLport is a multiplatform STL implementation based on SGI STL.
This package contains the runtime library for STLport.

%package -n %develname
Summary: Complete C++ standard library header files and libraries
Group: Development/C++
Requires: %libname = %version
Provides: %name-devel = %version-%release
Obsoletes: %{_lib}%{name}5-devel

%description -n %develname
This package contains the headers that programmers will need to develop
applications which will use %{libname}.
STLport is a multiplatform STL implementation based on SGI STL. Complete
C++ standard library, including <complex> and SGI STL iostreams. If you
would like to use your code with STLport add
"-nostdinc++ -I/usr/include/stlport" when compile and -lstlport when
link (eg: gcc -nostdinc++ -I/usr/include/stlport x.cc -lstlport).

%prep
%setup -q

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
mkdir -p %buildroot%{_includedir}
cp -r lib/* $RPM_BUILD_ROOT%{_libdir}
cp -r stlport $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_includedir}/stlport/BC50
rm -rf $RPM_BUILD_ROOT%{_includedir}/stlport/old_hp

# the major is 5.1, so it really shouldn't install *.so.5. This would
# break stuff if it went to major 5.2 in future. -AdamW 2007/07
rm -f $RPM_BUILD_ROOT%{_libdir}/*.so.5

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
[ $RPM_BUILD_ROOT != "/" ] && rm -rf $RPM_BUILD_ROOT

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %develname
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/stlport
