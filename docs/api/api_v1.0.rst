**********************
API v1.0 Documentation
**********************

###
API
###

Variables
*********

When reading this documentation you will find variables in two forms:

* **<variable>**: Variables that are between ``<>`` have to be replaced by their values in the URL. For example, ``/api/v1.0/variables/categories/<category>`` will turn into ``/api/v1.0/variables/categories/my_category``.
* **variable**: Variables that are NOT enclosed by ``<>``:
 * If the method is a GET variables that are between ``<>`` have to be replaced by their values in the URL. For example, ``/api/v1.0/variables/categories/<category>`` will turn into ``/api/v1.0/variables/categories/my_category``.
 * If the method is a POST or a PUT variables variables that are between ``<>`` have to be sent as a JSON object.


Responses
*********

All the responses from the agent will be in JSON format and will include three sections:

* **meta**: Meta information about the response. For example, *request_time*, *length* of the response or if there was any *error*.
* **parameters**: The parameters used for the call.
* **result**: The result of the call or a description of the error if there was any.

For example, for the following call::

    /api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00&net_masks=20,24

You will get the following response:

.. code-block:: json
    :linenos:

    {
      "meta": {
        "error": false,
        "length": 10,
        "request_time": 11.99163
      },
      "parameters": {
        "end_time": "2015-07-14T14:00",
        "exclude_net_masks": false,
        "limit_prefixes": 10,
        "net_masks": "20,24",
        "start_time": "2015-07-13T14:00"
      },
      "result": [
        {
          "as_dst": 43650,
          "key": "194.14.177.0/24",
          "sum_bytes": 650537594
        },
        ...
        {
          "as_dst": 197301,
          "key": "80.71.128.0/20",
          "sum_bytes": 5106731
        }
      ]
    }

#########
Endpoints
#########

Analytics Endpoint
******************

/api/v1.0/analytics/top_prefixes
================================

GET
---

Description
___________

Retrieves TOP prefixes sorted by the amount of bytes that they consumed during the specified period of time.

Arguments
_________

* **start_time**: Mandatory. Datetime in unicode string following the format ``%Y-%m-%dT%H:%M:%S``. Starting time of the range.
* **end_time**: Mandatory. Datetime in unicode string following the format ``%Y-%m-%dT%H:%M:%S``. Ending time of the range.
* **limit_prefixes**: Optional. Number of top prefixes to retrieve.
* **net_masks**: Optional. List of prefix lengths to filter in or out.
* **exclude_net_masks**: Optional. If set to any value it will return prefixes with a prefix length not included in net_masks. If set to 0 it will return only prefixes with a prefix length included in net_masks. Default is 0.
* **filter_proto**: Optional. If you don't set it you will get both IPv4 and IPv6 prefixes. If you set it to 4 you will get only IPv4 prefixes. Otherwise, if you set it to 6 you will get IPv6 prefixes.

Returns
_______

A list of prefixes sorted by sum_bytes. The attribute sum_bytes is the amount of bytes consumed during the specified time.

Examples
--------

::

    http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00
    http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00&net_masks=20,24
    http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00&net_masks=20,24&exclude_net_masks=1


/api/v1.0/analytics/top_asns
============================

GET
---

Description
___________

Retrieves TOP ASN's sorted by the amount of bytes that they consumed during the specified period of time.

Arguments
_________

* **start_time**: Mandatory. Datetime in unicode string following the format ``%Y-%m-%dT%H:%M:%S``. Starting time of the range.
* **end_time**: Mandatory. Datetime in unicode string following the format ``%Y-%m-%dT%H:%M:%S``. Ending time of the range.

Returns
_______

A list of ASN's sorted by sum_bytes. The attribute sum_bytes is the amount of bytes consumed during the specified time.

Examples
--------

::

    http://127.0.0.1:5000/api/v1.0/analytics/top_asns?start_time=2015-07-13T14:00&end_time=2015-07-14T14:00

/api/v1.0/analytics/find_prefix/<prefix>/<prefix_length>
========================================================

GET
---

Description
___________

Finds all prefixes in the system that contains the prefix ``<prefix>/<prefix_length>``

Arguments
_________

* **<<prefix>>**: Mandatory. IP prefix of the network you want to find.
* **<<prefix_length>>**: Mandatory. Prefix length of the network you want to find.
* **date**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``.

Returns
_______

It will return a dictionary where keys are the IP's of the BGP peers peering with SIR. Each one will have a list of prefixes that contain the prefix queried.

Examples
--------

::

    $ curl http://127.0.0.1:5000/api/v1.0/analytics/find_prefix/192.2.3.1/32\?date\=2015-07-22T05:00:01
    {
      "meta": {
        "error": false,
        "length": 2,
        "request_time": 1.88076
      },
      "parameters": {
        "date": "2015-07-22T05:00:01",
        "prefix": "192.2.3.1/32"
      },
      "result": {
        "193.182.244.0": [
          {
            "as_path": "1299 3356",
            "bgp_nexthop": "62.115.48.29",
            "comms": "1299:20000 8403:100 8403:2001",
            "event_type": "dump",
            "ip_prefix": "192.2.0.0/16",
            "local_pref": 100,
            "origin": 0,
            "peer_ip_src": "193.182.244.0"
          }
        ],
        "193.182.244.64": [
          {
            "as_path": "1299 3356",
            "bgp_nexthop": "80.239.132.249",
            "comms": "1299:20000 8403:100 8403:2001",
            "event_type": "dump",
            "ip_prefix": "192.2.0.0/16",
            "local_pref": 100,
            "origin": 0,
            "peer_ip_src": "193.182.244.64"
          }
        ]
      }
    }

/api/v1.0/analytics/find_prefixes_asn/<asn>
===========================================

GET
---

Description
___________

Finds all prefixes in the system that traverses and/or originates in ``<asn>``

Arguments
_________

* **<<asn>>**: Mandatory. ASN you want to query.
* **date**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``.
* **origin_only**: Optional. If set to any value it will return only prefixes that originate in ``<asn>``.

Returns
_______

It will return a dictionary where keys are the IP's of the BGP peers peering with SIR. Each one will have a list of prefixes that traverses and/or originates in ``<asn>``

Examples
--------

::

    curl http://127.0.0.1:5000/api/v1.0/analytics/find_prefixes_asn/345\?date\=2015-07-22T05:00:01\&origin_only=1
    {
      "meta": {
        "error": false,
        "length": 2,
        "request_time": 1.15757
      },
      "parameters": {
        "asn": "345",
        "origin_only": "1",
        "date": "2015-07-22T05:00:01"
      },
      "result": {
        "193.182.244.0": [
          {
            "as_path": "1299 209 721 27064 575 306 345",
            "bgp_nexthop": "62.115.48.29",
            "comms": "1299:25000 8403:100 8403:2001",
            "event_type": "dump",
            "ip_prefix": "55.3.0.0/16",
            "local_pref": 100,
            "origin": 0,
            "peer_ip_src": "193.182.244.0"
          },
          {
            "as_path": "1299 209 721 27065 6025 345",
            "bgp_nexthop": "62.115.48.29",
            "comms": "1299:20000 8403:100 8403:2001",
            "event_type": "dump",
            "ip_prefix": "156.112.250.0/24",
            "local_pref": 100,
            "origin": 0,
            "peer_ip_src": "193.182.244.0"
          }
        ],
        "193.182.244.64": [
          {
            "as_path": "1299 209 721 27064 575 306 345",
            "bgp_nexthop": "80.239.132.249",
            "comms": "1299:25000 8403:100 8403:2001",
            "event_type": "dump",
            "ip_prefix": "55.3.0.0/16",
            "local_pref": 100,
            "origin": 0,
            "peer_ip_src": "193.182.244.64"
          },
          {
            "as_path": "1299 209 721 27065 6025 345",
            "bgp_nexthop": "80.239.132.249",
            "comms": "1299:20000 8403:100 8403:2001",
            "event_type": "dump",
            "ip_prefix": "156.112.250.0/24",
            "local_pref": 100,
            "origin": 0,
            "peer_ip_src": "193.182.244.64"
          }
        ]
      }
    }

Variables Endpoint
******************

/api/v1.0/variables
===================

GET
---

Description
___________

Retrieves all the variables in the system.

Arguments
_________

Returns
_______

A list of all the variables.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables

POST
----

Description
___________

You can create a variable from the CLI with curl like this:

::

    curl -i -H "Content-Type: application/json" -X POST -d '{"name": "test_var", "content": "whatever", "category": "development", "extra_vars": {"ads": "qwe", "asd": "zxc"}}' http://127.0.0.1:5000/api/v1.0/variables

Arguments
_________

* **content**: Content of the variable.
* **category**: Category of the variable.
* **name**: Name of the variable.
* **extra_vars**: Use this field to add extra data to your variable. It is recommended to use a JSON string.

Returns
_______

The variable that was just created.

Examples
________

/api/v1.0/variables/categories
==============================

GET
---

Description
___________

Retrieves all the categories in the system.

Arguments
_________

Returns
_______

A list of all the categories.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories

/api/v1.0/variables/categories/<category>
=========================================

GET
---

Description
___________

Retrieves all the variables the belong to <category> in the system.

Arguments
_________

* **<category>**: Category you want to query.

Returns
_______

A list of variables belonging to <category>.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories/<category>

/api/v1.0/variables/categories/<category>/<name>
================================================

GET
---

Description
___________

Retrieves the variable with <name> and <category>.

Arguments
_________

* **<category>**: Category of the variable you want to retrieve.
* **<name>**: Name of the variable you want to retrieve.

Returns
_______

A list of variables belonging to <category>.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories/<category>/<name>

PUT
---

Description
___________

This API call allows you to modify all of some of the values of a variable. For example, you can update the name and the extra_vars of a variable with the following command:

.. code-block:: json
    :linenos:

     curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "test_varc", "extra_vars": "{'my_param1': 'my_value1', 'my_param2': 'my_value2'}"}' http://127.0.0.1:5000/api/v1.0/variables/categories/development/test_vara HTTP/1.0 200 OK Content-Type: application/json Content-Length: 358 Server: Werkzeug/0.10.4 Python/2.7.8 Date: Tue, 21 Jul 2015 10:16:22 GMT
     {
      "meta": {
        "error": false,
        "length": 1,
        "request_time": 0.0055
      },
      "parameters": {
        "categories": "development",
        "name": "test_vara"
      },
      "result": [
        {
          "category": "development",
          "content": "whatever",
          "extra_vars": "{my_param1: my_value1, my_param2: my_value2}",
          "name": "test_varc"
        }
      ]
      }

Arguments
_________

* **category**: Optional. New category.
* **content**: Optional. New content.
* **name**: Optional. New name.
* **<name>**: Name of the variable you want to modify.
* **<category>**: Category of the variable you want to modify.
* **extra_vars**: Optional. New extra_vars.

Returns
_______

The variable with the new data.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories/<category>/<name>

DELETE
------

Description
___________

Deletes a variable. For example:

.. code-block:: html
    :linenos:

     curl -i -X DELETE http://127.0.0.1:5000/api/v1.0/variables/categories/deveopment/test_vara HTTP/1.0 200 OK Content-Type: application/json Content-Length: 183 Server: Werkzeug/0.10.4 Python/2.7.8 Date: Tue, 21 Jul 2015 10:17:27 GMT
     {
      "meta": {
        "error": false,
        "length": 0,
        "request_time": 0.0016
      },
      "parameters": {
        "categories": "deveopment",
        "name": "test_vara"
      },
      "result": []
     }

Arguments
_________

* **<category>**: Category of the variable you want to delete.
* **<name>**: Name of the variable you want to delete.

Returns
_______

An empty list.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/variables/categories/<category>/<name>

Pmacct Endpoint
***************

/api/v1.0/pmacct/dates
======================

GET
---

Description
___________

Retrieves all the available dates in the system.

Arguments
_________

Returns
_______

A list of all the available dates in the system.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/dates

/api/v1.0/pmacct/flows
======================

GET
---

Description
___________

Retrieves all the available dates in the system.

Arguments
_________

* **start_time**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``. Starting time of the range.
* **end_time**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``. Ending time of the range.

Returns
_______

A list of all the available dates in the system.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/flows?limit_prefixes=10&start_time=2015-07-14T14:00&end_time=2015-07-14T14:01
    http://127.0.0.1:5000/api/v1.0/pmacct/flows?limit_prefixes=10&start_time=2015-07-13T14:00&end_time=2015-07-14T14:00

/api/v1.0/pmacct/bgp_prefixes
=============================

GET
---

Description
___________

Retrieves all the BGP prefixes in the system.

Arguments
_________

* **date**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``.

Returns
_______

A list of all the available BGP prefixes in the system.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/bgp_prefixes?date=2015-07-16T11:00:01

/api/v1.0/pmacct/raw_bgp
========================

GET
---

Description
___________

Retrieves the BGP raw data from pmacct. That includes AS PATH, local-pref, communities, etc....

.. warning:: Do it only if need it. If you have the full feed this can return hundreds of MB of data.

Arguments
_________

* **date**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``.

Returns
_______

The raw data from pmacct.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/raw_bgp?date=2015-07-16T11:00:01

/api/v1.0/pmacct/purge_bgp
==========================

GET
---

Description
___________

Deletes all the BGP data that is older than ``older_than``.


Arguments
_________

* **older_than**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``.

Returns
_______

The list of files containing BGP data that was deleted.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/purge_bgp?older_than=2015-07-29T13:00:01

/api/v1.0/pmacct/purge_flows
============================

GET
---

Description
___________

Deletes all the flows that are older than ``older_than``.


Arguments
_________

* **older_than**: Mandatory. Datetime in unicode string following the format ``'%Y-%m-%dT%H:%M:%S'``.

Returns
_______

The flows that were deleted.

Examples
________

::

    http://127.0.0.1:5000/api/v1.0/pmacct/purge_flows?older_than=2015-07-29T13:00:01
