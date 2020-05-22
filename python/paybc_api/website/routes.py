from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from python.paybc_api.website.oauth2 import authorization, require_oauth


bp = Blueprint(__name__, 'home')


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@bp.route('/search', methods=['POST'])
@require_oauth()
def search():
    if request.method == 'POST':
        # lookup the request using the VIPS API
        posted_data = request.get_json()
        return jsonify(search_for_invoice(posted_data))


@bp.route('/invoice/<invoice_number>', methods=['GET'])
@require_oauth()
def show(invoice_number):
    if request.method == 'GET':
        # lookup the request using the VIPS API
        return jsonify(get_invoice(invoice_number))


def search_for_invoice(posted_data):
    if posted_data is not None and posted_data['invoice_number'] == 1234 and posted_data['check'] == 4321:
        return dict({
            "items": [
                {"url": request.host_url + 'invoice/1234'}
            ]
        })
    else:
        return dict({
            "error": 'An IRP Review invoice with that number was not found'
        })


def get_invoice(invoice_number):
    if invoice_number == '1234':
        return dict({
            "items": [
                {"url": request.host_url + 'invoice/1234'}
            ]
        })
    else:
        return dict({
            "error": 'We are unable to find invoice ' + invoice_number
        })
