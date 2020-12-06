# Copyright Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import tools
from odoo.modules import loading

_logger = logging.getLogger(__name__)


def load_module_graph(
    cr,
    graph,
    status=None,
    perform_checks=True,
    skip_modules=None,
    report=None,
    models_to_check=None,
):
    """Suppress commits to have the upgrade of each module in a single
    transaction. This allows you to restart the migration when debugging
    migration scripts. The actual commit is executed when setting the module
    state, in odoo_patch/odoo/addons/base/model/ir_module.py.
    """

    if tools.config.options["test_enable"]:
        _logger.error(
            "Running any kind of test with openupgrade_framework loaded is "
            "currently not supported. It will cause a rollback of your module installation."
        )

    def no_commit(*args):
        pass

    no_commit._original_method = cr.commit
    cr.commit = no_commit

    try:
        res = loading.load_module_graph._original_method(
            cr,
            graph,
            status=status,
            perform_checks=perform_checks,
            skip_modules=skip_modules,
            report=report,
            models_to_check=models_to_check,
        )
        cr.commit._original_method()
    finally:
        cr.commit = cr.commit._original_method
    return res


load_module_graph._original_method = loading.load_module_graph
loading.load_module_graph = load_module_graph
