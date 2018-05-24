import json

def check_json_response(resp):
    assert resp.status_code == 200, "Expected http response status to be '%s' but was '%s'." % (200, resp.status_code)
    ret = json.loads(resp.text)
    assert ret['statusCode'] == '0', "Expected json statusCode to be '%s' but was '%s' : %s." % ('0', ret['statusCode'],ret['statusDesc'])
    return ret
