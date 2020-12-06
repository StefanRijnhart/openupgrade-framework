# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api
from odoo.addons.base.models.ir_module import Module


def write(self, vals):
    """ Execute actual commit when load_module_graph has finished processing a module """
    res = super(Module, self).write(vals)
    if vals.get('state') == 'installed' and hasattr(self.env.cr.commit, '_original_method'):
        self.env.cr.commit._original_method()
    return res


# Original method not present in 14.0
Module.write = write
