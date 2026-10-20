# -*- coding: utf-8 -*-
"""Download hero icons into images/. Run: python3 fetch_icons.py [start end] (default = all)."""
import os, subprocess, sys, urllib.request

ICONMAP = {
    "airi": ("images/airi.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/04999ff87145b9005694ffd78e1530a660017059a8fc11.jpg"),
    "aleister": ("images/aleister.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/15600.jpg"),
    "alice": ("images/alice.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/b9dd8e24c0fbad107475f6e31f5e36365847d373da15b1.png"),
    "allain": ("images/allain.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/3aa1f0f335f87801117dbfa1d69b072b5ef1f1c297fe21.jpg"),
    "amily": ("images/amily.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/65b8d8e674af00ee4ecbb4030e8fac385b88ea13824d31.jpg"),
    "annette": ("images/annette.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/17f4f562b9121128b4aff9e7b41644185f041e77964551.jpg"),
    "aoi": ("images/aoi.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/f1db425eba8ea88e5d4d8427c1706bcf6100183de1cc11.jpeg"),
    "arduin": ("images/arduin.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/8ac7305489de39cfaa10eb13f5a7824559bb7d0c7f2cc1.jpg"),
    "arthur": ("images/arthur.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/06/Honeyview_Arthur_111-e1718875297358.jpg"),
    "arum": ("images/arum.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/7faf7c96faeb8721b936e323becb57265afea9c3c8b281.jpg"),
    "astrid": ("images/astrid.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/91a969152f4340611e12e4eeb96a9aa259e021a48fbe91.jpg"),
    "ata": ("images/ata.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/71f7a36c0dd250ce0affeffcf14360f45e57c0420b4b61.jpg"),
    "aya": ("images/aya.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/d4510fa53f153c5e259543597c96bb88658d3efcbcd0f1.jpg"),
    "azzenka": ("images/azzenka.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/12700_B51-1.jpg"),
    "baldum": ("images/baldum.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/e751e70db18557783c2d23c9e5383e095b6bb947482b11.jpg"),
    "batman": ("images/batman.jpg", "https://static.wikia.nocookie.net/strikeofkings_gamepedia_en/images/f/f1/Batman_Leatherwing.jpg/revision/latest/scale-to-width-down/400?cb=20180314070053"),
    "billow": ("images/billow.jpg", "https://lienquan.garena.vn/wp-content/uploads/2025/01/59900-2.jpg"),
    "bright": ("images/bright.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/0045a9d59dc140647f4fa67b446c732c5fc55919650441.jpg"),
    "brunhilda": ("images/brunhilda.jpg", "https://static.wikia.nocookie.net/strikeofkings_gamepedia_en/images/d/d2/Brunhilda_profile.jpg/revision/latest/scale-to-width-down/400?cb=20200531221741"),
    "butterfly": ("images/butterfly.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/769a9fe6cb9b9725127a094bb6dd36545f0ed6543592e1.jpg"),
    "capheny": ("images/capheny.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/5c3212f3d7a6f95ad04a309d4d1f340a5ca5c222bda911.jpg"),
    "chaugnar": ("images/chaugnar.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/3eb3c69cef807c5706a98cc4b799619b5b3456990e6501.jpg"),
    "cresht": ("images/cresht.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/04b0a1140d89b8ef0cd4a655753bbb895c4938662bc9f1.jpg"),
    "darcy": ("images/darcy.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/903191ed8212c2c6c91f1f6f0a677a565c6102d8ecf4a1.jpg"),
    "dextra": ("images/dextra.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/38f3158929eb4b95500db65559e52d525fc5244a521d11.jpg"),
    "diaochan": ("images/diaochan.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/d93ee5059a95c391548419e69b6b9d1a5d2564f4eba891.jpg"),
    "dirak": ("images/dirak.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/ab0b68ebd2e8df3116d91231ec0e55fc5e16e1f05c8701-1.jpg"),
    "dyadia": ("images/dyadia.jpg", "https://lienquan.garena.vn/wp-content/uploads/2026/01/SeaTalk_IMG_20260119_104427.jpg"),
    "elandorr": ("images/elandorr.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/060f8e35db2f7fb1be51d7e5bdd1724a5db174d49d9de1.jpg"),
    "elsu": ("images/elsu.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/449789489494c0f108a3db5db3098e585bc98d17e666b1.jpg"),
    "enzo": ("images/enzo.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/81d7c827262287ce87639f3bfa048f5a5d149a6d571091.jpg"),
    "erin": ("images/erin.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/a1d3b1c36a643cb6d58c704139a2c24d65af7afac34cb1.jpg"),
    "errol": ("images/errol.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/5067bb53ba6435e11cc8777645d8de115cc136a9ca3b31.jpg"),
    "fennik": ("images/fennik.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/ab3f51a9731ffa085fd56a87139b8a775860e26837e191.jpg"),
    "flash": ("images/flash.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/dbb8d783c711cc0d2961e72cc8ed122c5ad9685dd58c11.jpg"),
    "florentino": ("images/florentino.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/9527c1cbad1c0656d0a4adf1dcec38e35c25f62d77d671.jpg"),
    "gildur": ("images/gildur.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/10800_B40-1.jpg"),
    "grakk": ("images/grakk.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/040403525e2882c0e3a6794c31976c89585357ba19a351.png"),
    "hayate": ("images/hayate.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/02c8e3d1db8ee8f32913b478884f33e05c8f254a7686f1.jpg"),
    "heino": ("images/heino.jpg", "https://lienquan.garena.vn/wp-content/uploads/2025/04/heino-2.jpg"),
    "helen": ("images/helen.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/e645dfa331fa48d593b33352e1f8030e636e1b3e19b951.jpg"),
    "iggy": ("images/iggy.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/b4563fbfd5756caeea04b7ef488ee39f60fffd803e9ab1.jpeg"),
    "ignis": ("images/ignis.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/a2c0e8ef7742c926f9bb10fbab12b03d5970da7009dc11.jpg"),
    "ilumia": ("images/ilumia.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/7ae8bcd437d0787c9f3bb9aa54907ede5ef5e858aff141.jpg"),
    "ishar": ("images/ishar.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/1009dcdfe78de2f6bc7fbdaea21cabc05df2198341d451.jpg"),
    "jinnar": ("images/jinnar.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/f3b0dc924b34f76c9265adb57758817a5b752794c417a1.jpg"),
    "kahlii": ("images/kahlii.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/fe313975ef498b33a7bf995a05d6f8b75847d42a599181.png"),
    "keera": ("images/keera.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/8491520381ab2a66489a6c5e1ec98e785e452a5c9fd3c1.jpg"),
    "kilgroth": ("images/kilgroth.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/4dd76a3f07965ade3c71b89874b64b935a29291ca4a111.gif"),
    "kriknak": ("images/kriknak.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/0dac2ca73eb28c03de2e43f85e868df458e710b5baeb41.png"),
    "krixi": ("images/krixi.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/7f04b1fd7f0520dd1ccbd1caad6faf1a5847d3f72e85b1.png"),
    "krizzix": ("images/krizzix.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/a7e49f01ef9804d479cb6537a9b51dee5db6c75c945151.png"),
    "lauriel": ("images/lauriel.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/18d4327ac2e366a736a060be082bbbef5943917dab8d81.jpg"),
    "laville": ("images/laville.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/c30059d2dc46ed31b72a4b02aa9e61f75eb136829228d1.jpg"),
    "liliana": ("images/liliana.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/28b06811cb721a8ecb28d6a1db401e745a9fd3a39ae401.jpg"),
    "lindis": ("images/lindis.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/4b2928793044600d4ca60ec95fb31f205a73d88927ca01.jpg"),
    "lorion": ("images/lorion.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/dab2c45af3206cd0ac30b450357aa8ce5fc5264d71f451.jpg"),
    "lubu": ("images/lubu.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/ecbf2434edb2b16cc0d5b286a88ab4335d2565110472b1.jpg"),
    "lumburr": ("images/lumburr.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/119dc57d5a3a59b520b93a42301ffb135e7dedbf1c28a1.jpg"),
    "maloch": ("images/maloch.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/752c4c954aa4a8f05a1b0be72aa5dc895c0def4d435aa1.jpg"),
    "marja": ("images/marja.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/1303e95b29e784888ae02d97848aed775b2b84e0372771.jpg"),
    "max": ("images/max.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/18000_B52-1.jpg"),
    "mganga": ("images/mganga.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/053654897539713c86a745376bc8e8125d25652cf33f01.jpg"),
    "mina": ("images/mina.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/09d93eb47007482254115f99686694d25847d3e83fdf41.png"),
    "ming": ("images/ming.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/58ba051be8f5ab56c0ea840ceb29c489658d529e847cf1.jpg"),
    "moren": ("images/moren.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/acqqwc-1.jpg"),
    "murad": ("images/murad.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/7dba55e7f433ab78ac6bd2cdfeec13495983e122346461.jpg"),
    "nakroth": ("images/nakroth.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/c7b840bdacd7e5a8b83af72ccd9ca1815ec64fdc5ffeb1.jpg"),
    "natalya": ("images/natalya.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/a450850337d6a5d19250b1d1e39692f15eccc530c915e1.jpg"),
    "omega": ("images/omega.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/cb7b811e7978882aefac079de6c93daf5fbcc5716f8ad1.jpg"),
    "omen": ("images/omen.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/00a78d4f7222a428cd06b45252f88a565a73df2c56ad81.jpg"),
    "ormarr": ("images/ormarr.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/fd2a04f2b129ef58988f2d311eac83e45b6d0919e7d901.jpg"),
    "paine": ("images/paine.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/47861c6d53d72d0dbea2d1dba0b0e0365e8ade6f180931.jpg"),
    "payna": ("images/payna.jpg", "https://static.wikia.nocookie.net/strikeofkings_gamepedia_en/images/3/37/Peura_Splash_Art.jpg/revision/latest/scale-to-width-down/400?cb=20260125083658"),
    "preyta": ("images/preyta.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/p1.jpeg"),
    "qi": ("images/qi.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/6da178e8a2c2871aeb856bec0f669ccd5d5684e01acd31.jpg"),
    "quillen": ("images/quillen.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/f6004ed060dcff380fc5b13574986bbc5bf778bc905561.jpg"),
    "raz": ("images/raz.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/6b79035779ab9195c76d91b3f2e7ca79591e6857831601.jpg"),
    "riktor": ("images/riktor.jpg", "https://static.wikia.nocookie.net/strikeofkings_gamepedia_en/images/7/7e/Riktor_Splash_Art.jpg/revision/latest/scale-to-width-down/400?cb=20220312122309"),
    "rouie": ("images/rouie.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/7f7ce6b3593a8ea52de5fa3be55469f85eb1402d093b71.jpg"),
    "rourke": ("images/rourke.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/749d47479eb9744d656b5e7c59f213555b1914bf90d291.jpg"),
    "roxie": ("images/roxie.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/51400-1.jpg"),
    "ryoma": ("images/ryoma.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/2f3fe854b98e664415c024a1e9f0396259d9b9ddb39921.jpg"),
    "sephera": ("images/sephera.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/eef053fb25793d536185559e8bf5a82d5c132caaa102e1.jpg"),
    "sinestrea": ("images/sinestrea.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/680ef284724e077237f33cfc2d8fa72d5fa194bad60f31.jpg"),
    "skud": ("images/skud.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/2b128ebef47ab5a8a2ae9d3db754cd585ee5e21149f621.jpg"),
    "slimz": ("images/slimz.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/122fe2fc229ca42dcbe6946db07ccd435b345a87702a11.png"),
    "stuart": ("images/stuart.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/aaba7b63f6e2f5577fbb3465925c8026658d3d704767f1.jpg"),
    "superman": ("images/superman.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/3310a88f1a679a6940e2f6e0da287c415a02b6ac709e01.jpg"),
    "taara": ("images/taara.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/f69423f533b12cbcd8ab15a7127e1e445e79e0b77e4ec1.jpg"),
    "tachi": ("images/tachi.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/ea94a6f76e867283974c8ced9d3aa2c5658d3150230cf1.jpg"),
    "teemee": ("images/teemee.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/d048143eef92ff2734c99f53b46e19db5a4dabef8a0fe1.jpg"),
    "teeri": ("images/teeri.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/3499773a79087475e48194e0fd02e27d658d428c2cbe51.jpg"),
    "telannas": ("images/telannas.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/5064b1bbcb8dcac94f88292537d6c35459e96577aa90c1.jpg"),
    "thane": ("images/thane.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/71e488144b7dc9f13d40321ce0556efc5847d39f2071a1.png"),
    "thejoker": ("images/thejoker.png", "https://static.wikia.nocookie.net/strikeofkings_gamepedia_en/images/2/28/The_Joker_Avatar.png/revision/latest/scale-to-width-down/400?cb=20180308200632"),
    "thorne": ("images/thorne.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/dd8031b80a4fc5978cdd4886a65a6eb35f5070fd5d0221.jpg"),
    "toro": ("images/toro.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/ffd2c29391b67831e97a0b16534a65d45ef5921c2bcb41.jpg"),
    "tulen": ("images/tulen.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/07210c9e529faa7766ba324bd86b75165a81722f3eab81.jpg"),
    "valhein": ("images/valhein.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/4b36c6e5e2d1ce9dd9e2841d2902043c5ee04efeb2f2d1.jpg"),
    "veera": ("images/veera.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/82a7e1d31f6b20d3faa502e1a215b76c6595119091e7a2-e1718879982854.jpg"),
    "veres": ("images/veres.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/46c5f246040b9e750779aa41ffcbeaa15c3f06d63ce241.jpg"),
    "violet": ("images/violet.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/f91d8c95b3b0c11c6fe5b8ac20e48cbd5d25650254d571.jpg"),
    "volkath": ("images/volkath.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/219b09a656af5274629409109ea2802d5d9472fe58bd81.jpg"),
    "wiro": ("images/wiro.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/61015ea8f83c0a833833297bb927ccd35be3c4834cd261.jpg"),
    "wisp": ("images/wisp.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/f3a7fe63c79a26ea789064ea3361781f5aec0b6084aa01.jpg"),
    "wonderwoman": ("images/wonderwoman.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/108ae03944a6aa1eb4313a2baa64efcd5a0e6c1551db11.jpg"),
    "wukong": ("images/wukong.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/aea009bf921dd684d19ee76c0c1441215ef5c39d1bd6b1.jpg"),
    "xeniel": ("images/xeniel.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/a56369ce162e24700689527a54d89b755a179e8628f391.jpg"),
    "yan": ("images/yan.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/f9471319a98fac8dce266dc86cd1efea658d4042ae0051.jpg"),
    "ybneth": ("images/ybneth.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/173809566ede28d1fee0731e43a1912c5b98deb97c82f1.jpg"),
    "yena": ("images/yena.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/61fa157164bf9d99e65bf40b802fb5745cfe1cd72c4671.jpg"),
    "yorn": ("images/yorn.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/44086d0bc26a170b21038a7cbf9413365c4938b95b2f91.jpg"),
    "yue": ("images/yue.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/3ee26051086fee856dc6df74811e9e35658d4142ce14c1.jpg"),
    "zanis": ("images/zanis.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/d7088075d6e144e11f476782718320865d256521539c41.jpg"),
    "zata": ("images/zata.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/fcd5c439a7cc37896ab98d568b662bec5ec66637da75d1.jpg"),
    "zephys": ("images/zephys.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/zephys-1.jpg"),
    "zill": ("images/zill.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/b1a6c37ad9558ac5767e25ded5b6fcf759966ca7c1d431.jpg"),
    "zip": ("images/zip.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/e0f8f382d1be41adc8947bf1b849479b5d3823c7418f71.jpg"),
    "zuka": ("images/zuka.jpg", "https://lienquan.garena.vn/wp-content/uploads/2024/05/d5166c51f37b444810f2ae3df056920d5c4938c59a4821.jpg"),
}

# wikia CDN (fandom splash fallbacks) rejects requests without a fandom Referer
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36",
      "Referer": "https://arenaofvalor.fandom.com/"}

def main():
    args = sys.argv[1:]
    items = sorted(ICONMAP.items())
    if len(args) == 2:
        items = items[int(args[0]):int(args[1])]
    os.makedirs("images", exist_ok=True)
    ok = skip = fail = 0
    for slug, (path, url) in items:
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            skip += 1
            continue
        try:
            try:
                req = urllib.request.Request(url, headers=UA)
                data = urllib.request.urlopen(req, timeout=30).read()
            except Exception:
                # curl has different TLS/header fingerprinting; wikia CDN accepts it
                data = subprocess.run(["curl", "-sf", "--max-time", "30",
                                       "-A", "Mozilla/5.0 Chrome/120", "-e", UA["Referer"], url],
                                      capture_output=True, timeout=40).stdout
            if len(data) < 500:
                raise ValueError("too small: %d bytes" % len(data))
            open(path, "wb").write(data)
            ok += 1
        except Exception as e:
            fail += 1
            print("FAIL", slug, e)
    print("chunk done: ok=%d skip=%d fail=%d" % (ok, skip, fail))

main()
