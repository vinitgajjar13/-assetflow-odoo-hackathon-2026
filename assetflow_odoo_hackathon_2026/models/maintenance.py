from odoo import fields, models, api


class Maintenance(models.Model):
    _name = "assetflow.maintenance"
    _description = "Asset Maintenance"
    _order = "id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )
    asset_id = fields.Many2one(
        "assetflow.asset",
        string="Asset",
        required=True,
    )
    issue = fields.Text(string="Issue Description")
    technician = fields.Char(string="Technician")
    maintenance_date = fields.Date(string="Maintenance Date")
    cost = fields.Float(string="Maintenance Cost")
    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("progress", "In Progress"),
            ("done", "Done"),
        ],
        default="pending",
        string="Status",
    )