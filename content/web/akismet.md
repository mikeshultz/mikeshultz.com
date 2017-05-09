Title: Akismet Spam Checking for django.contrib.comments
Date: 2013-01-15 11:04:12
Category: Web
Tags: web, akismet, django
Slug: akismet-spam-checking-for-django-contrib-comments
Authors: Mike Shultz
Summary: So I was trying to get Akismet working on our comments system the other day. I ran across Brant Steen's Post for a way to use Django signals to handle it. Sadly, this was out of sync with the Akismet python library. So, I updated it and here's the end result.

So I was trying to get Akismet working on our comments system the other day. I ran across Brant Steen's Post for a way to use Django signals to handle it. Sadly, this was out of sync with the [Akismet python library](http://www.voidspace.org.uk/python/akismet_python.html). So, I updated it and here's the end result:

    :::python
    from django.contrib.comments.models import Comment
    from django.contrib.comments.signals import comment_will_be_posted
    from akismet import Akismet, AkismetError
    from django.conf import settings

    def spam_check(sender, comment, request, **kwargs):
        api = Akismet(agent="Python Request/1.0")
        api.setAPIKey(settings.AKISMET_KEY, 'http://example.com')

        try:
            real_key = api.verify_key()
            if real_key:
                is_spam = api.comment_check(
                    comment.comment, 
                    data={
                        'user_ip': request.META.get('HTTP_X_FORWARDED_FOR') or request.META['REMOTE_ADDR'], 
                        'permalink': comment.get_absolute_url(),
                        'user_agent': request.META.get('HTTP_USER_AGENT'),
                    }
                )
                if is_spam:
                    return False
                else:
                    return True
            else:
                print 'Warning: key is invalid?'
        except AkismetError, e:
            logger.warning('Error:Something went wrong, allowing comment. %s:%s' % (e.response, e.statuscode))
            return True

    comment_will_be_posted.connect(spam_check,sender=Comment,dispatch_uid="comment_spam_check_akismet")

I added the import statement for the above `signals.py` to my project-app folder's `___init___.py` file to make sure it was imported and connected properly. So far, so good. Though you may want to setup a 400 error page, if you want to be nice to any false-positives.