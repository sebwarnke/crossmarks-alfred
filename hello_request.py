import sys
from workflow import Workflow, web, ICON_WEB


def get_all_bookmarks():
    response = web.get('http://localhost:8080/api/bookmark')
    response.raise_for_status()
    return response.json()


def search_key_for_bookmark(bookmark):
    elements = []
    elements.append(bookmark['name'])
    elements.append(bookmark['url'])
    # elements.append(bookmark['description'])
    return u' '.join(elements)


def main(wf):
    # Get query from Alfred
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    bookmarks_json = wf.cached_data('bookmarks_json', get_all_bookmarks, max_age=60)

    if query:
        bookmarks_json = wf.filter(query, bookmarks_json, key=search_key_for_bookmark)

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