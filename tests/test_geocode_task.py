def test():
    from src.tasks import geocode
    import datetime

    data = {u'remoteID': u'132', u'language': {u'nativeName': u'English', u'code': u'en', u'name': u'English'}, u'license': u'unknown', u'tags': [u'death', u'accident', u'road', u'injury'], u'publishedAt': datetime.datetime(2011, 1, 5, 8, 0), u'summary': u'Traffic Accident: Pedestrian was knocked down by a matatu.', u'content': u'Traffic Accident: Pedestrian was knocked down by a matatu.', u'source': u'kenya-traffic-incidents-2011', u'__v': 0, u'lifespan': u'temporary', u'updatedAt': datetime.datetime(2014, 2, 23, 16, 8, 16, 832000), u'_id': '530a1cf010a84e0000392a65', u'geo': {u'addressComponents': {u'adminArea1': u'Kenya', u'neighborhood': u'Yala', u'adminArea4': u'Siaya', u'adminArea5': u'Siaya'}}, u'createdAt': datetime.datetime(2014, 2, 23, 16, 8, 16, 831000)}

    data = geocode.run({})

    assert data['hiphophoray'] == "ho, hey, ho"