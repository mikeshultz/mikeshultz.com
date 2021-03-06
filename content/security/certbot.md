Title: Setting Up Let's Encrypt With Lighttpd (Using Certbot)
Date: 2017-05-09 21:17
Category: Security
Tags: letsencrypt, linux, ssl, tls, lighttpd, certbot
Slug: setting-up-lets-encrypt-with-lighttpd-and-certbot
Authors: Mike Shultz
Summary: Finally getting around to updating my previous post on Let's Encrypt and lighttpd

Finally getting around to updating [my previous post](/setting-up-lets-encrypt-with-lighttpd.html) on [Let's Encrypt](https://letsencrypt.org) and lighttpd.  I'll assume you're generally familiar with both. This time, however, we're going to use the much easier to use(and automate) [`certbot`](https://certbot.eff.org/), privided by the extraordinary [EFF](https://www.eff.org).

**NOTE**: If you have a full Web cluster, load balancer, or your server is behind a firewall, please consider going the traditional route of purchasing a certificate.  It won't waste Let's Encrypt's resources, and you'll have a much easier time getting it setup.

**NOTE**: If you're on a different distro than I am that uses different paths, or use a domain that *isn't* example.com, some of these commands may need to be altered.  *Run random commands from a Web site responsibly.*

## Install 

Folow the [EFF docs to get certbot installed for your distro](https://certbot.eff.org).  Come back here before you generate the certificate.

## Generate The Certificate

Choose one of the following options only.  [Option A](#easyway) is the easy way, but will require you to take down lighty and can not be automated.  [Option B](#hardway) can be automated and is a more high-availability way of doing things.

### (Option A) The Easy Way<a name="easyway"></a>

**NOTE**: If you **do not** want to take down lighty during this process, see the section [The Hard Way](#hardway).

First off, shut down lighty.  We want to get `certbot` up and running on standard Web ports, so we can't have anything conflicting there.  The following command may be different for your distro.

    systemctl stop lighttpd

Now we can validate, generate, and fetch our new certificate with one simple command.

    certbot certonly --standalone -d example.com -d www.example.com

This will get what we need and organize it under `/etc/letsencrypt/live/example.com/`.  Go ahead and start lighty again.

    systemctl start lighttpd

And skip ahead to [Reformat For Lighttpd](#reformat)

### (Option B) The Hard Way<a name="hardway"></a>

#### Create The Web Root

Create the Web root and make sure lighty has permissions to access these files.  We also need to use the setgid sticky bit here so when certbot runs, it creates the directory with permissions that lighty can read.  As of this writing, [there is no way to tell certbot to use certain permisssions](https://github.com/certbot/certbot/issues/1761).

    sudo -u lighttpd mkdir -p /var/certbot/public_html/.well-known/
    chmod g+s /var/certbot/public_html/.well-known

#### Configure Lighttpd

Now we need to configure lighty to serve these validation files on your new domain.  Edit `lighttpd.conf` or `vhosts.d/mysite.conf`, whichever you use and add the following to your general config(single site host) or to the proper vhost section(multi-site host): 

    ## Used for letsencrypt validation
    $HTTP["url"] =~ "^/.well-known/" {
        server.document-root = "/var/certbot/public_html/.well-known/"
        alias.url = ( "/.well-known/" => "/var/certbot/public_html/.well-known/" )
        dir-listing.activate = "enable"
    }


If you leave this config in place, this will work for any future validation as well.  `certbot` will delete any folders and files it creates, so there should be no major ramifications to leaving this in place.  Now reload lighty to bring in the new conf.

    systemctl restart lighttpd

**OR** with lighttpd-angel

    kill -HUP `cat /var/run/lighttpd-angel.pid`

#### Run Certbot

Now you can run certbot to generate and fetch your new cert.

    :::bash
    certbot certonly --webroot -w /var/certbot/public_html -d example.com -d www.example.com

It should go through the motions automagically and symlink all of your new certs in the `/etc/letsencrypt/live/example.com/` directory.

## Reformat Cert Files For Lighttpd<a name="reformat"></a>

Lighty likes its certificates formatted in a specific way, so we're going to combine the private keys and certificate into one file that we'll tell lighty about later.

    :::bash
    cat /etc/letsencrypt/live/example.com/privkey.pem /etc/letsencrypt/live/example.com/cert.pem > /etc/letsencrypt/live/example.com/combined.pem

## Give Lighty Permissions

Lighttpd will need permissions to read the certificates.  I prefer to grant group traverse rights.

    chown :lighttpd /etc/letsencrypt
    chown :lighttpd /etc/letsencrypt/live
    chmod g+x /etc/letsencrypt
    chmod g+x /etc/letsencrypt/live

Just to make sure, test and make sure the `lighttpd` user has read permissions.

    sudo -u lighttpd file -L /etc/letsencrypt/live/example.com/cert.pem

## Configure Lighttpd For Your New Cert

Configure lighty to use the new certificate and chain.  In this example, I've use the configuration suggested by [cipherli.st](https://cipherli.st), but you might want to do  your own legwork on that in case this is out of date, or you have different requirements.

    $SERVER["socket"] == ":443" {
        ssl.engine              = "enable"
        ssl.ca-file             = "/etc/letsencrypt/live/example.com/chain.pem"
        ssl.pemfile             = "/etc/letsencrypt/live/example.com/combined.pem"
        ssl.honor-cipher-order  = "enable"
        # The following is OPTIONAL
        ssl.cipher-list         = "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH:ECDHE-RSA-AES128-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA128:DHE-RSA-AES128-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA128:ECDHE-RSA-AES128-SHA384:ECDHE-RSA-AES128-SHA128:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES128-SHA128:DHE-RSA-AES128-SHA128:DHE-RSA-AES128-SHA:DHE-RSA-AES128-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA384:AES128-GCM-SHA128:AES128-SHA128:AES128-SHA128:AES128-SHA:AES128-SHA:DES-CBC3-SHA:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!RC4"
        ssl.use-compression     = "disable"
        setenv.add-response-header = (
            "X-Frame-Options" => "DENY",
            "X-Content-Type-Options" => "nosniff"
        )
        ssl.use-sslv2           = "disable"
        ssl.use-sslv3           = "disable"
    }

You should be pretty much done here, but for a little added privacy for your users, you can [force https using a redirect](#force)

## Force HTTPS<a name="force"></a>

It's generally a good practice to use HTTPS always. There's no real downside to it anymore. Unless you're not [automating renewal](#automate).

    $SERVER["socket"] == ":80" {
        url.redirect = (
            "^/(.*)" => "https://www.example.com/$1"
        )
    }

## Automate Renewal<a name="automate"></a>

Assuming you left the lighty config for `.well-known`, you can just run the sane `certbot` command you used above as a daily cronjob.  

Feel free to [yell at me](mailto:mike@mikeshultz.com) for any errors or omissions.