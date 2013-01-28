# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-
"""
Module for handling calls to the Wageningen University
glastuinbouwmodellen webservice.

Request messages look like this:
<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope
 xmlns:ns0="http://tempuri.org/"
 xmlns:ns1="http://schemas.datacontract.org/2004/07/Dashboard"
 xmlns:ns2="http://schemas.xmlsoap.org/soap/envelope/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Header/>
    <ns2:Body>
        <ns0:Simulate>
            <ns0:parameters>
                <ns1:StartTime>2013-01-27T10:38:56.742287+01:00</ns1:StartTime>
                <ns1:StopTime>2013-01-28T10:38:56.742287+01:00</ns1:StopTime>
            </ns0:parameters>
        </ns0:Simulate>
</ns2:Body>
</SOAP-ENV:Envelope>

Response message look like this:
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body>
        <SimulateResponse xmlns="http://tempuri.org/">
            <SimulateResult xmlns:a="http://schemas.datacontract.org/2004/07/Dashboard" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
                <a:WaterDemand xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0.11315392174303293</b:double>
                    <b:double>0.25328732726397574</b:double>
                    <b:double>0.30107012786278375</b:double>
                    <b:double>0.14407283036718452</b:double>
                    <b:double>0.15134198582018643</b:double>
                    <b:double>0.025092264672822717</b:double>
                    <b:double>0.020259423304625192</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                    <b:double>0</b:double>
                </a:WaterDemand>
            </SimulateResult>
        </SimulateResponse>
    </s:Body>
</s:Envelope>

"""
import datetime
import logging

import suds

from controlnext.utils import round_date


logging.getLogger('suds').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class WURService(object):
    """Service class to consume Wageningen University glastuinmodellen
    webservice.

    """
    WSDL_URL = ('http://www.glastuinbouwmodellen.wur.nl/Dashboard/'
                'Service.svc?wsdl')
    TIMESTAMP_INTERVAL = datetime.timedelta(seconds=60 * 60)  # one hour

    def __init__(self, _from, to, *args, **kwargs):
        self.client = suds.client.Client(self.WSDL_URL)
        # round to the hour
        self._from = round_date(_from, 60)
        self.to = round_date(to, 60)

    def _request_parameters(self):
        """Construct the request parameters. For now, only StartTime
        and StopTime are supported. Update with new parameters when they
        become available.

        For supported parameters see:
        http://www.glastuinbouwmodellen.wur.nl/Dashboard/Service.svc?xsd=xsd2

        """
        parameters = self.client.factory.create('parameters')
        parameters.StartTime = self._from
        parameters.StopTime = self.to
        return parameters

    def get_data(self):
        """Get data based on start and end time. Data is returned based on
        an hourly interval, but does not include timestamps, only floats.
        Data units are in m3 per acre per hour.

        """
        parameters = self._request_parameters()
        logger.debug("About to call WUR webservice.")
        result = self.client.service.Simulate(parameters)
        # returns only floats, no timestamps
        try:
            water_demand_data = result['WaterDemand'][0]
        except KeyError:
            logger.error('Did not receive expected WaterDemand key in '
                         'response.')
            raise
        except IndexError:
            logger.error('Unexpected response.')
            raise
        else:
            # add the hourly timestamps
            output = []
            time = self._from
            for demand_value in water_demand_data:
                output.append((time, demand_value))
                time += self.TIMESTAMP_INTERVAL
            return output
