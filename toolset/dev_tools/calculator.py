

def calculate(args): # formula: str
    try:
        return {'result': eval(args['formula']), 'status': 'success'}
    except Exception as e:
        return {'error': e, 'status': 'error'}

