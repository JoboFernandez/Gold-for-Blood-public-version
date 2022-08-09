import json


def get_how_to_play_content():
    with open("assets/how_to_play.json", "r") as f:
        htp_details = json.load(f)
        _intro = htp_details["intro"]
        _sections = htp_details["sections"]

    _content = f"{_intro}\n"
    for _section, _informations in _sections.items():
        _content += f"\n{_section.title()}\n"
        for _information in _informations:
            _content += f"\t{_information}\n"

    return _content


def get_credits_content():
    with open("assets/credits.json", "r") as f:
        credits_details = json.load(f)
        _intro = credits_details["intro"]
        _sections = credits_details["sections"]
        _outro = credits_details["outro"]

    _content = f"{_intro}\n"
    for _section, _references in _sections.items():
        _content += f"\n{_section.title()}\n"
        for _reference in _references:
            _content += f"\t{_reference}\n"
    _content += f"\n{_outro}"

    return _content

