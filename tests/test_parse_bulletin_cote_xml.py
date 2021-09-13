import unittest
import os
from lib.meteofrance import parse_bulletin_xml

DIRNAME = os.path.dirname(__file__)


class TestParseBulletinCoteXml(unittest.TestCase):

    def parse_xml(self, filename):
        with open(os.path.join(DIRNAME, filename)) as f:
            return parse_bulletin_xml(f.read().encode("utf-8"))

    def test_titre(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        self.assertEqual(parsed["titre"], """Bulletin côte "Port Camargue - Saint Raphaël" midi""")

    def test_chapeau(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        self.assertEqual(
            parsed["chapeau"],
            """Origine Météo-France.
Bulletin côtier pour la bande des 20 milles, de Port-Camargue à Saint-Raphaël, du lundi 13 septembre 2021 à 12H30 légales."""
        )

    def test_avis_special(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        self.assertEqual(
            parsed["avis_special"],
            """Pas d'avis de vent fort en cours ni prévu."""
        )

    def test_echeances_count(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        self.assertEqual(len(parsed["echeances"]), 6)

    def test_echeance_0(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        echeance = parsed["echeances"][0]
        self.assertEqual(
            echeance["titre"],
            "Situation générale le lundi 13 septembre 2021 à 06H00 UTC, et évolution"
        )
        self.assertEqual(len(echeance["regions"]), 1)
        self.assertSetEqual(set(["situation"]), set(echeance["regions"][0].keys()))
        self.assertEqual(
            echeance["regions"][0]["situation"],
            "Faible gradient de pression 1015 hPa avec dépression relative sur l'ouest du Golfe du Lion à l'avant d'un talweg atlantique."
        )

    def test_echeance_1(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        echeance = parsed["echeances"][1]
        self.assertEqual(
            echeance["titre"],
            "Observations le lundi 13 septembre 2021 à 09H00 UTC"
        )
        self.assertEqual(len(echeance["regions"]), 1)
        self.assertSetEqual(set(["observations"]), set(echeance["regions"][0].keys()))
        self.assertEqual(len(echeance["regions"][0]["observations"]), 1)
        self.assertSetEqual(set(["observation"]), set(echeance["regions"][0]["observations"][0].keys()))
        self.assertEqual(
            echeance["regions"][0]["observations"][0]["observation"],
            """Cap Camarat : vent Est-Sud-Est 4 nœuds.
Cap Cepet : vent Sud-Ouest 4 nœuds.
Le Levant : vent Ouest 6 nœuds,  1018 hPa en hausse.
Porquerolles : vent Ouest 6 nœuds.
Cap Couronne : vent Est 6 nœuds,  mer belle,  visibilité 6 milles."""
        )

    def test_echeance_2(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        echeance = parsed["echeances"][2]
        self.assertEqual(
            echeance["titre"],
            "Prévisions pour l'après-midi du lundi 13 septembre"
        )
        self.assertEqual(len(echeance["regions"]), 1)
        self.assertSetEqual(set(["previsions"]), set(echeance["regions"][0].keys()))
        self.assertSetEqual(set(["vent", "mer", "houle", "temps", "visibilite"]), set(echeance["regions"][0]["previsions"].keys()))
        self.assertEqual(
            echeance["regions"][0]["previsions"]["vent"],
            """- à l'ouest de Sicié : Sud-Est 3 à 4.
- à l'est de Sicié : Sud-Ouest 3 à 4, fraîchissant localement 5 à l'est de Camarat à la fin."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["mer"],
            """belle."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["houle"],
            """non significative."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["temps"],
            """très nuageux à l'ouest de Fos."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["visibilite"],
            """bonne."""
        )


    def test_echeance_3(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        echeance = parsed["echeances"][3]
        self.assertEqual(
            echeance["titre"],
            "Prévisions pour la nuit du lundi 13 septembre au mardi 14 septembre"
        )
        self.assertSetEqual(set(["previsions"]), set(echeance["regions"][0].keys()))
        self.assertSetEqual(set(["vent", "mer", "houle", "temps", "visibilite"]), set(echeance["regions"][0]["previsions"].keys()))
        self.assertEqual(
            echeance["regions"][0]["previsions"]["vent"],
            """- à l'ouest de Sicié : Sud-Est 3 à 4.
- à l'est de Sicié : Sud-Ouest 2 à 4."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["mer"],
            """belle à peu agitée."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["houle"],
            """- à l'ouest de Sicié : Sud-Ouest 0.5 à 1 m.
- à l'est de Sicié : non significative."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["temps"],
            """couvert. Localement pluies orageuses à l'ouest de Marseille."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["visibilite"],
            """localement moyenne sous pluies orageuses."""
        )


    def test_echeance_4(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        echeance = parsed["echeances"][4]
        self.assertEqual(
            echeance["titre"],
            "Prévisions pour la journée du mardi 14 septembre"
        )
        self.assertSetEqual(set(["previsions"]), set(echeance["regions"][0].keys()))
        self.assertSetEqual(set(["vent", "mer", "houle", "temps", "visibilite"]), set(echeance["regions"][0]["previsions"].keys()))
        self.assertEqual(
            echeance["regions"][0]["previsions"]["vent"],
            """- à l'ouest de Sicié : Sud-Est 4 à 5.
- à l'est de Sicié : secteur Sud-Est dominant 1 à 3."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["mer"],
            """belle à peu agitée, devenant agitée à l'ouest de Beauduc l'après-midi."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["houle"],
            """- à l'ouest de Sicié : Sud-Ouest 0.5 à 1 m.
- à l'est de Sicié : non significative."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["temps"],
            """très nuageux à couvert. Pluies orageuses à l'ouest de Marseille."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["visibilite"],
            """bonne, localement moyenne sous pluies orageuses."""
        )


    def test_echeance_5(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        echeance = parsed["echeances"][5]
        self.assertEqual(
            echeance["titre"],
            "Tendance pour la nuit du 14  au 15, et la journée du mercredi 15 septembre"
        )
        self.assertSetEqual(set(["previsions"]), set(echeance["regions"][0].keys()))
        self.assertSetEqual(set(["vent", "mer", "houle", "temps", "visibilite"]), set(echeance["regions"][0]["previsions"].keys()))
        self.assertEqual(
            echeance["regions"][0]["previsions"]["vent"],
            """- à l'ouest de Sicié : Sud-Est fraîchissant 5 à 6 la nuit.
- à l'est de Sicié : fraîchissant secteur Est 4 à 5 la nuit, mollissant 3 à 4 l'après-midi."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["mer"],
            """agitée à l'ouest de Beauduc, se généralisant en journée."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["houle"],
            """Sud à Sud-Ouest 0.5 à 1 m, s'amplifiant 1.5 à 2 m l'après-midi."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["temps"],
            """pluies orageuses, principalement à l'ouest de Sicié."""
        )
        self.assertEqual(
            echeance["regions"][0]["previsions"]["visibilite"],
            """moyenne sous pluies orageuses."""
        )

    def test_pied(self):
        parsed = self.parse_xml("bulletin_cote_1.xml")
        self.assertEqual(
            parsed["pied"],
            "Prochain bulletin le lundi 13 septembre 2021, vers 18H15 légales"
        )

    def test_unknown_tag_in_bulletin(self):
        with self.assertRaises(Exception) as context:
            self.parse_xml("bulletin_cote_broken_1.xml")
        self.assertTrue('unknown bulletin tag waza' in str(context.exception))


    def test_unknown_tag_in_echeance(self):
        with self.assertRaises(Exception) as context:
            self.parse_xml("bulletin_cote_broken_2.xml")
        self.assertTrue('unknown echeance tag waza' in str(context.exception))

    def test_unknown_tag_in_region(self):
        with self.assertRaises(Exception) as context:
            self.parse_xml("bulletin_cote_broken_3.xml")
        self.assertTrue('unknown region tag waza' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
