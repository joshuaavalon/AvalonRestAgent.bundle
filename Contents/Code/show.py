from os.path import basename, dirname
from urllib import unquote

from utils import convert_date, first_or, join_list_or, set_metadata_actors, \
    set_metadata_list, set_metadata_list_name, update_show


def as_show(media):
    if hasattr(media, "filename"):
        path = unquote(media.filename).decode("utf8")
    else:
        path = get_show_file(media)
    season_dir = dirname(path)
    show_dir = dirname(season_dir)
    return {
        "path": path,
        "dir": show_dir,
        "file": basename(path)
    }


def set_show(metadata, media, show):
    metadata.title = show.get("title")
    metadata.title_sort = show.get("sort_title")
    metadata.original_title = show.get("original_title")
    metadata.content_rating = show.get("content_rating")
    metadata.studio = first_or(show.get("studio"))
    metadata.originally_available_at = convert_date(show.get("aired"))
    metadata.summary = show.get("summary")
    metadata.rating = show.get("rating")
    set_metadata_list(metadata, "genres", show.get("genres"))
    set_metadata_list(metadata, "collections", show.get("collections"))
    set_metadata_actors(metadata, show.get("actors"))

    original_title = show.get("original_title")
    tagline = join_list_or(show.get("tagline"))
    update_show(media.id, original_title, tagline)


def get_show_file(media):
    for season in media.seasons:
        for episode in media.seasons[season].episodes:
            e = media.seasons[season].episodes[episode]
            return e.items[0].parts[0].file
    return None


def as_episode(media, season, episode):
    if hasattr(media, "filename"):
        path = unquote(media.filename).decode("utf8")
    else:
        path = get_show_file(media)
    season_dir = dirname(path)
    episode_obj = {
        "path": path,
        "dir": season_dir,
        "file": basename(path),
        "season": int(season),
        "episode": int(episode)
    }
    return episode_obj


def set_episode(metadata, episode):
    metadata.title = join_list_or(episode.get("title"))
    metadata.content_rating = episode.get("content_rating")
    metadata.originally_available_at = convert_date(episode.get("aired"))
    metadata.summary = episode.get("summary")
    metadata.rating = episode.get("rating")
    writers = [
        w.get("name") for w in episode.get("writers", [])
        if w.get("name") is not None
    ]
    directors = [
        d.get("name") for d in episode.get("directors", [])
        if d.get("name") is not None
    ]
    set_metadata_list_name(metadata, "writers", writers)
    set_metadata_list_name(metadata, "directors", directors)
