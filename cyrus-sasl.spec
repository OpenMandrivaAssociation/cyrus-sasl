%define major 2
%define libname %mklibname sasl %{major}
%define devname %mklibname sasl -d
%define sasl2_db_filename /var/lib/sasl2/sasl.db

%if %{cross_compiling}
# Work around libtool being a mess that can't
# handle spaces inside "$CC"
%define prefer_gcc 1
# gcc is more picky than clang about aliasing
%global optflags %{optflags} -fno-strict-aliasing
%endif

%define _disable_rebuild_configure 1

%bcond_with bootstrap
%if %{with bootstrap}
%bcond_with ldap
%else
%bcond_without ldap
%endif
%bcond_without krb5
%bcond_without mysql
%bcond_with srp
%bcond_without pgsql
%bcond_without sqlite3
%define SRPSTR %{with srp:en}%{!with srp:dis}abled
%define MYSQLSTR %{with mysql:en}%{!with mysql:dis}abled
%define PGSQLSTR %{with pgsql:en}%{!with pgsql:dis}enabled
%define SQLITE3STR %{with sqlite3:en}%{!with sqlite3:dis}enabled
%define LDAPSTR %{with ldap:en}%{!with ldap:dis}enabled

Summary:	The Simple Authentication and Security Layer
Name:		cyrus-sasl
Version:	2.1.28
Release:	4
License:	BSD-style
Group:		System/Libraries
Url:		https://cyrusimap.org/
# git clone https://github.com/cyrusimap/cyrus-sasl.git
# git archive --format=tar --prefix cyrus-sasl-2.1.27-$(date +%Y%m%d)/ HEAD | xz -vf9 > cyrus-sasl-2.1.27-$(date +%Y%m%d).tar.xz
Source0:	https://github.com/cyrusimap/cyrus-sasl/releases/download/cyrus-sasl-%{version}/cyrus-sasl-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	saslauthd.service
Source3:	saslauthd.sysconfig
Source4:	service.conf.example
Source7:	sasl-mechlist.c
Source8:	sasl-checkpass.c
# (tpg) patches from Debian
Patch10:	0001-Make-the-libsasl2-symbols-versioned.patch
Patch11:	0002-Use-etc-sasldb2-instead-of-.-sasldb-in-the-testsuite.patch
Patch12:	0003-Update-saslauthd.conf-location-in-documentation.patch
Patch13:	0004-Include-dbconverter-2-in-sbin_PROGRAMS-and-set-defau.patch
Patch14:	0005-Fixes-in-library-mutexes.patch
Patch15:	0006-Enable-autoconf-maintainer-mode.patch
Patch16:	0008-Don-t-overwrite-PIC-objects-with-non-PIC-variant.patch
Patch17:	0009-Look-for-generic-Berkeley-DB-first.patch
Patch18:	0010-Update-required-libraries-when-ld-as-needed-is-used.patch
#Patch19:	0013-Don-t-use-la-files-for-opening-plugins.patch
#Patch20:	0018-Temporary-multiarch-fixes.patch
Patch21:	0019-Add-reference-to-LDAP_SASLAUTHD-file-to-the-saslauth.patch
Patch22:	0022-Fix-keytab-option-for-MIT-Kerberos.patch
Patch23:	0025-Revert-upstream-soname-bump.patch
Patch24:	0027-properly-create-libsasl2.pc.patch
Patch25:	0032-Add-with_pgsql-include-postgresql-to-include-path.patch
#Patch26:	0017-Just-completely-remove-libobj-from-autotools-files.patch
#Patch27:	0018-We-need-to-look-for-compat-crypto.h-in-top_srcdir-as.patch

# (tpg) OpenMandriva patches
#Patch50:	cyrus-sasl-2.1.15-lib64.patch
#Patch51:	cyrus-sasl-2.1.27-20170616-kill-rpath.patch
# fix clashing function name
Patch52:	cyrus-sasl-2.1.27-dprintf_clash.patch
# Make it build with newer toolchains
Patch53:	cyrus-sasl-2.1.28-missing-includes.patch
BuildRequires:	groff
BuildRequires:	libtool
BuildRequires:	m4
BuildRequires:	gdbm-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	systemd-rpm-macros
BuildRequires:	rpm-helper
# 1.4.x is thread safe, which means we can disable sasl mutexes (see ./configure
# further below)
%if %{with krb5}
BuildRequires:	krb5-devel >= 1.4.1
BuildRequires:	pkgconfig(krb5-gssapi)
%endif
%if %{with mysql}
BuildRequires:	mysql-devel
%endif
%if %{with pgsql}
BuildRequires:	postgresql-devel
%endif
%if %{with sqlite3}
BuildRequires:	pkgconfig(sqlite3)
%endif
%if %{with ldap}
BuildRequires:	pkgconfig(ldap)
%endif
Requires(pre,post,preun):	rpm-helper

%description
SASL is the Simple Authentication and Security Layer,
a method for adding authentication support to connection-based protocols.
To use SASL, a protocol includes a command for identifying and authenticating
a user to a server and for optionally negotiating protection of subsequent
protocol interactions. If its use is negotiated, a security layer is inserted
between the protocol and the connection.
To actually use SASL you must install at least one of the %{libname}-plug-XXXX
authentication plugin, such as %{libname}-plug-plain.
The SQL auxprop plugin can be rebuild with different database backends:
	--with srp	SRP support	(%{SRPSTR})
	--with mysql	MySQL support	(%{MYSQLSTR})
	--with pgsql	Postgres SQL support	(%{PGSQLSTR})
	--with sqlite3	SQLite v3 support	(%{SQLITE3STR})

%package -n %{libname}
Summary:	Libraries for SASL a the Simple Authentication and Security Layer
Group:		System/Libraries

%description -n %{libname}
SASL is the Simple Authentication and Security Layer,
a method for adding authentication support to connection-based protocols.
To use SASL, a protocol includes a command for identifying and authenticating
a user to a server and for optionally negotiating protection of subsequent
protocol interactions. If its use is negotiated, a security layer is inserted
between the protocol and the connection.

%package -n %{devname}
Summary:	Libraries for SASL a the Simple Authentication and Security Layer
Group:		Development/C
Provides:	sasl-devel = %{version}
Requires:	%{libname} >= %{version}
Obsoletes:	%{_lib}sasl2-devel < 2.1.25-9

%description -n %{devname}
SASL is the Simple Authentication and Security Layer,
a method for adding authentication support to connection-based protocols.
To use SASL, a protocol includes a command for identifying and authenticating
a user to a server and for optionally negotiating protection of subsequent
protocol interactions. If its use is negotiated, a security layer is inserted
between the protocol and the connection.

%package -n %{libname}-plug-anonymous
Summary:	SASL ANONYMOUS mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-anonymous
Requires:	%{name} = %{version}

%description -n %{libname}-plug-anonymous
This plugin implements the SASL ANONYMOUS mechanism,
used for anonymous authentication.

%package -n %{libname}-plug-crammd5
Summary:	SASL CRAM-MD5 mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-crammd5
Requires:	%{name} = %{version}

%description -n %{libname}-plug-crammd5
This plugin implements the SASL CRAM-MD5 mechanism.
CRAM-MD5 is the mandatory-to-implement authentication mechanism for a
number of protocols; it uses MD5 with a challenge/response system to
authenticate the user.

%package -n %{libname}-plug-digestmd5
Summary:	SASL DIGEST-MD5 mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-digestmd5
Requires:	%{name} = %{version}

%description -n %{libname}-plug-digestmd5
This plugin implements the latest draft of the SASL DIGEST-MD5
mechanism.  Although not yet finalized, this is likely to become the
new mandatory-to-implement authentication system in all new protocols.
It's based on the digest md5 authentication system designed for HTTP.

%package -n %{libname}-plug-plain
Summary:	SASL PLAIN mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-plain
Requires:	%{name} = %{version}

%description -n %{libname}-plug-plain
This plugin implements the SASL PLAIN mechanism.  Although insecure,
PLAIN is useful for transitioning to new security mechanisms, as this
is the only mechanism which gives the server a copy of the user's
password.

%package -n %{libname}-plug-scram
Summary:	SASL SCRAM-SHA-1 mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-scram
Requires:	%{name} = %{version}

%description -n %{libname}-plug-scram
This plugin implements the SASL SCRAM-SHA-1 SASL plugin mechanism.

%package -n %{libname}-plug-login
Summary:	SASL LOGIN mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-login
Requires:	%{name} = %{version}

%description -n %{libname}-plug-login
This plugin implements the SASL LOGIN mechanism.
THIS PLUGIN IS DEPRECATED, is maintained only for compatibility reasons
and will be dropped soon.
Please use the plain plugin instead.

%package -n %{libname}-plug-gssapi
Summary:	SASL GSSAPI mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-gssapi
Requires:	krb5-libs
Requires:	%{name} = %{version}

%description -n %{libname}-plug-gssapi
This plugin implements the SASL GSSAPI (kerberos 5)mechanism.

%package -n %{libname}-plug-otp
Summary:	SASL OTP mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-otp
Requires:	%{name} = %{version}

%description -n %{libname}-plug-otp
This plugin implements the SASL OTP mechanism.

%package -n %{libname}-plug-sasldb
Summary:	SASL sasldb auxprop plugin
Group:		System/Libraries
Provides:	sasl-plug-sasldb
Requires:	%{name} = %{version}
Requires(pre,post,preun): rpm-helper

%description -n %{libname}-plug-sasldb
This package provides the SASL sasldb auxprop plugin, which stores secrets
in a Berkeley database file.

%package -n %{libname}-plug-srp
Summary:	SASL srp mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-srp
Requires:	%{name} = %{version}

%description -n %{libname}-plug-srp
This plugin implements the srp  mechanism.

%package -n %{libname}-plug-ntlm
Summary:	SASL ntlm authentication plugin
Group:		System/Libraries
Provides:	sasl-plug-ntlm
Requires:	%{name} = %{version}

%description -n %{libname}-plug-ntlm
This plugin implements the (unsupported) ntlm authentication.

%package -n %{libname}-plug-sql
Summary:	SASL MySQL plugin
Group:		System/Libraries
Provides:	sasl-plug-sql
Requires:	%{name} = %{version}
%rename		%{_lib}sasl2-plug-mysql
%rename		%{_lib}sasl2-plug-pgsql
%rename		%{_lib}sasl2-plug-sqlite3

%description -n %{libname}-plug-sql
This plugin implements the SQL authentication method based
on MySQL, PGSQL and SQLITE3.

%package -n %{libname}-plug-ldapdb
Summary:	SASL ldapdb auxprop plugin
Group:		System/Libraries
Provides:	sasl-plug-ldapdb
Requires:	%{name} = %{version}

%description -n %{libname}-plug-ldapdb
This plugin implements the LDAP auxprop authentication method.

%prep
%setup -q
install -m 0644 %{SOURCE4} .
%autopatch -p1

cp %{SOURCE7} sasl-mechlist.c
cp %{SOURCE8} sasl-checkpass.c

export CC="%{__cc}"
export CXX="%{__cxx}"
export ac_ct_CC_FOR_BUILD=cc
export ac_ct_CC="%{__cc}"

rm -f config/config.guess config/config.sub
rm -f config/ltconfig config/ltmain.sh config/libtool.m4 configure
rm -fr autom4te.cache
libtoolize -c -f -i
aclocal -I config
autoheader
autoconf
automake -a -c

%build
export ac_cv_prog_ac_ct_CC_FOR_BUILD=cc
export ac_ct_CC_FOR_BUILD=cc
export ac_ct_CC="%{__cc}"

%serverbuild
%configure \
	--disable-static \
	--enable-shared \
	--with-plugindir="%{_libdir}/sasl2" \
	--with-configdir=%{_sysconfdir}/sasl2:%{_libdir}/sasl2 \
	--with-dblib=gdbm \
	--with-dbpath=%{_sysconfdir}/sasl2/sasldb2 \
	--enable-checkapop \
	--enable-cram \
	--enable-digest \
	--enable-otp \
	--disable-krb4 \
	--enable-login \
	--enable-auth-sasldb \
	--enable-plain \
	--enable-anon \
	--disable-passdss \
	--enable-ntlm \
	--enable-gssapi \
	--enable-gss_mutexes \
%if %{with srp}
	--enable-srp \
	--enable-srp-setpass \
%else
	--disable-srp \
	--disable-srp-setpass \
%endif
%if %{with mysql}
	--enable-sql \
	--with-mysql=%{_libdir} \
%else
	--without-mysql \
%endif
%if %{with pgsql}
	--enable-sql \
	--with-pgsql=%{_libdir} \
%else
	--without-pgsql \
%endif
%if %{with sqlite3}
	--enable-sql \
	--with-sqlite3=%{_libdir} \
%else
	--without-sqlite \
%endif
%if %{with ldap}
	--with-ldap=%{_libdir} \
	--enable-ldapdb \
%endif
	--disable-macos-framework \
	--with-saslauthd=/var/run/saslauthd \
	--with-authdaemond=/var/run/authdaemon.courier-imap/socket \
	--with-devrandom=/dev/urandom

%make_build
%make_build -C saslauthd testsaslauthd

install saslauthd/LDAP_SASLAUTHD README.ldap

# Build a small program to list the available mechanisms, because I need it.
pushd lib
    ../libtool --mode=link %{__cc} -o sasl2-shared-mechlist \
	-I../include $CFLAGS ../sasl-mechlist.c $LDFLAGS ./libsasl2.la
    ../libtool --mode=link %{__cc} -o sasl2-shared-checkpass \
	-I../include $CFLAGS -DSASL2 ../sasl-checkpass.c $LDFLAGS ./libsasl2.la
popd

%install
mkdir -p %{buildroot}/var/lib/sasl2 %{buildroot}/var/run/saslauthd
mkdir -p %{buildroot}%{_sysconfdir}/sasl2

%make_install

install -m644 %{SOURCE2} -D %{buildroot}%{_unitdir}/saslauthd.service
install -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/sysconfig/saslauthd

# to be removed later
# we don't need these
#rm -f %{buildroot}%{_libdir}/sasl2/*.*a

# dbconverter-2 isn't installed by make install

cd utils
/bin/sh ../libtool --mode=install /usr/bin/install -c dbconverter-2 \
  %{buildroot}/%{_sbindir}/dbconverter-2

cd ..
cp saslauthd/testsaslauthd %{buildroot}%{_sbindir}

# quick README about the sasl.db file permissions
cat > README.OpenMandriva.sasldb <<EOF
Starting with %{libname}-plug-sasldb-2.1.22-6mdk, OpenMandriva by default
creates a system group called "sasl" and installs an empty
%{sasl2_db_filename} file with the following permissions:
mode 0640, ownership root:sasl.

If the %{sasl2_db_filename} file already exists, it is not changed
in any way.

It is recommended that administrators keep these permissions and add
application users to the "sasl" group if access to this database is needed.

For example, to permit the Postfix SMTP to authenticate users via the sasldb
auxprop plugin, add the "postfix" user to the "sasl" group and read the
"SMTP Authentication" section of the README.MDK documentation file for
details regarding Postfix's chroot setup.

For other applications in general, just add their user to the "sasl" group.

Have fun,
OpenMandriva Team.

EOF

# This is just to "close" vim's syntax misinterpretation.. ;p

# Provide an easy way to query the list of available mechanisms.
./libtool --mode=install install -m0755 lib/sasl2-shared-mechlist %{buildroot}%{_sbindir}/
./libtool --mode=install install -m0755 lib/sasl2-shared-checkpass %{buildroot}%{_sbindir}/

%pre -n %{libname}-plug-sasldb
%_pre_groupadd sasl

%post -n %{libname}-plug-sasldb
#convert old sasldb
# XXX - what about berkeley db versions? - andreas
if [ -f /var/lib/sasl/sasl.db -a ! -f %{sasl2_db_filename} ]; then
    echo "" | /usr/sbin/dbconverter-2 /var/lib/sasl/sasl.db %{sasl2_db_filename}
    if [ -f %{sasl2_db_filename} ]; then
# conversion was successfull
	chmod 0640 %{sasl2_db_filename}
	chown root:sasl %{sasl2_db_filename}
    fi
fi
if [ -f /var/lib/sasl/sasl.db.rpmsave -a ! -f %{sasl2_db_filename} ]; then
    echo "" | /usr/sbin/dbconverter-2 /var/lib/sasl/sasl.db.rpmsave %{sasl2_db_filename}
    if [ -f %{sasl2_db_filename} ]; then
# conversion was successfull
	chmod 0640 %{sasl2_db_filename}
	chown root:sasl %{sasl2_db_filename}
    fi
fi
if [ ! -f %{sasl2_db_filename} ]; then
# the file was never created before nor converted from sasl1
    touch %{sasl2_db_filename}
    chmod 0640 %{sasl2_db_filename}
    chown root:sasl %{sasl2_db_filename}
fi

%files
%doc COPYING AUTHORS ChangeLog README*
%dir /var/lib/sasl2
%dir /var/run/saslauthd
%dir %{_sysconfdir}/sasl2
%attr (644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/saslauthd
%{_sbindir}/dbconverter-2
%{_sbindir}/pluginviewer
%{_sbindir}/saslauthd
# These 2 exist if and only if database support is enabled
%optional %{_sbindir}/sasldblistusers2
%optional %{_sbindir}/saslpasswd2
%{_sbindir}/testsaslauthd
%{_unitdir}/saslauthd.service
%doc %{_mandir}/man8/*

%files -n %{libname}
%dir %{_sysconfdir}/sasl2
%dir %{_libdir}/sasl2
%{_libdir}/libsasl*.so.%{major}*

%files -n %{libname}-plug-anonymous
%{_libdir}/sasl2/libanonymous.so*

%files -n %{libname}-plug-otp
%{_libdir}/sasl2/libotp.so*

%files -n %{libname}-plug-scram
%{_libdir}/sasl2/libscram.so*

%files -n %{libname}-plug-crammd5
%{_libdir}/sasl2/libcrammd5.so*

%files -n %{libname}-plug-sasldb
%doc README.OpenMandriva.sasldb
%{_libdir}/sasl2/libsasldb.so*

%if %{with krb5}
%files -n %{libname}-plug-gssapi
%{_libdir}/sasl2/libgs2.so*
%{_libdir}/sasl2/libgssapiv2.so*
%endif

%files -n %{libname}-plug-digestmd5
%{_libdir}/sasl2/libdigestmd5.so*

%files -n %{libname}-plug-plain
%{_libdir}/sasl2/libplain.so*

%files -n %{libname}-plug-login
%{_libdir}/sasl2/liblogin.so*

%if %{with srp}
%files -n %{libname}-plug-srp
%{_libdir}/sasl2/libsrp.so*
%endif

%files -n %{libname}-plug-ntlm
%{_libdir}/sasl2/libntlm.so*

%if %{with mysql} || %{with pgsql} || %{with sqlite3}
%files -n %{libname}-plug-sql
%{_libdir}/sasl2/libsql.so*
%endif

%if %{with ldap}
%files -n %{libname}-plug-ldapdb
%{_libdir}/sasl2/libldapdb.so*
%endif

%files -n %{devname}
%{_sbindir}/sasl2-shared-mechlist
%{_sbindir}/sasl2-shared-checkpass
%{_includedir}/sasl
%{_libdir}/*.*so
%{_libdir}/pkgconfig/*.pc
%doc %{_mandir}/man3/*
