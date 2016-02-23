from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('api_call', '/api/call')

    config.add_route('vservers', '/vservers')
    config.add_route('vservers_stop', '/vservers/stop/{id}')
    config.add_route('vservers_start', '/vservers/start/{id}')
    config.add_route('vservers_reboot', '/vservers/reboot/{id}')
    config.add_route('vservers_pause', '/vservers/pause/{id}')
    config.add_route('vservers_unpause', '/vservers/unpause/{id}')

    config.add_route('servers', '/servers') # just ajax
    config.add_route('services', '/services') # just ajax

    config.add_route('start_instructions', '/instructions/start/{id}')
    config.add_route('stop_instructions', '/instructions/stop/{id}')

    config.add_route('api_sys', '/api/sys') # cpu report

    config.add_route('delservice', '/delservice/{id}')

    #config.add_route('save', '/save')
    #config.add_route('dsave', '/dsave')
    
    config.scan()
    return config.make_wsgi_app()
