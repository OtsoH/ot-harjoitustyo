import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_luodun_kassapaatteen_rahamaara_ja_myytyjen_lounaiden_maara_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_kateisosto_toimii_oikein(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(vaihtoraha, 60)
        self.assertEqual(self.kassapaate.edulliset, 1)

        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100640)
        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassapaate.maukkaat, 1)

        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100640)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.edulliset, 1)

        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100640)
        self.assertEqual(vaihtoraha, 300)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_korttiosto_toimii_oikein(self):
        tulos = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertTrue(tulos)
        self.assertEqual(self.kortti.saldo, 760)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

        tulos = self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertTrue(tulos)
        self.assertEqual(self.kortti.saldo, 360)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

        kortti = Maksukortti(200)
        tulos = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertFalse(tulos)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

        kortti = Maksukortti(300)
        tulos = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertFalse(tulos)
        self.assertEqual(kortti.saldo, 300)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_kortille_rahaa_ladattaessa_saldo_ja_kassan_rahamaara_kasvavat(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo, 1500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)
    
    def test_kortille_negatiivisen_summan_lataaminen_ei_muuta_saldoa_eika_kassan_rahamaaraa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kortti.saldo, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_kassassa_rahaa_euroina(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

   
