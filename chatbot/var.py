class var:
    KATA_YANG_TIDAK_DIABAIKAN = [
        'tampilkan', 'dari', 'wilayah', 'berapa', 'untuk', 'kode', 'sigmet', 'valid', 'dimana', 'dengan', 'ketinggian',
        'kapan', 'dan', 'kecepatan', 'kearah', 'lama', 'dikeluarkan', 'apa', 'berada', 'terbaru', 'bergerak',
        'yang', 'diobservasi', 'mana', 'intensitas', 'info', 'abu', 'vulkanik', 'terbaru', 'penyebaran',
        'terkini', 'status', 'seluruh', 'field', 'fl', 'date', 'lebih', 'kurang', 'dari', 'lokasi', 'titik',
        'flight information', 'gunung', 'posisi', 'gunung', 'diobservasi', 'polygon', 'flight', 'level', 'waktu',
        'meter', 'feet', 'movement', 'speed', 'intensitivity', 'status', 'kaki', 'meter', 'lintang', 'jam', 'hingga',
        'pergerakan', 'awan', 'diatas', 'dibawah'
    ]

    IGNORE_PATTERN = [
        r'[nsew]\d{4,5}', r'\d{2,5}'
    ]

    DATATABLE_TO_FIELD = {
        'kode sigmet': 'sigmet_code',
        'waktu valid': 'valid_date',
        'flight information': 'flight_information',
        'lokasi gunung': 'mountain',
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

    # attribute field
    attribute = {
        r"kode\ssigmet": "sigmet_code as kode_sigmet",
        r"waktu\svalid": "valid_date as waktu_valid",
        r"lokasi\sdikeluarkannya": "flight_information",
        r"lokasi\sgunung": "mountain as lokasi_gunung",
        r"posisi\sgunung": "mountain_pos as posisi_gunung ",
        r"waktu\sdiobservasi": "observed_at as diobservasi",
        (r"polygon", r"wilayah\spenyebaran\sabu\svulkanik|titik\spenyebaran\sabu\svulkanik"): "polygon_extracted as polygon",
        r"ketinggian\sabu\svulkanik": "feet as kaki, meter",
        r"flight level": "flight_level",
        r"pergerakan\sabu\svulkanik": "va_movement as arah_abu_vulkanik",
        "kecepatan\sabu\svulkanik": "va_speed as kecepatan_abu_vulkanik",
        (r"intensitas\sabu\svulkanik", r"intensitivity"): "intensitivity as intensitas",
        r"status": "status",
        r"jam\ssigmet\sdikeluarkan": "release_time as jam_dirilis",
        r"tanggal\ssigmet\sdikeluarkan": "release_date as tanggal_dirilis",
        r"waktu\sdikeluarkan": {
            "jam": "release_time as jam_dirilis",
            "tanggal": "release_date as tanggal_dirilis"
        },
        r"seluruh\sfield": "*",
        r"(info\ssigmet\sterkini|info\ssigmet\sterbaru)": "*"
    }

    condition = {
        (r'(untuk)', r'dengan'): "WHERE"
    }

    # attribute field for condition
    attribute_condition = {
        r"(info\ssigmet\sterkini|info\ssigmet\sterbaru)": "release_date",
        r"ketinggian\sawan\sabu\svulkanik\s\w+\s\d+\s(meter)": "meter",
        r"ketinggian\sawan\sabu\svulkanik\s\w+\s\d+\s(kaki)": "feet",
        r"untuk\sflight\slevel\s(\d{3})|untuk\sfl\s(\d{3})": "flight_level",
        r"lintang\s([nsew]\d{4,5}\s[nsew]\d{4,5})": "polygon",
        r"waktu\svalid\sdari\sjam": "from_valid_date",
        r"jam\s(\d{2}:\d{2})\s(\d{2}:\d{2})|jam\s(\d{2}:\d{2})\shingga\s(\d{2}:\d{2})": "to_valid_date",
        r"sigmet\skode\s(\d{2})|sigmet\s(\d{2})": "sigmet_code"
    }

    operator = {
        r"diatas": ">",
        r"dibawah": "<",
        r"sama\sdengan": "=",
        r"seluruh\sfield": "*",
        r"lintang": "LIKE",
    }

    data = {
        "sigmet code": {
            "pattern": r"sigmet\skode\s(\d{2})|sigmet\s(\d{2})",
            "attribute": "sigmet_code",
            "data": r"(\d{2})",
            "operator": "="
        },
        "ketinggian": r"(\d{3,6})\smeter|(\d{3,6})\skaki",
        "lintang": r"([nsew]\d{4,5}\s[nsew]\d{4,5})",
        "flight level": {
            "pattern": r"untuk\sflight\slevel\s(\d{3})|untuk\sfl\s(\d{3})",
            "attribute": "flight_level",
            "data": r"(\d{3})",
            "operator": "="
        },
        "valid": r"(\d{2}:\d{2})\s(\d{2}:\d{2})|(\d{2}:\d{2})\shingga\s(\d{2}:\d{2})|(\d{2}:\d{2})\s-\s(\d{2}:\d{2})",
        "current date": {
            "pattern": r"(info\ssigmet\sterkini|info\ssigmet\sterbaru)",
            "attribute": "release_date",
            "data": "DATE(convert_tz(now(), @@session.time_zone, '+07:00'))",
            "operator": "="
        }
    }

    """
        pattern datatale:
            (info/ssigmet/sterkini)|(info/ssigmet/sterbaru)|(sigmet\s\d{,2})
    """

    # pattern regex untuk pengecekan aturan produksi
    TAMPILKAN = r"^(tampilkan)"
    PATTERN_RULE_TAMPILKAN = {
        "field": r"tampilkan\s(seluruh\sfield|kode\ssigmet|waktu\svalid|lokasi\sdikeluarkannya|lokasi\sgunung|posisi\sgunung|waktu\sdiobservasi|polygon|flight\slevel|meter|kaki|pergerakan\sabu\svulkanik|kecepatan\sabu\svulkanik|intensitivity|status|jam\ssigmet\sdikeluarkan|tanggal\ssigmet\sdikeluarkan)+\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})",
        "ketinggian": r"ketinggian\sawan\sabu\svulkanik\s(diatas|dibawah)\s(\d{,6})\s(meter|kaki)",
        "flight level": r"untuk\sflight\slevel\s(\d{3})|untuk\sfl\s(\d{3})",
        "lintang": r"lintang\s([nsew]\d{4,5}\s[nsew]\d{4,5})",
        "valid": r"jam\s(\d{2}:\d{2})\s(\d{2}:\d{2})|jam\s(\d{2}:\d{2})\shingga\s(\d{2}:\d{2})",
        "penyebaran abu vulkanik": r"wilayah\spenyebaran\sabu\svulkanik\s\w+\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})",
    }

    BERAPA = r"^(berapa)"
    PATTERN_RULE_BERAPA = {
        'valid': r"waktu\svalid\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})",
        'ketinggian abu vulkanik': r"ketinggian\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})",
        'kecepatan abu vulkanik': r"kecepatan\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})"
    }

    DIMANA = r"^(dimana)"
    PATTERN_RULE_DIMANA = {
        'lokasi gunung': r'lokasi\sgunung\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})',
        'lokasi flight information': r'lokasi\sdikeluarkannya\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})',
        'penyebaran abu vulkanik': r'penyebaran\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})'
    }

    KAPAN = r"^(kapan)"
    PATTERN_RULE_KAPAN = {
        "dikeluarkan": r'dikeluarkannya\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})',
        "diobservasi": r'diobservasinya\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})'
    }

    APA = r"^(apa)"
    PATTERN_RULE_APA = {
        "status": r"status\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})",
        "intesitas abu vulkanik": r"intensitas\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})|"
                                  r"intensitivity\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})"
    }

    ARAH = r"(kearah)"
    PATTERN_RULE_ARAH = {
        "arah abu vulkanik": r"abu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2})"
    }

