%define debug_package %{nil}

Name:		dnscrypt-proxy
Version:	2.0.19
Release:	1%{?dist}
Summary:	A flexible DNS proxy, with support for encrypted DNS protocols
License:	ISC
URL:		https://github.com/jedisct1/%{name}

Source0:	%{url}/archive/%{version}.tar.gz
Source1:	%{name}.service

BuildRequires:	golang
BuildRequires:	git
BuildRequires:	systemd
%{?systemd_requires}


%description
A flexible DNS proxy, with support for encrypted DNS protocols

%prep
%setup -q

%build
mkdir build
ln -s vendor src
ln -rs %{name} src/
GOPATH=$PWD go build -ldflags="-s -w" -o build/%{name} %{name}

%install
install -D -m 755 build/%{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{name}/example-dnscrypt-proxy.toml %{buildroot}%{_sysconfdir}/%{name}/%{name}.toml

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%license LICENSE
%doc ChangeLog
%doc %{name}/example-*
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.toml
