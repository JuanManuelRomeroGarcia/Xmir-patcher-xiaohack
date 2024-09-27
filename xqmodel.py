#!/usr/bin/env python3

xqModelList = { }

def mi(model_id, model, similar = "", altname = ""):
    xqModelList[model] = { 'model': model, 'id': model_id, 'similar': similar, 'altname': altname }


mi( 3, "R1CM",  "", "miwifi-mini")
mi( 4, "R2D")
mi( 5, "R1CL",  "", "miwifi-nano")
mi( 6, "R2CM")
mi( 7, "R3")
mi( 8, "R3D",   "", "r3d")
mi( 9, "R3L",   "", "miwifi-3c")
mi(10, "R3P",   "", "mi-router-3-pro")
mi(11, "P01")
mi(12, "R3A")
mi(13, "R3G",   "", "mi-router-3g")
mi(14, "R4",    "", "mi-router-4")
mi(15, "R4C",   "", "mi-router-4q")
mi(16, "D01")
mi(17, "R4A",   "", "mi-router-4a-gigabit")
mi(18, "R4CM",  "", "mi-router-4c")
mi(19, "R4AC",  "", "mi-router-4a-100m")   # mi-router-4a-100m-intl  mi-router-4a-100m-intl-v2
mi(20, "R3GV2", "", "mi-router-3g-v2")
mi(21, "R2600")

mi(22, "R2100",   "", "mi-router-ac2100")
mi(23, "RM2100",  "", "redmi-router-ac2100") 
mi(24, "R3600",   "", "ax3600")
mi(25, "R1350")
mi(26, "R2200")
mi(27, "R2350",   "", "aiot-ac2350")
mi(28, "IR1200G")
mi(29, "RM1800")
mi(30, "R2100D")
mi(31, "RA67")
mi(32, "RA69",    "", "ax6")
mi(33, "RA71")
mi(34, "CR6006",  "", "mi-router-cr6606")
mi(35, "CR6008",  "", "mi-router-cr6608")
mi(36, "CR6009",  "", "mi-router-cr6609")
mi(37, "RA70",    "", "ax9000")  # AX9000
mi(38, "RA75",    "", "mi-ra75")
mi(39, "RA72")          # Mi Router AX6000  Certification: 2021-05-20

mi(0,  "RA50")          # Certification: 2022-13063
mi(0,  "RB02", "R4AV2", "mi-router-4a-gigabit-v2") # Xiaomi AC1200 (INT)
mi(0,  "R4AV2", "RB02", "mi-router-4a-gigabit-v2") # Xiaomi AC1200 (CN)

mi(43, "RA80", "RA82")  # AX3000 (CN)         Certification: 2022-2908
mi(44, "RA81")          # Redmi AX3000
mi(45, "RA82", "RA80")  # AX3000 (INT)
mi(46, "RA83")
mi(47, "RA74")          # AX5400

mi(49, "YY01")
mi(50, "RB01", "RB03", "redmi-router-ax6s")  # AX3200 (INT)
mi(51, "RB03", "RB01", "redmi-router-ax6s")  # AX6S    # CR8806 (China Mobile)
mi(52, "CR8808")
mi(53, "CR8809")
mi(54, "RB04")          # Redmi AX5400
mi(55, "CR5508")
mi(56, "CR5506")
mi(57, "CR5509")
mi(58, "RB08")          # HomeWiFi

mi(0,  "RB05")          # Redmi Router AX5700 # Certification: 2022-3478
mi(61, "RB06", "", "redmi-router-ax6000")   # Redmi AX6000
mi(62, "RB07")          # mediatek_mt7981

mi(64, "CB04")
mi(65, "CB0401")        # Xiaomi 5G CPE Pro, Magenta Internet 5G Box AX5400
mi(66, "RC01")          # AX10000    (WanGiga)   (BE10000)
mi(0,  "RC04")          # RA75 analog
mi(68, "CB0401V2")      # Xiaomi 5G CPE Pro

mi(70, "RC06")          # Xiaomi Router 7000 (BE7000)
mi(71, "RD01")          # Xiaomi Whole-Home Router Combo AX3000  # https://www.mi.com/xiaomi-routers/whole-room
mi(72, "WR30", "WR30U", "mi-router-wr30u")  # Xiaomi AX3000NE   WR30U/WR30T/WR30M
mi(0,  "WR30U", "WR30", "mi-router-wr30u")  # China Unicom
mi(0,  "WR30T", "WR30", "mi-router-wr30u")  # China Telecom  # Certification: 2022-3536
mi(0,  "WR30M", "WR30", "mi-router-wr30u")  # China Mobile   # Certification: 2022-3202   6.0.49
mi(73, "RD02")          # Xiaomi Whole-Home Router Combo AX3000 (sub-routing) # ipq5018 # Certification: 2023-11107
mi(74, "CR8818")
mi(75, "RD03", "RD23", "mi-router-ax3000t") # Xiaomi AX3000T (CN)
mi(76, "RD04", "RD12")  # Xiaomi Router AX1500 (CN)
mi(77, "RD05")
mi(78, "RD06")
mi(79, "CR8816")
mi(80, "CR8819")
mi(81, "RD08")          # Xiaomi Router BE6500 Pro
mi(0,  "RD10", "RD10M") # Xiaomi Mi Wi-Fi Range Extender N300 (DVB4398GL)
mi(0,  "RD11", "")      # Xiaomi AC1200M
mi(84, "RA80V2")        # Xiaomi AX3000 2023
mi(85, "RD15")          # Xiaomi BE3600 2.5G #  Certification: 2024-0811
mi(86, "BE36T")         # BE3600T 2.5G
mi(87, "RD12", "RD04")  # Xiaomi Router AX1500 (INT)
mi(88, "RD23", "RD03", "mi-router-ax3000t")  # Xiaomi Router AX3000T (INT)
mi(89, "RD16")          # Xiaomi BE3600 1G
mi(90, "RD18")          # Xiaomi BE5000
mi(0,  "RD28")          # Xiaomi Mesh System AX3000 NE
mi(0,  "RD13")          # Xiaomi Mesh System AC1200

# https://wikidevi.wi-cat.ru/List_of_Xiaomi_Wireless_Devices
# routers with unknown device number

mi(0, "BE36M")
mi(0, "BE306")


def get_modelid_by_name(name):
    name = name.upper()
    if name in xqModelList:
        return xqModelList[name]['id']
    return -1

def get_model_info(name):
    name = name.upper()    
    if name in xqModelList:
        return xqModelList[name]
    return { }

def get_model_by_id(id):
    if id > 0:
        for i, (name, item) in enumerate(xqModelList.items()):
            if item['id'] == id:
                return item
    return { }

