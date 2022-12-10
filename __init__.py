import sys
import os
import time
from flask import Flask, current_app
# from flask_sitemap import Sitemap

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f'{ path }/tools/')
sys.path.append(f'{ path }/scripts/')

app = Flask(__name__)
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
# ext = Sitemap(app=app)


with app.app_context():

    import routes

#     @ext.register_generator
#     def movie_views():
#         yield 'movie_views', {'id': 'id'}, time.strftime('%Y-%m-%d'), 'always', 0.7
#     @ext.register_generator
#     def serie_views():
#         yield 'serie_views', {'id': 'id'}, time.strftime('%Y-%m-%d'), 'always', 0.7


if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
