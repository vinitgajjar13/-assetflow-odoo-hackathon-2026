# from odoo import models, fields, api


# class assetflow_odoo_hackathon_2026(models.Model):
#     _name = 'assetflow_odoo_hackathon_2026.assetflow_odoo_hackathon_2026'
#     _description = 'assetflow_odoo_hackathon_2026.assetflow_odoo_hackathon_2026'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

