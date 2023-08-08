class var:
    KATA_YANG_TIDAK_DIABAIKAN = [
        'tampilkan', 'dari', 'wilayah', 'berapa', 'untuk', 'kode', 'sigmet', 'valid', 'dimana', 'dengan', 'ketinggian',
        'kapan', 'dan', 'kecepatan', 'kearah', 'lama', 'dikeluarkan', 'apa', 'berada', 'terbaru', 'bergerak',
        'yang', 'diobservasi', 'mana', 'intensitas', 'info', 'abu', 'vulkanik', 'terbaru', 'penyebaran',
        'terkini', 'status', 'seluruh', 'field', 'fl', 'date', 'lebih', 'kurang', 'dari', 'lokasi', 'titik',
        'flight information', 'gunung', 'posisi', 'gunung', 'polygon', 'flight', 'level', 'waktu',
        'meter', 'feet', 'movement', 'speed', 'intensitivity', 'kaki', 'meter', 'lintang', 'jam', 'hingga',
        'pergerakan', 'awan', 'diatas', 'dibawah', 'tanggal', 'sama', 'dibatalkan', 'tidak', 'ada', 'perubahan', 'ujung', 'padang',
        'dukono', 'ibu', 'karangetan', 'krakatau', 'lewotolo', 'semeru', 'antara', 'intensitifitas', 'melemah', 'mempunyai',
        'intensif', 'daya', 'barat', 'selatan', 'tenggara', 'timur', 'laut', 'utara', 'km/h', 'dirilis', 'dilintang'
    ]

    IGNORE_PATTERN = [
        r'[nsew]\d{4,5}', r'\d{2,5}', r'((\d{,2}\.\d{,2})|(\d{1,2}))'
    ]

    # attribute field
    attribute = {
        r"kode\ssigmet": "sigmet_code as kode_sigmet",
        r"waktu\svalid": "valid_date as waktu_valid",
        r"lokasi\sdikeluarkannya": "flight_information",
        r"lokasi\sgunung": "mountain as lokasi_gunung",
        r"posisi\sgunung": "mountain_pos as posisi_gunung",
        r"waktu\sdiobservasi": "observed_at as diobservasi",
        (r"polygon", r"wilayah\spenyebaran\sabu\svulkanik|titik\spenyebaran\sabu\svulkanik"): "polygon_extracted as polygon",
        r"ketinggian\sabu\svulkanik": "feet as kaki, meter",
        r"flight level": "flight_level",
        r"pergerakan\sabu\svulkanik": "va_movement as arah_pergerakan_abu_vulkanik",
        "kecepatan\sabu\svulkanik": "va_speed as kecepatan_abu_vulkanik",
        (r"intensitas\sabu\svulkanik", r"intensitivity"): "intensitivity as intensitas_abu_vulkanik",
        r"status": "status as status_sigmet",
        r"jam\ssigmet\sdikeluarkan": "release_time as jam_dirilis",
        r"tanggal\ssigmet\sdikeluarkan": "release_date as tanggal_dirilis",
        r"waktu\sdikeluarkan": {
            "jam": "release_time as jam_dirilis",
            "tanggal": "release_date as tanggal_dirilis"
        },
        r"seluruh\sfield": "release_date as tanggal_sigmet_dirilis, release_time as jam_sigmet_dirilis, status as status_sigmet, cancelation_sigmet_code as sigmet_yang_dibatalkan, sigmet_code as kode_sigmet, valid_date as waktu_valid, flight_information, mountain as lokasi_gunung, "
                           "mountain_pos as posisi_gunung, observed_at as diobservasi, polygon_extracted as polygon, flight_level, feet as kaki, meter, "
                           "va_movement as arah_pergerakan_abu_vulkanik, va_speed as kecepatan_abu_vulkanik, intensitivity as intensitas_abu_vulkanik",
        r"(info\ssigmet\sterkini|info\ssigmet\sterbaru)": "release_date as tanggal_sigmet_dirilis, release_time as jam_sigmet_dirilis, status as status_sigmet, cancelation_sigmet_code as sigmet_yang_dibatalkan, sigmet_code as kode_sigmet, valid_date as waktu_valid, flight_information, mountain as lokasi_gunung, "
                           "mountain_pos as posisi_gunung, observed_at as diobservasi, polygon_extracted as polygon, flight_level, feet as kaki, meter, "
                           "va_movement as arah_pergerakan_abu_vulkanik, va_speed as kecepatan_abu_vulkanik, intensitivity as intensitas_abu_vulkanik"
    }

    condition = {
        (r'untuk', r'dengan', r'yang'): "WHERE"
    }

    operator = {
        r"diatas": ">",
        r"dibawah": "<",
        r"sama\sdengan": "=",
    }

    pattern_matching_attribute = {
        "tanggal dikeluarkan": {
            "pattern": r"(tanggal\s(\d{2}\-\d{2}\-\d{4}))|(dirilis\spada\stanggal\s(\d{2}\-\d{2}\-\d{4}))",
            "data": r"(\d{2}\-\d{2}\-\d{4})",
            "attribute": "release_date",
            "default_operator": "="
        },
        "sigmet code": {
            "pattern": r"sigmet\skode\s(\d{2})|sigmet\s(\d{2})",
            "attribute": "sigmet_code",
            "data": r"(\d{2})",
            "default_operator": "="
        },
        "flight level": {
            "pattern": r"untuk\sflight\slevel\s(\d{3})|untuk\sfl\s(\d{3})",
            "attribute": "flight_level",
            "data": r"(\d{3})",
            "default_operator": "="
        },
        "data terbaru": {
            "pattern": r"(info\ssigmet\sterkini|info\ssigmet\sterbaru)",
            "attribute": "release_date",
            "data": "DATE(convert_tz(now(), @@session.time_zone, '+07:00'))",
            "default_operator": "="
        },
        "waktu valid": {
            "pattern": r"waktu\svalid\sdari\sjam\s((\d{2}:\d{2})\s(\d{2}:\d{2})|(\d{2}:\d{2})\shingga\s(\d{2}:\d{2}))",
            "attribute": ['from_valid_date', 'to_valid_date'],
            "data": r"(\d{2}:\d{2})\s(\d{2}:\d{2})|(\d{2}:\d{2})\shingga\s(\d{2}:\d{2})|(\d{2}:\d{2})\s-\s(\d{2}:\d{2})",
            "default_operator": "valid_date"
        },
        "ketinggian dalam bentuk meter": {
            "pattern": r"ketinggian\sawan\sabu\svulkanik\s(diatas|dibawah|sama\sdengan)\s\d+\s(meter)",
            "attribute": "meter",
            "data": r"(\d{3,6})\smeter",
            "default_operator": None
        },
        "ketinggian dalam bentuk kaki": {
            "pattern": r"ketinggian\sawan\sabu\svulkanik\s(diatas|dibawah|sama\sdengan)\s\d+\s(kaki)",
            "attribute": "feet",
            "data": r"(\d{3,6})\skaki",
            "default_operator": None
        },
        "lintang": {
            "pattern": r"dilintang\s([nsew]\d{4,5}\s[nsew]\d{4,5})",
            "attribute": "polygon",
            "data": r"([nsew]\d{4,5}\s[nsew]\d{4,5})",
            "default_operator": "LIKE"
        },
        "status sigmet": {
            "pattern": r"status\ssigmet\s(dibatalkan|tidak\sada\sperubahan)",
            "attribute": "status",
            "data": r"(dibatalkan|tidak\sada\sperubahan)",
            "default_operator": "LIKE"
        },
        "flight information": {
            "pattern": r"dikeluarkan\sdari\sflight\sinformation\s(ujung\spadang|jakarta)",
            "attribute": "flight_information",
            "data": r"(ujung\spadang|jakarta)",
            "default_operator": "LIKE"
        },
        "mountain location": {
            "pattern": r"berada\sdigunung\s(dukono|ibu|karangetan|krakatau|lewotolo|semeru)",
            "attribute": "mountain",
            "data": r"(dukono|ibu|karangetan|krakatau|lewotolo|semeru)",
            "default_operator": "LIKE"
        },
        "mountain position": {
            "pattern": r"berada\sdigunung\sdengan\sposisi\s([nsew]\d{4,5}\s[nsew]\d{4,5})",
            "attribute": "mountain_pos",
            "data": r"([nsew]\d{4,5}\s[nsew]\d{4,5})",
            "default_operator": "LIKE"
        },
        "observed at": {
            "pattern": r"diobservasi\santara\sjam\s(\d{2}:\d{2})\s(\d{2}:\d{2})|jam\s(\d{2}:\d{2})\shingga\s(\d{2}:\d{2})",
            "attribute": "observed_at",
            "data": r"(\d{2}:\d{2})\s(\d{2}:\d{2})|(\d{2}:\d{2})\shingga\s(\d{2}:\d{2})|(\d{2}:\d{2})\s-\s(\d{2}:\d{2})",
            "default_operator": "valid_date"
        },
        "intensitivity": {
            "pattern": r"status\sintensitas\sabu\svulkanik\s(melemah|intensif|tidak\sada\sperubahan)",
            "attribute": "intensitivity",
            "data": r"(melemah|intensif|tidak\sada\sperubahan)",
            "default_operator": "LIKE"
        },
        "volcanic ash movement": {
            "pattern": r"awan\sabu\svulkaniknya\sbergerak\skearah\s(barat\slaut|barat|barat\sdaya|selatan|tenggara|timur\slaut|timur|utara)",
            "attribute": "va_movement",
            "data": r"(barat\slaut|barat\sdaya|barat|selatan|tenggara|timur\slaut|timur|utara)",
            "default_operator": "="
        },
        "volcanic ash speed": {
            "pattern": r"kecepatan\sawan\sabu\svulkaniknya\s(diatas|dibawah|sama\sdengan)\s((\d{,2}\.\d{,2})|(\d{1,2}))\skm\/h",
            "attribute": "va_speed",
            "data": r"((\d{,2}\.\d{,2})|(\d{1,2}))\skm",
            "default_operator": None
        }
    }
    # pattern regex untuk pengecekan aturan produksi
    TAMPILKAN = r"^(tampilkan)"
    PATTERN_RULE_TAMPILKAN = {
        "field": r"tampilkan\s((seluruh\sfield)|(kode\ssigmet)((,\s)|(\sdan\s))?|(waktu\svalid)((,\s)|(\sdan\s))?|(lokasi\sdikeluarkannya)((,\s)|(\sdan\s))?|(lokasi\sgunung((,\s)|(\sdan\s))?)|(posisi\sgunung)((,\s)|(\sdan\s))?|(waktu\sdiobservasi)((,\s)|(\sdan\s))?|(polygon)((,\s)|(\sdan\s))?|(flight\slevel)((,\s)|(\sdan\s))?|(ketinggian\sabu\svulkanik)((,\s)|(\sdan\s))?|(pergerakan\sabu\svulkanik)((,\s)|(\sdan\s))?|(kecepatan\sabu\svulkanik)((,\s)|(\sdan\s))?|(intensitas\sabu\svulkanik)((,\s)|(\sdan\s))?|(status)((,\s)|(\sdan\s))?|(jam\ssigmet\sdikeluarkan)((,\s)|(\sdan\s))?|(tanggal\ssigmet\sdikeluarkan)((,\s)|(\sdan\s))?)+\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))",
        "ketinggian": r"ketinggian\sawan\sabu\svulkanik\s(diatas|dibawah)\s(\d{,6})\s(meter|kaki)",
        "flight level": r"untuk\sflight\slevel\s(\d{3})|untuk\sfl\s(\d{3})",
        "lintang": r"dilintang\s([nsew]\d{4,5}\s[nsew]\d{4,5})",
        "valid": r"waktu\svalid\sdari\sjam\s((\d{2}:\d{2})\s(\d{2}:\d{2})|(\d{2}:\d{2})\shingga\s(\d{2}:\d{2}))",
        "penyebaran abu vulkanik": r"wilayah\spenyebaran\sabu\svulkanik\s\w+\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))",
        "status": r"status\ssigmet\s(dibatalkan|tidak\sada\sperubahan)",
        "flight information": r"dikeluarkan\sdari\sflight\sinformation\s(ujung\spadang|jakarta)",
        "mountain location": r"gunung\s(dukono|ibu|karangetan|krakatau|lewotolo|semeru)",
        "mountain position": r"gunung\sdengan\sposisi\s([nsew]\d{4,5}\s[nsew]\d{4,5})",
        "release_date": r"dirilis\spada\stanggal\s(\d{2}\-\d{2}\-\d{4})",
        "observed": r"diobservasi\santara\sjam\s((\d{2}:\d{2})\s(\d{2}:\d{2})|(\d{2}:\d{2})\shingga\s(\d{2}:\d{2}))",
        "intesitivity": r"status\sintensitas\sabu\svulkanik\s(melemah|intensif|tidak\sada\sperubahan)",
        "volcanic ash movement": r"awan\sabu\svulkaniknya\sbergerak\skearah\s(barat\slaut|barat\sdaya|barat|selatan|tenggara|timur\slaut|timur|utara)",
        "volcanic ash speed": r"kecepatan\sawan\sabu\svulkaniknya\s(diatas|dibawah|sama\sdengan)\s((\d{,2}\.\d{,2})|(\d{1,2}))\skm\/h",
    }

    BERAPA = r"^(berapa)"
    PATTERN_RULE_BERAPA = {
        'valid': r"waktu\svalid\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))",
        'ketinggian abu vulkanik': r"ketinggian\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))",
        'kecepatan abu vulkanik': r"kecepatan\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))"
    }

    DIMANA = r"^(dimana)"
    PATTERN_RULE_DIMANA = {
        'lokasi gunung': r'lokasi\sgunung\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))',
        'lokasi flight information': r'lokasi\sdikeluarkannya\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))',
        'penyebaran abu vulkanik': r'penyebaran\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))'
    }

    KAPAN = r"^(kapan)"
    PATTERN_RULE_KAPAN = {
        "dikeluarkan": r'dikeluarkannya\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))',
        "diobservasi": r'diobservasinya\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))'
    }

    APA = r"^(apa)"
    PATTERN_RULE_APA = {
        "status": r"status\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))",
        "intesitas abu vulkanik": r"intensitas\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))|"
                                  r"intensitivity\sabu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))"
    }

    ARAH = r"(kearah)"
    PATTERN_RULE_ARAH = {
        "arah abu vulkanik": r"abu\svulkanik\suntuk\s(info\ssigmet\sterkini|info\ssigmet\sterbaru|kode\ssigmet\s\d{2}|sigmet\stanggal\s(\d{2}\-\d{2}\-\d{4}))"
    }

