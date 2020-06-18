import sys
import argparse
from workflow import Workflow, web, ICON_WEB, ICON_WARNING, PasswordNotFound


def get_all_bookmarks(username, password):
    response = web.get('http://localhost:8080/api/bookmark', auth=(username, password), params=dict())
    response.raise_for_status()
    return response.json()


def search_key_for_bookmark(bookmark):
    elements = []
    elements.append(bookmark['name'])
    elements.append(bookmark['url'])
    # elements.append(bookmark['description'])
    return u' '.join(elements)


def main(wf):

    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest='username', default=None)
    parser.add_argument('--pass', dest='password', default=None)
    parser.add_argument('query', nargs='?', default=None)

    args = parser.parse_args(wf.args)

    if args.username and args.password:
        wf.settings['username'] = args.username
        wf.save_password('crossmarks_password', args.password)
        return 0

    username = wf.settings.get("username")

    try:
        password = wf.get_password("crossmarks_password")
    except PasswordNotFound:
        wf.add_item('No password set.',
                    'Please use cmlogin to store your credentials.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    if not (username and password):
        wf.add_item('Credentials missing!',
                    'Please set username and password to connect with Crossmarks',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback();
        return 0

    query = args.query

    def wrapper():
        return get_all_bookmarks(username, password)

    bookmarks_json = wf.cached_data('bookmarks_json', wrapper, max_age=60)

    if query:
        bookmarks_json = wf.filter(query, bookmarks_json, key=search_key_for_bookmark, min_score=20)

    if not bookmarks_json:  # we have no data to show, so show a warning and stop
        wf.add_item('No bookmarks found', icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    for bookmark_json in bookmarks_json:
        wf.add_item(title=bookmark_json['name'],
                    subtitle=bookmark_json['url'],
                    valid=True,
                    arg=bookmark_json['url'],
                    icon=ICON_WEB)
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))