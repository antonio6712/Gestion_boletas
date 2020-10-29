# -*- coding: utf-8 -*-
from odoo import http

# class Gestionboletas(http.Controller):
#     @http.route('/gestionboletas/gestionboletas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestionboletas/gestionboletas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestionboletas.listing', {
#             'root': '/gestionboletas/gestionboletas',
#             'objects': http.request.env['gestionboletas.gestionboletas'].search([]),
#         })

#     @http.route('/gestionboletas/gestionboletas/objects/<model("gestionboletas.gestionboletas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestionboletas.object', {
#             'object': obj
#         })