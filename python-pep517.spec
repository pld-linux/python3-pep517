#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Wrappers to build Python packages using PEP 517 hooks
Summary(pl.UTF-8):	Opakowanie do budowania pakietów Pythona przy użyciu uchwytów PEP 517
Name:		python-pep517
Version:	0.10.0
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pep517/
Source0:	https://files.pythonhosted.org/packages/source/p/pep517/pep517-%{version}.tar.gz
# Source0-md5:	59b482ecdc9f9153bd3183e8d0da99ff
URL:		https://pypi.org/project/pep517/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-importlib_metadata
BuildRequires:	python-pip
BuildRequires:	python-pytest
BuildRequires:	python-pytest-flake8
BuildRequires:	python-toml
BuildRequires:	python-zipp
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
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
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-toml
BuildRequires:	sphinx-pdg-3
%endif
# replace with other requires if defined in setup.py
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PEP 517 specifies a standard API for systems which build Python
packages.

%description -l pl.UTF-8
PEP 517 określa standardowe API dla systemów budujących pakiety
Pythona.

%package -n python3-pep517
Summary:	Wrappers to build Python packages using PEP 517 hooks
Summary(pl.UTF-8):	Opakowanie do budowania pakietów Pythona przy użyciu uchwytów PEP 517
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-pep517
PEP 517 specifies a standard API for systems which build Python
packages.

%description -n python3-pep517 -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_flake8" \
%{__python} -m pytest tests -k 'not test_classic_package'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_flake8" \
%{__python3} -m pytest tests -k 'not test_classic_package and not test_meta_for_this_package and not test_meta_output'
%endif
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# _in_process.py is executed by filename
%py_postclean -x _in_process.py
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/pep517
%{py_sitescriptdir}/pep517-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pep517
%defattr(644,root,root,755)
# copy %doc from python2 package here
%{py3_sitescriptdir}/pep517
%{py3_sitescriptdir}/pep517-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
