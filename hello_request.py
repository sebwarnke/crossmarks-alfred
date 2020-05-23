import sys
from workflow import Workflow, web, ICON_WEB


def main(wf):
    response = web.get('http://localhost:8080/api/bookmark')

    bookmarks_json = response.json()
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

# for bookmark in bookmarks:
#     print('\n------\n')
#     print('ID:   ' + bookmark['id'])
#     print('Name: ' + bookmark['name'])
#     print('Url:  ' + bookmark['url'])
#     print('Created at: ' + bookmark['createdAt'])
#
#     if bookmark['description'] is not None:
#         print('Description:  ' + bookmark['description'])
