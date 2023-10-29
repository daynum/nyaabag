import requests
import index_parser
import torrent


class Nyaa:

    def __init__(self):
        self.SITE = index_parser.TorrentSite.NYAASI
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0'}


    def last_uploads(self, number_of_results):
        r = requests.get(self.SITE.value, headers=self.headers)

        # If anything up with nyaa servers let the user know.
        r.raise_for_status()

        json_data = index_parser.parse_nyaa(
            request_text=r.text,
            limit=number_of_results + 1,
            site=self.SITE
        )
        return torrent.json_to_class(json_data)

    def search(self, keyword, **kwargs):
        url = self.SITE.value

        user = kwargs.get('user', None)
        category = kwargs.get('category', 0)
        subcategory = kwargs.get('subcategory', 0)
        filters = kwargs.get('filters', 0)
        page = kwargs.get('page', 0)

        if user:
            user_uri = f"user/{user}"
        else:
            user_uri = ""

        if page > 0:
            r = requests.get("{}/{}?f={}&c={}_{}&q={}&p={}".format(
                url, user_uri, filters, category, subcategory, keyword,
                page), headers=self.headers)
        else:
            r = requests.get("{}/{}?f={}&c={}_{}&q={}".format(
                url, user_uri, filters, category, subcategory, keyword), headers=self.headers)

        r.raise_for_status()

        json_data = index_parser.parse_nyaa(
            request_text=r.text,
            limit=None,
            site=self.SITE
        )

        return torrent.json_to_class(json_data)

    def get(self, view_id):
        r = requests.get(f'{self.SITE.value}/view/{view_id}', headers=self.headers)
        r.raise_for_status()

        json_data = index_parser.parse_single(request_text=r.text, site=self.SITE)

        return torrent.json_to_class(json_data)

    def get_user(self, username):
        r = requests.get(f'{self.SITE.value}/user/{username}', headers=self.headers)
        r.raise_for_status()

        json_data = index_parser.parse_nyaa(
            request_text=r.text,
            limit=None,
            site=self.SITE
        )
        return torrent.json_to_class(json_data)
