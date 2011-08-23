#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
#
# little python script to display events
#
# run it with: python show_event.py -n1
#
# nginx is configured in /etc/nginx/sites-enabled/default to
# forward /events/<id> to this script via FastCGI

from mako.template import Template
from mako.lookup import TemplateLookup
import MySQLdb
import MySQLdb.cursors
import base64

from flup.server.fcgi import WSGIServer
import time, os, sys
import optparse
import re

__usage__ = "%prog -n <num>"
__version__ = "$Id$"
__author__ = "Matt Kangas <matt@daylife.com>"

FCGI_SOCKET_DIR = '/tmp'
FCGI_SOCKET_UMASK = 0111

# Render the template event.mako, which references the templates in ../iMeetUp
mylookup = TemplateLookup(directories=['../iMeetUp'], input_encoding="utf8")
template = Template(filename="event.mako", input_encoding="utf8", lookup=mylookup)
errortemplate = Template(filename="error.mako", input_encoding="utf8", lookup=mylookup)

path_re = re.compile('^/events/([0-9]+)')
img_path_re = re.compile('^/events/img/([0-9]+)')

class template_context:
    def __init__(self, event_id):
        self.template_name = ("/events/%s.de.html.mako" % event_id)

class blogofile:
    def __init__(self, event_id):
        self.template_context = template_context(event_id)

def render_event(start_response, event_id):
    db = MySQLdb.connect(
        user="imeetup",
        passwd="BPPGIVgDBZO4Jymo424OoHh",
        db="imeetup",
        cursorclass=MySQLdb.cursors.DictCursor,
        init_command='SET NAMES utf8',
        charset="utf8",
        use_unicode=True)

    c = db.cursor()
    c.execute("""SELECT \
            da.*, \
            DATE_FORMAT(da.StartDate, '%%d.%%m.%%Y %%H:%%i') AS StartDate, \
            DATE_FORMAT(da.EndDate, '%%d.%%m.%%Y %%H:%%i') AS EndDate, \
            a.Name AS Activity, \
            up.Nickname \
        FROM \
            DatedActivity AS da LEFT JOIN \
            Activity AS a ON (da.ActivityID = a.ActivityID) LEFT JOIN \
            UserProfile AS up ON (da.Host = up.UserID) \
        WHERE \
            ID = %s""", (event_id, ))

    event = c.fetchone()

    if not event:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        page = errortemplate.render(error='No such event', bf=blogofile(event_id))
        return [ unicode(page).encode('utf8') ]

    if event['Privacy'] != 3:
        start_response('403 Forbidden', [('Content-Type', 'text/html')])
        page = errortemplate.render(error='Event is not public', bf=blogofile(event_id))
        return [ unicode(page).encode('utf8') ]

    start_response('200 OK', [('Content-Type', 'text/html')])
    page = template.render(event=event, bf=blogofile(event_id))
    return [ unicode(page).encode('utf8') ]

def render_image(start_response, user_id):
    db = MySQLdb.connect(
        user="imeetup",
        passwd="BPPGIVgDBZO4Jymo424OoHh",
        db="imeetup",
        cursorclass=MySQLdb.cursors.DictCursor,
        init_command='SET NAMES utf8',
        charset="utf8",
        use_unicode=True)

    c = db.cursor()
    c.execute("""SELECT \
            Photo, \
            PhotoPrivacy \
        FROM \
            UserProfile \
        WHERE \
            UserID = %s""", (user_id, ))

    img = c.fetchone()

    if not img:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        page = errortemplate.render(error='No such user')
        return [ unicode(page).encode('utf8') ]

    if img['PhotoPrivacy'] != 3:
# TODO: an error image instead?
        start_response('403 Forbidden', [('Content-Type', 'text/html')])
        page = errortemplate.render(error='Image is not public')
        return [ unicode(page).encode('utf8') ]

    start_response('200 OK', [('Content-Type', 'image/jpeg')])
    return [ base64.b64decode(img['Photo']) ]

def myapp(environ, start_response):
    """Handle /events/<id>"""
    path = environ['PATH_INFO']
    print "Handling ", path
    match = path_re.match(path)
    if match:
        return render_event(start_response, match.group(1))
    
    imgmatch = img_path_re.match(path)
    if imgmatch:
        return render_image(start_response, imgmatch.group(1))

    start_response('404 Not Found', [('Content-Type', 'text/html')])
    page = errortemplate.render(error='Invalid URL')
    return [ unicode(page).encode('utf8') ]

def get_application():
    return myapp

def get_socketpath(name, server_number):
    return os.path.join(FCGI_SOCKET_DIR, 'fcgi-%s-%s.socket' % (name, server_number))

def main(args_in, app_name="event"):
    p = optparse.OptionParser(description=__doc__, version=__version__)
    p.set_usage(__usage__)
    p.add_option("-v", action="store_true", dest="verbose", help="verbose logging")
    p.add_option("-n", type="int", dest="server_num", help="Server instance number")
    opt, args = p.parse_args(args_in)

    if not opt.server_num:
        print "ERROR: server number not specified"
        p.print_help()
        return

    socketfile = get_socketpath(app_name, opt.server_num)
    app = get_application()

    try:
        WSGIServer(app,
               bindAddress = socketfile,
               umask = FCGI_SOCKET_UMASK,
               multiplexed = True,
               ).run()
    finally:
        # Clean up server socket file
        os.unlink(socketfile)

if __name__ == '__main__':
    main(sys.argv[1:])
