from odoo import fields, models
from .. import ellipro as EP


class ElliproDataMixin(models.AbstractModel):
    """
    Fields for ellipro informations
    """

    _name = "coreff.ellipro.data.mixin"
    _description = "Coreff Ellipro Data Mixin"

    ellipro_visibility = fields.Boolean(compute="_compute_ellipro_visibility")

    ellipro_identifiant_interne = fields.Char()
    ellipro_siret = fields.Char()
    ellipro_siren = fields.Char()
    ellipro_business_name = fields.Char()
    ellipro_trade_name = fields.Char()
    ellipro_city = fields.Char()
    ellipro_zipcode = fields.Char()
    ellipro_street_address = fields.Char()
    ellipro_phone_number = fields.Char()

    ellipro_order_result = fields.Char()
    ellipro_rating_score = fields.Integer()
    ellipro_rating_riskclass = fields.Integer()
    ellipro_order_product = fields.Char(default="50001")  #! temp

    def _compute_ellipro_visibility(self):
        company = self.env.user.company_id
        for rec in self:
            rec.ellipro_visibility = company.coreff_connector_id == self.env.ref(
                "coreff_ellipro.coreff_connector_ellipro_api"
            )

    def ellipro_get_infos(self):
        for rec in self:
            self.env.user.company_id.pappers_api_token,
            search_type = EP.SearchType.ID
            request_type = EP.RequestType.SEARCH.value
            type_attribute = EP.IdType.ESTB

            admin = EP.Admin(
                self.env.user.company_id.ellipro_contract,
                self.env.user.company_id.ellipro_user,
                self.env.user.company_id.ellipro_password,
            )
            main_only = "true"
            search_request = EP.Search(
                search_type,
                rec.coreff_company_code,
                self.env.user.company_id.ellipro_max_hits,
                type_attribute,
                main_only,
            )
            response = EP.search(admin, search_request, request_type)
            response = EP.search_response_handle(response)[0]

            self.ellipro_identifiant_interne = response.get(
                "ellipro_identifiant_interne", False
            )
            self.ellipro_siret = response.get("ellipro_siret", False)
            self.ellipro_siren = response.get("ellipro_siren", False)
            self.ellipro_business_name = response.get("ellipro_business_name", False)
            self.ellipro_trade_name = response.get("ellipro_trade_name", False)
            self.city = response.get("city", False)
            self.zip = response.get("zip", False)
            self.street = response.get("street", False)
            self.phone = response.get("phone", False)

    def ellipro_order(self):
        request_type = EP.RequestType.ONLINEORDER.value
        order_request = EP.Order(
            self.ellipro_identifiant_interne, self.ellipro_order_product
        )

        admin = EP.Admin(
            self.env.user.company_id.ellipro_contract,
            self.env.user.company_id.ellipro_user,
            self.env.user.company_id.ellipro_password,
        )

        result = EP.search(admin, order_request, request_type)
        parsed_result = EP.parse_order(result)
        self.ellipro_order_result = parsed_result["ellipro_order_result"]
        self.ellipro_rating_score = parsed_result["ellipro_rating_score"]
        self.ellipro_rating_riskclass = parsed_result["ellipro_rating_riskclass"]
