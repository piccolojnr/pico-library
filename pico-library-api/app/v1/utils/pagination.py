from flask import url_for


def _pagination_nav_links(pagination, endpoint):
    nav_links = {}
    per_page = pagination["items_per_page"]
    this_page = pagination["page"]
    last_page = pagination["total_pages"]
    nav_links["self"] = url_for(f"api.{endpoint}", page=this_page, per_page=per_page)
    nav_links["first"] = url_for(f"api.{endpoint}", page=1, per_page=per_page)
    if pagination["has_prev"]:
        nav_links["prev"] = url_for(
            f"api.{endpoint}", page=this_page - 1, per_page=per_page
        )
    if pagination["has_next"]:
        nav_links["next"] = url_for(
            f"api.{endpoint}", page=this_page + 1, per_page=per_page
        )
    nav_links["last"] = url_for(f"api.{endpoint}", page=last_page, per_page=per_page)
    return nav_links


def _pagination_nav_header_links(pagination, endpoint):
    url_dict = _pagination_nav_links(pagination, endpoint)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f"<{url}>; rel={rel}"
    return link_header.strip().strip(",")
