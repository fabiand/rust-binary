
%global rust_version 0.12.0
%global staticprefix rust-%{rust_version}-x86_64-unknown-linux-gnu

%global debug_package %{nil}
# Do not check any files in docdir for requires
%global __requires_exclude_from ^%{_bindir}/.*$

Name:           rust-binary
Version:        %{rust_version}
Release:        1%{?dist}
Summary:        The Rust Programming Language (official static build)

License:        ASL 2.0, MIT
URL:            http://www.rust-lang.org
Source0:        http://static.rust-lang.org/dist/%{staticprefix}.tar.gz

ExclusiveArch:  x86_64


%description
This is a compiler for Rust, including standard libraries, tools and
documentation.
This package is wrapping the official binary builds.


%prep
%setup -q -n "%{staticprefix}"


%build
# Nothing

%install
./install.sh \
    --prefix=%{buildroot}/%{_prefix} --libdir=%{buildroot}/%{_libdir} \
    --disable-verify

# Create ld.so.conf file
mkdir -p %{buildroot}/%{_sysconfdir}/ld.so.conf.d
cat <<EOF | tee /%{buildroot}/%{_sysconfdir}/ld.so.conf.d/rust-%{_target_cpu}.conf
%{_libdir}/rustlib/
%{_libdir}/rustlib/%{_target_cpu}-unknown-linux-gnu/lib/
EOF

# Remove buildroot from manifest
sed -i "s#^%{buildroot}##" %{buildroot}/%{_libdir}/rustlib/manifest


%post -p /sbin/ldconfig


%files
%doc COPYRIGHT LICENSE-APACHE LICENSE-MIT README.md
%{_sysconfdir}/ld.so.conf.d/rust-*.conf
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_libdir}/lib*
%{_libdir}/rustlib/*
%{_datadir}/man/*


%changelog
* Sun Dec 28 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0

* Sat Jul 05 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.11.0-1
- Initial package

