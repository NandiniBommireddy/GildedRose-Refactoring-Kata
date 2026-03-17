# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def update_item(self, name, sell_in, quality):
        item = Item(name, sell_in, quality)
        GildedRose([item]).update_quality()
        return item

    def test_conjured_item_degrades_twice_as_fast_before_sell_date(self):
        item = self.update_item("Conjured Mana Cake", 3, 6)

        self.assertEqual(2, item.sell_in)
        self.assertEqual(4, item.quality)

    def test_conjured_item_degrades_four_times_after_sell_date(self):
        item = self.update_item("Conjured Mana Cake", 0, 6)

        self.assertEqual(-1, item.sell_in)
        self.assertEqual(2, item.quality)

    def test_conjured_item_quality_never_drops_below_zero_before_sell_date(self):
        item = self.update_item("Conjured Mana Cake", 3, 1)

        self.assertEqual(2, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_conjured_item_quality_never_drops_below_zero_after_sell_date(self):
        item = self.update_item("Conjured Mana Cake", 0, 3)

        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

        
if __name__ == '__main__':
    unittest.main()
