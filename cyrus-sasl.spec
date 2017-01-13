%define major 2
%define libname %mklibname sasl %{major}
%define devname %mklibname sasl -d
%define sasl2_db_filename /var/lib/sasl2/sasl.db

%define _disable_rebuild_configure 1

%define KRB5 1
%define MYSQL 1
%define SRP 0
%define PGSQL 1
%define SQLITE3 1
%define LDAP 1
%define SRPSTR enabled
%define MYSQLSTR enabled
%define PGSQLSTR enabled
%define SQLITE3STR enabled
%define LDAPSTR enabled

%{?_with_krb5: %{expand: %%global KRB5 1}}
%{?_without_krb5: %{expand: %%global KRB5 0}}
%{?_with_srp: %{expand: %%global SRP 1}}
%{?_without_srp: %{expand: %%global SRP 0}}
%{?_with_mysql: %{expand: %%global MYSQL 1}}
%{?_without_mysql: %{expand: %%global MYSQL 0}}
%{?_with_pgsql: %{expand: %%global PGSQL 1}}
%{?_without_pgsql: %{expand: %%global PGSQL 0}}
%{?_with_sqlite3: %{expand: %%global SQLITE3 1}}
%{?_without_sqlite3: %{expand: %%global SQLITE3 0}}
%{?_with_ldap: %{expand: %%global LDAP 1}}
%{?_without_ldap: %{expand: %%global LDAP 0}}

%{?_with_srp: %{expand: %%global SRPSTR enabled}}
%{?_without_srp: %{expand: %%global SRPSTR disabled}}
%{?_with_mysql: %{expand: %%global MYSQLSTR enabled}}
%{?_without_mysql: %{expand: %%global MYSQLSTR disabled}}
%{?_with_pgsql: %{expand: %%global PGSQLSTR enabled}}
%{?_without_pgsql: %{expand: %%global PGSQLSTR disabled}}
%{?_with_sqlite3: %{expand: %%global SQLITE3STR enabled}}
%{?_without_sqlite3: %{expand: %%global SQLITE3STR disabled}}
%{?_with_ldap: %{expand: %%global LDAPSTR enabled}}
%{?_without_ldap: %{expand: %%global LDAPSTR disabled}}

# bootstrapping overrides the above LDAP defines
%{?bootstrap: %{expand: %%global LDAP 0}}
%{?bootstrap: %{expand: %%global LDAPSTR disabled}}

%define snap 20170113

Summary:	The Simple Authentication and Security Layer
Name:		cyrus-sasl
Version:	2.1.27
Release:	0.%{snap}.1
License:	BSD-style
Group:		System/Libraries
Url:		http://cyrusimap.org/
# git clone https://github.com/cyrusimap/cyrus-sasl.git
# git archive --format=tar --prefix cyrus-sasl-2.1.27-$(date +%Y%m%d)/ HEAD | xz -vf > cyrus-sasl-2.1.27-$(date +%Y%m%d).tar.xz
Source0:	%{name}-%{version}-%{snap}.tar.xz
#Source0:	ftp://ftp.cyrusimap.org/cyrus-sasl/%{name}-%{version}.tar.gz
Source2:	saslauthd.service
Source3:	saslauthd.sysconfig
Source4:	service.conf.example
Source7:	sasl-mechlist.c
Source8:	sasl-checkpass.c
# (tpg) patches from Debian
Patch0:		0001-Make-the-libsasl2-symbols-versioned.patch
Patch1:		0002-Use-etc-sasldb2-instead-of-.-sasldb-in-the-testsuite.patch
Patch2:		0003-Update-saslauthd.conf-location-in-documentation.patch
Patch3:		0004-Include-dbconverter-2-in-sbin_PROGRAMS-and-set-defau.patch
Patch4:		0005-Fixes-in-library-mutexes.patch
Patch5:		0006-Enable-autoconf-maintainer-mode.patch
Patch6:		0007-Define-_XOPEN_SOURCE-in-auth_shadow.c-to-get-proper-.patch
Patch7:		0008-Don-t-overwrite-PIC-objects-with-non-PIC-variant.patch
Patch8:		0009-Look-for-generic-Berkeley-DB-first.patch
Patch9:		0010-Update-required-libraries-when-ld-as-needed-is-used.patch
Patch10:	0011-Drop-krb5support-dependency.patch
Patch11:	0012-LDAP-fixes.patch
Patch12:	0013-Don-t-use-la-files-for-opening-plugins.patch
Patch13:	0014-Don-t-use-R-when-searching-for-SQLite-libraries.patch
Patch14:	0015-Revert-1.103-revision-to-unbreak-GSSAPI.patch
Patch15:	0016-Fix-segfault-in-GSSAPI.patch
Patch16:	0017-Fix-dovecot-authentication.patch
Patch17:	0018-Temporary-multiarch-fixes.patch
Patch18:	0019-Add-reference-to-LDAP_SASLAUTHD-file-to-the-saslauth.patch
Patch19:	0020-Send-IMAP-logout.patch
Patch20:	0021-Fix-canonuser-ldapdb-garbage-in-out-buffer.patch
Patch21:	0022-Fix-keytab-option-for-MIT-Kerberos.patch
Patch22:	0023-Release-server-creds-when-they-are-no-longer-needed.patch
Patch23:	0024-Fix-typo-in-debugging-logs.patch
Patch24:	0025-Revert-upstream-soname-bump.patch
Patch25:	0026-Fix-return-SASL_FAIL-in-void-sasl_dispose.patch
Patch26:	0027-properly-create-libsasl2.pc.patch
Patch27:	0028-2.1.26-Allow-CAPABILITY-lines-in-IMAP-login-reply-v4.patch
Patch28:	0029-Fix-early-hangup-in-ipc_unix.c.patch
Patch29:	0030-Change-linking-from-sasldb-.libs-libsasldb.al-to-sas.patch
Patch30:	0031-Cleanup-for-modern-autotools.patch
Patch31:	0032-Add-with_pgsql-include-postgresql-to-include-path.patch

BuildRequires:	groff
BuildRequires:	libtool
BuildRequires:	db-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(libssl)
# 1.4.x is thread safe, which means we can disable sasl mutexes (see ./configure
# further below)
%if %{KRB5}
BuildRequires:	krb5-devel >= 1.4.1
%endif
%if %{MYSQL}
BuildRequires:	mysql-devel
%endif
%if %{PGSQL}
BuildRequires:	postgresql-devel
%endif
%if %{SQLITE3}
BuildRequires:	pkgconfig(sqlite3)
%endif
%if %{LDAP}
BuildRequires:	openldap-devel
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

%package -n	%{libname}
Summary:	Libraries for SASL a the Simple Authentication and Security Layer
Group:		System/Libraries

%description -n	%{libname}
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 

%package -n	%{devname}
Summary:	Libraries for SASL a the Simple Authentication and Security Layer
Group:		Development/C
Provides:	sasl-devel = %{version}
Requires:	%{libname} >= %{version}
Obsoletes:	%{_lib}sasl2-devel < 2.1.25-9

%description -n	%{devname}
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 

%package -n	%{libname}-plug-anonymous
Summary:	SASL ANONYMOUS mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-anonymous
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-anonymous
This plugin implements the SASL ANONYMOUS mechanism,
used for anonymous authentication.

%package -n	%{libname}-plug-crammd5
Summary:	SASL CRAM-MD5 mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-crammd5
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-crammd5
This plugin implements the SASL CRAM-MD5 mechanism.
CRAM-MD5 is the mandatory-to-implement authentication mechanism for a
number of protocols; it uses MD5 with a challenge/response system to
authenticate the user.

%package -n	%{libname}-plug-digestmd5
Summary:	SASL DIGEST-MD5 mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-digestmd5
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-digestmd5
This plugin implements the latest draft of the SASL DIGEST-MD5
mechanism.  Although not yet finalized, this is likely to become the
new mandatory-to-implement authentication system in all new protocols.
It's based on the digest md5 authentication system designed for HTTP.

%package -n	%{libname}-plug-plain
Summary:	SASL PLAIN mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-plain
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-plain
This plugin implements the SASL PLAIN mechanism.  Although insecure,
PLAIN is useful for transitioning to new security mechanisms, as this
is the only mechanism which gives the server a copy of the user's
password.

%package -n	%{libname}-plug-scram
Summary:	SASL SCRAM-SHA-1 mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-scram
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-scram
This plugin implements the SASL SCRAM-SHA-1 SASL plugin mechanism.

%package -n	%{libname}-plug-login
Summary:	SASL LOGIN mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-login
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-login
This plugin implements the SASL LOGIN mechanism.
THIS PLUGIN IS DEPRECATED, is maintained only for compatibility reasons 
and will be dropped soon.
Please use the plain plugin instead.

%if %{KRB5}
%package -n	%{libname}-plug-gssapi
Summary:	SASL GSSAPI mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-gssapi
Requires:	krb5-libs
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-gssapi
This plugin implements the SASL GSSAPI (kerberos 5)mechanism.
%endif

%package -n	%{libname}-plug-otp
Summary:	SASL OTP mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-otp
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-otp
This plugin implements the SASL OTP mechanism.

%package -n	%{libname}-plug-sasldb
Summary:	SASL sasldb auxprop plugin
Group:		System/Libraries
Provides:	sasl-plug-sasldb
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-sasldb
This package provides the SASL sasldb auxprop plugin, which stores secrets
in a Berkeley database file.

%if %{SRP}
%package -n	%{libname}-plug-srp
Summary:	SASL srp mechanism plugin
Group:		System/Libraries
Provides:	sasl-plug-srp
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-srp
This plugin implements the srp  mechanism.
%endif

%package -n	%{libname}-plug-ntlm
Summary:	SASL ntlm authentication plugin
Group:		System/Libraries
Provides:	sasl-plug-ntlm
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-ntlm
This plugin implements the (unsupported) ntlm authentication.

%if %{MYSQL}
%package -n	%{libname}-plug-mysql
Summary:	SASL MySQL plugin
Group:		System/Libraries
Provides:	sasl-plug-sql
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-mysql
This plugin implements the MySQL authentication method
%endif

%if %{PGSQL}
%package -n	%{libname}-plug-pgsql
Summary:	SASL PostgreSQL plugin
Group:		System/Libraries
Provides:	sasl-plug-sql
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-pgsql
This plugin implements the PostgreSQL authentication method
%endif

%if %{SQLITE3}
%package -n	%{libname}-plug-sqlite3
Summary:	SASL SQLite v3 plugin
Group:		System/Libraries
Provides:	sasl-plug-sql
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-sqlite3
This plugin implements the SQLite v3 authentication method
%endif

%if %{LDAP}
%package -n	%{libname}-plug-ldapdb
Summary:	SASL ldapdb auxprop plugin
Group:		System/Libraries
Provides:	sasl-plug-ldapdb
Requires:	%{name} = %{version}

%description -n	%{libname}-plug-ldapdb
This plugin implements the LDAP auxprop authentication method.
%endif

%prep
%setup -qn %{name}-%{version}-%{snap}
install -m 0644 %{SOURCE4} .
%apply_patches

cp %{SOURCE7} sasl-mechlist.c
cp %{SOURCE8} sasl-checkpass.c

./autogen.sh

%build
%serverbuild
%configure \
	--disable-static \
	--enable-shared \
	--with-plugindir=%{_libdir}/sasl2 \
	--with-configdir=%{_sysconfdir}/sasl2:%{_libdir}/sasl2 \
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
	--disable-gss_mutexes \
%if %{SRP}
	--enable-srp \
	--enable-srp-setpass \
%else
	--disable-srp \
	--disable-srp-setpass \
%endif
%if %{MYSQL}
	--enable-sql \
	--with-mysql=%{_libdir} \
%else
	--without-mysql \
%endif
%if %{PGSQL}
	--enable-sql \
	--with-pgsql=%{_libdir} \
%else
	--without-pgsql \
%endif
%if %{SQLITE3}
	--enable-sql \
	--with-sqlite3=%{_libdir} \
%else
	--without-sqlite \
%endif
%if %{LDAP}
	--with-ldap=%{_prefix} \
	--enable-ldapdb \
%endif
	--disable-macos-framework \
	--with-saslauthd=/var/run/saslauthd \
	--with-authdaemond=/var/run/authdaemon.courier-imap/socket \
	--with-devrandom=/dev/urandom

%make
%make -C saslauthd testsaslauthd
%make -C sample

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

%makeinstall_std

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
cd sample
/bin/sh ../libtool --mode=install /usr/bin/install -c client \
  %{buildroot}/%{_sbindir}/sasl-sample-client
/bin/sh ../libtool --mode=install /usr/bin/install -c server \
  %{buildroot}/%{_sbindir}/sasl-sample-server
cd ..

# multiarch policy
%multiarch_includes %{buildroot}%{_includedir}/sasl/md5global.h

# quick README about the sasl.db file permissions
cat > README.Mandriva.sasldb <<EOF
Starting with %{libname}-plug-sasldb-2.1.22-6mdk, Mandriva by default 
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
Mandriva Team.

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
%doc COPYING AUTHORS INSTALL NEWS README*
%doc doc/{TODO,ONEWS,*.txt,*.html}
%doc service.conf.example
%dir /var/lib/sasl2
%dir /var/run/saslauthd
%dir %{_sysconfdir}/sasl2
%attr (644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/saslauthd
%{_sbindir}/dbconverter-2
%{_sbindir}/pluginviewer
%{_sbindir}/sasl-sample-client
%{_sbindir}/sasl-sample-server
%{_sbindir}/saslauthd
%{_sbindir}/sasldblistusers2
%{_sbindir}/saslpasswd2
%{_sbindir}/testsaslauthd
%{_unitdir}/saslauthd.service
%{_mandir}/man8/*

%files -n %{libname}
%dir %{_libdir}/sasl2
%{_libdir}/libsasl*.so.%{major}*

%files -n %{libname}-plug-anonymous
%{_libdir}/sasl2/libanonymous.so

%files -n %{libname}-plug-otp
%{_libdir}/sasl2/libotp.so

%files -n %{libname}-plug-scram
%{_libdir}/sasl2/libscram.so

%files -n %{libname}-plug-crammd5
%{_libdir}/sasl2/libcrammd5.so

%files -n %{libname}-plug-sasldb
%doc README.Mandriva.sasldb
%{_libdir}/sasl2/libsasldb.so

%if %{KRB5}
%files -n %{libname}-plug-gssapi
%{_libdir}/sasl2/libgs2.so
%{_libdir}/sasl2/libgssapiv2.so
%endif

%files -n %{libname}-plug-digestmd5
%{_libdir}/sasl2/libdigestmd5.so

%files -n %{libname}-plug-plain
%{_libdir}/sasl2/libplain.so

%files -n %{libname}-plug-login
%{_libdir}/sasl2/liblogin.so

%if %{SRP}
%files -n %{libname}-plug-srp
%{_libdir}/sasl2/libsrp.so
%endif

%files -n %{libname}-plug-ntlm
%{_libdir}/sasl2/libntlm.so

%if %{MYSQL}
%files -n %{libname}-plug-mysql
%{_libdir}/sasl2/libmysql.so
%endif

%if %{PGSQL}
%files -n %{libname}-plug-pgsql
%{_libdir}/sasl2/libpgsql.so
%endif

%if %{SQLITE3}
%files -n %{libname}-plug-sqlite3
%{_libdir}/sasl2/libsqlite3.so
%endif

%if %{LDAP}
%files -n %{libname}-plug-ldapdb
%{_libdir}/sasl2/libldapdb.so
%endif

%files -n %{devname}
%{_sbindir}/sasl2-shared-mechlist
%{_sbindir}/sasl2-shared-checkpass
%{_includedir}/sasl
%{multiarch_includedir}/sasl/md5global.h
%{_libdir}/*.*so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
