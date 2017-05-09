Title: Setting Up Let's Encrypt With Lighttpd
Date: 2015-12-04 10:20
Category: Security
Tags: letsencrypt, linux, ssl, tls, lighttpd
Slug: setting-up-lets-encrypt-with-lighttpd
Authors: Mike Shultz
Summary: So earlier today(yesterday, now) Let's Encrypt was released as a public beta and thought I'd test it out on this site. The certs that it generates currently have a short expiration(4 months at the time of this writing) but since I'd never pay to encrypt this site but still like having encryption always available, thought I'd give it a shot.

So earlier today(yesterday, now) [Let's Encrypt was released as a public beta](https://letsencrypt.org/2015/12/03/entering-public-beta.html) and thought I'd test it out on this site. The certs that it generates currently have a short expiration(4 months at the time of this writing) but since I'd never pay to encrypt this site but still like having encryption always available, thought I'd give it a shot.

The auto-config stuff doesn't yet work for lighttpd so it requires some manual effort but overall, it's still pretty easy and you don't even have to mess with DNS. This was also build on a RHEL 7 system and destination paths may be different.

**NOTE**: This is still meant for smaller sites, so you really should not bother with this if you've got a full Web cluster or any kind of unique setup. The server will also need to be accessable by the Let's Encrypt servers and an IP list has not been published(that I found). So if you're firewalled, you're either going to have to open up during setup or just get a paid cert with a service that uses other validation means.

## Generating The Certificate

This part is super easy and there's not a whole lot to describe.

## Setup letsencrypt

The following commands need root to fully work properly. First we need to get the letsencrypt package and install it. We'll put it out of the way in /tmp for the time being.

    :::bash
    mkdir /tmp/build && cd /tmp/build

Clone the git repository here.

    :::bash
    git clone https://github.com/letsencrypt/letsencrypt

## Generate Everything!

Move into the directory so we know what to work with cd letsencrypt and we can run the necessary generation command right from here. You can dig further into the letsencrypt options(this will also install packages if the dependencies aren't already met) with ./letsencrypt-auto --help.

Replace the E-mail address and domain name(s) below to suit your own site. The path changes didn't seem to change anything for me, but the default locations worked pretty well. If it hasn't already, this will install dependencies(or try).

    :::bash
    ./letsencrypt-auto certonly --manual --email me@example.com -d example.com -d www.example.com

## Validation

This will now display some instructions on how to deal with validation. It will ask you to create some directories and files for verification and run a temporary Web server on TCP port 80. If you follow these directions to the letter it will work just fine. However, you will have to shut down any current Web servers listening on port 80 but for many of us, myself included, this is not ideal or not possible.

So, I recommend following the directions up until the point where it asks you to start a Web server. We should also make sure lighty has rights to those new files, too.

    :::bash
    chown -R lighttpd:lighttpd /tmp/letsencrypt/public_html

Then, in another SSH session you can add the following to your host/vhost entrie in the lighttpd.conf file and try and put it early in the vhost config, especially if your config is setup to proxy or redirect wildcard URLs.

    :::lighttpd
    ## Used for letsencrypt validation
    $HTTP["url"] =~ "^/.well-known/" {
        server.document-root = "/tmp/letsencrypt/public_html/.well-known/"
        alias.url = ( "/.well-known/" => "/tmp/letsencrypt/public_html/.well-known/" )
        dir-listing.activate = "disable"
    }

This will work for any future validation as well, but you may not want to leave it enabled after you are finished. When you've added the needed directories and files and updated lighty's config, go ahead and reload lighty and test the URL to make sure it works okay. After that all checks out, hit enter on the original terminal so letsencrypt-auto will continue the rest of the validation process.

Now it will automatically generate your private key, CSR, request the signed certificate from Let's Encrypt's servers, and download the needed certificate chain. For me, it put all of the needed PEM files in /etc/letsencrypt/archive/ and symlinked all the current/good ones to /etc/letsencrypt/live/. I'm guessing this is how it will deal with all future renewals by generating new certs in the archive directory and updating the symlink in `live1.

## Setup Certificates For Lighty

Lighty likes its certificates in a specific format to work properly and Let's Encrypt doesn't format them in exactly the way lighttpd wants it. Specifically, it wants the private key and signed certificate in the same PEM file. Simple enough. Just replace the proper directory paths with your own.

    :::bash
    cat /etc/letsencrypt/live/example.com/privkey.pem /etc/letsencrypt/live/example.com/cert.pem > /etc/letsencrypt/live/example.com/combined.pem

The certificates will also need to be readable by lighttpd, so we're going to need to fiddle with the permissions a bit here.

Give lighty group ownership of some directories to it can read and traverse the basic structure. Default permissions should prevent it from seeing more than it should but you may want look over it all when complete just in case.

    :::bash
    chown :lighttpd /etc/letsencrypt
    chown :lighttpd /etc/letsencrypt/archive
    chown :lighttpd /etc/letsencrypt/live

And we'll make sure group owner has read and traverse rights as well.

    :::bash
    chmod g+x /etc/letsencrypt/archive/
    chmod g+x /etc/letsencrypt/live/

Give it a little test and make sure it can read the files okay. It should output with the filetype and not give any errors.

    sudo -u lighttpd file /etc/letsencrypt/live/example.com/cert1.pem

## Configure Lighttpd

So now we just need a pretty simple SSL configuration in your host/vhost configuration. Edit your vhost config or lighttpd.conf and add the following, changing the paths as necessary.

    :::lighttpd
    $SERVER["socket"] == ":443" {
        ssl.engine              = "enable"
        ssl.ca-file             = "/etc/letsencrypt/live/example.com/chain.pem"
        ssl.pemfile             = "/etc/letsencrypt/live/example.com/combined.pemssl.honor-cipher-order  = "enable"
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

The previous SSL configuration is based off best practices laid out by cipherli.st. Please read what they have for more detailed information.

## Force HTTPS

This is optional but if you'd like to force encryption, add a little redirect to your lighty config.

    :::lighttpd
    $SERVER["socket"] == ":80" {
        url.redirect = (
            "^/(.*)" => "https://www.example.com/$1"
        )
    }

## Fin?

Now, in theory, you should be able to reload lighttpd, test out your site, and everything should be good to go. There are probably ways to automate this a bit and everything, but since Let's Encrypt is still in beta, I'm not going to expend the effort just yet.

If you'd like to add anything or have any corrections, please E-mail me at mike@mikeshultz.com...