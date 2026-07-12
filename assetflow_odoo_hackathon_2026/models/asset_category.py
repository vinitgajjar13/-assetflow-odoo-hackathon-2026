from odoo import fields, models, api


class AssetCategory(models.Model):
    _name = "assetflow.asset.category"
    _description = "Asset Category"
    _order = "name"

    name = fields.Char(string="Category Name", required=True)
    code = fields.Char(string="Category Code", required=True)
    warranty_period = fields.Integer(
        string="Warranty (Months)",
        default=12,
        required=True,
    )
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

    asset_ids = fields.One2many(
        "assetflow.asset",
        "category_id",
        string="Assets",
    )