Title: Switched to Jekyll
Date: 2013-07-31 13:58:00
Category: Web
Tags: web, jekyll
Slug: switched-to-jekyll
Authors: Mike Shultz
Summary: I was getting sick of having to use a DB for my personal site.  Not only does it cause a hassle for maintenance, but it wastes resources.  I miss the days of the old static Web, but I don't miss making changes to nav or overall structure across dozens or more HTML files.

Was getting sick of having to use a DB for my personal site.  Not only does it cause a hassle for maintenance, but it wastes resources.  I miss the days of the old static Web, but I don't miss making changes to nav or overall structure across dozens or more HTML files.

I recently heard of [Jekyll](http://jekyllrb.com/), which pre-processes [Markdown](http://daringfireball.net/projects/markdown/) into static HTML Web sites so I had to give it a shot.

## Simplicity

It is just about as easy to update a wiki, with the exception of deployment.  However, that can be scripted, or even automated if you need to take the time.  I'm currently leaning on having the production server do a `git pull` every hour or so off of [Github](http://github.com).  

So the updating process should be about as simple as:

1. Write a new file in markdown
1. Save it
1. Commit the file, then run `git push` to push it up to Github

Then the server should do the rest.

## Gotchas

Since Jekyll was made primarilly for blogs, getting other somewhat dynamic content into the system is tricky.  For my purposes, I wanted to have a section for my projects, as well.

In this case, I basically broke up the `_posts` directory into two sub directories.  Each type used a different `layout`, an that was used to differentiate between the two.  So my directory structure looks like this:

    _posts/blog
    _posts/blog/2013-01-15-akismet-for-django-comments.md
    _posts/blog/2013-07-31-switched-to-jekyll.md
    _posts/projects
    _posts/projects/2012-02-05-ratial.md
    _posts/projects/2012-08-07-pyqual.md
    _posts/projects/2012-03-18-soaked-paper.md
    _posts/projects/2012-01-15-hot-for-congress.md
    _posts/projects/2012-01-15-itchy-puppet.md
    _posts/projects/2013-02-03-corp-tools.md

A blog file would have `layout: post` in the 'front-matter', and projects would have `layout: project`.  In my index file, I make sure to check the `page.layout` variable to figure out what goes where.

    <ul class="posts">
    {% for post in site.posts %}
        {% if post.layout == 'post' %}
        <li>
            <a href="{{ post.url }}">{{ post.title }}</a><br />
            <span>{{ post.date | date_to_string }}</span>
            <p>{{ post.excerpt }}</p>
        </li>
        {% endif %}
    {% endfor %}
    </ul>
    [...]
    <ul class="projects">
    {% for post in site.posts %}
        {% if post.layout == 'project' %}
        <li>
            <a href="{{ post.url }}">{{ post.title }}</a><br />
            <span>Updated {{ post.update | date_to_string }}{% if post.status %} ({{ post.status }}){% endif %}</span>
        </li>
        {% endif %}
    {% endfor %}
    </ul>

This allowed the front page to look like it does.