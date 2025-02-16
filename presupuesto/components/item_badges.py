from typing import Dict, List

import reflex as rx
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)


badge_props = {
    "radius": "full",
    "variant": "surface",
    "size": "3",
    "margin": "5px",
    "cursor": "pointer",
    "style": {"_hover": {"opacity": 0.75}},
}





def _badge(text: str, color_scheme: LiteralAccentColor) -> rx.Component:
    return rx.badge(
        text, color_scheme=color_scheme, radius="large", variant="surface", size="3"
    )


def item_badge(item: str, item_dict: Dict[str, LiteralAccentColor]) -> rx.Component:
    return rx.match(
        item,
        *[(t, _badge(t, item_dict.get(t, "blue"))) for t in item_dict],
        _badge("item", "blue"),
    )