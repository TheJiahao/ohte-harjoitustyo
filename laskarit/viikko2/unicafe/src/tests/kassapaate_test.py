import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self) -> None:
        self.kassapaate = Kassapaate()
        self.kortti_riittavalla_saldolla = Maksukortti(1000)
        self.kortti_riittamattomalla_saldolla = Maksukortti(100)

    def test_kassapaatteen_rahamaara_alussa_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_myyty_loinaiden_maara_nolla_kappaletta_alussa(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisella_edullisen_ostaminen_kasvattaa_kassan_rahaa(
        self,
    ):
        self.kassapaate.syo_edullisesti_kateisella(1000)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_kateisella_maukkaan_ostaminen_kasvattaa_kassan_rahaa(
        self,
    ):
        self.kassapaate.syo_maukkaasti_kateisella(1000)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_kateisella_edullisen_ostamisessa_vaihtoraha_on_oikea(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(1000)

        self.assertEqual(vaihtoraha, 760)

    def test_kateisella_maukkaan_ostamisessa_vaihtoraha_on_oikea(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(1000)

        self.assertEqual(vaihtoraha, 600)

    def test_kateisella_edullisen_ostaminen_kasvattaa_myytyjen_edullisten_maaraa(
        self,
    ):
        edullisia_alussa = self.kassapaate.edulliset
        self.kassapaate.syo_edullisesti_kateisella(1000)

        self.assertEqual(self.kassapaate.edulliset, edullisia_alussa + 1)

    def test_kateisella_maukkaan_ostaminen_kasvattaa_myytyjen_maukkaiden_maaraa(
        self,
    ):
        maukkaita_alussa = self.kassapaate.maukkaat
        self.kassapaate.syo_maukkaasti_kateisella(1000)

        self.assertEqual(self.kassapaate.maukkaat, maukkaita_alussa + 1)

    def test_vaihtoraha_oikein_jos_kateismaksu_edulliseen_ei_riita(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(100)

        self.assertEqual(vaihtoraha, 100)

    def test_vaihtoraha_oikein_jos_kateismaksu_maukkaaseen_ei_riita(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(100)

        self.assertEqual(vaihtoraha, 100)

    def test_kassan_raha_ei_muutu_jos_kateismaksu_edulliseen_ei_riita(self):
        kassassa_rahaa_alussa = self.kassapaate.kassassa_rahaa
        self.kassapaate.syo_edullisesti_kateisella(100)

        self.assertEqual(self.kassapaate.kassassa_rahaa, kassassa_rahaa_alussa)

    def test_kassan_raha_ei_muutu_jos_kateismaksu_maukkaaseen_ei_riita(self):
        kassassa_rahaa_alussa = self.kassapaate.kassassa_rahaa
        self.kassapaate.syo_maukkaasti_kateisella(100)

        self.assertEqual(self.kassapaate.kassassa_rahaa, kassassa_rahaa_alussa)

    def test_myytyjen_edullisten_maara_ei_muutu_jos_kateismaksu_ei_riita(
        self,
    ):
        myyty_alussa = self.kassapaate.edulliset
        self.kassapaate.syo_edullisesti_kateisella(100)

        self.assertEqual(self.kassapaate.edulliset, myyty_alussa)

    def test_myytyjen_maukkaiden_maara_ei_muutu_jos_kateismaksu_ei_riita(
        self,
    ):
        myyty_alussa = self.kassapaate.maukkaat
        self.kassapaate.syo_maukkaasti_kateisella(100)

        self.assertEqual(self.kassapaate.maukkaat, myyty_alussa)

    def test_kortilta_veloitetaan_oikea_summa_jos_kortin_saldo_riittaa_edulliseen(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti_riittavalla_saldolla)

        self.assertEqual(self.kortti_riittavalla_saldolla.saldo, 760)

    def test_kortilta_veloitetaan_oikea_summa_jos_kortin_saldo_riittaa_maukkaaseen(
        self,
    ):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti_riittavalla_saldolla)

        self.assertEqual(self.kortti_riittavalla_saldolla.saldo, 600)

    def test_palautetaan_true_jos_kortin_saldo_riittaa_edulliseen(self):
        vastaus = self.kassapaate.syo_edullisesti_kortilla(
            self.kortti_riittavalla_saldolla
        )

        self.assertEqual(vastaus, True)

    def test_palautetaan_true_jos_kortin_saldo_riittaa_maukkaaseen(self):
        vastaus = self.kassapaate.syo_maukkaasti_kortilla(
            self.kortti_riittavalla_saldolla
        )

        self.assertEqual(vastaus, True)

    def test_myytyjen_lounaiden_maara_kasvaa_jos_kortin_saldo_riittaa_edulliseen(self):
        myyty_alussa = self.kassapaate.edulliset

        self.kassapaate.syo_edullisesti_kortilla(self.kortti_riittavalla_saldolla)

        self.assertEqual(self.kassapaate.edulliset, myyty_alussa + 1)

    def test_myytyjen_lounaiden_maara_kasvaa_jos_kortin_saldo_riittaa_maukkaaseen(self):
        myyty_alussa = self.kassapaate.maukkaat

        self.kassapaate.syo_maukkaasti_kortilla(self.kortti_riittavalla_saldolla)

        self.assertEqual(self.kassapaate.maukkaat, myyty_alussa + 1)

    def test_saldo_ei_muutu_jos_kortin_saldo_ei_riita_edulliseen(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti_riittamattomalla_saldolla)

        self.assertEqual(self.kortti_riittamattomalla_saldolla.saldo, 100)

    def test_saldo_ei_muutu_jos_kortin_saldo_ei_riita_maukkaaseen(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti_riittamattomalla_saldolla)

        self.assertEqual(self.kortti_riittamattomalla_saldolla.saldo, 100)

    def test_myytyjen_lounaiden_maara_ei_muutu_jos_kortin_saldo_ei_riita_edulliseen(
        self,
    ):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti_riittamattomalla_saldolla)

        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_myytyjen_lounaiden_maara_ei_muutu_jos_kortin_saldo_ei_riita_maukkaaseen(
        self,
    ):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti_riittamattomalla_saldolla)

        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_palauttaa_false_jos_kortin_saldo_ei_riita(self):
        vastaus = self.kassapaate.syo_edullisesti_kortilla(
            self.kortti_riittamattomalla_saldolla
        )

        self.assertEqual(vastaus, False)

    def test_syo_maukkaasti_palauttaa_false_jos_kortin_saldo_ei_riita(self):
        vastaus = self.kassapaate.syo_maukkaasti_kortilla(
            self.kortti_riittamattomalla_saldolla
        )

        self.assertEqual(vastaus, False)

    def test_kassan_raha_ei_muutu_ostettaessa_edullinen_jos_kortin_saldo_riittaa(
        self,
    ):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti_riittavalla_saldolla)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_raha_ei_muutu_ostettaessa_maukas_jos_kortin_saldo_riittaa(
        self,
    ):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti_riittavalla_saldolla)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_raha_ei_muutu_ostettaessa_edullinen_jos_kortin_saldo_ei_riita(
        self,
    ):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti_riittamattomalla_saldolla)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_raha_ei_muutu_ostettaessa_maukas_jos_kortin_saldo_ei_riita(
        self,
    ):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti_riittamattomalla_saldolla)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kortille_ladattaessa_kortin_saldo_kasvaa(self):
        kortti = Maksukortti(1000)

        self.kassapaate.lataa_rahaa_kortille(kortti, 500)
        self.assertEqual(kortti.saldo, 1500)

    def test_kortille_ladattaessa_kassan_raha_kasvaa(self):
        kortti = Maksukortti(1000)

        self.kassapaate.lataa_rahaa_kortille(kortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)

    def test_negatiivisen_saldon_lataaminen_ei_muuta_kortin_saldoa(self):
        kortti = Maksukortti(1000)

        self.kassapaate.lataa_rahaa_kortille(kortti, -100)

        self.assertEqual(kortti.saldo, 1000)

    def test_negatiivisen_saldon_lataaminen_ei_muuta_kassan_rahaa(self):
        kortti = Maksukortti(1000)

        self.kassapaate.lataa_rahaa_kortille(kortti, -100)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
