# ©2021 - Chris Mann (Open User Systems)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models
from odoo.exceptions import UserError
import urllib.parse


class CrmLead(models.Model):
    """
    Fields for creditsafe informations
    """

    _inherit = "crm.lead"

    def creditsafe_lookup(self):
        if self.partner_name is not False:
            company_name = urllib.parse.quote(self.partner_name)
            creditsafe_url = "https://app.creditsafe.com/search"
            creditsafe_params = f"?limit=15&name={company_name}&page=1"

            action = {
                "type": "ir.actions.act_url",
                "target": "new",
                "url": creditsafe_url + creditsafe_params,
            }
            return action
        else:
            raise UserError(
                "Missing [Company Name] to perform Creditsafe lookup."
            )
            return False
