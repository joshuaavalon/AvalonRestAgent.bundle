import hashlib
from os.path import basename, dirname, exists, join
from urllib import unquote

from log import PlexLog
from mutagen import File
from utils import convert_date, set_metadata_list, update_album, update_track


def as_album(media):
    path = get_album_file(media)
    album_dir = dirname(path)
    return {
        "path": path,
        "dir": album_dir,
        "file": basename(path)
    }


def set_album(metadata, media, album):
    metadata.summary = album.get("summary")
    metadata.rating = album.get("rating")
    set_metadata_list(metadata, "genres", album.get("genres"))
    set_metadata_list(metadata, "collections", album.get("collections"))
    aired = convert_date(album.get("aired"))
    metadata.originally_available_at = aired

    update_album(media.id, media.title, album.get("collections"))

    set_album_cover(metadata, album)

    for track in media.children:
        part = track.items[0].parts[0].file
        update_tracks(track.id, part)


def update_tracks(media_id, track_file):
    try:
        tags = File(track_file, None, True)
        artist_str = " / ".join(tags["artist"])
        update_track(media_id, artist_str)
    except Exception, e:
        PlexLog.error(e)


def set_album_cover(metadata, media):
    path = get_album_file(media)
    album_dir = dirname(path)
    file_path = join(album_dir, "cover.jpg")
    if not exists(file_path):
        file_path = join(album_dir, "cover.png")
    if not exists(file_path):
        return
    cover = Core.storage.load(file_path)
    key = hashlib.md5(cover).hexdigest()
    metadata.posters[key] = Proxy.Media(cover)


def get_album_file(media):
    if hasattr(media, "filename"):
        return unquote(media.filename).decode("utf8")
    for track in media.children:
        return track.items[0].parts[0].file
