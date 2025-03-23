import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)
    
    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(self.maksukortti.saldo, 2000)
    
    def test_saldo_vahenee_oikein_jos_rahaa_on_tarpeeksi(self):
        self.assertTrue(self.maksukortti.ota_rahaa(100))
        self.assertEqual(self.maksukortti.saldo, 900)
    
    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.assertFalse(self.maksukortti.ota_rahaa(10000))
        self.assertEqual(self.maksukortti.saldo, 1000)
    
    def test_metodi_palauttaa_true_jos_rahat_riittivat(self):
        self.assertTrue(self.maksukortti.ota_rahaa(500))
    
    def test_metodi_palauttaa_true_jos_rahat_riittivat_muuten_false(self):
        self.assertTrue(self.maksukortti.ota_rahaa(500))
        self.assertEqual(self.maksukortti.saldo, 500)
        
        self.assertFalse(self.maksukortti.ota_rahaa(1500))
        self.assertEqual(self.maksukortti.saldo, 500)

    def test_saldo_euroina_palauttaa_oikean_saldon(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
    
    def test_str_palauttaa_oikean_merkkijonon(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

