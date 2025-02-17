#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Wrappers to build Python packages using PEP 517 hooks
Summary(pl.UTF-8):	Opakowanie do budowania pakietów Pythona przy użyciu uchwytów PEP 517
Name:		python3-pep517
Version:	0.13.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pep517/
Source0:	https://files.pythonhosted.org/packages/source/p/pep517/pep517-%{version}.tar.gz
# Source0-md5:	fcf81721b503ebaf63c8dccc576191f4
URL:		https://pypi.org/project/pep517/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.6
%if %{with tests}
BuildRequires:	python3-pip
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-toml
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata
BuildRequires:	python3-zipp
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-toml
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PEP 517 specifies a standard API for systems which build Python
packages.

%description -l pl.UTF-8
PEP 517 określa standardowe API dla systemów budujących pakiety
Pythona.

%package apidocs
Summary:	API documentation for Python pep517 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pep517
Group:		Documentation

%description apidocs
API documentation for Python pep517 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pep517.

%prep
%setup -q -n pep517-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_flake8" \
%{__python3} -m pytest tests -k 'not test_classic_package and not test_meta_for_this_package and not test_meta_output'
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{py3_sitescriptdir}/pep517
%{py3_sitescriptdir}/pep517-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
