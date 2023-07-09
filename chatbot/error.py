class Error:
    def __init__(self, rule=None):
        self.rule = rule

    def rule_error(self):
        match self.rule:
            case 'aturan 1':
                _str = "Mohon periksa kembali kalimat yang anda inputkan. Berikut contoh kalimat input:\n" \
                       "- Tampilkan seluruh field untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
                       "- Tampilkan (info sigmet terkini/info sigmet terbaru) dengan ketinggian awan abu vulkanik (diatas/dibawah) 1234 (meter|kaki)\n" \
                       "- Tampilkan (info sigmet terkini/info sigmet terbaru) untuk (flight level/fl) 123\n" \
                       "- Tampilkan (info sigmet terkini/info sigmet terbaru) untuk wilayah penyebaran abu vulkaniknya berada di lintang S1234 N12345- Tampilkan (info sigmet terkini/info sigmet terbaru) dengan waktu valid dari jam 23:59 hingga 01:00\n" \
                       "- Tampilkan wilayah penyebaran abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                return _str
            case 'aturan 2':
                _str = "Mohon periksa kembali kalimat yang anda inputkan. Berikut contoh kalimat input:\n" \
                       "- Berapa lama waktu valid untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
                       "- Berapa ketinggian abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
                       "- Berapa kecepatan abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                return _str
            case 'aturan 3':
                _str = "Mohon periksa kembali kalimat yang anda inputkan. Berikut contoh kalimat input:\n" \
                       "- Dimana lokasi gunung untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
                       "- Dimana lokasi dikeluarkannya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
                       "- Dimana titik penyebaran abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                return _str
            case 'aturan 4':
                _str = "Mohon periksa kembali kalimat yang anda inputkan. Berikut contoh kalimat input:\n" \
                       "- Kapan waktu dikeluarkannya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
                       "- Kapan waktu diobservasinya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                return _str
            case 'aturan 5':
                _str = "Mohon periksa kembali kalimat yang anda inputkan. Berikut contoh kalimat input:\n" \
                       "- Apa status untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
                       "- Apa intensitas abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                return _str
            case 'aturan 6':
                _str = "Mohon periksa kembali kalimat yang anda inputkan. Berikut contoh kalimat input:\n" \
                       "- Kearah mana pergerakan abu vulkanik (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"
                return _str+"\n"
            case _:
                return self.default_error()

    def default_error(self):
        _str = "Kalimat input yang dapat diproses antara lain:\n" \
               "Tampilkan:\n" \
               "\t- Tampilkan seluruh field untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "\t- Tampilkan (info sigmet terkini/info sigmet terbaru) dengan ketinggian awan abu vulkanik (diatas/dibawah) 1234 (meter|kaki)\n" \
               "\t- Tampilkan (info sigmet terkini/info sigmet terbaru) untuk (flight level/fl) 123- Tampilkan (info sigmet terkini/info sigmet terbaru) untuk wilayah penyebaran abu vulkaniknya berada di lintang S1234 N12345- Tampilkan (info sigmet terkini/info sigmet terbaru) dengan waktu valid dari jam 23:59 hingga 01:00\n" \
               "\t- Tampilkan wilayah penyebaran abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "Berapa:\n" \
               "\t- Berapa lama waktu valid untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "\t- Berapa ketinggian abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "\t- Berapa kecepatan abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "Dimana:\n" \
               "\t- Dimana lokasi gunung untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "\t- Dimana lokasi dikeluarkannya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "\t- Dimana titik penyebaran abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "Kapan:\n" \
               "\t- Kapan waktu dikeluarkannya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "\t- Kapan waktu diobservasinya untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "Apa:\n" \
               "\t- Apa status untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "\t- Apa intensitas abu vulkanik untuk (info sigmet terkini/info sigmet terbaru/kode sigmet 99)\n" \
               "Kearah:\n" \
               "\t- Kearah mana pergerakan abu vulkanik (info sigmet terkini/info sigmet terbaru/kode sigmet 99)"

        return _str+"\n"
