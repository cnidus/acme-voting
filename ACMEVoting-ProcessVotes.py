from chalice import Chalice

app = Chalice(app_name='ACMEVoting-ProcessVotes')

@app.route('/CastVote', methods=['POST', 'PUT'])
def CastVote(key):
    request = app.current_request
    if request.method == 'PUT':
        stagedvotes[key] == request.json_body
    elif request.method == 'POST':
        stagedvotes[key] == request.json_body

    identity = request.context['identity']

    return identity

@app.route('/GetVotes', methods=['POST', 'PUT'])
def GetVotes(key):
    request = app.current_request
    return request
