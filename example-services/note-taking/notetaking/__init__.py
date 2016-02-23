from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('compose', '/compose')
    config.add_route('delete', '/delete')
    config.add_route('apiinsert','/api/insert')
    config.add_route('apidelete','/api/delete')
    config.add_route('apilist','/api/list')
    config.scan()
    return config.make_wsgi_app()
