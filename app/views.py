from app import app
from flask import render_template
from flask import request
import traceback
from .dbhelper import get_history
from .dbhelper import save_history
from flickr_services import FlickrServices
from .utils import solve_pagination

@app.route('/')
@app.route('/index')
def index():
    title = 'Flickr Store'
    return render_template('index.html', title=title, active='')

@app.route('/images', methods=['GET', 'POST'])
def image_search():
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Searching Image %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    try:
        user_ip = request.remote_addr
        search_term = request.args['searchterm']
        page_no = int(request.args.get('page_no',0))
        if not page_no:
            page_no=1
        save_history(user_ip=user_ip, search_term=search_term)
        flickr = FlickrServices()
        data = flickr.get_images(search_term=search_term, page_no=page_no)
        images_list = data[0]
        total_pages = data[1]
        paginator=solve_pagination(total_pages,page_no)
        start_page=paginator[0]
        end_page=paginator[1]
        pages_list = [i for i in range(start_page, end_page + 1)]
        if not images_list:
            print "images fetched"
            currentpage = None
            pages_list = None
            search_term = None
        return render_template('images.html', title='Images', images_list=images_list, total_pages=total_pages, currentpage=page_no, active='search', pages_list=pages_list, search_term=search_term)
    except Exception as e:
        print traceback.format_exc(e)
        return "Ooops...There is some problem"

@app.route('/search', methods=['GET', 'POST'])
def search():
    title = 'Search Image'
    return render_template('search.html', title=title, active='search')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_ip = request.remote_addr
    search_terms = get_history(user_ip=user_ip)
    return render_template('dashboard.html', title='Dashboard', search_terms=search_terms, active='dashboard')
