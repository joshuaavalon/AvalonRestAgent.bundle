from base64 import b64encode
from datetime import datetime

import requests
from log import PlexLog


def request_json(url, json):
    PlexLog.debug("Request JSON %s" % str(request_json))
    response = requests.post(url, json=json)
    status_code = response.status_code
    if status_code != 200:
        PlexLog.error("HTTP response (%d)" % status_code)
        return None

    try:
        response_json = response.json()
    except ValueError:
        PlexLog.error("Invalid JSON response")
        return None

    PlexLog.debug("Response JSON: %s" % str(response_json))
    return response_json


def create_id(title, year):
    return b64encode("%s:%d" % (title, year)).replace("/", "_")


def set_metadata_list(metadata, field, source):
    metadata_list = getattr(metadata, field)
    if source is not None and metadata_list is not None:
        metadata_list.clear()
        for value in source:
            metadata_list.add(value)


def set_metadata_list_name(metadata, field, source):
    metadata_list = getattr(metadata, field)
    if source is not None and metadata_list is not None:
        metadata_list.clear()
        for value in source:
            metadata_list.new().name = value


def set_metadata_actors(metadata, actors):
    metadata.roles.clear()
    if actors is None:
        return
    for actor in actors:
        role = metadata.roles.new()
        role.name = actor.get("name")
        role.role = actor.get("role")
        role.photo = actor.get("photo")


def convert_date(date_str):
    if date_str is None:
        return None
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None
    return date


def join_list_or(items, sep=" / ", default=None):
    if items is None or len(items) <= 0:
        return default
    return sep.join(items)


def first_or(items, default=None):
    if items is None or len(items) <= 0:
        return default
    return items[0]


def update_season_summary(media_id, summary):
    if summary is None:
        PlexLog.warn("Missing summary!")
        return
    query = {
        "summary.value": summary
    }
    update_put(media_id, 3, query)


def update_show(media_id, original_title, tagline):
    if original_title is None and tagline is None:
        PlexLog.warn("Missing original_title and tagline!")
        return
    query = {}
    if tagline is not None:
        query["tagline.value"] = tagline
    if original_title is not None:
        query["originalTitle.value"] = original_title
    update_put(media_id, 2, query)


def update_album(media_id, title, collections):
    if title is None and (collections is None or len(collections) < 0):
        return
    query = {}
    if title is not None:
        query["titleSort.value"] = title
        query["titleSort.locked"] = 1

    if collections is not None:
        for i, collection in enumerate(collections):
            query["collection[" + str(i) + "].tag.tag"] = collection
    update_put(media_id, 9, query)


def update_track(media_id, artist):
    if artist is None:
        PlexLog.warn("Missing artist!")
    query = {
        "originalTitle.value": artist
    }
    update_put(media_id, 10, query)


def update_put(media_id, update_type, parameters):
    token = Prefs["Token"]
    if not token:
        PlexLog.warn("Missing token!")
        return
    localhost = "http://127.0.0.1:32400"
    page_url = localhost + "/library/metadata/" + media_id
    xml_element = XML.ElementFromURL(page_url)
    container = xml_element.xpath("//MediaContainer")[0]
    section = String.Unquote(container.get("librarySectionID").encode("utf-8"))
    query = {
        "type": update_type,
        "id": media_id,  # Movie Type 1
        "X-Plex-Token": token
    }
    query.update(parameters)

    request_url = localhost + "/library/sections/" + section + "/all?"
    response = requests.put(request_url, params=query)
    if not response.ok:
        PlexLog.error("Fail to put update (%d)" % response.status_code)
