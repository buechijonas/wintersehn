import typing as t

from searx.plugins import Plugin, PluginInfo

IMAGE_FIELDS = {"img_src", "thumbnail_src", "thumbnail"}


def proxify(result, field_name, url_src):
    if field_name not in IMAGE_FIELDS or not url_src:
        return True
    from searx.webapp import image_proxify

    return image_proxify(url_src) or False


@t.final
class SXNGPlugin(Plugin):
    id = "image_proxy_rewrite"

    def __init__(self, plg_cfg):
        super().__init__(plg_cfg)
        self.info = PluginInfo(
            id=self.id,
            name="Image proxy rewrite",
            description="Route all result images through the image proxy",
            preference_section="privacy",
        )

    def on_result(self, request, search, result):
        result.filter_urls(proxify)
        return True
