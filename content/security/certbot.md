Title: Setting Up Let's Encrypt With Lighttpd (Using Certbot)
Date: 2017-05-09 21:17
Category: Security
Tags: letsencrypt, linux, ssl, tls, lighttpd, certbot
Slug: setting-up-lets-encrypt-with-lighttpd-and-certbot
Authors: Mike Shultz
Summary: Finally gotting around to updating my previous post on Let's Encrypt and lighttpd

Finally gotting around to updating my previous post on [Let's Encrypt](https://letsencrypt.org) and lighttpd.  I'll assume you're generally familiar with both. 

**NOTE**: If you have a full Web cluster, load balancer, or something behind a firewall, please consider going the traditional route of getting a certificate.  It won't waste Let's Encrypt's resources, and you'll have a much easier time getting it setup.

## Install 

Folow the [EFF docs to get certbot installed for your distro](https://certbot.eff.org).  Come back here before you generate the certificate.

## Generate The Certificate

Choose one of the following options only.  The first one is the easy way, but will require you to take down lighty.  The second one is a more high-availability way of doing things.

### The Easy Way<a name="easyway"></a>

**NOTE**: If you don't want to take down lighty during this process, see the section [The Hard Way](#hardway).

First off, shut down lighty.  We want to get `certbot` up and running on standard Web ports, so we can't have anything conflicting there.  The following command may be different for your distro.

    systemctl stop lighttpd

Now we can validate, generate, and fetch our new certificate with one simple command.

    certbot certonly --standalone -d example.com -d www.example.com

This will get what we need and organize it under `/etc/letsencrypt/live/example.com/`.  Go ahead and start lighty again.

    systemctl start lighttpd

And skip ahead to [Reformat For Lighttpd](#reformat)

### The Hard Way<a name="hardway"></a>

#### Create The Web Root

Create the Web root and make sure lighty has permissions to access these files.

    mkdir -p /var/letsencrypt && chown -R lighttpd:lighttpd /var/letsencrypt

#### Configure Lighttpd

Now we need to configure lighty to serve these validation files on your new domain.  Edit `lighttpd.conf` or `vhosts.d/mysite.conf`, whichever you use and add the following: 

    ## Used for letsencrypt validation
    $HTTP["url"] =~ "^/.well-known/" {
        server.document-root = "/var/certbot/public_html/.well-known/"
        alias.url = ( "/.well-known/" => "/var/certbot/public_html/.well-known/" )
        dir-listing.activate = "enable"
    }

This will work for any future validation as well, but you may not want to leave it enabled after you are finished.  I'm assuming the ACME validation uses one time use tokens, but I haven't dug into the source to find out, so either do the research yourself or just disable it when we're done.  Now reload lighty to bring in the new conf.

    systemctl reload lighttpd

**OR** with lighttpd-angel

    kill -HUP `cat /var/run/lighttpd.pid`

`certbot` should go through the motions and finish validation after this. **VERIFY ME**  It should generate your private key, CSR, and get the requested certificate and cert chain from Let's Encrypt. It should put all these files in `/etc/letsencrypt/live/example.com/`.

#### Run Certbot

So, we need to use the setgid sticky bit here so when certbot runs, it creates the directory with permissions that lighty can read.

    :::bash
    sudo -u lighttpd mkdir -p /var/certbot/public_html/.well-known/
    chmod g+s /var/certbot/public_html/.well-known

Now you can run certbot to generate and fetch your new cert.

    :::bash
    certbot certonly --webroot -w /var/certbot/public_html -d example.com -d www.example.com

## Reformat For Lighttpd<a name="reformat"></a>

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

## Configure Lighttpd

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

It's generally a good practice to use HTTPS always. There's no real downside to it anymore.

    $SERVER["socket"] == ":80" {
        url.redirect = (
            "^/(.*)" => "https://www.example.com/$1"
        )
    }

## Automate Renewal

Assuming you left the lighty config for `.well-known`, you can just run the sane `certbot` command you used above as a daily cronjob.

Feel free to [yell at me](mailto:mike@mikeshultz.com) for any errors or omissions.