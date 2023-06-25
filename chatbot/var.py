class var:
    KATA_YANG_TIDAK_DIABAIKAN = [
        'tampilkan', 'dari', 'wilayah', 'berapa', 'untuk', 'kode', 'sigmet', 'valid', 'dimana', 'dengan', 'ketinggian',
        'kapan', 'dan', 'kecepatan', 'kearah', 'lama', 'dikeluarkan', 'apa', 'berada', 'terbaru', 'bergerak',
        'yang', 'diobservasi', 'mana', 'intensitas', 'info', 'abu', 'vulkanik', 'terbaru', 'penyebaran',
        'terkini', 'status', 'seluruh', 'field', 'valid', 'fl', 'date', 'lebih', 'kurang', 'dari', 'lokasi', 'titik',
        'flight information', 'gunung', 'posisi', 'gunung', 'diobservasi', 'polygon', 'flight', 'level', 'waktu',
        'meter', 'feet', 'movement', 'speed', 'intensitivity', 'status', 'kaki', 'meter', 'lintang', 'jam', 'hingga'
    ]

    IGNORE_PATTERN = [
        r'[nsew]\d{4,5}', r'\d{2,5}'
    ]

    NUMBER = r'\d{2,5}'

    KATA_YANG_TIDAK_DIABAIKAN_RE = [
        r'\d{2,5}'
    ]

    FIELD = [
        'seluruh field', 'sigmet code', 'valid date', 'flight information', 'mountain', 'mountain pos',
        'observed_at', 'polygon', 'flight level', 'meter', 'feet', 'movement', 'speed',
        'intensitivity', 'status', 'release time', 'release date'
    ]

    DATATABLE_TO_FIELD = {
        'kode sigmet': 'sigmet_code',
        'waktu valid': 'valid_date',
        'flight information': 'flight_information',
        'gunung': 'mountain',
        'posisi gunung': 'mountain_pos',
        'waktu diobservasi': 'observed_at',
        'polygon': 'polygon_extracted',
        'flight level': 'flight_level',
        'ketinggian dalam bentuk meter': 'meter',
        'ketinggian dalam bentuk feet': 'feet',
        'pergerakan abu vulkanik': 'va_movement',
        'kecepatan abu vulkanik': 'va_speed',
        'intensitivity': 'intensitivity',
        'status': 'status',
        'jam sigmet dikeluarkan': 'release_time',
        'tanggal sigmet dikeluarkan': 'release_date'
    }

    DATATABLE = [
        'info sigmet terkini',
        'info sigmet terbaru',
        'sigmet'
    ]
    pattern_datatable = r"(info/ssigmet/sterkini)|(info/ssigmet/sterbaru)|(sigmet\s\d{,2})"

    # pattern regex untuk aturan produksi
    TAMPILKAN = r"^(tampilkan)"
    PATTERN_RULE_TAMPILKAN = {
        "ketinggian": r"ketinggian\s(lebih\sdari|kurang\sdari)\s(\d{,6})\s(kaki)|ketinggian\s(lebih\sdari|kurang\sdari)\s(\d{,6})\s(meter)",
        "flight level": r"untuk\sflight\slevel\s(\d{3})|untuk\sfl\s(\d{3})",
        "lintang": r"lintang\s([nsew]\d{4,5}\s[nsew]\d{4,5})",
        "valid": r"jam\s(\d{2}:\d{2})\s(\d{2}:\d{2})|jam\s(\d{2}:\d{2})\shingga\s(\d{2}:\d{2})",
        "penyebaran abu vulkanik": r"wilayah\spenyebaran\sabu\svulkanik\s\w+\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})",
    }

    BERAPA = r"^(berapa)"
    PATTERN_RULE_BERAPA = {
        'valid': r"(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})\svalid",
        'ketinggian abu vulkanik': r"ketinggian\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})",
        'kecepatan abu vulkanik': r"kecepatan\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})"
    }

    DIMANA = r"^(dimana)"
    PATTERN_RULE_DIMANA = {
        'lokasi gunung': r'lokasi\sgunung\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})',
        'lokasi flight information': r'lokasi\sflight\sinformation\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})',
        'penyebaran abu vulkanik': r'penyebaran\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})'
    }

    KAPAN = r"^(kapan)"
    PATTERN_RULE_KAPAN = {
        "dikeluarkan": r'(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})\sdikeluarkan',
        "diobservasi": r'(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})\sdiobservasi'
    }

    APA = r"^(apa)"
    PATTERN_RULE_APA = {
        "status": r"status\sdari\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})",
        "intesitas abu vulkanik": r"intensitas\sabu\svulkanik\sdari\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})"
    }

    ARAH = r"(kearah)"
    PATTERN_RULE_ARAH = {
        "arah abu vulkanik": r"abu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|sigmet\s\d{2})\sbergerak"
    }

