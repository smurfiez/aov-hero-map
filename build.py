# -*- coding: utf-8 -*-
"""Generate heroes.js (AoV global roster with WZRY counterparts) and index.html for a static match-up site."""
import json, os


WZRY_PY = {
  "不知火舞": "bù zhī huǒ wǔ",
  "东皇太一": "dōng huáng tài yī",
  "亚瑟": "yà sè",
  "伽罗": "gā luó",
  "公孙离": "gōng sūn lí",
  "兰陵王": "lán líng wáng",
  "关羽": "guān yǔ",
  "典韦": "diǎn wéi",
  "刘备": "liú bèi",
  "刘禅": "liú chán",
  "司马懿": "sī mǎ yì",
  "后羿": "hòu yì",
  "周瑜": "zhōu yú",
  "哪吒": "né zhā",
  "墨子": "mò zi",
  "夏侯惇": "xià hóu dūn",
  "太乙真人": "tài yǐ zhēn rén",
  "妲己": "dá jǐ",
  "姜子牙": "jiāng zi yá",
  "娜可露露": "nà kě lù lù",
  "嬴政": "yíng zhèng",
  "孙尚香": "sūn shàng xiāng",
  "孙悟空": "sūn wù kōng",
  "孙膑": "sūn bìn",
  "安琪拉": "ān qí lā",
  "宫本武藏": "gōng běn wǔ cáng",
  "小乔": "xiǎo qiáo",
  "庄周": "zhuāng zhōu",
  "张良": "zhāng liáng",
  "张飞": "zhāng fēi",
  "成吉思汗": "chéng jí sī hán",
  "扁鹊": "biǎn què",
  "曹操": "cáo cāo",
  "李元芳": "lǐ yuán fāng",
  "李白": "lǐ bái",
  "梦奇": "mèng qí",
  "橘右京": "jú yòu jīng",
  "武则天": "wǔ zé tiān",
  "牛魔": "niú mó",
  "狄仁杰": "dí rén jié",
  "猪八戒": "zhū bā jiè",
  "王昭君": "wáng zhāo jūn",
  "甄姬": "zhēn jī",
  "白起": "bái qǐ",
  "百里守约": "bǎi lǐ shǒu yuē",
  "程咬金": "chéng yǎo jīn",
  "老夫子": "lǎo fū zǐ",
  "芈月": "mǐ yuè",
  "花木兰": "huā mù lán",
  "蔡文姬": "cài wén jī",
  "虞姬": "yú jī",
  "诸葛亮": "zhū gě liàng",
  "貂蝉": "diāo chán",
  "赵云": "zhào yún",
  "达摩": "dá mó",
  "钟无艳": "zhōng wú yàn",
  "钟馗": "zhōng kuí",
  "铠": "kǎi",
  "阿轲": "ā kē",
  "韩信": "hán xìn",
  "项羽": "xiàng yǔ",
  "马可波罗": "mǎ kě bō luó",
  "高渐离": "gāo jiàn lí",
  "鲁班七号": "lǔ bān qī hào",
}

PY = {
  "阿杜恩": "ā dù ēn",
  "莫托斯": "mò tuō sī",
  "查戈纳尔": "chá gē nà ěr",
  "克莱斯": "kè lái sī",
  "哥德尔": "gē dé ěr",
  "夸克": "kuā kè",
  "朗博": "lǎng bó",
  "马洛斯": "mǎ luò sī",
  "麦克斯": "mài kè sī",
  "美娜": "měi nà",
  "欧米茄": "ōu mǐ jiā",
  "渥马尔": "wò mǎ ěr",
  "诺可西": "nuò kě xī",
  "塔拉": "tǎ lā",
  "萨尼": "sà ní",
  "托罗": "tuō luó",
  "泽尼尔": "zé ní ěr",
  "伊伯内斯": "yī bó nèi sī",
  "阿塔": "ā tǎ",
  "巴杜姆": "bā dù mǔ",
  "艾瑞": "ài ruì",
  "维罗": "wéi luó",
  "爱里": "ài lǐ",
  "亚莲": "yà lián",
  "艾蜜莉": "ài mì lì",
  "阿思崔德": "ā sī cuī dé",
  "夜姬": "yè jī",
  "埃罗": "āi luó",
  "弗洛倫": "fú luò lún",
  "凯尔格罗斯": "kǎi ěr gé luó sī",
  "吕布": "lǚ bù",
  "夜叉": "yè chā",
  "筱清": "xiǎo qīng",
  "瑞克": "ruì kè",
  "兰铎": "lán duó",
  "龙马": "lóng mǎ",
  "司科德": "sī kē dé",
  "超人": "chāo rén",
  "雾己": "wù jǐ",
  "绯泪": "fēi lèi",
  "安格列": "ān gé liè",
  "神奇女侠": "shén qí nǚ xiá",
  "青硯": "qīng yàn",
  "叶娜": "yè nà",
  "赵云": "zhào yún",
  "瑟斐斯": "sè fěi sī",
  "祖卡": "zǔ kǎ",
  "维": "wéi",
  "葵": "kuí",
  "蝙蝠侠": "biān fú xiá",
  "布莱特": "bù lái tè",
  "刀锋宝贝": "dāo fēng bǎo bèi",
  "恩佐": "ēn zuǒ",
  "闪电侠": "shǎn diàn xiá",
  "姬拉": "jī lā",
  "科里纳卡": "kē lǐ nà kǎ",
  "莫拉": "mò lā",
  "纳克罗斯": "nà kè luó sī",
  "潘因": "pān yīn",
  "奎伦": "kuí lún",
  "拉兹": "lā zī",
  "西内斯特": "xī nèi sī tè",
  "悟空": "wù kōng",
  "札塔": "zhá tǎ",
  "齐尔": "qí ěr",
  "比洛": "bǐ luò",
  "阿莱斯特": "ā lái sī tè",
  "阿兹卡": "ā zī kǎ",
  "达西": "dá xī",
  "貂蝉": "diāo chán",
  "迪拉克": "dí lā kè",
  "伊吉": "yī jí",
  "伊耿斯": "yī gěng sī",
  "卢米娅": "lú mǐ yà",
  "伊雪": "yī xuě",
  "金纳": "jīn nà",
  "卡莉": "kǎ lì",
  "克里希": "kè lǐ xī",
  "萝尔": "luó ěr",
  "莉莉安": "lì lì ān",
  "洛里昂": "luò lǐ áng",
  "玛迦": "mǎ jiā",
  "穆加爵": "mù jiā jué",
  "娜塔亚": "nà tǎ yà",
  "辟雷鞑": "pì léi dá",
  "赛菲拉": "sài fēi lā",
  "图伦": "tú lún",
  "薇拉": "wēi lā",
  "约": "yuē",
  "海诺": "hǎi nuò",
  "戴雅": "dài yǎ",
  "布鲁希达": "bù lǔ xī dá",
  "卡芬妮": "kǎ fēn nī",
  "艾兰朵尔": "ài lán duǒ ěr",
  "艾斯": "ài sī",
  "艾琳": "ài lín",
  "菲尼克": "fēi ní kè",
  "亥犽": "hài yà",
  "拉维尔": "lā wéi ěr",
  "琳蒂": "lín dì",
  "摩恩": "mó ēn",
  "史兰兹": "shǐ lán zī",
  "斯图尔特": "sī tú ěr tè",
  "缇莉": "tí lì",
  "特尔安娜斯": "tè ěr ān nà sī",
  "小丑": "xiǎo chǒu",
  "索恩": "suǒ ēn",
  "凡恩": "fán ēn",
  "维奥莱特": "wéi ào lái tè",
  "灵灵": "líng líng",
  "约恩": "yuē ēn",
  "爱丽丝": "ài lì sī",
  "安奈特": "ān nài tè",
  "阿亚": "ā yà",
  "海伦": "hǎi lún",
  "克里奇克斯": "kè lǐ qí kè sī",
  "明": "míng",
  "佩娜": "pèi nà",
  "萝伊": "luó yī",
  "提米": "tí mǐ",
  "齐普": "qí pǔ",
}

# mapping_type: direct | old | loose | original
H = []
def h(aov, aov_cn, wzry, role, lane, mtype, note, tier="", icon=""):
    H.append(dict(aov_name=aov, aov_cn=aov_cn, wzry_name=wzry, role=role, lane=lane,
                  mapping_type=mtype, note=note, tier=tier,
                  image=icon or ("images/" + aov.lower().replace("'", "").replace(" ", "") + (".png" if aov == "Vei" else ".jpg"))))

# ---------- TANK ----------
h("Arduin","阿杜恩","夏侯惇","Tank","Top","old","近战坦克，旧版映射","A")
h("Arthur","莫托斯","亚瑟","Tank","Top","direct","新手推荐，全能战士","A")
h("Chaugnar","查戈纳尔","庄周","Tank","Support","direct","梦蝶减控坦辅","B")
h("Cresht","克莱斯","张飞","Tank","Support","direct","换形坦辅","A")
h("Gildur","哥德尔","墨子","Mage/Tank","Mid","direct","炮台法师+法坦，中路定海神针","S")
h("Grakk","夸克","钟馗","Tank","Support","direct","钩子先手坦克","C")
h("Lumburr","朗博","牛魔","Tank","Support","direct","团战开团坦克","B")
h("Maloch","马洛斯","刘备","Tank","Top","old","老版刘备映射","B")
h("Max","麦克斯","哪吒","Tank/Warrior","Top","direct","冲阵真伤战士","A")
h("Mina","美娜","白起","Tank","Top","old","老版白起映射","B")
h("Omega","欧米茄","刘禅","Tank","Support","old","推塔控场坦克","B")
h("Ormarr","渥马尔","钟无艳","Tank","Top","direct","石化控制坦克","B")
h("Roxie","诺可西","—","Tank/Warrior","Top","original","坦战，无CN对应","B")
h("Taara","塔拉","程咬金","Tank","Top","old","回复坦克，旧版映射","B")
h("Thane","萨尼","项羽","Tank","Top","direct","坦度+开团，顶级先手","A")
h("Toro","托罗","—","Tank","Top","original","无CN对应","C")
h("Xeniel","泽尼尔","—","Tank/Support","Support","original","真伤换血坦克","B")
h("Y'bneth","伊伯内斯","—","Tank","Top","original","无CN对应","C")
h("Ata","阿塔","猪八戒","Tank","Top","direct","肉盾回血","B")
h("Baldum","巴杜姆","—","Tank","Top","original","无CN对应","B")
h("Arum","艾瑞","东皇太一","Tank/Support","Support","direct","吸血坦辅","A")
h("Wiro","维罗","—","Tank","Top","original","印尼本土英雄，无CN对应","C")

# ---------- WARRIOR ----------
h("Airi","爱里","宫本武藏","Warrior","Top","old","突进战士，旧版映射","A")
h("Allain","亚莲","—","Warrior","Top","original","无CN对应","A")
h("Amily","艾蜜莉","铠","Warrior","Top","direct","冲阵战士","A")
h("Astrid","阿思崔德","—","Warrior","Top","original","无CN对应","B")
h("Dextra","夜姬","—","Warrior/Mage","Top","original","真伤战士，无CN对应","B")
h("Errol","埃罗","—","Warrior","Top","original","无CN对应","C")
h("Florentino","弗洛倫","—","Warrior","Top","original","顶级1v1对线，无CN对应","S")
h("Kil'Groth","凯尔格罗斯","老夫子","Warrior","Top","loose","机制近似，非1:1","B")
h("Lu Bu","吕布","曹操","Warrior","Top","old","真伤战士，旧版映射曹操","A")
h("Omen","夜叉","老夫子","Warrior","Top","loose","分推战士，老夫子近似","S")
h("Qi","筱清","达摩","Warrior","Top","loose","换形战士，近似达摩","B")
h("Riktor","瑞克","—","Warrior","Jungle","original","无CN对应","B")
h("Rourke","兰铎","公孙离","Warrior/Marksman","Top","direct","位移战士","A")
h("Ryoma","龙马","橘右京","Warrior","Jungle","direct","剑气突进","A")
h("Skud","司科德","达摩","Warrior","Top","old","换形战士，旧版达摩","B")
h("Superman","超人","关羽","Warrior","Top","direct","骑乘冲阵","A")
h("Tachi","雾己","—","Warrior","Top","original","无CN对应","B")
h("Veres","绯泪","—","Warrior/Assassin","Jungle","original","近战爆发，无CN对应","A")
h("Volkath","安格列","—","Warrior/Assassin","Jungle","original","突进战士，无CN对应","B")
h("Wonder Woman","神奇女侠","—","Warrior","Top","original","DC授权，无CN对应","B")
h("Yan","青硯","—","Warrior","Jungle","original","无CN对应","A")
h("Yena","叶娜","花木兰","Warrior","Top","direct","双剑形态战士","A")
h("Zanis","赵云","典韦","Warrior","Jungle","old","跳斩战士，旧版典韦","A")
h("Zephys","瑟斐斯","赵云","Warrior/Assassin","Jungle","old","突进战士，旧版赵云","A")
h("Zuka","祖卡","花木兰","Warrior/Assassin","Jungle","loose","位移战士，近似花木兰","A")
h("Vei","维","—","Warrior","Top","original","无CN对应","B")

# ---------- ASSASSIN ----------
h("Aoi","葵","—","Assassin","Jungle","original","迷雾岛忍者，无CN对应","A")
h("Batman","蝙蝠侠","兰陵王","Assassin","Jungle","direct","隐身刺客（DC）","A")
h("Bright","布莱特","—","Assassin","Jungle","original","光刃刺客，无CN对应","B")
h("Butterfly","刀锋宝贝","阿轲","Assassin","Jungle","direct","隐身背刺刺客","S")
h("Enzo","恩佐","—","Assassin","Jungle","original","宗教审判刺客，无CN对应","A")
h("Flash","闪电侠","—","Assassin/Mage","Jungle","original","DC授权，无CN对应","B")
h("Keera","姬拉","—","Assassin","Jungle","original","无CN对应","A")
h("Kriknak","科里纳卡","娜可露露","Assassin","Jungle","direct","鹰形态刺客","A")
h("Murad","莫拉","李白","Assassin","Jungle","old","时间刺客，旧版映射","A")
h("Nakroth","纳克罗斯","韩信","Assassin","Jungle","direct","位移刺客","A")
h("Paine","潘因","司马懿","Assassin","Jungle","direct","灵体刺客","A")
h("Quillen","奎伦","阿轲","Assassin","Jungle","direct","新版背刺映射阿轲","A")
h("Raz","拉兹","不知火舞","Mage/Assassin","Mid","direct","翻滚爆发","A")
h("Sinestrea","西内斯特","—","Assassin","Jungle","original","无CN对应","B")
h("Wukong","悟空","孙悟空","Assassin","Jungle","direct","分身刺客","S")
h("Zata","札塔","—","Assassin","Jungle","original","无CN对应","A")
h("Zill","齐尔","—","Assassin/Mage","Jungle","original","无CN对应","B")
h("Billow","比洛","—","Assassin","Jungle","original","无CN对应","A")

# ---------- MAGE ----------
h("Aleister","阿莱斯特","张良","Mage","Mid","old","结界法师，旧版映射","B")
h("Azzen'Ka","阿兹卡","甄姬","Mage","Mid","direct","水系控场法师","A")
h("D'Arcy","达西","—","Mage","Mid","original","无CN对应","B")
h("Diao Chan","貂蝉","王昭君","Mage","Mid","direct","冰控法师","A")
h("Dirak","迪拉克","—","Mage","Mid","original","无CN对应","B")
h("Iggy","伊吉","—","Mage","Mid","original","火焰控场，无CN对应","B")
h("Ignis","伊耿斯","周瑜","Mage","Mid","old","火系法师，旧版映射","B")
h("Ilumia","卢米娅","武则天","Mage","Mid","direct","御权控场法师","A")
h("Ishar","伊雪","—","Mage/Support","Mid","original","无CN对应","B")
h("Jinnar","金纳","高渐离","Mage","Mid","direct","钢琴AOE法师","S")
h("Kahlii","卡莉","嬴政","Mage","Mid","direct","远程消耗法师","A")
h("Krixi","克里希","小乔","Mage","Mid","direct","扇子爆发法师","A")
h("Lauriel","萝尔","貂蝉","Mage","Mid","direct","收割法师","S")
h("Liliana","莉莉安","—","Mage/Assassin","Mid","original","双形态法师，无CN对应","A")
h("Lorion","洛里昂","—","Mage","Mid","original","无CN对应","B")
h("Marja","玛迦","芈月","Mage/Tank","Top","direct","吸血暗影法师","A")
h("Mganga","穆加爵","扁鹊","Mage/Support","Mid","old","毒奶法师，旧版映射","B")
h("Natalya","娜塔亚","安琪拉","Mage","Mid","direct","范围爆发法师","S")
h("Preyta","辟雷鞑","姜子牙","Mage","Mid","old","减抗法师，旧版映射","B")
h("Sephera","赛菲拉","—","Mage/Support","Mid","original","无CN对应","B")
h("Tulen","图伦","诸葛亮","Mage","Mid","direct","位移收割法师","S")
h("Veera","薇拉","妲己","Mage","Mid","direct","锁定控制法师","A")
h("Yue","约","—","Mage","Mid","original","无CN对应","A")
h("Heino","海诺","—","Mage","Mid","original","无CN对应","A")
h("Dyadia","戴雅","—","Mage","Mid","original","无CN对应","B")

# ---------- MARKSMAN ----------
h("Brunhilda","布鲁希达","—","Marksman","Dragon","original","无CN对应","B")
h("Capheny","卡芬妮","—","Marksman","Dragon","original","走射射手，无CN对应","A")
h("Eland'orr","艾兰朵尔","梦奇","Marksman","Dragon","loose","球状射手，近似梦奇","A")
h("Elsu","艾斯","百里守约","Marksman","Dragon","direct","超远狙击","A")
h("Erin","艾琳","—","Marksman","Dragon","original","无CN对应","B")
h("Fennik","菲尼克","李元芳","Marksman","Dragon","direct","飞镖射手","A")
h("Hayate","亥犽","马可波罗","Marksman","Dragon","direct","真伤旋弹射手","S")
h("Laville","拉维尔","后羿","Marksman","Dragon","direct","新版后羿映射","A")
h("Lindis","琳蒂","成吉思汗","Marksman","Dragon","loose","陷阱射手，近似成吉思汗","B")
h("Moren","摩恩","—","Marksman","Dragon","original","无CN对应","C")
h("Slimz","史兰兹","—","Marksman","Dragon","original","原创射手，无CN对应","C")
h("Stuart","斯图尔特","—","Marksman","Dragon","original","无CN对应","B")
h("Teeri","缇莉","—","Marksman","Dragon","original","回旋镖射手，无CN对应","B")
h("Tel'Annas","特尔安娜斯","伽罗","Marksman","Dragon","direct","超远射程","A")
h("The Joker","小丑","虞姬","Marksman","Dragon","direct","物理免疫射手","A")
h("Thorne","索恩","成吉思汗","Marksman","Dragon","loose","分区映射，近似成吉思汗","B")
h("Valhein","凡恩","狄仁杰","Marksman","Dragon","loose","三色弹射手，近似狄仁杰","B")
h("Violet","维奥莱特","孙尚香","Marksman","Dragon","direct","翻滚炮射","A")
h("Wisp","灵灵","—","Marksman","Dragon","original","原创射手，无CN对应","C")
h("Yorn","约恩","鲁班七号","Marksman","Dragon","old","炮台射手，旧版映射","A")

# ---------- SUPPORT ----------
h("Alice","爱丽丝","孙膑","Support","Support","direct","时空辅助","B")
h("Annette","安奈特","—","Support/Mage","Support","original","无CN对应","A")
h("Aya","阿亚","—","Support","Support","original","无CN对应","B")
h("Helen","海伦","—","Support","Support","original","无CN对应","A")
h("Krizzix","克里奇克斯","—","Support","Support","original","无CN对应","B")
h("Ming","明","—","Support","Support","original","无CN对应","A")
h("Payna","佩娜","蔡文姬","Support","Support","direct","琴音奶辅","A")
h("Rouie","萝伊","—","Support","Support","original","无CN对应","B")
h("TeeMee","提米","太乙真人","Support","Support","direct","经济增益+复活","B")
h("Zip","齐普","—","Support/Tank","Support","original","无CN对应","B")

# AoV item -> (WZRY item, mapping_type, one-line EN reason)
ITEMS_MAP = {
  # Physic attack
  "Short Sword": ("铁剑", "direct", "Same base attack-damage starter as WZRY's 铁剑 (+20 AD)."),
  "Dagger": ("匕首", "direct", "Same base attack-speed starter (+10% AS)."),
  "Gloves": ("搏击拳套", "direct", "Same base crit starter (+8% crit)."),
  "Bloodied Club": ("吸血之镰", "direct", "Same base lifesteal starter (+8% phys lifesteal)."),
  "Chain Hammer": ("迅捷长矛", "direct", "Same AD building block (WZRY's 迅捷长矛 +35 AD)."),
  "Cleaving Claymore": ("风暴巨剑", "direct", "Same mid AD brick (WZRY's 风暴巨剑 +75 AD)."),
  "Arcane Hammer": ("速击之枪", "loose", "Same AD+AS combo, but AoV adds on-hit movement speed — WZRY's 速击之枪 does not."),
  "Tempest Blades": ("狂暴双刃", "loose", "AS+MS item; WZRY's 狂暴双刃 is the closest (15% AS + 7.5% MS)."),
  "Astral Spear": ("陨星", "loose", "Armor-pen spear; in WZRY you build toward 碎星锤 via 陨星 instead."),
  "Shuriken": ("末世", "loose", "Early on-hit damage; the full on-hit item in WZRY is 末世."),
  "Chaos Bow": ("穿云弓", "loose", "Ranged-only pen bow; WZRY's ranged special is 穿云弓 (AS+crit instead of pen)."),
  "Longinus' Spear": ("暗影战斧", "direct", "Near-identical: AD + CDR + HP + armor pen (WZRY's 暗影战斧)."),
  "Fafnir's Talon": ("末世", "direct", "Same kit: AD + AS + lifesteal + on-hit % current HP damage."),
  "Claves Sancti": ("无尽战刃", "direct", "Ranged crit finisher: AD + crit + crit damage, like 无尽战刃."),
  "Muramasa": ("暗影战斧", "direct", "AD + CDR + HP + % armor pen — the classic 暗影战斧 shape."),
  "The Beast": ("制裁之刃", "direct", "Lifesteal + low-HP self-recovery, same idea as 制裁之刃's 回魂."),
  "Omni Arms": ("宗师之力", "direct", "Same passive: after a skill, next attack hits extra — 宗师之力's 强击."),
  "Slikk's Sting": ("影刃", "direct", "AS + crit + MS with crit on-hit — 影刃's territory."),
  "Fenrir's Tooth": ("强者破军", "direct", "Big AD + bonus damage vs targets below 50% HP — that's 破军."),
  "Blitz Blade": ("闪电匕首", "direct", "AS + chain-lightning on-hit, identical to 闪电匕首's 电弧."),
  "Devil's Handshake": ("影刃", "direct", "Stacking AS on-hit — 影刃's 暴风 passive, same concept."),
  "Rankbreaker": ("碎星锤", "direct", "AD + flat armor pen; WZRY's 碎星锤 is the pen bruiser item."),
  "Uriel's Brand": ("破魔刀", "direct", "Attack + magic defense hybrid with low-HP shield — 破魔刀's niche."),
  "Curse of Death (Item)": ("暗影战斧", "loose", "Same AD+CDR+HP stats as 暗影战斧, but its max-HP shred passive has no WZRY match."),
  "Death Sickle": ("名刀·司命", "direct", "Near-identical: near-death invincibility burst — 名刀·司命's 暗幕."),
  "Bow of Slaughter": ("逐日之弓", "loose", "Ranged crit bow; the lifesteal-on-kill active is AoV-only."),
  "Dawnning Star": ("仁者破晓", "direct", "Ranged-doubled on-hit bonus — same design as 破晓's 普攻伤害提升."),
  "Frost Hammer": ("冰痕之握", "direct", "Slow on-hit after attacks/skills — 冰痕之握's 强击 slow."),
  # Magic attack
  "Spell Tome": ("咒术典籍", "direct", "Same base AP starter."),
  "Lapis Ring": ("蓝宝石", "direct", "Same base mana starter (+400 mana in WZRY)."),
  "Pendant of Faith": ("—", "original", "Pure mana-regen starter — WZRY has no equivalent basic item."),
  "Ancient Scriptures": ("圣者法典", "direct", "Same mid AP brick (WZRY's 圣者法典 +60 AP + CDR)."),
  "Enchanted Scroll": ("大棒", "direct", "Same pure-AP brick (+120 AP)."),
  "Trick Blade": ("巫术法杖", "loose", "Skill-then-next-attack passive — WZRY moved it to 巫术法杖 (magic, bigger)."),
  "Spoopy Mask": ("日暮之流", "loose", "AP + magic pen; WZRY's on-hit pen item is 日暮之流."),
  "Phoenix Tear": ("时之预言", "direct", "Same level-up HP/mana restore passive — 时之预言's 英勇奖赏."),
  "Virtue's Bracelet": ("圣者法典", "direct", "AP + CDR + regen brick, 圣者法典's role."),
  "Vlad's Impaler": ("血族之书", "direct", "AP + 12% magic lifesteal — same as 血族之书."),
  "Carano's Vow": ("炽热支配", "direct", "Low-HP cleanse + shield + lifesteal, near-identical to 炽热支配."),
  "Boomstick": ("回响之杖", "direct", "Skill-hit AoE explosion — 回响之杖's 回响, same numbers ballpark."),
  "Hecate's Diadem": ("博学者之怒", "direct", "Big-AP finisher with bonus % AP — that's 博学者之怒."),
  "Orb of the Magi": ("贤者天书", "loose", "Stacks AP/HP over time + level-up restore; closest WZRY scaler is 贤者天书."),
  "Rhea's Blessing": ("噬神之书", "direct", "AP + ~24% magic lifesteal + lifesteal-to-CDR conversion — same item concept."),
  "Zweihander": ("金色圣剑", "direct", "AP + stacking AS on-hit — 金色圣剑's 圣剑 passive."),
  "Frosty's Revenge": ("凝冰之息", "direct", "AP + slow on hit — 凝冰之息's 凝冰 slow."),
  "Berith's Agony": ("痛苦面具", "direct", "Skill applies % current-HP DoT — 痛苦面具's 折磨, same mechanic."),
  "Apocalypse": ("巫术法杖", "direct", "AP + CDR + skill-then-next-attack bonus — 巫术法杖's 强击."),
  "Soaring Aura": ("日暮之流", "direct", "Stacks a bonus on hitting heroes — 日暮之流's 净魔 stacks, same design."),
  "Holy of Holies": ("贤者天书", "direct", "+0.5% damage per 100 AP — identical to 贤者天书's 刻印."),
  "Arctic Orb": ("辉月", "direct", "Active invincibility + lifesteal — 辉月's 月之守护, same kit."),
  "Frost Guard": ("时之预言", "loose", "AP + stacking armor/magic defense — WZRY's defense stacker is 时之预言."),
  "Virtue's Necklace": ("圣杯", "direct", "AP + CDR + mana regen — 圣杯's mana-sustain role."),
  "Mage Robe": ("破茧之衣", "direct", "AP + HP + HP-to-AP + pen — 破茧之衣, near-identical."),
  "Staff of Nuul": ("虚无法杖", "direct", "AP + CDR + 40% magic pen — 虚无法杖 (45% pen), same job."),
  "Evil Secrets": ("虚无法杖", "loose", "Flat magic pen instead of percent — WZRY's pen finisher is 虚无法杖 (45%)."),
  "Tome of the Reaper": ("痛苦面具", "direct", "AP + CDR + HP + soul DoT on hit — 痛苦面具's role."),
  # Defense
  "Ring of Vitality": ("红玛瑙", "direct", "Same base HP starter (+300 HP)."),
  "Light Armor": ("布甲", "direct", "Same base armor starter."),
  "Gladiator's Gauntlets": ("抗魔斗篷", "direct", "Same base magic-defense starter."),
  "Talisman of Strength": ("—", "original", "Standalone HP-regen basic — WZRY has no such starter."),
  "Necklace of Vitality": ("力量腰带", "direct", "Mid HP brick, 力量腰带's role."),
  "Greaves of Protection": ("力量腰带", "direct", "Bigger HP brick — same 力量腰带 build path."),
  "Heart of Incubus": ("红莲斗篷", "direct", "Armor + burn aura — 红莲斗篷's 业炎."),
  "Belt of Clarity": ("魔女斗篷", "direct", "Magic def + HP + damage-mitigation, 魔女斗篷's role."),
  "Platinum Gauntlets": ("雪山圆盾", "direct", "Armor + CDR brick — 雪山圆盾, same stats shape."),
  "Knight's Plate": ("不祥征兆", "direct", "Slows the attacker's AS when hit — 不祥征兆's 寒铁."),
  "Mantle of Ra": ("红莲斗篷", "direct", "Armor + HP + burn aura — 红莲斗篷 again, the full version."),
  "Shield of the Lost": ("不祥征兆", "direct", "Slow/AS-reduce attacker on hit — 不祥征兆, same idea."),
  "The Aegis": ("不祥征兆", "loose", "Same tank stats, but the AoE attack-speed slow is unique to AoV."),
  "Gaia's Standard": ("永夜守护", "direct", "Magic def + burst-damage healing — 永夜守护's 守护."),
  "Medallion of Troy": ("魔女斗篷", "direct", "Magic def + CDR + magic shield — 魔女斗篷's 迷雾 shield."),
  "Blade of Eternity": ("贤者的庇护", "direct", "Once-per-game revive — 贤者的庇护's 复生."),
  "Frost Cape": ("冰痕之握", "direct", "Skill-then-slow-next-attack — 冰痕之握, physical tank version."),
  "Amulet of Longevity": ("霸者重装", "direct", "Out-of-combat HP regen — 霸者重装's 复苏, same mechanic."),
  "Rock Shield": ("旭日初光", "loose", "Active personal shield; WZRY's shield generators are 旭日初光/极寒风暴, no exact match."),
  "Mail of Pain": ("反伤刺甲", "direct", "Armor + damage thorn reflect — 反伤刺甲's 反刺."),
  "Hercules' Madness": ("暴烈之甲", "direct", "AD + armor + low-HP shield, 暴烈之甲's tank-hybrid role."),
  "Odin's Will": ("暴烈之甲", "loose", "Stacks damage/MS when hit — 暴烈之甲's 无畏 stacking, same design family."),
  # Movement
  "Boots of Speed": ("神速之靴", "direct", "Base movement boots (+30 MS), freely switchable — same as WZRY."),
  "Sonic Boots": ("影忍之足", "direct", "Armor + MS + phys damage reduction — 影忍之足, identical."),
  "Gilded Greaves": ("抵抗之靴", "direct", "Magic def + MS + CC resist — 抵抗之靴, identical."),
  "Flashy Boots": ("冷静之靴", "direct", "CDR boots — 冷静之靴, same thing."),
  "Enchanted Kicks": ("秘法之靴", "direct", "Magic-pen boots — 秘法之靴, same role."),
  "War Boots": ("急速战靴", "direct", "AS boots + on-hit regen — 急速战靴, identical."),
  "Hermes' Select": ("疾步之靴", "direct", "HP + big MS + out-of-combat speed — 疾步之靴, identical."),
  # Jungling
  "Kukri": ("狩猎宽刃", "direct", "Jungle starter — 狩猎宽刃, same entry item."),
  "Monster's Bane": ("游击弯刀", "direct", "AP jungle item (+40 AP + jungle dmg) — 游击弯刀, identical."),
  "Gnoll Cleaver": ("巡守利斧", "direct", "HP jungle item (+400 HP + burn) — 巡守利斧, identical."),
  "Mr. Stabby": ("追击刀锋", "direct", "AD jungle item (+25 AD) — 追击刀锋, identical."),
  "Whispering Wind": ("追击刀锋", "loose", "AS jungle item — WZRY has no AS jungle slot, use 追击刀锋."),
  "Loki's Curse": ("符文大剑", "direct", "AP jungle finisher (+AP + CDR) — 符文大剑, same tier."),
  "Leviathan": ("巨人之握", "direct", "HP jungle finisher (+1200 HP + CDR) — 巨人之握, same tier."),
  "Soulreaver": ("贪婪之噬", "direct", "AD jungle finisher (+90 AD + CDR) — 贪婪之噬, same tier."),
  "Scorching Wind": ("贪婪之噬", "loose", "AS + lifesteal jungle item — no WZRY equivalent, closest is 贪婪之噬."),
  # Support
  "Elemental Gem": ("学识宝石", "direct", "Roving support gem — 学识宝石, same experience/gold-share idea."),
}

# one-line reason for each hero's tier
TIER_REASON = {
  # TANK
  "Arduin":"Charge + damage reduction combo is reliable, strong early lane, but late-game output caps out",
  "Arthur":"Shield + stun + DR is zero-difficulty, strong early pressure, drops in team-fight value late",
  "Chaugnar":"Slow CC is easy to counter, no follow-up damage in fights, pure utility",
  "Cresht":"Transform form gives tankiness + AoE CC, strong engage, but useless if caught first",
  "Gildur":"Turret locks map zones, high magic damage, flexible mid/tank, top late-game ceiling",
  "Grakk":"Hook is a coin flip, no early value on a miss — high floor, low ceiling",
  "Lumburr":"Ult's AoE slow is a team tool, but own damage is low, needs team follow-up",
  "Maloch":"Shield + sustain wins early lanes, value drops after mid game",
  "Max":"Dive + true damage, strong in lane and fights, but no mobility, fears engage",
  "Mina":"DR + sustain is solid, but no decisive moment in team fights",
  "Omega":"Siege + control, strong late split-push, but needs the team to start fights",
  "Ormarr":"Petrify CC + tankiness is stable, but slow, damage depends on team",
  "Roxie":"Tank-wybrid has both sustain and damage but neither stands out, average",
  "Taara":"Sustain tank, strong attrition, but no CC, fights depend on the team",
  "Thane":"Dive initiate + shield, one of the most reliable first-strikers, ult is timing-dependent",
  "Toro":"Pure HP with no damage or CC, only a body block in fights",
  "Xeniel":"True-damage tank, strong early pressure, ult ceiling is average",
  "Y'bneth":"Strong early pressure but low late team-fight value, out of meta",
  "Ata":"Heal + shield is stable, but damage contribution is low",
  "Baldum":"Strong early/mid fights, falls off fast late game",
  "Arum":"Sustain tank support, heal + durability both online in fights, damage from the team",
  "Wiro":"Sustain tank support, kit is competent but not a meta pick",
  # WARRIOR
  "Airi":"Duel + ult burst strong early/mid, struggles vs tanks late",
  "Allain":"High-mobility duelist, skill-dependent, needs good fight entry",
  "Amily":"Dive burst can one-shot squishies with ult, but has no escape",
  "Astrid":"Solid dive, can play early, low ceiling late",
  "Dextra":"True-damage warrior, strong early pressure, needs protection late",
  "Errol":"Not strong in any phase, low ceiling",
  "Florentino":"Best-in-league 1v1 duelist, strong every phase, split-push and fights",
  "Kil'Groth":"CC + sustain is solid, but burst ceiling is average",
  "Lu Bu":"True damage carries every phase, but no mobility, fears CC",
  "Omen":"Ult teleport makes split-push threatening, can force 5v4, high pressure value",
  "Qi":"Transform warrior, decent early, ult ceiling is average",
  "Riktor":"Stable jungle tempo, but team-fight burst ceiling is low",
  "Rourke":"High mobility, hard to hit, strong in every phase",
  "Ryoma":"Sword-qi burst + mobility, strong early/mid, falls off late",
  "Skud":"Transform + stun is solid, but burst ceiling is average",
  "Superman":"Riding charge engage is strong, needs team damage follow-up",
  "Tachi":"Stable duelist but no standout mechanic",
  "Veres":"High-burst diver, can kill carries, entry-timing dependent",
  "Volkath":"Dive all comes from entry, a whiffed ult means no contribution",
  "Wonder Woman":"Complete kit but not meta-strong, middle-of-the-pack",
  "Yan":"High-mobility duelist, strong early/mid, average ceiling late",
  "Yena":"Dual-form burst, ult one-shots squishies, entry-dependent",
  "Zanis":"Leap-in burst, strong in fights, average in lane",
  "Zephys":"High-mobility dive, high ceiling but skill-dependent, drops a tier on whiffed ults",
  "Zuka":"High-mobility dive burst, high team-fight value",
  "Vei":"Can duelist early, low ceiling late",
  # ASSASSIN
  "Aoi":"Burst + smoke escape, strong early/mid, weak late",
  "Batman":"Stealth backstab, high burst, entry-timing dependent",
  "Bright":"Competent kit but burst ceiling is average",
  "Butterfly":"Stealth backstab + burst, one-shots, currently hard to counter",
  "Enzo":"High-burst assassin, kills carries, position-dependent",
  "Flash":"Has mobility and CC but low burst, weak in the current meta",
  "Keera":"Strong early burst, struggles vs tanks late",
  "Kriknak":"Hawk ult gives range plus mobility, high fight value",
  "Murad":"Time-burst is strong, but the kit is outdated",
  "Nakroth":"Many dashes, high ceiling, skill-dependent, drops on whiffed combos",
  "Paine":"Spirit-dive burst is high, but weak at farming and sieging",
  "Quillen":"New backstab design, high burst, position-dependent",
  "Raz":"Rolling burst, strong early, hard to hit",
  "Sinestrea":"Competent burst but ceiling is low",
  "Wukong":"Clones + true damage, strong early pressure, splits and shreds alike",
  "Zata":"Strong early/mid burst, weak vs tanks late",
  "Zill":"Mage-assassin hybrid, competent but not meta",
  "Billow":"Burst can kill carries, entry-timing dependent",
  # MAGE
  "Aleister":"Barrier CC is strong, but the kit is outdated",
  "Azzen'Ka":"Water CC + self-preservation, high utility, average damage",
  "D'Arcy":"Competent kit but low burst ceiling",
  "Diao Chan":"Ice CC is strong in fights, depends on landing the ult",
  "Dirak":"Burst is fine but lacks follow-up CC",
  "Iggy":"Fire control wins early, weak late",
  "Ignis":"Fire AoE is fine, outdated, average ceiling",
  "Ilumia":"Authority CC gives high fight value, depends on ult timing",
  "Ishar":"Mage-support hybrid, competent but niche in the meta",
  "Jinnar":"Keyboard AoE excels at farming and burst, strong every phase, sets the tempo",
  "Kahlii":"Ranged poke carries every phase, fears close-range engage",
  "Krixi":"Fan burst is strong early, hard to hit",
  "Lauriel":"Execution + sustain is top-tier, snowballs, T1 mid currently",
  "Liliana":"Dual-form burst is high, depends on form-switch timing",
  "Lorion":"Competent kit but low ceiling",
  "Marja":"Lifesteal + CC, strong in lane, high sustain in fights",
  "Mganga":"Poison + heal is fine, kit is outdated",
  "Natalya":"Top-tier AoE burst, damage online every phase, can duel or control teams",
  "Preyta":"Resistance-strip is outdated, average ceiling",
  "Sephera":"Mage-support hybrid, competent but niche in the meta",
  "Tulen":"Mobility + execution, drives tempo, high ceiling",
  "Veera":"Lock-on CC is easy to land, stable in fights",
  "Yue":"Original mage with high burst, depends on skill chaining",
  "Heino":"High burst + mobility, strong early pressure",
  "Dyadia":"Competent kit but low ceiling",
  # MARKSMAN
  "Brunhilda":"Competent kit but low late ceiling",
  "Capheny":"Kiting carries every phase, positioning-dependent",
  "Eland'orr":"Early burst + sustain, meta-strong marksman",
  "Elsu":"Ultra-long snipes hit hard, fears dive",
  "Erin":"Competent kit but not meta-strong",
  "Fennik":"Dart pressure is strong early, online every phase",
  "Hayate":"True-damage spin shots carry every phase, ignore magic resist, T1 marksman",
  "Laville":"High late output, early-game dive victim",
  "Lindis":"Trap CC is decent early, average ceiling",
  "Moren":"Not strong in any phase, low ceiling",
  "Slimz":"Original marksman, weak in meta, low ceiling",
  "Stuart":"Competent kit but low ceiling",
  "Teeri":"Boomerang kit is fine, average in the meta",
  "Tel'Annas":"Ultra-long range, top late output, fears dive",
  "The Joker":"Phys-immune mechanic is unique, strong vs physical comps",
  "Thorne":"Zone mechanic is fine, average in the meta",
  "Valhein":"Tri-color bullet kit is fine but not meta-strong",
  "Violet":"Rolling cannon is strong early, high mobility",
  "Wisp":"Original marksman, weak in meta, low ceiling",
  "Yorn":"Late turret output is high, early dive victim",
  # SUPPORT
  "Alice":"Time control is fine, average ceiling",
  "Annette":"High utility every phase, complete kit",
  "Aya":"Competent support kit but not meta-strong",
  "Helen":"Sustain support with high fight value, complete kit",
  "Krizzix":"Competent kit, average ceiling",
  "Ming":"Complete support kit, high fight value",
  "Payna":"Sustained healing + protection, online every phase",
  "Rouie":"Competent support, average ceiling",
  "TeeMee":"Gold + revive is valuable late, lacks protection early",
  "Zip":"Tank-support hybrid is fine, average ceiling",
}

ROLES = ["All","Tank","Warrior","Assassin","Mage","Marksman","Support"]
ROLE_KEY = {"Tank":"tank","Warrior":"warrior","Assassin":"assassin","Mage":"mage","Marksman":"marksman","Support":"support"}
# split into primary/secondary role for filter (filter by primary = first)
for x in H:
    x["role_key"] = ROLE_KEY[x["role"].split("/")[0]]
    x["is_original"] = x["mapping_type"] == "original"
    x["wzry_display"] = x["wzry_name"] if x["wzry_name"] != "—" else "无对应英雄"
    x["tier_reason"] = TIER_REASON.get(x["aov_name"], "")
    if not x["tier_reason"]:
        print("WARN: no tier_reason for", x["aov_name"])
    x["pinyin"] = PY[x["aov_cn"]]
    x["wzry_pinyin"] = "" if x["wzry_name"] == "—" else WZRY_PY[x["wzry_name"]]

print("total heroes:", len(H))
orig = sum(1 for x in H if x["is_original"])
print("originals:", orig, "ports/loose:", len(H)-orig)

OUT = os.path.dirname(os.path.abspath(__file__))
js = "const HEROES = " + json.dumps(H, ensure_ascii=False, indent=1) + ";\n"
js += "const ROLES = " + json.dumps(ROLES, ensure_ascii=False) + ";\n"
open(OUT+"/heroes.js","w",encoding="utf-8").write(js)
print("wrote heroes.js", os.path.getsize(OUT+"/heroes.js"))

# ---------- ITEMS ----------
if os.path.exists(OUT + "/items.json"):
    items = json.load(open(OUT + "/items.json", encoding="utf-8"))
    imap = json.load(open(OUT + "/items_iconmap.json", encoding="utf-8")) if os.path.exists(OUT + "/items_iconmap.json") else {}
    for it in items:
        m = ITEMS_MAP.get(it["name"])
        if not m:
            print("WARN: no mapping for item", it["name"])
            continue
        wzry_cn, mtype, reason = m
        it["wzry_cn"] = wzry_cn
        it["wzry_display"] = wzry_cn if wzry_cn != "—" else "No WZRY equivalent"
        it["mapping_type"] = mtype
        it["reason"] = reason
        it["icon"] = imap.get(it.get("icon_file", ""), "")
    ijs = "const ITEMS = " + json.dumps(items, ensure_ascii=False, indent=1) + ";\n"
    open(OUT + "/items.js", "w", encoding="utf-8").write(ijs)
    print("wrote items.js", os.path.getsize(OUT + "/items.js"), "items:", len(items))
