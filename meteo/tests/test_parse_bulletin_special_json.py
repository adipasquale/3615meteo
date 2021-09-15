import unittest
import os
from meteo.meteofrance.bulletin_special import parse_bulletin_json
import datetime


DIRNAME = os.path.dirname(__file__)


class TestParseBulletinSpecialXml(unittest.TestCase):

    def parse(self, filename):
        with open(os.path.join(DIRNAME, filename), "r") as f:
            return parse_bulletin_json(f.read())

    def test_titre(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(parsed["titre"], "BMS COTE MEDITERRANEE")

    def test_code(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(parsed["code"], "BMSCOTE-02")

    def test_numero(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(parsed["numero"], "346")

    def test_type_avis(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(parsed["type_avis"], "AVIS DE GRAND FRAIS")

    def test_blocs_count(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(len(parsed["blocs"]), 1)

    def test_bloc_code(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(parsed["blocs"][0]["code"], "BMSCOTE-02-02")

    def test_bloc_title(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(parsed["blocs"][0]["titre"], "PROVENCE : de Port-Camargue au Cap Cépet.")

    def test_bloc_begin_time(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(parsed["blocs"][0]["begin_time"].date(), datetime.date(2021, 9, 15))
      self.assertEqual(parsed["blocs"][0]["begin_time"].hour, 3)
      self.assertEqual(parsed["blocs"][0]["begin_time"].minute, 2)

    def test_bloc_end_time(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(parsed["blocs"][0]["end_time"].date(), datetime.date(2021, 9, 15))
      self.assertEqual(parsed["blocs"][0]["end_time"].hour, 15)
      self.assertEqual(parsed["blocs"][0]["end_time"].minute, 0)

    def test_bloc_texts(self):
      parsed = self.parse("bulletin_special_1.json")
      self.assertEqual(len(parsed["blocs"][0]["texts"]), 2)
      self.assertEqual(parsed["blocs"][0]["texts"][0], "En cours et valable jusqu'au mercredi 15 septembre à 15H00 UTC")
      self.assertEqual(parsed["blocs"][0]["texts"][1], "VENT : Sud-Est 7. Rafales")

if __name__ == '__main__':
    unittest.main()
