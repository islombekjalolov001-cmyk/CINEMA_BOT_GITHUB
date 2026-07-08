"""Small helpers shared by every paginated inline keyboard."""
from __future__ import annotations

import math


def total_pages(total_items: int, page_size: int) -> int:
    if total_items <= 0:
        return 1
    return math.ceil(total_items / page_size)


def offset_for_page(page: int, page_size: int) -> int:
    """`page` is 1-indexed."""
    return max(page - 1, 0) * page_size


def clamp_page(page: int, pages: int) -> int:
    return min(max(page, 1), max(pages, 1))
