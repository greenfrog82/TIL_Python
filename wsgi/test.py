def application(env, start_response):
    start_response('200 OK', [('Context-Type', 'text/html')])
    return [b'Hello World'] # Python3
    # return ['Hello World'] # Python2