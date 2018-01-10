def includeme(config): 
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('admin', '/admin')
    config.add_route('students', '/student')
    config.add_route('student', '/student/{s}')
    config.add_route('professors', '/professor')
    config.add_route('professor', '/professor/{p}')
