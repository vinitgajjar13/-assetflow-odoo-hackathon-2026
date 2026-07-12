# from odoo import http


# class Assetflow-odoo-hackathon-2026(http.Controller):
#     @http.route('/assetflow_odoo_hackathon_2026/assetflow_odoo_hackathon_2026', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/assetflow_odoo_hackathon_2026/assetflow_odoo_hackathon_2026/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('assetflow_odoo_hackathon_2026.listing', {
#             'root': '/assetflow_odoo_hackathon_2026/assetflow_odoo_hackathon_2026',
#             'objects': http.request.env['assetflow_odoo_hackathon_2026.assetflow_odoo_hackathon_2026'].search([]),
#         })

#     @http.route('/assetflow_odoo_hackathon_2026/assetflow_odoo_hackathon_2026/objects/<model("assetflow_odoo_hackathon_2026.assetflow_odoo_hackathon_2026"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('assetflow_odoo_hackathon_2026.object', {
#             'object': obj
#         })

