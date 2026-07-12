from odoo import models, fields, api


class Booking(models.Model):
    _name = "assetflow.booking"
    _description = "Resource Booking"
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
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
    )
    start_datetime = fields.Datetime(string="Start Date Time")
    end_datetime = fields.Datetime(string="End Date Time")
    purpose = fields.Text(string="Purpose")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("approved", "Approved"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        string="Status",
    )