%define major 5.2
%define libname %mklibname %name %major
%define develname %mklibname %name -d

Summary:	Complete C++ standard library header files and libraries
Name:		STLport
Version:	5.2.1
Release:	%mkrel 1
License:	GPL
Group:		Development/C++
URL:		http://www.stlport.org/
Source0:	http://www.stlport.com/archive/STLport-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
STLport is a multiplatform STL implementation based on SGI STL.
This package contains the runtime library for STLport.

%package -n	%{libname}
Summary:	Complete C++ standard library
Group:		Development/C++
Provides:	lib%{name} = %version-%release

%description -n	%{libname}
STLport is a multiplatform STL implementation based on SGI STL.
This package contains the runtime library for STLport.

%package -n	%{develname}
Summary:	Complete C++ standard library header files and libraries
Group:		Development/C++
Requires:	%{libname} >= %version
Provides:	%name-devel = %version-%release
Obsoletes:	%{_lib}%{name}5-devel

%description -n	%{develname}
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
%serverbuild

pushd build/lib
%make -f gcc.mak all CC="gcc" CXX="g++" CXXFLAGS="$CXXFLAGS -fPIC"
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}

pushd build/lib
%make -f gcc.mak install \
    CC="gcc" CXX="g++" EXTRA_CXXFLAGS="$RPM_OPT_FLAGS" \
    BASE_INSTALL_DIR=%{buildroot}%{_prefix} \
    INSTALL_LIB_DIR=%{buildroot}%{_libdir} \
    INSTALL_LIB_DIR_DBG=%{buildroot}%{_libdir} \
    INSTALL_LIB_DIR_STLDBG=%{buildroot}%{_libdir} \
    INSTALL_HDR_DIR=%{buildroot}%{_includedir}
popd

# the major is 5.1, so it really shouldn't install *.so.5. This would
# break stuff if it went to major 5.2 in future. -AdamW 2007/07
rm -f %{buildroot}%{_libdir}/*.so.5

# fix linkage
ln -snf libstlportg.so.%{version} %{buildroot}%{_libdir}/libstlportg.so.%{major}
ln -snf libstlportg.so.%{major} %{buildroot}%{_libdir}/libstlportg.so

ln -snf libstlport.so.%{version} %{buildroot}%{_libdir}/libstlport.so.%{major}
ln -snf libstlport.so.%{major} %{buildroot}%{_libdir}/libstlport.so

ln -snf libstlportstlg.so.%{version} %{buildroot}%{_libdir}/libstlportstlg.so.%{major}
ln -snf libstlportstlg.so.%{major} %{buildroot}%{_libdir}/libstlportstlg.so


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/stlport
