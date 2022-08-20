from .controller import index, userRegister, userLogin, add_get_Temp, get_upd_del_Temp


def initialize_routes(api):
    api.add_resource(index, '/')
    api.add_resource(userRegister, '/register')
    api.add_resource(userLogin, '/login')
    api.add_resource(add_get_Temp, '/template')
    api.add_resource(get_upd_del_Temp, '/template/<template_id>')

    
