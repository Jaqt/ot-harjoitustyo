import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_rahan_lataaminen_kasvattaaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(250)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 12.50 euroa")

    def test_saldo_vahenee_oikein_kun_rahaa_tarpeeksi(self):
        self.maksukortti.ota_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 9.00 euroa")

    def test_saldo_ei_muutu_kun_rahaa_ei_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1001)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_ota_rahaa_palauttaa_true_kun_rahat_riitaa_muuten_false(self):
        self.assertEqual(self.maksukortti.ota_rahaa(100), True)
        self.assertEqual(self.maksukortti.ota_rahaa(1001), False)

    def test_saldo_euroina_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.00)