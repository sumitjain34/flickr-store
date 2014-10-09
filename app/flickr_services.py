import requests
import traceback

class FlickrServices:
    def __init__(self):
        print "initializing flickr services"
        self.base_url = 'https://api.flickr.com/services/rest/'
        self.api_key = '111cd221a28c155bbd003a7b42a107f6'

    def make_request(self, url, method='get', params=None, data=None):
        if method == 'get':
            response = requests.get(url, params=params)
        else:
            response = requests.post(url, data=data)
        return response

    def generate_links(self, photo_raw_data):
        images_list = []
        for i in range(0, len(photo_raw_data), 3):
            images = []
            j = i
            for _ in range(3):
                try:
                    raw_data = photo_raw_data[j]
                    j += 1
                    url = 'http://farm%d.staticflickr.com/%s/%s_%s.jpg' % (
                        raw_data['farm'], raw_data['server'], raw_data['id'], raw_data['secret'])
                    images.append(url)
                except:
                    continue
            images_list.append(images)
        return images_list

    def get_images_data(self, search_term=None, page_no=1):
        url = self.base_url
        params = {}
        params['method'] = 'flickr.photos.search'
        params['api_key'] = self.api_key
        params['text'] = search_term
        params['per_page'] = 51
        params['page'] = page_no
        params['format'] = 'json'
        params['nojsoncallback'] = 1
        try:
            response = self.make_request(url=url, params=params)
            print response.status_code
            if response.status_code == 200:
                return response.json()
            else:
                return False
        except Exception as e:
            print traceback.format_exc(e)
            print "Exception in fetching images url"
            return False

    def get_images(self, search_term=None, page_no=1):
        images_data = self.get_images_data(search_term, page_no=page_no)
        total_pages = images_data.get('photos').get('pages')
        photo_raw_data = images_data.get('photos').get('photo')
        images_list = self.generate_links(photo_raw_data)
	print "returning images list"
        return [images_list, total_pages]

