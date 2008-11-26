%define major 2
%define libname %mklibname sasl %{major}
%define up_name cyrus-sasl
%define sasl2_db_filename /var/lib/sasl2/sasl.db

%define MYSQL 1
%define SRP 0
%define PGSQL 0
%define SQLITE 0
%define LDAP 1
%define SRPSTR disabled
%define MYSQLSTR enabled
%define PGSQLSTR disabled
%define SQLITESTR disabled
%define LDAPSTR enabled

%{?_with_srp: %{expand: %%global SRP 1}}
%{?_without_srp: %{expand: %%global SRP 0}}
%{?_with_mysql: %{expand: %%global MYSQL 1}}
%{?_without_mysql: %{expand: %%global MYSQL 0}}
%{?_with_pgsql: %{expand: %%global PGSQL 1}}
%{?_without_pgsql: %{expand: %%global PGSQL 0}}
%{?_with_sqlite: %{expand: %%global SQLITE 1}}
%{?_without_sqlite: %{expand: %%global SQLITE 0}}
%{?_with_ldap: %{expand: %%global LDAP 1}}
%{?_without_ldap: %{expand: %%global LDAP 0}}

%{?_with_srp: %{expand: %%global SRPSTR enabled}}
%{?_without_srp: %{expand: %%global SRPSTR disabled}}
%{?_with_mysql: %{expand: %%global MYSQLSTR enabled}}
%{?_without_mysql: %{expand: %%global MYSQLSTR disabled}}
%{?_with_pgsql: %{expand: %%global PGSQLSTR enabled}}
%{?_without_pgsql: %{expand: %%global PGSQLSTR disabled}}
%{?_with_sqlite: %{expand: %%global SQLITESTR enabled}}
%{?_without_sqlite: %{expand: %%global SQLITESTR disabled}}
%{?_with_ldap: %{expand: %%global LDAPSTR enabled}}
%{?_without_ldap: %{expand: %%global LDAPSTR disabled}}

# bootstrapping overrides the above LDAP defines
%{?bootstrap: %{expand: %%global LDAP 0}}
%{?bootstrap: %{expand: %%global LDAPSTR disabled}}

Summary: The Simple Authentication and Security Layer
Name: %{up_name}
Version: 2.1.22
Release: %mkrel 29
Source0: ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{up_name}-%{version}.tar.gz
Source1: ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{up_name}-%{version}.tar.gz.sig
Source2: saslauthd.init
Source3: saslauthd.sysconfig
Source4: service.conf.example
Source5: saslauthd.8
Patch0: cyrus-sasl-doc.patch
Patch1: cyrus-sasl-2.1.19-no_rpath.patch
Patch2: cyrus-sasl-2.1.15-lib64.patch
Patch3: cyrus-sasl-2.1.20-gssapi-dynamic.patch
Patch4: cyrus-sasl-2.1.19-pic.patch
Patch5: cyrus-sasl-latest_bdb.diff
Patch6: cyrus-sasl-2.1.22-sed_syntax.diff
Patch7: cyrus-sasl-2.1.21-sizes.patch
Patch8: cyrus-sasl-2.1.22-digest-commas.patch
Patch9: cyrus-sasl-2.1.22-automake-1.10.patch
Patch10: cyrus-sasl-2.1.22-rimap.patch
Patch11: cyrus-sasl-2.1.22-warnings.patch
License: BSD style
Group: System/Libraries
URL: http://asg.web.cmu.edu/cyrus/download/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: %{libname} = %{version}
#Obsoletes: cyrus-sasl <= 2.1.0
Requires(pre):   rpm-helper
Requires(post):  rpm-helper
Requires(preun): rpm-helper
BuildRequires:  autoconf
# 2.1.22 doesn't build with automake 1.8
BuildRequires:  automake1.7
BuildRequires:  db4-devel
BuildRequires:  pam-devel
BuildRequires:  openssl-devel >= 0.9.6a
BuildRequires:  libtool >= 1.4
# 1.4.x is thread safe, which means we can disable sasl mutexes (see ./configure
# further below)
BuildRequires:  krb5-devel >= 1.4.1
%if %{MYSQL}
BuildRequires:	mysql-devel
%endif
%if %{PGSQL}
BuildRequires:	postgresql-devel
%endif
%if %{SQLITE}
BuildRequires:	sqlite-devel
%endif
%if %{LDAP}
BuildRequires: openldap-devel
%endif
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
	--with sqlite	SQLite support	(%{SQLITESTR})

%package -n %{libname}
Summary: Libraries for SASL a the Simple Authentication and Security Layer
Group: System/Libraries

%description -n %{libname}
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 

%package -n %{libname}-devel
Summary: Libraries for SASL a the Simple Authentication and Security Layer
Group: Development/C
%if %{_lib} != lib
Provides: libsasl-devel = %{version}
Provides: libsasl2-devel = %{version}
%endif
Provides: %{mklibname -d sasl} = %{version}
Requires: %{libname} = %{version}

%description -n %{libname}-devel
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 

%package -n %{libname}-plug-anonymous
Summary: SASL ANONYMOUS mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-anonymous

%description -n %{libname}-plug-anonymous
This plugin implements the SASL ANONYMOUS mechanism,
used for anonymous authentication.

%package -n %{libname}-plug-crammd5
Summary: SASL CRAM-MD5 mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-crammd5

%description -n %{libname}-plug-crammd5
This plugin implements the SASL CRAM-MD5 mechanism.
CRAM-MD5 is the mandatory-to-implement authentication mechanism for a
number of protocols; it uses MD5 with a challenge/response system to
authenticate the user.

%package -n %{libname}-plug-digestmd5
Summary: SASL DIGEST-MD5 mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-digestmd5

%description -n %{libname}-plug-digestmd5
This plugin implements the latest draft of the SASL DIGEST-MD5
mechanism.  Although not yet finalized, this is likely to become the
new mandatory-to-implement authentication system in all new protocols.
It's based on the digest md5 authentication system designed for HTTP.

%package -n %{libname}-plug-plain
Summary: SASL PLAIN mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-plain

%description -n %{libname}-plug-plain
This plugin implements the SASL PLAIN mechanism.  Although insecure,
PLAIN is useful for transitioning to new security mechanisms, as this
is the only mechanism which gives the server a copy of the user's
password.

#package -n %{libname}-plug-scrammd5
#Summary: SASL SCRAM-MD5 mechanism plugin
#Group: System/Libraries
#Requires: %{libname} = %{version}
#Provides: sasl-plug-scrammd5
#
#description -n %{libname}-plug-scrammd5
#This plugin implements the SASL SCRAM-MD5 mechanism.  Although
#deprecated (this will be replaced by DIGEST-MD5 at some point), it may
#be useful for the time being.

%package -n %{libname}-plug-login
Summary: SASL LOGIN mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-login

%description -n %{libname}-plug-login
This plugin implements the SASL LOGIN mechanism.
THIS PLUGIN IS DEPRECATED, is maintained only for compatibility reasons 
and will be dropped soon.
Please use the plain plugin instead.

%package -n %{libname}-plug-gssapi
Summary: SASL GSSAPI mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Requires: krb5-libs
Provides: sasl-plug-gssapi

%description -n %{libname}-plug-gssapi
This plugin implements the SASL GSSAPI (kerberos 5)mechanism.

%package -n %{libname}-plug-otp
Summary: SASL OTP mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-otp

%description -n %{libname}-plug-otp
This plugin implements the SASL OTP mechanism.

%package -n %{libname}-plug-sasldb
Summary: SASL sasldb auxprop plugin
Group: System/Libraries
# Requirement for %%{name} is due to dbconverter-2 being
# potentially called in %%post
Requires(post): %{name} >= %{version}
# That requirement has to be here (in "Requires") also
# (http://archives.mandrivalinux.com/cooker/2005-06/msg00109.php)
Requires: %{libname} = %{version}, %{name} >= %{version}
Provides: sasl-plug-sasldb

%description -n %{libname}-plug-sasldb
This package provides the SASL sasldb auxprop plugin, which stores secrets
in a Berkeley database file.

%if %{SRP}
%package -n %{libname}-plug-srp
Summary: SASL srp mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-srp

%description -n %{libname}-plug-srp
This plugin implements the srp  mechanism.
%endif

%package -n %{libname}-plug-ntlm
Summary: SASL ntlm authentication plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-ntlm

%description -n %{libname}-plug-ntlm
This plugin implements the (unsupported) ntlm authentication.

%if %{MYSQL} || %{PGSQL} || %{SQLITE}
%package -n %{libname}-plug-sql
Summary: SASL sql auxprop plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-sql

%description -n %{libname}-plug-sql
This plugin implements the SQL auxprop authentication method
It can be rebuild with different database backends:
	--with mysql	MySQL support	(%{MYSQLSTR})
	--with pgsql	Postgres SQL support	(%{PGSQLSTR})
	--with sqlite	SQLite support	(%{SQLITESTR})
%endif

%if %{LDAP}
%package -n %{libname}-plug-ldapdb
Summary: SASL ldapdb auxprop plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Provides: sasl-plug-ldapdb

%description -n %{libname}-plug-ldapdb
This plugin implements the LDAP auxprop authentication method.
%endif

%prep

%setup -q -n %{up_name}-%{version}
install -m 0644 %{SOURCE4} .
%patch0 -p1 -b .sasldoc
%patch1 -p1 -b .rpath
%patch2 -p1 -b .lib64
#%patch3 -p1 -b .gssapi
%patch4 -p1 -b .pic
%patch5 -p0 -b .latest_bdb
%patch6 -p0 -b .sed_syntax
%patch7 -p1 -b .sizes
%patch8 -p2 -b .digest-commas
%patch9 -p1 -b .automake-1.10
%patch10 -p1 -b .rimap
%patch11 -p1 -b .warnings

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure.in
rm -f configure

rm -f config/ltconfig config/libtool.m4
libtoolize -f -c
aclocal-1.7 -I config -I cmulocal
automake-1.7 -a -c -f
autoheader
autoconf -f
pushd saslauthd
rm -f config/ltconfig
libtoolize -f -c
aclocal-1.7 -I ../config -I ../cmulocal
automake-1.7 -a -c -f
autoheader
autoconf -f
popd

%build

%serverbuild
# i have to trim spaces into CFLAGS or configure will whine
export CFLAGS=`echo ${CFLAGS} | sed -e 's/  */ /'`

export LDFLAGS="-L%{_libdir}"

%{?__cputoolize: %{__cputoolize} -c saslauthd}
%configure 	--enable-static --enable-shared \
		--with-plugindir=%{_libdir}/sasl2 \
		--with-configdir=%{_sysconfdir}/sasl2:%{_libdir}/sasl2 \
		--disable-krb4 \
		--enable-login \
%if %{SRP}
		--enable-srp --enable-srp-setpass \
%else
		--without-srp --without-srp-srp-setpass \
%endif
		--enable-ntlm \
		--enable-db4 \
		--enable-gssapi \
		--disable-gss_mutexes \
%if %{MYSQL}
		--enable-sql --with-mysql=%{_prefix} \
%else
		--without-mysql \
%endif
%if %{PGSQL}
		--enable-sql --with-pgsql=%{_prefix} \
%else
		--without-pgsql \
%endif
%if %{SQLITE}
		--enable-sql --with-sqlite=%{_prefix} \
%else
		--without-sqlite \
%endif
%if %{LDAP}
		--with-ldap=%{_prefix} \
		--enable-ldapdb \
%endif
		--with-dbpath=%{sasl2_db_filename} \
		--with-saslauthd=/var/lib/sasl2 \
		--with-authdaemond=/var/run/authdaemon.courier-imap/socket

# ugly hack: there is an ordering problem introduced in 2.1.21 
# when --enable-static is given to ./configure which calling 
# make twice "solves"
# no parallel make on cluster
make || :
make
make -C saslauthd testsaslauthd
make -C sample

install saslauthd/LDAP_SASLAUTHD README.ldap

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/var/lib/sasl2
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_sysconfdir}/sasl2

%makeinstall_std

install -m 0644 %{SOURCE2} %{buildroot}%{_initrddir}/saslauthd
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/saslauthd
# install fixed saslauthd.8 manpage
install -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man8/

# we don't need these
rm -f %{buildroot}%{_libdir}/sasl2/*.a

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

%clean
rm -rf %{buildroot}

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

%post
%_post_service saslauthd

%preun
%_preun_service saslauthd

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files
%defattr(-,root,root)
%doc COPYING AUTHORS INSTALL NEWS README* ChangeLog
%doc doc/{TODO,ONEWS,*.txt,*.html}
%doc service.conf.example
%dir /var/lib/sasl2
%attr (755,root,root) %{_initrddir}/saslauthd
%dir %{_sysconfdir}/sasl2
%attr (644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/saslauthd
%{_sbindir}/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%dir %{_libdir}/sasl2
%{_libdir}/libsasl*.so.*

%files -n %{libname}-plug-anonymous
%defattr(-,root,root)
%{_libdir}/sasl2/libanonymous*.so*
%{_libdir}/sasl2/libanonymous*.la

%files -n %{libname}-plug-otp
%defattr(-,root,root)
%{_libdir}/sasl2/libotp*.so*
%{_libdir}/sasl2/libotp*.la

%files -n %{libname}-plug-sasldb
%defattr(-,root,root)
%doc README.Mandriva.sasldb
%{_libdir}/sasl2/libsasldb*.so*
%{_libdir}/sasl2/libsasldb*.la

%files -n %{libname}-plug-gssapi
%defattr(-,root,root)
%{_libdir}/sasl2/libgssapi*.so*
%{_libdir}/sasl2/libgssapi*.la

%files -n %{libname}-plug-crammd5
%defattr(-,root,root)
%{_libdir}/sasl2/libcrammd5*.so*
%{_libdir}/sasl2/libcrammd5*.la

%files -n %{libname}-plug-digestmd5
%defattr(-,root,root)
%{_libdir}/sasl2/libdigestmd5*.so*
%{_libdir}/sasl2/libdigestmd5*.la

%files -n %{libname}-plug-plain
%defattr(-,root,root)
%{_libdir}/sasl2/libplain*.so*
%{_libdir}/sasl2/libplain*.la

%files -n %{libname}-plug-login
%defattr(-,root,root)
%{_libdir}/sasl2/liblogin*.so*
%{_libdir}/sasl2/liblogin*.la

%if %{SRP}
%files -n %{libname}-plug-srp
%defattr(-,root,root)
%{_libdir}/sasl2/libsrp*.so*
%{_libdir}/sasl2/libsrp*.la
%endif

%files -n %{libname}-plug-ntlm
%defattr(-,root,root)
%{_libdir}/sasl2/libntlm*.so*
%{_libdir}/sasl2/libntlm*.la

%if %{MYSQL} || %{PGSQL} || %{SQLITE}
%files -n %{libname}-plug-sql
%defattr(-,root,root)
%{_libdir}/sasl2/libsql*.so*
%{_libdir}/sasl2/libsql*.la
%endif

%if %{LDAP}
%files -n %{libname}-plug-ldapdb
%defattr(-,root,root)
%{_libdir}/sasl2/libldap*.so*
%{_libdir}/sasl2/libldap*.la
%endif

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.*so
%{_libdir}/*.*a
%{_mandir}/man3/*
