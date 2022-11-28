odoo.define('coreff.autocomplete.core', function (require) {
    'use strict';

    var rpc = require('web.rpc');
    var session = require('web.session');
    var concurrency = require('web.concurrency');

    var Autocomplete = {
        _dropPreviousOdoo: new concurrency.DropPrevious(),
        _dropPreviousClearbit: new concurrency.DropPrevious(),
        _timeout : 1000, // Timeout for Clearbit autocomplete in ms

        autocomplete: function (value, valueIsCompanyCode, countryId, isHeadOffice) {
            value = value.trim();
            var self = this;
            var def = $.Deferred();
                self._getCompanies(valueIsCompanyCode, countryId, isHeadOffice, value).then(res => {
                    if ("error" in res) {
                        return def.reject(res.error);
                    }
                    else {
                        return def.resolve(res);
                    }
                });

                return def;
        },

        getCreateData: function (company) {
            var self = this;
            var def = $.Deferred();
            var company_data = company;
            
            const getCountryId = async (company) => {
                var countryId;
                countryId = await self._getCountryId(company.country_id);
                return countryId;
            };
            getCountryId(company).then(res => {
                company_data.country_id = res;
                def.resolve({
                    company: company_data
                });
            });
            return def;
        },

        isOnline: function () {
            return navigator && navigator.onLine;
        },

        validateSearchTerm: function (search_val, onlyCompanyCode) {
            if (onlyCompanyCode) {
                return search_val && search_val.length > 8;
            }
            else {
                return search_val && search_val.length > 3;
            }
        },

        getUser: function () {
            return rpc.query({
                model: 'res.users',
                method: 'read',
                args: [session.uid, ['name', 'company_id']],
            }).then(function (res) {
                return res[0];
            });
        },

        getConnector: function (company_id) {
            return rpc.query({
                model: 'res.company',
                method: 'read',
                args: [company_id, ['name', 'coreff_connector_id']]
            }).then(function (res) {
                return res[0];
            });
        },

        getFieldList: function (connector_id) {
            return rpc.query({
                model: 'coreff.connector',
                method: 'read',
                args: [connector_id, ['name', 'autocomplete_fields']]
            }).then(function (res) {
                return res[0];
            })
        },

        _getCompanies: function (valueIsCompanyCode, countryId, isHeadOffice, value) {
            var data = {};
            data.valueIsCompanyCode = valueIsCompanyCode;
            data.country_id = countryId;
            data.is_head_office = isHeadOffice;
            data.value = value;
            data.user_id = session.uid;
            return rpc.query({
                model: 'coreff.api',
                method: 'get_companies',
                args: [data],
            }).then(function (res) {
                return res;
            });
        },

        _getCountryId: function (code) {
            var domain = [['code', '=', code]];

            return rpc.query({
                model: 'res.country',
                method: 'search_read',
                args: [domain]
            }).then(function (res) {
                return res[0];
            });
        }

    };

    return Autocomplete;
});
