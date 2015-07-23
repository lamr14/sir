import helpers.api
from flask import g


def top_prefixes(request):
    # curl http://127.0.0.1:5000/api/v1.0/top_prefixes\?limit_prefixes=10\&start_time\=2015-07-13T14:00\&end_time\=2015-07-14T14:00
    db = getattr(g, 'db')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    limit_prefixes = int(request.args.get('limit_prefixes', 0))
    net_masks = request.args.get('net_masks', '')
    exclude_net_masks = request.args.get('exclude_net_masks', False)

    result = db.aggregate_per_prefix(
        start_time, end_time,
        limit=limit_prefixes,
        net_masks=net_masks,
        exclude_net_masks=exclude_net_masks)

    parameters = {
        'limit_prefixes': limit_prefixes,
        'start_time': start_time,
        'end_time': end_time,
        'net_masks': net_masks,
        'exclude_net_masks': exclude_net_masks,
    }
    return helpers.api.build_api_response(result, error=False, **parameters)


def top_asns(request):
    # curl http://127.0.0.1:5000/api/v1.0/top_asns\?start_time=2015-07-13T14:00\&end_time=2015-07-14T14:00
    db = getattr(g, 'db')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    result = db.aggregate_per_as(start_time, end_time)
    parameters = {
        'start_time': start_time,
        'end_time': end_time,
    }
    return helpers.api.build_api_response(result, error=False, **parameters)


def find_prefix(request, prefix):
    # curl http://127.0.0.1:5000/api/v1.0/top_asns\?start_time=2015-07-13T14:00\&end_time=2015-07-14T14:00
    fs = getattr(g, 'fs')
    date = request.args.get('date')
    print date
    result = fs.find_prefix(prefix, date)
    parameters = {
        'prefix': prefix,
        'date': date,
    }
    return helpers.api.build_api_response(result, error=False, **parameters)
