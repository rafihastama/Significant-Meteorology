import json

class Error:
    def __init__(self, rule=None):
        self.rule = rule

    def rule_error(self):
        match self.rule:
            case 'aturan 1':
                dict_json = {
                    "error": {
                        "Tampilkan seluruh field untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                        "Tampilkan (info sigmet terkini/info sigmet terbaru) dengan ketinggian awan abu vulkanik (diatas/dibawah) 1234 (meter atau kaki)",
                        "Tampilkan (info sigmet terkini/info sigmet terbaru) untuk (flight level/fl) 123",
                        "Tampilkan (info sigmet terkini/info sigmet terbaru) untuk wilayah penyebaran abu vulkaniknya berada di lintang S1234 N12345",
                        "Tampilkan (info sigmet terkini/info sigmet terbaru) dengan waktu valid dari jam 23:59 hingga 01:00",
                        "Tampilkan wilayah penyebaran abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                        "Tampilkan info sigmet terkini dengan status sigmet (dibatalkan/tidak ada perubahan)",
                        "Tampilkan info sigmet terkini untuk sigmet yang dikeluarkan dari flight information (ujung padang/jakarta)",
                        "Tampilkan info sigmet terkini untuk sigmet yang berada digunung (dukono/ibu/karangetan/krakatau/lewotolo/semeru)",
                        "Tampilkan info sigmet terkini untuk sigmet yang berada digunung dengan posisi lintang n1234 n12345",
                        "Tampilkan info sigmet terkini untuk sigmet yang diobservasi antara jam 21:00 hingga 03:00",
                        "Tampilkan info sigmet terkini dengan status intensitifitas abu vulkanik (melemah/intensif/tidak ada perubahan)",
                        "Tampilkan info sigmet terkini yang awan abu vulkaniknya bergerak kearah (barat laut/barat data/barat/tenggara/timur/timur laut/utara)",
                        "Tampilkan info sigmet terkini dengan kecepatan awan abu vulkaniknya diatas (diatas/dibawah/sama dengan) 31.5 km/h"
                    }
                }
                return dict_json
            case 'aturan 2':
                dict_json = {
                    "error": {
                        "Berapa lama waktu valid untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                        "Berapa ketinggian abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                        "Berapa kecepatan abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    }
                }
                return dict_json
            case 'aturan 3':
                dict_json = {
                    "error": {
                        "Dimana lokasi gunung untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                        "Dimana lokasi dikeluarkannya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                        "Dimana titik penyebaran abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    }
                }
                return dict_json
            case 'aturan 4':
                dict_json = {
                    "error": {
                        "Kapan waktu dikeluarkannya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                        "Kapan waktu diobservasinya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    }
                }
                return dict_json
            case 'aturan 5':
                dict_json = {
                    "error": {
                        "Apa status untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                        "Apa intensitas abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    }
                }
                return dict_json
            case 'aturan 6':
                dict_json = {
                    "error": {
                        "Kearah mana pergerakan abu vulkanik (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    }
                }
                return dict_json
            case _:
                return self.default_error()

    def default_error(self):
        dict_json = {
            "error": {
                    "Tampilkan seluruh field untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                    "Tampilkan (info sigmet terkini/info sigmet terbaru) dengan ketinggian awan abu vulkanik (diatas/dibawah) 1234 (meter atau kaki)",
                    "Tampilkan (info sigmet terkini/info sigmet terbaru) untuk (flight level/fl) 123",
                    "Tampilkan (info sigmet terkini/info sigmet terbaru) untuk wilayah penyebaran abu vulkaniknya berada di lintang S1234 N12345",
                    "Tampilkan (info sigmet terkini/info sigmet terbaru) dengan waktu valid dari jam 23:59 hingga 01:00",
                    "Tampilkan wilayah penyebaran abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    "Berapa lama waktu valid untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                    "Berapa ketinggian abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                    "Berapa kecepatan abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    "Dimana lokasi gunung untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                    "Dimana lokasi dikeluarkannya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                    "Dimana titik penyebaran abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    "Kapan waktu dikeluarkannya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                    "Kapan waktu diobservasinya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    "Apa status untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)",
                    "Apa intensitas abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                    "Kearah mana pergerakan abu vulkanik (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
            }
        }

        return dict_json
