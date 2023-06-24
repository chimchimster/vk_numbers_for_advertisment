import re

from database.database import MySQLDatabase
from statistics.statistics import StatisticsManager
from telegram_logs.telegram_logs import logger

from auxiliary.auxiliary import vk_date_of_birth_universalizer
from vk_scripts.vk_scripts import get_members_ids, get_full_data, offset_checker


statistics = StatisticsManager()


def get_groups():
    with open('groups.txt', 'r') as file:

        groups = [group.strip() for group in file.readlines() if group]

        return groups


def data_handler(data):

    result = []

    for member_data in data:
        has_phone = None
        try:
            has_phone = re.findall(r'(\+79|89)((?!\1{5,})\d{9,})', member_data.get('mobile_phone'))[0]

            if re.match(r'(\d+)\1{4,}', has_phone[1]):
                has_phone = None

        except:
            ...
        if member_data.get('mobile_phone') and has_phone:

            mobile = '+79' + has_phone[1]

            date_of_birth = key_checker(member_data, 'bdate')
            country = key_checker(member_data, 'country').get('title')
            city = key_checker(member_data, 'city').get('title')
            date_of_birth = vk_date_of_birth_universalizer(date_of_birth)

            result.append((
                member_data['first_name'],
                member_data['last_name'],
                date_of_birth,
                country,
                city,
                mobile,
                member_data['sex'],
            ))

    return result


def key_checker(dictionary: dict, key: str):

    key_exists = dictionary.get(key)

    if key_exists:
        return key_exists
    return {}


# 369406758,131719576,225687034,492998141,502562885,383054380,122219867,346467664,314092145,293872139,131506476,510142392,343868390,324616461,484805392,329513314,312159909,9432968,364507002,207392766,373483230,1644740,253646745,198251347,154208103,338845968,138117021,263032949,21489565,210023705,348503831,456855268,117247339,470786959,314581634,283366415,341951504,445825415,173734200,95601654,476417621,51317757,154010505,166888680,423388172,334283189,68522672,271267893,228189175,339375768,386347382,193437488,458904824,334994545,89689188,275531207,143031225,52600443,455367660,4297306,241621600,79779474,478433968,332265708,278951654,278977278,71109912,191358116,496305228,320518506,278538094,271774539,134147526,98967315,140809450,308395706,307695590,305946547,363318213,73252987,228443585,242039719,108765586,468336063,274998029,290835458,273153900,375154995,369063964,53810896,164957759,428760666,326592429,332582332,278823964,283592944,428712495,205179819,386675074,111822657,354786746,231192753,151977567,242455757,416934101,63365923,270243565,255149726,252946179,194302824,377103296,457824986,155643317,199757951,174581387,500240783,205981267,22881982,265124716,115031186,8023875,94164332,119296751,270031838,206547149,194851315,352642373,355563761,462535604,87559434,56365628,458795763,32544053,126927094,396115834,436421828,291005986,337727075,2481939,329153682,297819709,145968358,149089379,213249581,374835708,148918590,76601291,275279714,82356274,134751074,332196280,19637538,387358770,202830530,4567218,40954640,357535909,393403253,409127677,175355182,30337424,252821486,90257906,277163218,295445398,277571507,86840787,146012595,167757932,144406839,279108504,61853180,482206863,14518099,6239735,159519781,457066023,287167214,132543544,50165541,332305755,399192568,162053398,185668904,5732890,187545683,309208821,319502577,6560171,119656844,176734705,203205345,193458206,214612636,466295669,301498260,134952645,277489392,89500980,513662190,52626178,307896796,158137658,278121208,373337462,448987882,314313414,161945971,131617161,335289717,379343666,21601224,62292787,335171800,197912141,62913478,105615550,16806538,98829063,374801216,158992228,240247840,149056627,42690294,318323026,88906206,13490767,335796095,475069512,26869918,349111830,337899203,355987446,359453159,33591301,124954172,81190656,309305358,202872714,263087383,301324723,103501960,308586929,61177019,84715444,110150366,216994618,360535447,91020579,367840025,363048828,60178801,87200803,133426704,197424,251687258,332294999,143304172,32585475,361465670,33242786,20315685,65118177,174540755,272027263,468709988,227482517,84345787,276202540,213975604,238176520,83861750,238362931,152343453,12521056,441637334,53795112,337971748,32770177,240477693,102432453,330103358,52179731,246349575,207262745,336697852,333079555,433417684,154450289,321722048,344011418,350760657,258314021,115745375,259518119,89737898,312933709,147625841,236361417,63413633,389026566,469685288,381203014,300424796,245355577,92135664,336813555,304050869,148328879,198045748,160682942,383083950,20575247,122333820,75125946,225046930,246163289,321305236,276704061,268161637,352264033,452828118,13422965,171347040,98361149,224108909,202676178,51755546,299053378,262189308,28988446,53942465,351667713,127323517,238250780,355058662,142070047,6904619,74401675,272171404,322745944,136335638,391254128,228658624,248186461,55035443,81523064,170876617,42176883,20747882,158757588,28334321,358300089,150467663,200241968,233558318,1317087,239170679,17785981,192310821,232337051,166008633,319856522,396268722,274101206,52722230,5420906,50984589,289662244,23144779,184818169,264197124,324789635,336060509,68117472,61646024,366130653,251301685,196299204,35637824,273195053,133086857,35158579,391110509,136054839,217058025,244281083,122215608,274206459,191526684,245135885,246126832,362687644,11138984,86811623,37687686,22719645,200345963,112499097,222543708,6407265,319266684,17050428,371724062,73322265,20856195,292341906,327828780,285800676,187077900,191647267,10641644,301974863,185149590,181817680,197444137,370449092,169166378,89660514,301201629,29761993,316552444,355052250,387444534,327501843,57459594,84995219,294995211,137400022,332092421,409001670,217859361,421527735,70083878,28028330,236572328,230584388,336838292,94874459,332440004,272718832,269809944,80544974,19588942,337005121,430059708,294838343,97006403,230142212,104565680,501659680,172861802,160017730,347376155,265120813,390572412,492066419,368918974,407795110,258107245,329200103,116507608,366668290,142514378,235366013,377465558,204363442,103791187,204316616,11188564,61490197,33127494,278777688,374759395,126725213,131648470,98169052,54606955,83421136,59563393,51621929,263048380,102225353,400647475,132804517,367668097,1283046,229733990,206940052,374464224,22405571,94274312,225136264,181952331,139041873,51320018,28051712,163687329,150475836,22208468,229510038,25491080,148166535,391864726,305228933,67702731,5530620,280667891,27906059,434234791,227138043,411951075,148047063,235488772,234358548,9056530,169838406,231688466,280494890,68375758,121038007,152098473,11353833,391883557,50294070,382014917,121827155,4251020,272762265,251044599,55556501,66321190,206333688,324471597,369933968,230134802,84319519,331990545,274410427,282105359,284887657,184271481,25445740,177744347,60420109,81303099,181432905,319152786,227638770,195341231,334734130,262927409,33635984,75171035,35837586,57376157,132407361,4701582,213221671,32124262,220023610,480248484,15917112,346349250,321913667,314536429,163349131,208644688,172566517,53055426,84824835,435747500,112801704,209108571,311106709,96114143,25119248,375654762,361104362,100605829,163970626,66773025,167745708,323646405,91856424,337993158,299524989,403184136,355580027,349771645,10051396,30124235,197783300,336940641,146822317,69664358,289852378,54960356,243343581,362517820,22028198,24738718,142818670,472887877,271407940,101930724,25041145,286265336,67899399,6840715,24704262,425518165,263580352,221229698,320327890,285067067,368750061,216491823,234085889,203605522,201813014,279459852,296239159,256693384,279394722,359694322,210861108,466338186,358924186,305344652,49647848,342658657,116106817,282397500,68483102,161008140,361087024,138163003,361482997,222389495,251190803,34145768,438897997,260516485,29624549,251696548,23494999,4249590,253331560,184847012,93090505,364279776,338864247,340128420,242737721,332125912,114424525,388905671,101861260,28836864,231224504,337541260,275298646,57820230,251358729,170249435,190459806,374337902,260036867,347240311,376052103,141121431,22342264,361050917,173994579,19663697,358797982,65902771,340093345,135745983,333959643,19138675,193429905,225871434,282184657,308546126,402526826,60423988,293556470,245368867,411095842,45009086,383652038,77671693,174125872,13530186,278196402,252848761,8812615,26375604,317797443,280269978,8988631,335613070,26694240,171240743,82083612,347191414,69966190,105847435,70869754,99087418,155745334,343420212,26897041,94856056,18419265,148255812,72116216,51986182,241982173,330383091,135329520,230340903,247555689,260203241,328560454,217632350,136246880,34478627,272621236,197701775,6307726,110497293,83158392,349790874,10632544,270883969,301543378,426628175,152801092,201515332,253929362,56344089,217511120,109516281,332104355,291744944,27973390,22221919,140127022,166068086,33846138,196308701,385011992,211221649,464959075,10811917,64259102,383617772,280190980,2806420,197319928,12388910,208154164,104857905,94341202,197153755,3453572,411023933,378268745,325428436,82794952,206949936,151765265,68927217,31289155,191846327,7625725,282060309,358466516,181935106,274005170,216342806,26846907,453469884,219708429,74723545,287936017,261069822,318515730,296175406,178599436,156632085,123724411,12922921,66617751,257560437,20732283,83696498,112864224,273429068,306772431,203616895,200927896,219071190,13617286,304761775,291762202,29264547,44961345,159899380,135763760,146367277,192073934,270105986,101101969,137938258,5595858,4165576,8520814,9492409,223510136,234241135,14226573,252152340,328066282,346801422,72906557,149117013,196963285,27103063,238131457,171947125,240244271,209595816,247162269,23112976,36526281,77151643,150275622,328532263,84212909,157487340,324633000,105028474,376638046,280331885,213784130,196476771,895637,43109453,10478925,16871741,7526660,19647316,333165789,277241812,152127083,15018628,144703462,39640479,329659207,99037035,370246389,67894425,234987597,162687553,11460393,369474095,34830613,185237549,151002722,58406837,43011069,54002654,216407125,511674185,87315786,331569225,130115165,210781597,25342253,37869222,101522088,51196406,28717302,155095096,7031412,33336436,176963823,194002150,37336732,293676733,77564753,228718588,80061920,333225039,154520,167289966,58577716,207109643,32175834,200772541,50781850,24301663,223277864,274458397,205220010,54063146,28733832,189320629,66727830,33972925,13841112,151201682,105174580,99462847,17095609,18437194,146330213,40559491,112113298,185957389,42167218,97902803,38805634,56689534,147036699
def main():

    groups = get_groups()

    for group in groups:
        offset = offset_checker(group)

        members_ids = get_members_ids(group, offset)

        step = 1000
        for start in range(0, len(members_ids), step):

            full_data = get_full_data(members_ids[start:start+step])

            data_to_db = data_handler(full_data)

            MySQLDatabase('temp_db').insert_into_table('phone_numbers', ['first_name', 'last_name', 'date_of_birth', 'country', 'city', 'phone_number', 'sex'], data_to_db)

            kwargs = {group: len(data_to_db)}
            statistics.update_statistics(**kwargs)

    logger.send_message(statistics.get_statistics())


if __name__ == '__main__':
    main()
