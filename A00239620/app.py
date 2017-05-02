from flask import Flask, request
from model import db
from register_data import RegisterTimer
from flask_restplus import Api, Resource, fields
import my_utils
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/check_user/parcial2_villegas/data.db'
api = Api(app, version='1.0', title='API for check system variables', description='An API to check system variables such as free ram, cpu usage and free disk')
ns = api.namespace('v1.0/checks', description='Operations related to check system variables')

db.app = app
db.init_app(app)

db.create_all()
thread = RegisterTimer(60)
thread.start()

model1 = api.model('checks',{
    'checks': fields.List(fields.String),
})

@ns.route('/')
class Check(Resource):
    @api.response(200, 'List of checks succesfully returned', model1)
    def get(self):
        ''' return the check that can be made by the user '''
        ret = {}
        ret['data'] = ['cpu', 'ram', 'disk']
        return ret;


parser = api.parser()
parser.add_argument('size', type=int, help='parameter for size history', location='query', )

@ns.route('/<string:type>/hisotry')
class CheckHistory(Resource):
    @api.response(200, 'history of data of a specify check')
    @api.response(404, 'the type check doesnt exist')
    @api.expect(parser)
    def get(self, type):
        ''' return the of data of a specified '''

        size = int(request.args.get('size',1))
        data = {}
        if type == 'cpu':
            data['data'] = my_utils.get_cpu_history(size)
        elif type == 'ram':
            data['data'] = my_utils.get_free_ram_history(size)
            pass
        elif type == 'disk':
            data['data'] = my_utils.get_free_disk_history(size)
            pass
        else:
            return "check %s doesn't exist" % type , 404 

        return json.dumps(data)


if __name__ == "__main__":
    app.run('0.0.0.0', port=8080)
    thread.stop()
    
    
      
    