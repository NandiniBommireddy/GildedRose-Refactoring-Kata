# -*- coding: utf-8 -*-


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemUpdater:
    def update(self, item):
        self.update_quality(item)
        self.update_sell_in(item)
        if item.sell_in < 0:
            self.update_expired_quality(item)

    def update_quality(self, item):
        self.decrease_quality(item, 1)

    def update_sell_in(self, item):
        item.sell_in -= 1

    def update_expired_quality(self, item):
        self.decrease_quality(item, 1)

    def increase_quality(self, item, amount):
        item.quality = min(50, item.quality + amount)

    def decrease_quality(self, item, amount):
        item.quality = max(0, item.quality - amount)


class AgedBrieUpdater(ItemUpdater):
    def update_quality(self, item):
        self.increase_quality(item, 1)

    def update_expired_quality(self, item):
        self.increase_quality(item, 1)


class BackstagePassUpdater(ItemUpdater):
    def update_quality(self, item):
        increase = 1
        if item.sell_in < 11:
            increase += 1
        if item.sell_in < 6:
            increase += 1
        self.increase_quality(item, increase)

    def update_expired_quality(self, item):
        item.quality = 0


class SulfurasUpdater(ItemUpdater):
    def update(self, item):
        return


class ConjuredUpdater(ItemUpdater):
    def update_quality(self, item):
        self.decrease_quality(item, 2)

    def update_expired_quality(self, item):
        self.decrease_quality(item, 2)


class UpdaterFactory:
    _UPDATERS = {
        "Aged Brie": AgedBrieUpdater(),
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater(),
        "Sulfuras, Hand of Ragnaros": SulfurasUpdater(),
    }

    _CONJURED_PREFIX = "Conjured"

    @classmethod
    def for_item(cls, item):
        if item.name.startswith(cls._CONJURED_PREFIX):
            return ConjuredUpdater()
        return cls._UPDATERS.get(item.name, ItemUpdater())


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            UpdaterFactory.for_item(item).update(item)
