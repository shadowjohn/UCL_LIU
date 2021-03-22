# -*- coding: utf-8 -*-
VERSION=1.32
import portalocker
import os
import sys
import gtk
from gtk import gdk 
    
import gobject
import hashlib
import php
import re
import win32api
import configparser
#,,,z ,,,x 用thread去輸出字
import thread
import base64
import random
# 播放打字音用
#from pydub import AudioSegment
#from pydub.playback import play
paudio_player = None



#切中文使用
from re import compile as _Re
_unicode_chr_splitter = _Re( '(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)' ).split
#import atexit
def split_unicode_chrs( text ):
  return [ chr for chr in _unicode_chr_splitter( text ) if chr ]
# Fix exit crash problem
# 改用 
# https://stackoverflow.com/questions/23727539/runtime-error-in-python/24035224#24035224
'''
def cleanup():
  timeout_sec = 5
  for p in all_processes: # list of your processes
    p_sec = 0
    for second in range(timeout_sec):
      if p.poll() == None:
        time.sleep(1)
        p_sec += 1
    if p_sec >= timeout_sec:
      p.kill() # supported from python 2.6
  #print 'cleaned up!'
  #atexit.register(cleanup)  
def win_kill(pid):
  # From : https://stackoverflow.com/questions/320232/ensuring-subprocesses-are-dead-on-exiting-python-program
  #kill a process by specified PID in windows
  import win32api
  import win32con
  hProc = None
  try:
    hProc = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
    win32api.TerminateProcess(hProc, 0)
  except Exception:
    return False
  finally:
    if hProc != None:
        hProc.Close()
  return True
'''    
# 用來取反白字
# https://stackoverflow.com/questions/1007185/how-to-retrieve-the-selected-text-from-the-active-window
# import win32ui
# https://superuser.com/questions/1120624/run-script-on-any-selected-text

# 額外出字處理的 app
f_arr = [ "putty","pietty","pcman","xyplorer","kinza.exe","oxygennotincluded.exe","iedit.exe","iedit_.exe" ]
f_big5_arr = [ "zip32w","daqkingcon.exe","EWinner.exe" ]

# 2019-10-20 增加出字模式
UCL_PIC_BASE64 = "AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAMIOAADCDgAAAAAAAAAAAAD////////////////////////////////////////////////////////////////////////////////////////////////+/v7//Pz8//v7+//7+/v//f39////////////////////////////////////////////////////////////1s7B/1pVU/9PT0//Tk5Q/56rtP/Cua7/bGlp/2pqa/9tbGz/ampp/25xd//R2eL//////////////////////8O1of8kIyn/fYCD/0A0Lf9vgZD/kIJv/yUrMv9WUEr/FBcd/19eXv8fHR//q7zL///////////////////////CtKH/MDE4/6qwt/9zZFf/boCP/49/bf9VZXf/v7Ok/y0zP//T09P/QDcw/6q7yv//////////////////////w7Wj/yEcGv8pKy//OTUy/3GCkf+Pf23/VWV3/7+zo/8sMz//09PS/0A3MP+qu8r//////////////////////8KzoP84O0H/b2to/y4pJf9wgpH/j4Bt/1BfcP+1qpv/KjA7/8fHx/89NC//qrvK///////////////////////Cs6D/O0FM/9HS0f9IOi//boGQ/5KCcP8UFhn/Ly0p/w0PEv80MzP/FRcc/62+zP//////////////////////wrOh/zI1Ov9hXFT/AwAB/3GDk/+QgW//NkBK/6iqrP+trKz/qqqq/62vs//l6u///////////////////////76vnf8aFhb/Mzs+/0M9OP9wgpD/j39t/1Fhc//7//////////////////////////////////////////////+vnYv/QUtX/9ff3/96alv/bX+P/49/bf9RYHL/+/7/////////////v7Ko/5ifqf/7/v//////////////////inhn/19vgf//////fGpa/21/jv+Of23/UWBy//v+/////////////4Z0Yv9KWmv/+f3/////////////+/bv/1pNQv+Kmaf/samg/z01L/93iZn/n5B+/ygrMf93eXr/fHx8/3p4dv8vKib/eIqc//////////////////37+P/Mycf/5+rt/9HMxv+zs7X/3uPo/+zo4/+4trT/srKy/7Kysv+ysrL/tba5/+Tp7v//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
DEFAULT_OUTPUT_TYPE = "DEFAULT"
#BIG5
#PASTE

# 不使用肥米的 app
# 2021-03-19 2077 也不能使用肥米
f_pass_app = [ "mstsc.exe","Cyberpunk2077.exe" ]

#import pywinauto             
#pwa = pywinauto.keyboard

my = php.kit()

reload(sys)
sys.setdefaultencoding('UTF-8')

# Debug 模式
is_DEBUG_mode = False



message = ("\nUCLLIU 肥米輸入法\nBy 羽山秋人(http://3wa.tw)\nVersion: %s\n\n若要使用 Debug 模式：uclliu.exe -d\n" % (VERSION));

TC_CDATA = u"万与丑专业丛东丝丢两严丧个丬丰临为丽举么义乌乐乔习乡书买乱争于亏云亘亚产亩亲亵亸亿仅从仑仓仪们价众优伙会伛伞伟传伤伥伦伧伪伫体余佣佥侠侣侥侦侧侨侩侪侬俣俦俨俩俪俭债倾偬偻偾偿傥傧储傩儿兑兖党兰关兴兹养兽冁内冈册写军农冢冯冲决况冻净凄凉凌减凑凛几凤凫凭凯击凼凿刍划刘则刚创删别刬刭刽刿剀剂剐剑剥剧劝办务劢动励劲劳势勋勐勚匀匦匮区医华协单卖卢卤卧卫却卺厂厅历厉压厌厍厕厢厣厦厨厩厮县参叆叇双发变叙叠叶号叹叽吁后吓吕吗吣吨听启吴呒呓呕呖呗员呙呛呜咏咔咙咛咝咤咴咸哌响哑哒哓哔哕哗哙哜哝哟唛唝唠唡唢唣唤唿啧啬啭啮啰啴啸喷喽喾嗫呵嗳嘘嘤嘱噜噼嚣嚯团园囱围囵国图圆圣圹场坂坏块坚坛坜坝坞坟坠垄垅垆垒垦垧垩垫垭垯垱垲垴埘埙埚埝埯堑堕塆墙壮声壳壶壸处备复够头夸夹夺奁奂奋奖奥妆妇妈妩妪妫姗姜娄娅娆娇娈娱娲娴婳婴婵婶媪嫒嫔嫱嬷孙学孪宁宝实宠审宪宫宽宾寝对寻导寿将尔尘尧尴尸尽层屃屉届属屡屦屿岁岂岖岗岘岙岚岛岭岳岽岿峃峄峡峣峤峥峦崂崃崄崭嵘嵚嵛嵝嵴巅巩巯币帅师帏帐帘帜带帧帮帱帻帼幂幞干并广庄庆庐庑库应庙庞废庼廪开异弃张弥弪弯弹强归当录彟彦彻径徕御忆忏忧忾怀态怂怃怄怅怆怜总怼怿恋恳恶恸恹恺恻恼恽悦悫悬悭悯惊惧惨惩惫惬惭惮惯愍愠愤愦愿慑慭憷懑懒懔戆戋戏戗战戬户扎扑扦执扩扪扫扬扰抚抛抟抠抡抢护报担拟拢拣拥拦拧拨择挂挚挛挜挝挞挟挠挡挢挣挤挥挦捞损捡换捣据捻掳掴掷掸掺掼揸揽揿搀搁搂搅携摄摅摆摇摈摊撄撑撵撷撸撺擞攒敌敛数斋斓斗斩断无旧时旷旸昙昼昽显晋晒晓晔晕晖暂暧札术朴机杀杂权条来杨杩杰极构枞枢枣枥枧枨枪枫枭柜柠柽栀栅标栈栉栊栋栌栎栏树栖样栾桊桠桡桢档桤桥桦桧桨桩梦梼梾检棂椁椟椠椤椭楼榄榇榈榉槚槛槟槠横樯樱橥橱橹橼檐檩欢欤欧歼殁殇残殒殓殚殡殴毁毂毕毙毡毵氇气氢氩氲汇汉污汤汹沓沟没沣沤沥沦沧沨沩沪沵泞泪泶泷泸泺泻泼泽泾洁洒洼浃浅浆浇浈浉浊测浍济浏浐浑浒浓浔浕涂涌涛涝涞涟涠涡涢涣涤润涧涨涩淀渊渌渍渎渐渑渔渖渗温游湾湿溃溅溆溇滗滚滞滟滠满滢滤滥滦滨滩滪漤潆潇潋潍潜潴澜濑濒灏灭灯灵灾灿炀炉炖炜炝点炼炽烁烂烃烛烟烦烧烨烩烫烬热焕焖焘煅煳熘爱爷牍牦牵牺犊犟状犷犸犹狈狍狝狞独狭狮狯狰狱狲猃猎猕猡猪猫猬献獭玑玙玚玛玮环现玱玺珉珏珐珑珰珲琎琏琐琼瑶瑷璇璎瓒瓮瓯电画畅畲畴疖疗疟疠疡疬疮疯疱疴痈痉痒痖痨痪痫痴瘅瘆瘗瘘瘪瘫瘾瘿癞癣癫癯皑皱皲盏盐监盖盗盘眍眦眬着睁睐睑瞒瞩矫矶矾矿砀码砖砗砚砜砺砻砾础硁硅硕硖硗硙硚确硷碍碛碜碱碹磙礼祎祢祯祷祸禀禄禅离秃秆种积称秽秾稆税稣稳穑穷窃窍窑窜窝窥窦窭竖竞笃笋笔笕笺笼笾筑筚筛筜筝筹签简箓箦箧箨箩箪箫篑篓篮篱簖籁籴类籼粜粝粤粪粮糁糇紧絷纟纠纡红纣纤纥约级纨纩纪纫纬纭纮纯纰纱纲纳纴纵纶纷纸纹纺纻纼纽纾线绀绁绂练组绅细织终绉绊绋绌绍绎经绐绑绒结绔绕绖绗绘给绚绛络绝绞统绠绡绢绣绤绥绦继绨绩绪绫绬续绮绯绰绱绲绳维绵绶绷绸绹绺绻综绽绾绿缀缁缂缃缄缅缆缇缈缉缊缋缌缍缎缏缐缑缒缓缔缕编缗缘缙缚缛缜缝缞缟缠缡缢缣缤缥缦缧缨缩缪缫缬缭缮缯缰缱缲缳缴缵罂网罗罚罢罴羁羟羡翘翙翚耢耧耸耻聂聋职聍联聩聪肃肠肤肷肾肿胀胁胆胜胧胨胪胫胶脉脍脏脐脑脓脔脚脱脶脸腊腌腘腭腻腼腽腾膑臜舆舣舰舱舻艰艳艹艺节芈芗芜芦苁苇苈苋苌苍苎苏苘苹茎茏茑茔茕茧荆荐荙荚荛荜荞荟荠荡荣荤荥荦荧荨荩荪荫荬荭荮药莅莜莱莲莳莴莶获莸莹莺莼萚萝萤营萦萧萨葱蒇蒉蒋蒌蓝蓟蓠蓣蓥蓦蔷蔹蔺蔼蕲蕴薮藁藓虏虑虚虫虬虮虽虾虿蚀蚁蚂蚕蚝蚬蛊蛎蛏蛮蛰蛱蛲蛳蛴蜕蜗蜡蝇蝈蝉蝎蝼蝾螀螨蟏衅衔补衬衮袄袅袆袜袭袯装裆裈裢裣裤裥褛褴襁襕见观觃规觅视觇览觉觊觋觌觍觎觏觐觑觞触觯詟誉誊讠计订讣认讥讦讧讨让讪讫训议讯记讱讲讳讴讵讶讷许讹论讻讼讽设访诀证诂诃评诅识诇诈诉诊诋诌词诎诏诐译诒诓诔试诖诗诘诙诚诛诜话诞诟诠诡询诣诤该详诧诨诩诪诫诬语诮误诰诱诲诳说诵诶请诸诹诺读诼诽课诿谀谁谂调谄谅谆谇谈谊谋谌谍谎谏谐谑谒谓谔谕谖谗谘谙谚谛谜谝谞谟谠谡谢谣谤谥谦谧谨谩谪谫谬谭谮谯谰谱谲谳谴谵谶谷豮贝贞负贠贡财责贤败账货质贩贪贫贬购贮贯贰贱贲贳贴贵贶贷贸费贺贻贼贽贾贿赀赁赂赃资赅赆赇赈赉赊赋赌赍赎赏赐赑赒赓赔赕赖赗赘赙赚赛赜赝赞赟赠赡赢赣赪赵赶趋趱趸跃跄跖跞践跶跷跸跹跻踊踌踪踬踯蹑蹒蹰蹿躏躜躯车轧轨轩轪轫转轭轮软轰轱轲轳轴轵轶轷轸轹轺轻轼载轾轿辀辁辂较辄辅辆辇辈辉辊辋辌辍辎辏辐辑辒输辔辕辖辗辘辙辚辞辩辫边辽达迁过迈运还这进远违连迟迩迳迹适选逊递逦逻遗遥邓邝邬邮邹邺邻郁郄郏郐郑郓郦郧郸酝酦酱酽酾酿释里鉅鉴銮錾钆钇针钉钊钋钌钍钎钏钐钑钒钓钔钕钖钗钘钙钚钛钝钞钟钠钡钢钣钤钥钦钧钨钩钪钫钬钭钮钯钰钱钲钳钴钵钶钷钸钹钺钻钼钽钾钿铀铁铂铃铄铅铆铈铉铊铋铍铎铏铐铑铒铕铗铘铙铚铛铜铝铞铟铠铡铢铣铤铥铦铧铨铪铫铬铭铮铯铰铱铲铳铴铵银铷铸铹铺铻铼铽链铿销锁锂锃锄锅锆锇锈锉锊锋锌锍锎锏锐锑锒锓锔锕锖锗错锚锜锞锟锠锡锢锣锤锥锦锨锩锫锬锭键锯锰锱锲锳锴锵锶锷锸锹锺锻锼锽锾锿镀镁镂镃镆镇镈镉镊镌镍镎镏镐镑镒镕镖镗镙镚镛镜镝镞镟镠镡镢镣镤镥镦镧镨镩镪镫镬镭镮镯镰镱镲镳镴镶长门闩闪闫闬闭问闯闰闱闲闳间闵闶闷闸闹闺闻闼闽闾闿阀阁阂阃阄阅阆阇阈阉阊阋阌阍阎阏阐阑阒阓阔阕阖阗阘阙阚阛队阳阴阵阶际陆陇陈陉陕陧陨险随隐隶隽难雏雠雳雾霁霉霭靓静靥鞑鞒鞯鞴韦韧韨韩韪韫韬韵页顶顷顸项顺须顼顽顾顿颀颁颂颃预颅领颇颈颉颊颋颌颍颎颏颐频颒颓颔颕颖颗题颙颚颛颜额颞颟颠颡颢颣颤颥颦颧风飏飐飑飒飓飔飕飖飗飘飙飚飞飨餍饤饥饦饧饨饩饪饫饬饭饮饯饰饱饲饳饴饵饶饷饸饹饺饻饼饽饾饿馀馁馂馃馄馅馆馇馈馉馊馋馌馍馎馏馐馑馒馓馔馕马驭驮驯驰驱驲驳驴驵驶驷驸驹驺驻驼驽驾驿骀骁骂骃骄骅骆骇骈骉骊骋验骍骎骏骐骑骒骓骔骕骖骗骘骙骚骛骜骝骞骟骠骡骢骣骤骥骦骧髅髋髌鬓魇魉鱼鱽鱾鱿鲀鲁鲂鲄鲅鲆鲇鲈鲉鲊鲋鲌鲍鲎鲏鲐鲑鲒鲓鲔鲕鲖鲗鲘鲙鲚鲛鲜鲝鲞鲟鲠鲡鲢鲣鲤鲥鲦鲧鲨鲩鲪鲫鲬鲭鲮鲯鲰鲱鲲鲳鲴鲵鲶鲷鲸鲹鲺鲻鲼鲽鲾鲿鳀鳁鳂鳃鳄鳅鳆鳇鳈鳉鳊鳋鳌鳍鳎鳏鳐鳑鳒鳓鳔鳕鳖鳗鳘鳙鳛鳜鳝鳞鳟鳠鳡鳢鳣鸟鸠鸡鸢鸣鸤鸥鸦鸧鸨鸩鸪鸫鸬鸭鸮鸯鸰鸱鸲鸳鸴鸵鸶鸷鸸鸹鸺鸻鸼鸽鸾鸿鹀鹁鹂鹃鹄鹅鹆鹇鹈鹉鹊鹋鹌鹍鹎鹏鹐鹑鹒鹓鹔鹕鹖鹗鹘鹚鹛鹜鹝鹞鹟鹠鹡鹢鹣鹤鹥鹦鹧鹨鹩鹪鹫鹬鹭鹯鹰鹱鹲鹳鹴鹾麦麸黄黉黡黩黪黾鼋鼌鼍鼗鼹齄齐齑齿龀龁龂龃龄龅龆龇龈龉龊龋龌龙龚龛龟志制咨只里系范松没尝尝闹面准钟别闲干尽脏拼";
TC_TDATA = u"萬與醜專業叢東絲丟兩嚴喪個爿豐臨為麗舉麼義烏樂喬習鄉書買亂爭於虧雲亙亞產畝親褻嚲億僅從侖倉儀們價眾優夥會傴傘偉傳傷倀倫傖偽佇體餘傭僉俠侶僥偵側僑儈儕儂俁儔儼倆儷儉債傾傯僂僨償儻儐儲儺兒兌兗黨蘭關興茲養獸囅內岡冊寫軍農塚馮衝決況凍淨淒涼淩減湊凜幾鳳鳧憑凱擊氹鑿芻劃劉則剛創刪別剗剄劊劌剴劑剮劍剝劇勸辦務勱動勵勁勞勢勳猛勩勻匭匱區醫華協單賣盧鹵臥衛卻巹廠廳曆厲壓厭厙廁廂厴廈廚廄廝縣參靉靆雙發變敘疊葉號歎嘰籲後嚇呂嗎唚噸聽啟吳嘸囈嘔嚦唄員咼嗆嗚詠哢嚨嚀噝吒噅鹹呱響啞噠嘵嗶噦嘩噲嚌噥喲嘜嗊嘮啢嗩唕喚呼嘖嗇囀齧囉嘽嘯噴嘍嚳囁嗬噯噓嚶囑嚕劈囂謔團園囪圍圇國圖圓聖壙場阪壞塊堅壇壢壩塢墳墜壟壟壚壘墾坰堊墊埡墶壋塏堖塒塤堝墊垵塹墮壪牆壯聲殼壺壼處備複夠頭誇夾奪奩奐奮獎奧妝婦媽嫵嫗媯姍薑婁婭嬈嬌孌娛媧嫻嫿嬰嬋嬸媼嬡嬪嬙嬤孫學孿寧寶實寵審憲宮寬賓寢對尋導壽將爾塵堯尷屍盡層屭屜屆屬屢屨嶼歲豈嶇崗峴嶴嵐島嶺嶽崠巋嶨嶧峽嶢嶠崢巒嶗崍嶮嶄嶸嶔崳嶁脊巔鞏巰幣帥師幃帳簾幟帶幀幫幬幘幗冪襆幹並廣莊慶廬廡庫應廟龐廢廎廩開異棄張彌弳彎彈強歸當錄彠彥徹徑徠禦憶懺憂愾懷態慫憮慪悵愴憐總懟懌戀懇惡慟懨愷惻惱惲悅愨懸慳憫驚懼慘懲憊愜慚憚慣湣慍憤憒願懾憖怵懣懶懍戇戔戲戧戰戩戶紮撲扡執擴捫掃揚擾撫拋摶摳掄搶護報擔擬攏揀擁攔擰撥擇掛摯攣掗撾撻挾撓擋撟掙擠揮撏撈損撿換搗據撚擄摑擲撣摻摜摣攬撳攙擱摟攪攜攝攄擺搖擯攤攖撐攆擷擼攛擻攢敵斂數齋斕鬥斬斷無舊時曠暘曇晝曨顯晉曬曉曄暈暉暫曖劄術樸機殺雜權條來楊榪傑極構樅樞棗櫪梘棖槍楓梟櫃檸檉梔柵標棧櫛櫳棟櫨櫟欄樹棲樣欒棬椏橈楨檔榿橋樺檜槳樁夢檮棶檢欞槨櫝槧欏橢樓欖櫬櫚櫸檟檻檳櫧橫檣櫻櫫櫥櫓櫞簷檁歡歟歐殲歿殤殘殞殮殫殯毆毀轂畢斃氈毿氌氣氫氬氳匯漢汙湯洶遝溝沒灃漚瀝淪滄渢溈滬濔濘淚澩瀧瀘濼瀉潑澤涇潔灑窪浹淺漿澆湞溮濁測澮濟瀏滻渾滸濃潯濜塗湧濤澇淶漣潿渦溳渙滌潤澗漲澀澱淵淥漬瀆漸澠漁瀋滲溫遊灣濕潰濺漵漊潷滾滯灩灄滿瀅濾濫灤濱灘澦濫瀠瀟瀲濰潛瀦瀾瀨瀕灝滅燈靈災燦煬爐燉煒熗點煉熾爍爛烴燭煙煩燒燁燴燙燼熱煥燜燾煆糊溜愛爺牘犛牽犧犢強狀獷獁猶狽麅獮獰獨狹獅獪猙獄猻獫獵獼玀豬貓蝟獻獺璣璵瑒瑪瑋環現瑲璽瑉玨琺瓏璫琿璡璉瑣瓊瑤璦璿瓔瓚甕甌電畫暢佘疇癤療瘧癘瘍鬁瘡瘋皰屙癰痙癢瘂癆瘓癇癡癉瘮瘞瘺癟癱癮癭癩癬癲臒皚皺皸盞鹽監蓋盜盤瞘眥矓著睜睞瞼瞞矚矯磯礬礦碭碼磚硨硯碸礪礱礫礎硜矽碩硤磽磑礄確鹼礙磧磣堿镟滾禮禕禰禎禱禍稟祿禪離禿稈種積稱穢穠穭稅穌穩穡窮竊竅窯竄窩窺竇窶豎競篤筍筆筧箋籠籩築篳篩簹箏籌簽簡籙簀篋籜籮簞簫簣簍籃籬籪籟糴類秈糶糲粵糞糧糝餱緊縶糸糾紆紅紂纖紇約級紈纊紀紉緯紜紘純紕紗綱納紝縱綸紛紙紋紡紵紖紐紓線紺絏紱練組紳細織終縐絆紼絀紹繹經紿綁絨結絝繞絰絎繪給絢絳絡絕絞統綆綃絹繡綌綏絛繼綈績緒綾緓續綺緋綽緔緄繩維綿綬繃綢綯綹綣綜綻綰綠綴緇緙緗緘緬纜緹緲緝縕繢緦綞緞緶線緱縋緩締縷編緡緣縉縛縟縝縫縗縞纏縭縊縑繽縹縵縲纓縮繆繅纈繚繕繒韁繾繰繯繳纘罌網羅罰罷羆羈羥羨翹翽翬耮耬聳恥聶聾職聹聯聵聰肅腸膚膁腎腫脹脅膽勝朧腖臚脛膠脈膾髒臍腦膿臠腳脫腡臉臘醃膕齶膩靦膃騰臏臢輿艤艦艙艫艱豔艸藝節羋薌蕪蘆蓯葦藶莧萇蒼苧蘇檾蘋莖蘢蔦塋煢繭荊薦薘莢蕘蓽蕎薈薺蕩榮葷滎犖熒蕁藎蓀蔭蕒葒葤藥蒞蓧萊蓮蒔萵薟獲蕕瑩鶯蓴蘀蘿螢營縈蕭薩蔥蕆蕢蔣蔞藍薊蘺蕷鎣驀薔蘞藺藹蘄蘊藪槁蘚虜慮虛蟲虯蟣雖蝦蠆蝕蟻螞蠶蠔蜆蠱蠣蟶蠻蟄蛺蟯螄蠐蛻蝸蠟蠅蟈蟬蠍螻蠑螿蟎蠨釁銜補襯袞襖嫋褘襪襲襏裝襠褌褳襝褲襇褸襤繈襴見觀覎規覓視覘覽覺覬覡覿覥覦覯覲覷觴觸觶讋譽謄訁計訂訃認譏訐訌討讓訕訖訓議訊記訒講諱謳詎訝訥許訛論訩訟諷設訪訣證詁訶評詛識詗詐訴診詆謅詞詘詔詖譯詒誆誄試詿詩詰詼誠誅詵話誕詬詮詭詢詣諍該詳詫諢詡譸誡誣語誚誤誥誘誨誑說誦誒請諸諏諾讀諑誹課諉諛誰諗調諂諒諄誶談誼謀諶諜謊諫諧謔謁謂諤諭諼讒諮諳諺諦謎諞諝謨讜謖謝謠謗諡謙謐謹謾謫譾謬譚譖譙讕譜譎讞譴譫讖穀豶貝貞負貟貢財責賢敗賬貨質販貪貧貶購貯貫貳賤賁貰貼貴貺貸貿費賀貽賊贄賈賄貲賃賂贓資賅贐賕賑賚賒賦賭齎贖賞賜贔賙賡賠賧賴賵贅賻賺賽賾贗讚贇贈贍贏贛赬趙趕趨趲躉躍蹌蹠躒踐躂蹺蹕躚躋踴躊蹤躓躑躡蹣躕躥躪躦軀車軋軌軒軑軔轉軛輪軟轟軲軻轤軸軹軼軤軫轢軺輕軾載輊轎輈輇輅較輒輔輛輦輩輝輥輞輬輟輜輳輻輯轀輸轡轅轄輾轆轍轔辭辯辮邊遼達遷過邁運還這進遠違連遲邇逕跡適選遜遞邐邏遺遙鄧鄺鄔郵鄒鄴鄰鬱郤郟鄶鄭鄆酈鄖鄲醞醱醬釅釃釀釋裏钜鑒鑾鏨釓釔針釘釗釙釕釷釺釧釤鈒釩釣鍆釹鍚釵鈃鈣鈈鈦鈍鈔鍾鈉鋇鋼鈑鈐鑰欽鈞鎢鉤鈧鈁鈥鈄鈕鈀鈺錢鉦鉗鈷缽鈳鉕鈽鈸鉞鑽鉬鉭鉀鈿鈾鐵鉑鈴鑠鉛鉚鈰鉉鉈鉍鈹鐸鉶銬銠鉺銪鋏鋣鐃銍鐺銅鋁銱銦鎧鍘銖銑鋌銩銛鏵銓鉿銚鉻銘錚銫鉸銥鏟銃鐋銨銀銣鑄鐒鋪鋙錸鋱鏈鏗銷鎖鋰鋥鋤鍋鋯鋨鏽銼鋝鋒鋅鋶鐦鐧銳銻鋃鋟鋦錒錆鍺錯錨錡錁錕錩錫錮鑼錘錐錦鍁錈錇錟錠鍵鋸錳錙鍥鍈鍇鏘鍶鍔鍤鍬鍾鍛鎪鍠鍰鎄鍍鎂鏤鎡鏌鎮鎛鎘鑷鐫鎳鎿鎦鎬鎊鎰鎔鏢鏜鏍鏰鏞鏡鏑鏃鏇鏐鐔钁鐐鏷鑥鐓鑭鐠鑹鏹鐙鑊鐳鐶鐲鐮鐿鑔鑣鑞鑲長門閂閃閆閈閉問闖閏闈閑閎間閔閌悶閘鬧閨聞闥閩閭闓閥閣閡閫鬮閱閬闍閾閹閶鬩閿閽閻閼闡闌闃闠闊闋闔闐闒闕闞闤隊陽陰陣階際陸隴陳陘陝隉隕險隨隱隸雋難雛讎靂霧霽黴靄靚靜靨韃鞽韉韝韋韌韍韓韙韞韜韻頁頂頃頇項順須頊頑顧頓頎頒頌頏預顱領頗頸頡頰頲頜潁熲頦頤頻頮頹頷頴穎顆題顒顎顓顏額顳顢顛顙顥纇顫顬顰顴風颺颭颮颯颶颸颼颻飀飄飆飆飛饗饜飣饑飥餳飩餼飪飫飭飯飲餞飾飽飼飿飴餌饒餉餄餎餃餏餅餑餖餓餘餒餕餜餛餡館餷饋餶餿饞饁饃餺餾饈饉饅饊饌饢馬馭馱馴馳驅馹駁驢駔駛駟駙駒騶駐駝駑駕驛駘驍罵駰驕驊駱駭駢驫驪騁驗騂駸駿騏騎騍騅騌驌驂騙騭騤騷騖驁騮騫騸驃騾驄驏驟驥驦驤髏髖髕鬢魘魎魚魛魢魷魨魯魴魺鮁鮃鯰鱸鮋鮓鮒鮊鮑鱟鮍鮐鮭鮚鮳鮪鮞鮦鰂鮜鱠鱭鮫鮮鮺鯗鱘鯁鱺鰱鰹鯉鰣鰷鯀鯊鯇鮶鯽鯒鯖鯪鯕鯫鯡鯤鯧鯝鯢鯰鯛鯨鯵鯴鯔鱝鰈鰏鱨鯷鰮鰃鰓鱷鰍鰒鰉鰁鱂鯿鰠鼇鰭鰨鰥鰩鰟鰜鰳鰾鱈鱉鰻鰵鱅鰼鱖鱔鱗鱒鱯鱤鱧鱣鳥鳩雞鳶鳴鳲鷗鴉鶬鴇鴆鴣鶇鸕鴨鴞鴦鴒鴟鴝鴛鴬鴕鷥鷙鴯鴰鵂鴴鵃鴿鸞鴻鵐鵓鸝鵑鵠鵝鵒鷳鵜鵡鵲鶓鵪鶤鵯鵬鵮鶉鶊鵷鷫鶘鶡鶚鶻鶿鶥鶩鷊鷂鶲鶹鶺鷁鶼鶴鷖鸚鷓鷚鷯鷦鷲鷸鷺鸇鷹鸌鸏鸛鸘鹺麥麩黃黌黶黷黲黽黿鼂鼉鞀鼴齇齊齏齒齔齕齗齟齡齙齠齜齦齬齪齲齷龍龔龕龜誌製谘隻裡係範鬆冇嚐嘗鬨麵準鐘彆閒乾儘臟拚";
mTC_CDATA = list(TC_CDATA);
mTC_TDATA = list(TC_TDATA);
def about_uclliu():
  _msg_text = ("肥米輸入法\n\n作者：羽山秋人 (http://3wa.tw)\n版本：%s" % VERSION)
  _msg_text += "\n\n熱鍵提示：\n\n"
  _msg_text += "「,,,VERSION」目前版本\n"
  _msg_text += "「,,,UNLOCK」回到正常模式\n"
  _msg_text += "「,,,LOCK」進入遊戲模式\n"
  _msg_text += "「,,,C」簡體模式\n"
  _msg_text += "「,,,T」繁體模式\n"
  _msg_text += "「,,,S」UI變窄\n"
  _msg_text += "「,,,L」UI變寬\n"
  _msg_text += "「,,,+」UI變大\n"
  _msg_text += "「,,,-」UI變小\n"
  _msg_text += "「,,,X」框字的字根轉回文字\n"
  _msg_text += "「,,,Z」框字的文字變成字根\n"
  return _msg_text  
def simple2trad(data):
  global mTC_TDATA
  global mTC_CDATA
  mdata = split_unicode_chrs(data)        
  for k in range(0,len(mdata)):
    if mdata[k] in mTC_CDATA:
      idx = mTC_CDATA.index(mdata[k])
      mdata[k] = mTC_TDATA[idx]  
  data = my.implode("",mdata)
  return data
def trad2simple(data):
  global mTC_TDATA
  global mTC_CDATA
  mdata = split_unicode_chrs(data)        
  for k in range(0,len(mdata)):
    if mdata[k] in mTC_TDATA:
      idx = mTC_TDATA.index(mdata[k])
      mdata[k] = mTC_CDATA[idx]  
  data = my.implode("",mdata)
  return data
  

if len(sys.argv)!=2:
  print( my.utf8tobig5(message) );
elif sys.argv[1]=="-d":
  is_DEBUG_mode = True

def debug_print(data):
  global is_DEBUG_mode
  if is_DEBUG_mode == True:
    print(data)
    
def md5_file(fileName):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        print("Reading file has problem:", filename)
        return
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest()


#PWD=my.pwd()   
PWD = os.path.dirname(os.path.realpath(sys.argv[0]))
#my.file_put_contents("c:\\temp\\aaa.txt",PWD);
#debug_print(PWD)
#sys.exit(0)

#此是防止重覆執行
#if os.path.isdir("C:\\temp") == False:
#  os.mkdir("C:\\temp")
check_file_run = open(PWD + '\\UCLLIU.lock', "a+")
try:  
  portalocker.lock(check_file_run, portalocker.LOCK_EX | portalocker.LOCK_NB)
except:
  md = gtk.MessageDialog(None, 
          gtk.DIALOG_DESTROY_WITH_PARENT, 
          gtk.MESSAGE_QUESTION, 
          gtk.BUTTONS_OK, "【肥米輸入法】已執行...")          
  md.set_position(gtk.WIN_POS_CENTER)
  response = md.run()            
  if response == gtk.RESPONSE_OK or response == gtk.RESPONSE_DELETE_EVENT:
    md.destroy()
    ctypes.windll.user32.PostQuitMessage(0)
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    sys.exit(0)
         
import ctypes
import pythoncom, pyHook
from pyHook import HookManager
from pyHook.HookManager import HookConstants 

import win32clipboard
import pango
import SendKeysCtypes
import time

#http://wiki.alarmchang.com/index.php?title=Python_%E5%AD%98%E5%8F%96_Windows_%E7%9A%84%E5%89%AA%E8%B2%BC%E7%B0%BF_ClipBoard_%E7%AF%84%E4%BE%8B
import win32gui
import win32process
import psutil
#import win32com
import win32con
#import win32com.client

#2018-07-13 1.12版增加
#檢查 C:\temp\UCLLIU.ini 初始化設定檔
#取螢幕大小

#2019-03-02 調整，將 UCLLIU.ini 跟隨在 UCLLIU.exe 旁
INI_CONFIG_FILE = 'C:\\temp\\UCLLIU.ini'
if my.is_file(INI_CONFIG_FILE):
  my.copy(INI_CONFIG_FILE,PWD+"\\UCLLIU.ini")
  my.unlink(INI_CONFIG_FILE)
INI_CONFIG_FILE = PWD + "\\UCLLIU.ini" 

#user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()

#screen_width=user32.GetSystemMetrics(0)
#screen_height=user32.GetSystemMetrics(1)
#debug_print("screen width, height : %s , %s" % (screen_width,screen_height))
#window = gtk.Window()
#From : https://www.familylifemag.com/question/701406/how-do-i-get-monitor-resolution-in-python
screen_width = gtk.gdk.screen_width()
screen_height = gtk.gdk.screen_height()

  
config = configparser.ConfigParser()
config['DEFAULT'] = {
                      "X": screen_width-700,
                      "Y": int(screen_height*0.87),
                      "ALPHA": "1", #嘸蝦米全顯示時時的初值
                      "SHORT_MODE": "0", #0:簡短畫面，或1:長畫面
                      "ZOOM": "1", #整體比例大小
                      "SEND_KIND_1_PASTE": "", #出字模式1
                      "SEND_KIND_2_BIG5": "", #出字模式2
                      "KEYBOARD_VOLUME": "30", #打字聲音量，0~100
                      "SP": "0", #短根
                      "CTRL_SP": "0", #使用CTRL+SPACE換肥米
                      "PLAY_SOUND_ENABLE": "0" #打字音
                    };
if my.is_file(INI_CONFIG_FILE):
  _config = configparser.ConfigParser()
  _config.read(INI_CONFIG_FILE)    
  for k in _config['DEFAULT'].keys(): # ['X','Y','ALPHA','ZOOM','SHORT_MODE','SEND_KIND_1_PASTE','SEND_KIND_2_BIG5'] 
    if k in config['DEFAULT'].keys():
      config['DEFAULT'][k]=_config['DEFAULT'][k]
      
config['DEFAULT']['X'] = str(int(config['DEFAULT']['X']));
config['DEFAULT']['Y'] = str(int(config['DEFAULT']['Y'])); 
config['DEFAULT']['ALPHA'] = "%.2f" % ( float(config['DEFAULT']['ALPHA'] ));
config['DEFAULT']['SHORT_MODE'] = str(int(config['DEFAULT']['SHORT_MODE']));
config['DEFAULT']['ZOOM'] = "%.2f" % ( float(config['DEFAULT']['ZOOM'] ));
config['DEFAULT']['SEND_KIND_1_PASTE'] = str(config['DEFAULT']['SEND_KIND_1_PASTE']);
config['DEFAULT']['SEND_KIND_2_BIG5'] = str(config['DEFAULT']['SEND_KIND_2_BIG5']);
config['DEFAULT']['KEYBOARD_VOLUME'] = str(int(config['DEFAULT']['KEYBOARD_VOLUME']));
config['DEFAULT']['SP'] = str(int(config['DEFAULT']['SP']));
config['DEFAULT']['CTRL_SP'] = str(int(config['DEFAULT']['CTRL_SP']));
config['DEFAULT']['PLAY_SOUND_ENABLE'] = str(int(config['DEFAULT']['PLAY_SOUND_ENABLE']));

# merge f_arr and f_big5_arr
config['DEFAULT']['SEND_KIND_1_PASTE'] = my.trim(config['DEFAULT']['SEND_KIND_1_PASTE'])
config['DEFAULT']['SEND_KIND_1_PASTE'] =  my.str_replace("\"","",config['DEFAULT']['SEND_KIND_1_PASTE'])
config['DEFAULT']['SEND_KIND_2_BIG5'] = my.trim(config['DEFAULT']['SEND_KIND_2_BIG5'])
config['DEFAULT']['SEND_KIND_2_BIG5'] =  my.str_replace("\"","",config['DEFAULT']['SEND_KIND_2_BIG5'])

if config['DEFAULT']['SEND_KIND_1_PASTE'] != "": 
  f_arr = f_arr + my.explode(",",config['DEFAULT']['SEND_KIND_1_PASTE'])
if config['DEFAULT']['SEND_KIND_2_BIG5'] != "": 
  f_big5_arr = f_big5_arr + my.explode(",",config['DEFAULT']['SEND_KIND_2_BIG5'])

if int(config['DEFAULT']['KEYBOARD_VOLUME']) < 0:
  config['DEFAULT']['KEYBOARD_VOLUME'] = "0"
if int(config['DEFAULT']['KEYBOARD_VOLUME']) > 100:
  config['DEFAULT']['KEYBOARD_VOLUME'] = "100"
  
#print(f_arr)
#print(f_big5_arr)

# array_unique
f_arr = list(set(f_arr))
f_big5_arr = list(set(f_big5_arr))
#print(f_arr)
#print(f_big5_arr)

if float(config['DEFAULT']['ALPHA'])>=1:
  config['DEFAULT']['ALPHA']="1"
if float(config['DEFAULT']['ALPHA'])<=0.1:
  config['DEFAULT']['ALPHA']="0.1"
  
if int(config['DEFAULT']['SHORT_MODE'])>=1:
  config['DEFAULT']['SHORT_MODE']="1"
if int(config['DEFAULT']['SHORT_MODE'])<=0:
  config['DEFAULT']['SHORT_MODE']="0"
  
if float(config['DEFAULT']['ZOOM'])>=3:
  config['DEFAULT']['ZOOM']="3"
if float(config['DEFAULT']['ZOOM'])<=0.1:
  config['DEFAULT']['ZOOM']="0.1"

if int(config['DEFAULT']['SP'])<=0:
  config['DEFAULT']['SP']="0"  
else:
  config['DEFAULT']['SP']="1"  
  
if int(config['DEFAULT']['CTRL_SP'])<=0:
  config['DEFAULT']['CTRL_SP']="0"  
else:
  config['DEFAULT']['CTRL_SP']="1"    

if int(config['DEFAULT']['PLAY_SOUND_ENABLE'])<=0:
  config['DEFAULT']['PLAY_SOUND_ENABLE']="0"  
else:
  config['DEFAULT']['PLAY_SOUND_ENABLE']="1"  

# GUI Font
GLOBAL_FONT_FAMILY = "Mingliu,Malgun Gothic,roman" #roman
GUI_FONT_12 = my.utf8tobig5("%s %d" % (GLOBAL_FONT_FAMILY,int( float(config['DEFAULT']['ZOOM'])*12) ));
GUI_FONT_14 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*14) ));
GUI_FONT_16 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*16) ));
GUI_FONT_18 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*18) ));
GUI_FONT_20 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*20) ));
GUI_FONT_22 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*22) ));
GUI_FONT_26 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*26) ));
# print config setting
debug_print("UCLLIU.ini SETTING:")
debug_print("X:%s" % (config["DEFAULT"]["X"]))
debug_print("Y:%s" % (config["DEFAULT"]["Y"]))
debug_print("ALPHA:%s" % (config["DEFAULT"]["ALPHA"]))
debug_print("SHORT_MODE:%s" % (config["DEFAULT"]["SHORT_MODE"]))
debug_print("ZOOM:%s" % (config["DEFAULT"]["ZOOM"]))
debug_print("SEND_KIND_1_PASTE:%s" % (config["DEFAULT"]["SEND_KIND_1_PASTE"]))
debug_print("SEND_KIND_2_BIG5:%s" % (config["DEFAULT"]["SEND_KIND_2_BIG5"]))
debug_print("SP:%s" % (config["DEFAULT"]["SP"]))

def saveConfig():
  global config
  global INI_CONFIG_FILE
  with open(INI_CONFIG_FILE, 'w') as configfile:
    config.write(configfile)
def run_big_small(kind):
  global config
  global GLOBAL_FONT_FAMILY
  global GUI_FONT_12
  global GUI_FONT_14
  global GUI_FONT_16
  global GUI_FONT_18
  global GUI_FONT_20
  global GUI_FONT_22
  global GUI_FONT_26
  global simple_btn
  global x_btn
  global gamemode_btn
  global uclen_btn
  global hf_btn
  global type_label
  global word_label
  kind = float(kind)
  if kind > 0:
    if float(config['DEFAULT']['ZOOM']) < 3:
      config['DEFAULT']['ZOOM'] = str(float(config['DEFAULT']['ZOOM'])+kind)
  else:
    if float(config['DEFAULT']['ZOOM']) > 0.3:
      config['DEFAULT']['ZOOM'] = str(float(config['DEFAULT']['ZOOM'])+kind)
  
  GUI_FONT_12 = my.utf8tobig5("%s %d" % (GLOBAL_FONT_FAMILY,int( float(config['DEFAULT']['ZOOM'])*12) ));
  GUI_FONT_14 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*14) ));
  GUI_FONT_16 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*16) ));
  GUI_FONT_18 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*18) ));
  GUI_FONT_20 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*20) ));
  GUI_FONT_22 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*22) ));
  GUI_FONT_26 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*26) ));  
  
  if is_simple():
    simple_btn.set_size_request(0,int( float(config['DEFAULT']['ZOOM'])*40))  
  simple_label=simple_btn.get_child()
  simple_label.modify_font(pango.FontDescription(GUI_FONT_16))
  
  x_label=x_btn.get_child()
  x_label.modify_font(pango.FontDescription(GUI_FONT_14))  
  x_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*40),int( float(config['DEFAULT']['ZOOM'])*40))

  gamemode_label=gamemode_btn.get_child()
  gamemode_label.modify_font(pango.FontDescription(GUI_FONT_12))
  gamemode_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*80),int( float(config['DEFAULT']['ZOOM'])*40))
    
  uclen_label=uclen_btn.get_child()
  uclen_label.modify_font(pango.FontDescription(GUI_FONT_22))
  uclen_btn.set_size_request(int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))
  
  hf_label=hf_btn.get_child()
  hf_label.modify_font(pango.FontDescription(GUI_FONT_22))
  hf_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40) )
  
  type_label.modify_font(pango.FontDescription(GUI_FONT_22))
  type_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*100) ,int( float(config['DEFAULT']['ZOOM'])*40) )
 
  word_label.modify_font(pango.FontDescription(GUI_FONT_20))
  word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*350),int( float(config['DEFAULT']['ZOOM'])*40))
          
  saveConfig()
    

def run_short():
  global config
  global word_label
  global type_label
  global gamemode_btn
  word_label.set_visible(False)
  type_label.set_visible(False)
  gamemode_btn.set_visible(False)
  config["DEFAULT"]["SHORT_MODE"]="1"
  saveConfig()
def run_long():
  global word_label
  global type_label
  global gamemode_btn
  word_label.set_visible(True)
  type_label.set_visible(True)
  gamemode_btn.set_visible(True)
  config["DEFAULT"]["SHORT_MODE"]="0"
  type_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*100),int( float(config['DEFAULT']['ZOOM'])*40))
  word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*350),int( float(config['DEFAULT']['ZOOM'])*40))
  saveConfig()
  
saveConfig()    
#check if exists tab cin json
is_need_trans_tab = False
is_need_trans_cin = False
is_all_fault = False
#my.unlink("liu.json")
#my.unlink("liu.cin")
if my.is_file(PWD + "\\liu.json") == False:
  if my.is_file(PWD + "\\liu.cin") == False:
    if my.is_file(PWD + "\\liu-uni.tab") == False:
      is_all_fault=True
    else:
      is_need_trans_tab=True
      is_need_trans_cin=True   
  else:
    is_need_trans_cin=True  

if is_all_fault==True and my.is_file("C:\\windows\\SysWOW64\\liu-uni.tab")==True:
  my.copy("C:\\windows\\SysWOW64\\liu-uni.tab",PWD+"\\liu-uni.tab")
  is_all_fault=False
  is_need_trans_tab=True
  is_need_trans_cin=True
  
if is_all_fault==True and my.is_file("C:\\Program Files\\BoshiamyTIP\\liu-uni.tab")==True:
  my.copy("C:\\Program Files\\BoshiamyTIP\\liu-uni.tab",PWD+"\\liu-uni.tab")
  is_all_fault=False
  is_need_trans_tab=True
  is_need_trans_cin=True

# 2019-04-13 加入 小小輸入法臺灣包2018年版wuxiami.txt，http://fygul.blogspot.com/2018/05/yong-tw2018.html 裡linux包中的/tw/wuxiami.txt
if is_all_fault==True and my.is_file(PWD + "\\wuxiami.txt")==True:
  debug_print("Run wuxiami.txt ...");
  my.copy(PWD+"\\wuxiami.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  m = my.explode("#修正錯誤：2018-4-15,17",data);
  data = my.trim(m[1])
  data = my.str_replace("\t"," ",data);
  data = my.implode("\n",m);  
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;  
# 2018-06-25 加入 RIME liur_trad.dict.yaml 表格支援
if is_all_fault==True and my.is_file(PWD + "\\liur_trad.dict.yaml")==True:
  debug_print("Run Rime liur_trad.dict.yaml ...");
  my.copy(PWD+"\\liur_trad.dict.yaml",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  # 2021-03-21
  # 不知道為啥 rime 要把好字的打改成 ~ 開頭@_@?
  data = my.str_replace("~","",data); 
  # 2021-03-21
  # 修正 ... 因為字根裡也有 ... 笑死 XD
  m = my.explode("#字碼格式: 字 + Tab + 字碼",data);
  data = my.trim(m[1])
  data = my.str_replace("\t"," ",data);
  # swap field
  m = my.explode("\n",data);
  for i in range(1,len(m)):
    d = my.explode(" ",m[i]);
    m[i] = "%s %s" % (d[1],d[0]);
  data = my.implode("\n",m);  
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;
  
# 2018-04-08 加入 terry 表格支援
if is_all_fault==True and my.is_file(PWD + "\\terry_boshiamy.txt")==True:
  #將 terry_boshiamy.txt 轉成 正常的 liu.cin、然後轉成 liu.json
  debug_print("Run terry ...")
  my.copy(PWD+"\\terry_boshiamy.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  m = my.explode("## 無蝦米-大五碼-常用漢字：",data);
  data = my.trim(m[1])
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;
  
  
# 2018-03-22 加入 fcitx 輸入法支援
if is_all_fault==True and my.is_file(PWD + "\\fcitx_boshiamy.txt")==True:
  #將 fcitx_boshiamy.txt 轉成 正常的 liu.cin、然後轉成 liu.json
  debug_print("Run fcitx ...")
  my.copy(PWD+"\\fcitx_boshiamy.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  data = my.str_replace("键码=,.'abcdefghijklmnopqrstuvwxyz[]\n","",data);
  data = my.str_replace("码长=5\n","",data);
  data = my.str_replace("[数据]",'''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''',data);
  #這版的日文很怪，正常的 a, 、 s, 都有怪字，我看全拿掉，用 j開頭的版本
  bad_words = [];
  res = re.findall('^(?!j)(\w+[,\.]\w*) (.*)\n',data,re.M);
  for k in res:
    d=" ".join(k);
    bad_words.append(d);
  #然後修正看不到的奇怪字
  #bad_words = ['','','','']
  mdata = my.explode("\n",data);
  new_mdata = [];
  for line in mdata:
    if not any(bad_word in line for bad_word in bad_words):
      new_mdata.append(line);
  data = my.implode("\n",new_mdata);
  #然後修正日文 ja, = あ 也相容 a, = あ
  res = re.findall('j(\w*[,\.]) (.*)\n',data,re.M);
  #print(res) 
  for k in res:
    d=" ".join(k);
    data = data + d +"\n";  
  data = data + "%chardef end";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;  
  
if is_all_fault == True:
  message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
  message.set_markup("無字根檔，請購買正版嘸蝦米，將「C:\\windows\\SysWOW64\\liu-uni.tab」或「C:\\Program Files\\BoshiamyTIP\\liu-uni.tab」與uclliu.exe放在一起執行")  
  response = message.run()
  #print(gtk.ResponseType.BUTTONS_OK)
  if response == -5 or response == -4:
    ctypes.windll.user32.PostQuitMessage(0)
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    my.exit()
  #message.show()
  gtk.main()
           
if is_need_trans_tab==True:
  #需要轉tab檔                                                                             
  #Check liu-uni.tab md5 is fuck up
  if md5_file( ("%s\\liu-uni.tab" % (PWD)) )== "4e89501681ba0405b4c0e03fae740d8c":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("請不要使用義守大學的字根檔，這組 liu-uni.tab 太舊不支援...");
    response = message.run()
    #print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      ctypes.windll.user32.PostQuitMessage(0)
      #atexit.register(cleanup)
      #os.killpg(0, signal.SIGKILL)
      my.exit()
    #message.show()
    gtk.main()
  if md5_file( ("%s\\liu-uni.tab" % (PWD)) )== "260312958775300438497e366b277cb4":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("此組字根檔並非正常的 liu-uni.tab，這個不支援...");
    response = message.run()
    #print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      ctypes.windll.user32.PostQuitMessage(0)
      #atexit.register(cleanup)
      #os.killpg(0, signal.SIGKILL)
      my.exit()
    #message.show()
    gtk.main()
  import liu_unitab2cin
  #print(PWD)  
  liu_unitab2cin.convert_liu_unitab( ("%s\\liu-uni.tab" % (PWD)), ("%s\\liu.cin" % (PWD) ))

if is_need_trans_cin==True:
  import cintojson
  cinapp = cintojson.CinToJson()
  cinapp.run( "liu" , "liu.cin",False)


last_key = "" #to save last 7 word for game mode
flag_is_capslock_down=False
flag_is_play_capslock_otherkey=False 
flag_is_win_down=False
flag_is_shift_down=False
flag_is_ctrl_down=False
flag_is_play_otherkey=False
flag_shift_down_microtime=0
flag_isCTRLSPACE=False
play_ucl_label=""
ucl_find_data=[]
same_sound_data=[] #同音字表
same_sound_index=0 #預設第零頁
same_sound_max_word=6 #一頁最多五字
is_has_more_page=False #是否還有下頁
same_sound_last_word="" #lastword
wavs = my.glob(PWD + "\\*.wav")
o_song = {}
m_play_song = []
max_thread___playMusic_counts = 5 #最多同時五個執行緒在作動
step_thread___playMusic_counts = 0 #目前0個執行緒

for i in range(0,len(wavs)):
  #from : https://pythonbasics.org/python-play-sound/
  #m_song.extend([ AudioSegment.from_wav(wavs[i]) ])
  o_song[ wavs[i] ] = {
                        "filename":wavs[i],
                        "data":[],
                        "wf":"",
                        "paudio_stream":""      
                      }
#debug_print(PWD)
#debug_print(list(m_song))
#my.exit()
# 用來出半型字的
# https://stackoverflow.com/questions/2422177/python-how-can-i-replace-full-width-characters-with-half-width-characters
HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000

WIDE_MAP = dict((i, i + 0xFEE0) for i in xrange(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
                  
def widen(s):
  #https://gist.github.com/jcayzac/1485005
  """
  Convert all ASCII characters to the full-width counterpart.
  
  >>> print widen('test, Foo!')
  ｔｅｓｔ，　Ｆｏｏ！
  >>> 
  """
  return unicode(s).translate(WIDE_MAP)

#def pleave(self, event):
#  my.exit();

if my.is_file(PWD + "\\liu.json") == False:
  message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
  message.set_markup("缺少liu.json")  
  response = message.run()
  #print(gtk.ResponseType.BUTTONS_OK)
  if response == -5 or response == -4:
    ctypes.windll.user32.PostQuitMessage(0)
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    my.exit()
  #message.show()
  gtk.main()
  #my.exit()
if my.is_file(PWD + "\\pinyi.txt")==True:
  same_sound_data = my.explode("\n",my.trim(my.file_get_contents(PWD + "\\pinyi.txt")))  
  
uclcode = my.json_decode(my.file_get_contents(PWD + "\\liu.json"))

uclcode_r = {}
#然後把 chardefs 的字碼，變成對照字根，可以加速 ,,,z、,,,x 反查的速度
#only short key
for k in uclcode["chardefs"]:
   for kk in range(0,len(uclcode["chardefs"][k])):
     _word = uclcode["chardefs"][k][kk]     
     if _word not in uclcode_r:
       uclcode_r[_word] = k
     else:
       if len(k) < len(uclcode_r[_word]):
         uclcode_r[_word] = k


def thread___playMusic(keyboard_valume):
  try:
    # https://stackoverflow.com/questions/43679631/python-how-to-change-audio-volume
    # 調整聲音大小
    # https://stackoverrun.com/cn/q/10107660
    # Last : https://www.thinbug.com/q/45219574
    global paudio_player
    global o_song
    global m_play_song
    global step_thread___playMusic_counts
    import pyaudio
    import audioop
    import wave
    if paudio_player == None:       
      #os.setpgrp()
      paudio_player = pyaudio.PyAudio()
    
    #time.sleep(0.01)      
    if len(m_play_song) !=0 :
      #print("TEST")
      # https://stackoverflow.com/questions/36664121/modify-volume-while-streaming-with-pyaudio
      chunk = 2048
      #s = random.choice(m_song)
      m_play_song = m_play_song[ : 2]
      #print("TEST1")
      s = m_play_song.pop(0) #m_play_song[0]
      #print("TEST2")  
      if len(o_song[s]["data"]) == 0:
        #print("TEST3")
        o_song[s]["wf"] = wf = wave.open(s, 'rb')
        o_song[s]["paudio_stream"] = paudio_player.open(format = paudio_player.get_format_from_width(o_song[s]["wf"].getsampwidth()),
                      channels = o_song[s]["wf"].getnchannels(),
                      rate = o_song[s]["wf"].getframerate(),
                      output = True)
        # 寫聲音檔輸出來播放
        while True:
          #print("TEST4")    
          d = o_song[s]["wf"].readframes(chunk)
          if d == "": break      
          # 這是調整音量大小的方法
          o_song[s]["data"].extend([ audioop.mul(d, 2, keyboard_valume / 100.0 ) ])              
      #print("TEST5")
      for i in range(0,len(o_song[s]["data"])):
        o_song[s]["paudio_stream"].write(o_song[s]["data"][i])
    if step_thread___playMusic_counts > 0:
      step_thread___playMusic_counts = step_thread___playMusic_counts -1         
  except Exception as e:
    debug_print("thread___playMusic error:")
    debug_print(e)  
           
def thread___x(data):
  #字根轉中文 thread  
  selectData=my.trim(data);  
  menter = my.explode("\n",selectData);
  output = "";
  for kLine in range(0,len(menter)):
    m = my.explode(" ", menter[kLine]);        
    #print(len(m));
    for i in range(0,len(m)):
      #轉小寫
      ucl_split_code = my.strtolower(m[i])
      output += uclcode_to_chinese(ucl_split_code)      
    if kLine != len(menter)-1:      
      output+="{ENTER}"
  senddata(output)  
def word_to_sp(data):
  #中文轉最簡字根
  #回傳字根文字
  #中文轉字根 thread
  selectData=data; #my.trim(data);
  selectData=selectData.replace("\r","");
  menter = my.explode("\n",selectData);
  output = "";
  for kLine in range(0,len(menter)):
    output_arr = []
    m = split_unicode_chrs(menter[kLine]);
    for k in range(0,len(m)):
      _uclcode = find_ucl_in_uclcode(m[k]);
      if _uclcode!="":
        output_arr.append(_uclcode)  
    output += my.implode(" ",output_arr);    
    if kLine != len(menter)-1:      
      output+="{ENTER}"
  #print(output)
  output = output.replace(" ","{SPACE}");
  output = output.replace("\n ","{ENTER}");  
  output = output.replace("\n","{ENTER}"); 
  return output 
def show_sp_to_label(data):
  #顯示最簡字根到輸入結束框後
  global config
  global play_ucl_label
  if config['DEFAULT']['SP']=="0":
    return
  sp = "簡根："+my.strtoupper(word_to_sp(data))
  #word_label.set_label(sp)
  #word_label.modify_font(pango.FontDescription(GUI_FONT_18))
  type_label_set_text(sp)     
def thread___z(data):
  output = word_to_sp(data)                   
  senddata(output) 
       
def find_ucl_in_uclcode(chinese_data):
  #用中文反找蝦碼(V1.10版寫法)
  global uclcode_r
  if chinese_data in uclcode_r:
    return uclcode_r[chinese_data];
  else:
    return chinese_data;
     
def find_ucl_in_uclcode_old(chinese_data):
  #用中文反找蝦碼(V1.9版寫法)
  finds = []  
  for k in uclcode["chardefs"]:
    if chinese_data in uclcode["chardefs"][k]:
      index = uclcode["chardefs"][k].index(chinese_data)
      finds.append(k+"_"+str(index))
  finds.sort(key=len, reverse=False)
  
  shorts_arr = []
  shorts_len = 999;
  for k in finds:
    if len(shorts_arr)==0 or len(k) <=shorts_len :
      if len(k) == shorts_len:
        shorts_arr.append(k)
        shorts_len = len(k)
      else:
        shorts_arr = []
        shorts_arr.append(k)
        shorts_len = len(k)
  shorts_arr = sorted(shorts_arr, key = lambda x: int(x.split("_")[1]))
  if len(shorts_arr) >= 1:
    d = shorts_arr[0].split("_")
    return d[0]        
  else:
    return "";

#print(find_ucl_in_uclcode("肥"))
#my.exit();      
def toAlphaOrNonAlpha():
  global uclen_btn
  global hf_btn
  global win
  global config
  global user32 
  global win
  #2019-10-22 check screen size and uclliu position
  # 偵測肥米的位置，超出螢幕時，彈回
  #screen_width=user32.GetSystemMetrics(0)
  #screen_height=user32.GetSystemMetrics(1)
  
  screen_width = gtk.gdk.screen_width()
  screen_height = gtk.gdk.screen_height()
  
  [ _x,_y ] = win.get_position()
  [_width,_height] = win.get_size()
  
  new_position_x = _x
  new_position_y = _y
  if _x  > screen_width - _width:
    new_position_x = screen_width-_width-20    
    win.move( new_position_x,new_position_y)
  if _y > screen_height - _height - 40:
    new_position_y = screen_height-_height - 40 
    win.move( new_position_x,new_position_y)
  
  if _x < 0:
    new_position_x = 0
    win.move( new_position_x,new_position_y)
  if _y < 0:
    new_position_y = 0
    win.move( new_position_x,new_position_y)
  
  #c = hf_btn.get_child()
  #hf_kind = c.get_label()
  #hf_kind = hf_btn.get_label()
  if uclen_btn.get_label()=="英" and hf_btn.get_label()=="半":
    win.set_opacity(0.2)
    #win.set_mnemonics_visible(True)
    win.set_keep_above(False)
    win.set_keep_below(True)    
  else:
    #win.set_opacity(1)
    #debug_print(win.get_opacity())
    #if float(win.get_opacity()) != float(config["DEFAULT"]["ALPHA"]): 
    win.set_opacity( float(config["DEFAULT"]["ALPHA"]) )
    #debug_print(float(config["DEFAULT"]["ALPHA"]))
    #win.set_mnemonics_visible(True)
    win.set_keep_above(True)
    win.set_keep_below(False)
def toggle_ucl():
  global uclen_btn
  global play_ucl_label
  global win
  global debug_print
  global GUI_FONT_22
  if uclen_btn.get_label()=="肥":
    uclen_btn.set_label("英")
    play_ucl_label=""
    type_label_set_text()
    win.set_keep_above(False)
    win.set_keep_below(True)
  else:
    uclen_btn.set_label("肥")
    win.set_keep_above(True)
    win.set_keep_below(False)
  uclen_label=uclen_btn.get_child()
  uclen_label.modify_font(pango.FontDescription(GUI_FONT_22))
                                              
  #window_state_event_cb(None,None)
  debug_print("window_state_event_cb(toggle_ucl)")
  toAlphaOrNonAlpha()    
def is_ucl():
  global uclen_btn  
  #print("WTF: %s" % uclen_btn.get_label())
  if uclen_btn.get_label()=="肥":
    return True
  else:
    return False
def is_simple():
  global simple_btn      
  #print("WTF simple: %s" % simple_btn.get_visible())
  #(w,h) = simple_btn.get_size_request();  
  return simple_btn.get_visible()
      
def gamemode_btn_click(self):
  global gamemode_btn 
  if gamemode_btn.get_label()=="正常模式":
    gamemode_btn.set_label("遊戲模式")
    if uclen_btn.get_label() == "肥":
      uclen_btn_click(uclen_btn)    
  else:
    gamemode_btn.set_label("正常模式")
def x_btn_click(self):
  print("Bye Bye");
  global tray
  #global menu  
  tray.set_visible(False)
  #menu.set_visible(False)
  ctypes.windll.user32.PostQuitMessage(0)
  #atexit.register(cleanup)
  #os.killpg(0, signal.SIGKILL)
  sys.exit()
# draggable
def winclicked(self, event):
  # make UCLLIU can draggable  
  self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  #self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  #self.window.begin_resize_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  # Write to UCLLIU.ini
  global config
  global win
  
  #_x = win.get_allocation().width
  #_y = win.get_allocation().height
  
  [ _x,_y ] = win.get_position()
  #print( "x_root , y_root : %d , %d" % (event.x,event.y))
  #print( "WIN X,Y:%d , %d" % (_x,_y)) 
  config["DEFAULT"]["X"] = str(int(_x))
  config["DEFAULT"]["Y"] = str(int(_y))
  debug_print( "config X,Y:%s , %s" % (config["DEFAULT"]["X"],config["DEFAULT"]["Y"])) 
  saveConfig();
  pass
def uclen_btn_click(self):
  toggle_ucl()
  #pass
def hf_btn_click(self):
  global GUI_FONT_22
  kind=self.get_label()
  if kind=="半":
    self.set_label("全")    
  else:
    self.set_label("半")    
  hf_label=self.get_child()
  hf_label.modify_font(pango.FontDescription(GUI_FONT_22))
  toAlphaOrNonAlpha()
  pass
def is_hf(self):
  global hf_btn
  c = hf_btn.get_child()
  kind = c.get_label()
  return (kind=="半")
   
# http://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
def type_label_set_text(last_word_label_txt=""):
  global type_label
  global play_ucl_label
  global debug_print
  global GUI_FONT_22
  global GUI_FONT_20
  global config
  type_label.set_label(play_ucl_label)
  type_label.modify_font(pango.FontDescription(GUI_FONT_22))
  if my.strlen(play_ucl_label) > 0:
    debug_print("ShowSearch")
    show_search()
    pass
  else:    
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription(GUI_FONT_20))
    pass
  # 如果 last_word_label_txt 不是空值，代表有簡根或其他用字
  word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
  if last_word_label_txt != "":
    word_label.set_label( last_word_label_txt )
    word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color("#007fff"))
  #如果是短米，自動看幾個字展長
  if config["DEFAULT"]["SHORT_MODE"]=="1":
    _tape_label = type_label.get_label()
    _len_tape_label = len(_tape_label)
    #一字30
    if _len_tape_label == 0:
      type_label.set_visible(False)
    else:
      type_label.set_visible(True)
    type_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*18*_len_tape_label) ,int( float(config['DEFAULT']['ZOOM'])*40) ) 
    
    _word_label = word_label.get_label()
    _len_word_label = len(_word_label)
    #一字30
    if _len_word_label == 0:
      word_label.set_visible(False)
    else:
      word_label.set_visible(True)
    word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*15*_len_word_label) ,int( float(config['DEFAULT']['ZOOM'])*40) )    
    
  return True
def word_label_set_text():
  global word_label
  global ucl_find_data 
  global play_ucl_label
  global is_has_more_page
  global GUI_FONT_20
  global GUI_FONT_18
  global GUI_FONT_16
  global GUI_FONT_14
  global GUI_FONT_12
  
  if play_ucl_label == "":
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription(GUI_FONT_18))
    return
  step=0
  m = []
  try:  
    for k in ucl_find_data:
      m.append("%d%s" % (step,k))
      step=step+1
    tmp = my.implode(" ",m)
    if is_has_more_page == True:
      tmp = "%s ..." % (tmp)
    word_label.set_label(tmp)
    
    debug_print(("word_label lens: %d " % (len(tmp))));
    
    lt = len(tmp);
    word_label.modify_font(pango.FontDescription(GUI_FONT_20))
    '''
    if lt<=10: 
      word_label.modify_font(pango.FontDescription(GUI_FONT_20))
    elif lt>10 and lt<=18:
      word_label.modify_font(pango.FontDescription(GUI_FONT_18))
    elif lt>18 and lt<25:
      word_label.modify_font(pango.FontDescription(GUI_FONT_16))
    else:
      word_label.modify_font(pango.FontDescription(GUI_FONT_12))
    '''
    if config["DEFAULT"]["SHORT_MODE"]=="1":
      _word_label = word_label.get_label()
      _len_word_label = len(_word_label)
      #一字30
      if _len_word_label == 0:
        word_label.set_visible(False)
      else:
        word_label.set_visible(True)
      word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*15*_len_word_label) ,int( float(config['DEFAULT']['ZOOM'])*40) )    
        
    return True
  except:
    play_ucl_label=""
    play_ucl("")
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription(GUI_FONT_18))  
    return True
def uclcode_to_chinese(code):
  global ucl_find_data
  global debug_print  
  c = code
  c = my.trim(c)
  if c == "":
    return ""
  #print(c)
  if c not in uclcode["chardefs"] and c[-1]=='v' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=2 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][1]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='r' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=3 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][2]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='s' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=4 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][3]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='f' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=5 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][4]       
    return ucl_find_data
  elif c in uclcode["chardefs"]:
    #print("Debug V2")
    ucl_find_data = uclcode["chardefs"][c][0]    
    return ucl_find_data
  else:    
    return code 
def show_search():
  #真的要顯示了
  global play_ucl_label
  global ucl_find_data
  global is_need_use_pinyi
  global is_has_more_page
  global same_sound_index
  global same_sound_last_word
  global debug_print
  same_sound_index = 0
  is_has_more_page = False
  same_sound_last_word=""
  debug_print("ShowSearch1")
  c = my.strtolower(play_ucl_label)
  c = my.trim(c)
  #print("ShowSearch2")
  #print("C[-1]:%s" % c[-1])
  #print("C[:-1]:%s" % c[:-1])  
  # 此部分可以修正 V 可以出第二字，還不錯
  # 2017-07-13 Fix when V is last code
  #print("LAST V : %s" % (c[-1]))
  is_need_use_pinyi=False  
  if c[0] == "'" and len(c)>1:
    c=c[1:]
    is_need_use_pinyi=True
  if c not in uclcode["chardefs"] and c[-1]=='v' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=2 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][1]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='r' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=3 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][2]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='s' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=4 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][3]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='f' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=5 :
    #print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][4]   
    word_label_set_text()
    return True
  elif c in uclcode["chardefs"]:
    #print("Debug V2")
    ucl_find_data = uclcode["chardefs"][c]
    word_label_set_text()
    return True
  else:
    #print("Debug V3")
    ucl_find_data=[]  
    #play_ucl_label=""  
    ucl_find_data=[]
    word_label_set_text()
    return False  
  
  #print(find)
  #print("ShowSearch3")
  #print("FIND: [%s] %s" % (play_ucl_label,find))
  #pass
def play_ucl(thekey):
  global type_label
  global play_ucl_label
  play_ucl_label = type_label.get_label();
  # 不可以超過5個字
  if len(play_ucl_label) < 5:
    play_ucl_label = "%s%s" % (play_ucl_label,thekey)
    type_label_set_text()
  return True
def senddata(data):
  global play_ucl_label
  global ucl_find_data
  global same_sound_index
  global is_has_more_page
  global same_sound_last_word
  global debug_print
  global f_arr
  global f_big5_arr
  #2019-10-20 增加出字強制選擇
  global DEFAULT_OUTPUT_TYPE
  #for i in range(0,len(mTC_TDATA)):
  #  print(mTC_TDATA[i]);
  #my.exit(); 
  #print(mTC_TDATA)
  #簡繁轉換  
  if is_simple():    
    data = trad2simple(data)
      
    
  
  same_sound_index = 0 #回到第零頁
  is_has_more_page = False #回到沒有分頁
  same_sound_last_word=""
  play_ucl_label=""
  ucl_find_data=[]  
  type_label_set_text()  
  
  
  
  hwnd = win32gui.GetForegroundWindow()
  pid = win32process.GetWindowThreadProcessId(hwnd)
  pp="";
  if len(pid) >=2:
    pp=pid[1]
  else:
    pp=pid[0]
  #print("PP:%s" % (pp))
  debug_print("PP:%s" % (pp))
  p=psutil.Process(pp)
  
  debug_print("ProcessP:%s" % (p))
  
  check_kind="0"
  
  # 這是貼上模式
  for k in f_arr:
    #break;
    k = my.strtolower(k)
    exec_proc = my.strtolower(p.exe())
    if my.is_string_like(exec_proc,k) or DEFAULT_OUTPUT_TYPE == "PASTE":  
      check_kind="1"      
      
      win32clipboard.OpenClipboard()
      orin_clip=""
      try:
        orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
      except:
        pass
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
      win32clipboard.EmptyClipboard()
      win32clipboard.CloseClipboard()
            
      win32clipboard.OpenClipboard() 
      win32clipboard.EmptyClipboard()#這一行特別重要，經過實驗如果不加這一行的話會做動不正常
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
      win32clipboard.CloseClipboard()
      #https://win32com.goermezer.de/microsoft/windows/controlling-applications-via-sendkeys.html
      #shell.SendKeys("+{INSERT}", 0)
      #2018-04-05 修正 vim 下打中文字的問題
      #debug_print("Debug Oxygen Not Included")
      #SendKeysCtypes.SendKeys("+{INSERT}",pause=0)
      if k == "oxygennotincluded.exe":
        #2019-02-10 修正 缺氧 無法輸入中文的問題
        SendKeysCtypes.SendKeys("^v",pause=0)
      elif k == "iedit_.exe":
        #2019-10-29 修正 PhotoImpact x3 無法輸入中文的問題
        SendKeysCtypes.SendKeys("^v",pause=0)
      else:
        SendKeysCtypes.SendKeys("+{INSERT}",pause=0)
      #SendKeysCtypes.SendKeys("ggggg",pause=0)
      #0xA0 = left shift
      #0x2d = insert            
      #win32api.keybd_event(0x10, 1,0,0)
      #win32api.keybd_event(45, 1,0,0)      
      #time.sleep(.05)            
      #win32api.keybd_event(45,0 ,win32con.KEYEVENTF_KEYUP ,0)
      #win32api.keybd_event(0x10,0 ,win32con.KEYEVENTF_KEYUP ,0)
      
      #win32api.keybd_event(win32con.SHIFT_PRESSED, 0, 0x2d, 0,win32con.KEYEVENTF_KEYUP ,0)
       
      #reload(sys)                                    
      #sys.setdefaultencoding('UNICODE') 
      #SendKeysCtypes.SendKeys("肥".encode("UTF-8"),pause=0)
      #reload(sys)                                    
      #sys.setdefaultencoding('UTF-8')
      #也許要設delay...
      time.sleep(0.05)
      win32clipboard.OpenClipboard()    
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
      win32clipboard.CloseClipboard()            
      break
  for k in f_big5_arr:
    k = my.strtolower(k)
    if my.is_string_like(my.strtolower(p.exe()),k) or DEFAULT_OUTPUT_TYPE == "BIG5":
      debug_print("Debug_f_big5_arr")
      #SendKeysCtypes.SendKeys(my.utf8tobig5(data),pause=0)
      check_kind="2"
      win32clipboard.OpenClipboard()
      orin_clip=""
      try:
        orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
      except:
        pass      
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_TEXT, my.utf8tobig5(data))
      win32clipboard.CloseClipboard()
      #之前是用 shell，改用 SendKeysCtypes.SendKeys 看看
      #shell = win32com.client.Dispatch("WScript.Shell")
      #shell.SendKeys("^v", 0)
      SendKeysCtypes.SendKeys("^v")
      time.sleep(0.05)
      win32clipboard.OpenClipboard()    
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
      win32clipboard.CloseClipboard()         
      break
            
  if check_kind=="0":
    #reload(sys)                                    
    #sys.setdefaultencoding('UTF-8')
    #print("CP950")
    #2019-03-02 
    #修正斷行、空白、自定詞庫等功能
    _str = data.decode("UTF-8")
    _str = my.str_replace(" ","{SPACE}",_str)
    _str = my.str_replace("(","{(}",_str)
    _str = my.str_replace(")","{)}",_str)
    _str = my.str_replace("\n","{ENTER}",_str)
    SendKeysCtypes.SendKeys(_str,pause=0)
    #reload(sys)
    #sys.setdefaultencoding('UTF-8')
  
  #reload(sys)                                    
  #sys.setdefaultencoding('auto')
  #SendKeysCtypes.SendKeys(data.decode("auto"),pause=0)
  
def use_pinyi(data):
  global same_sound_data
  global ucl_find_data
  global same_sound_index
  global same_sound_max_word
  global is_has_more_page
  global debug_print
  finds=""
  for k in same_sound_data:
    if my.is_string_like(k,data):
      #if k.startswith(u'\xe7\x9a\x84'):
      #  k = u[1:]
      finds="%s%s " % (finds,my.trim(k))
      #print(k)
  finds=my.trim(finds);
  finds=my.explode(" ",finds)
  #print(finds)
  #finds=finds[:] 
  #for k in finds:
  #  print(k.encode("UTF-8"))
  finds = my.array_unique(finds)
  #print("Debug data: %s " % data.encode("UTF-8"))
  debug_print("Debug Finds: %d " % len(finds))
  debug_print("Debug same_sound_index: %d " % same_sound_index)
  debug_print("Debug same_sound_max_word: %d " % same_sound_max_word)  
  maxword = same_sound_index + same_sound_max_word
  # 2020-08-10 103 分頁異常，修正同音字少一字，最後分頁有機會顯示錯誤的問題
  if maxword >= len(finds):
    maxword = len(finds)
    is_has_more_page = False
  else:
    is_has_more_page = True
  ucl_find_data = finds[same_sound_index:maxword]
  debug_print("DEBUG same_sound_index: %d " % same_sound_index)
  same_sound_index=same_sound_index+same_sound_max_word
   
  if same_sound_index>=len(finds):
    same_sound_index=0
  word_label_set_text()
  #finds=my.str_replace(data," ",finds)
  #finds=my.str_replace("  "," ",finds)
def OnMouseEvent(event):
  global flag_is_shift_down
  global flag_is_play_otherkey
  global hm
  #if flag_is_shift_down==True:
    #如果同時按著 shift 時，滑鼠有操作就視窗按別的鍵 ok
  if event.MessageName == "mouse left down" or event.MessageName == "mouse right down" :
    #flag_is_shift_down=False
    flag_is_play_otherkey=True
    #debug_print(('MessageName: %s' % (event.MessageName)))
    #debug_print(('Message: %s' % (event.Message))) 
    #debug_print("Debug event MouseA")
    #debug_print(flag_is_play_otherkey)
    #hm.UnhookMouse()
  return True

# run always thread  

    
def OnKeyboardEvent(event):  
  global last_key
  global flag_is_win_down
  global flag_is_shift_down
  global flag_is_capslock_down
  global flag_is_play_capslock_otherkey
  global flag_is_ctrl_down    
  global flag_is_play_otherkey
  global play_ucl_label
  global ucl_find_data
  global is_need_use_pinyi
  global same_sound_last_word
  global gamemode_btn
  global simple_btn
  global debug_print
  global VERSION
  global f_arr
  global GUI_FONT_16
  global f_pass_app    
  global config 
  global m_play_song
  global max_thread___playMusic_counts
  global step_thread___playMusic_counts
  global flag_shift_down_microtime 
  global hm   
  # From : https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
  # 1.26 版，加入打字音的功能
  try:
    if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1" and event.MessageName == "key down" and len(o_song.keys())!=0 and step_thread___playMusic_counts < max_thread___playMusic_counts:
      step_thread___playMusic_counts = step_thread___playMusic_counts + 1                  
      m_play_song.extend( [ random.choice(o_song.keys()) ])
      thread.start_new_thread( thread___playMusic,(int(config['DEFAULT']['KEYBOARD_VOLUME']),))
      #thread___playMusic(m_song,int(config['DEFAULT']['KEYBOARD_VOLUME']))
    
    
    #  playsound.playsound(mp3s[1])
    #print(dir())  
    #try:  
    #print(event)
    '''
    debug_print(('MessageName: %s' % (event.MessageName)))
    debug_print(('Message: %s' % (event.Message)))
    debug_print(('Time: %s' % (event.Time)))
    debug_print(('Window: %s' % (event.Window)))
    debug_print(('WindowName: %s' % (event.WindowName)))
    debug_print(('Ascii: %s, %s' % (event.Ascii, chr(event.Ascii))))
    debug_print(('Key: %s' % (event.Key)))
    debug_print(('KeyID: %s' % (event.KeyID)))
    debug_print(('ScanCode: %s' % (event.ScanCode)))
    debug_print(('Extended: %s' % (event.Extended)))
    debug_print(('Injected: %s' % (event.Injected)))
    debug_print(('Alt: %s' % (event.Alt)))
    debug_print(('Transition: %s' % (event.Transition)))
    debug_print(('IS_UCL %s' % (is_ucl())))
    debug_print('---')
    debug_print(('last_key: %s' % (last_key[-8:])))
    '''
    
    hwnd = win32gui.GetForegroundWindow()  
    pid = win32process.GetWindowThreadProcessId(hwnd)
    pp="";
    if len(pid) >=2:
      pp=pid[1]
    else:
      pp=pid[0]
    #print("PP:%s" % (pp))
    #debug_print("PP:%s" % (pp))
    p=psutil.Process(pp)
    #debug_print("ProcessP:%s" % (p))
    #print("GGGGGGG %s " % (p.exe()))
    
    #print(dir(p))
    exec_proc = my.strtolower(p.exe())
    #debug_print("Process :%s" % (exec_proc))
    #print ("HWND:")
    #print (win32gui.GetWindowText(hwnd))
    
    for k in f_pass_app:        
      if my.is_string_like(exec_proc,k):
        if is_ucl()==True:
          toggle_ucl()
        return True
    # chrome 遠端桌面也不需要肥米
    if my.is_string_like(my.strtolower(win32gui.GetWindowText(hwnd)),"- chrome "):
      if is_ucl()==True:
        toggle_ucl()
      return True
    
    if event.MessageName == "key up":    
          
      last_key = last_key + chr(event.Ascii)
      last_key = last_key[-10:]
      if my.strtolower(last_key[-4:])==",,,c":
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        if is_ucl()==False:
          # change to ucl
          toggle_ucl()
        simple_btn.set_size_request( int(float(config['DEFAULT']['ZOOM'])*40),int(float(config['DEFAULT']['ZOOM'])*40) )
        simple_label=simple_btn.get_child()
        simple_label.set_label("簡")
        simple_btn.set_visible(True)
        simple_label.modify_font(pango.FontDescription(GUI_FONT_16))      
        #simple_label.set_justify(gtk.JUSTIFY_CENTER)
      if my.strtolower(last_key[-4:])==",,,t":
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        if is_ucl()==False:
          # change to ucl
          toggle_ucl()
        simple_btn.set_size_request(0,int(float(config['DEFAULT']['ZOOM'])*40) )
        simple_label=simple_btn.get_child()
        simple_label.set_label("")
        simple_btn.set_visible(False)
        simple_label.modify_font(pango.FontDescription(GUI_FONT_16))       
      if my.strtolower(last_key[-7:])==",,,lock":
        last_key = ""
        if gamemode_btn.get_label()=="正常模式":
          gamemode_btn_click(gamemode_btn)
      if my.strtolower(last_key[-4:])==",,,-":
        #run small
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()
        run_big_small(-0.1)        
      if my.strtolower(last_key[-4:])==",,,+":
        #run big
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()
        run_big_small(0.1)
      if my.strtolower(last_key[-4:])==",,,s":
        # run short
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        run_short()
      if my.strtolower(last_key[-4:])==",,,l":
        # run long
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        run_long()
      if my.strtolower(last_key[-4:])==",,,x" and is_ucl():
        # 將框選嘸蝦米的文字，轉成中文字
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        orin_clip=""
        try:
          win32clipboard.OpenClipboard()
          orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
          pass
        try:
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
          win32clipboard.EmptyClipboard()
          win32clipboard.CloseClipboard()
        except:
          pass      
        SendKeysCtypes.SendKeys("^C",pause=0.05)
        #也許要設delay...      
        #try:
        win32clipboard.OpenClipboard()
        #try:
        selectData=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        # 參考 http://www.runoob.com/python/python-multithreading.html      
        thread.start_new_thread( thread___x, (selectData, ))
        win32clipboard.CloseClipboard()       
        #except:
        #  pass
        #也許要設delay...
        time.sleep(0.05)
        try:
          win32clipboard.OpenClipboard()    
          win32clipboard.EmptyClipboard()
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
          win32clipboard.CloseClipboard()           
        except:
          pass
        return False   
      if my.strtolower(last_key[-4:])==",,,z" and is_ucl():
        # 將框選的文字，轉成嘸蝦米的字
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()                   
        orin_clip=""
        try:
          win32clipboard.OpenClipboard()
          orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
          pass
        try:
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
          win32clipboard.EmptyClipboard()
          win32clipboard.CloseClipboard()
        except:
          pass
        SendKeysCtypes.SendKeys("^C",pause=0.05)
        try:
          win32clipboard.OpenClipboard()
          #try:
          time.sleep(0.05)
          selectData=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
          #簡轉繁
          selectData = simple2trad(selectData)       
                          
          thread.start_new_thread( thread___z, (selectData, ))
        except:
          pass
        #也許要設delay...
        time.sleep(0.05)
        try:
          win32clipboard.OpenClipboard()    
          win32clipboard.EmptyClipboard()
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
          win32clipboard.CloseClipboard()
        except:
          pass
        return False             
      if my.strtolower(last_key[-9:])==",,,unlock":          
        last_key = ""               
        if gamemode_btn.get_label()=="遊戲模式":
          gamemode_btn_click(gamemode_btn)
      if my.strtolower(last_key[-10:])==",,,version":
        last_key= ""   
        message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
        message.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        message.set_keep_above(True)
        _msg_text = about_uclliu()       
        message.set_markup( _msg_text )
        #toAlphaOrNonAlpha()
        message.show()
        toAlphaOrNonAlpha()  
        response = message.run()
        #toAlphaOrNonAlpha()
        debug_print("Show Version")
        debug_print(response)
        #print(gtk.ResponseType.BUTTONS_OK)
        if response == -5 or response == -4:
          #message.hide()
          message.destroy()
          #toAlphaOrNonAlpha()  
          play_ucl_label=""
          ucl_find_data=[]
          type_label_set_text()
          toAlphaOrNonAlpha()
          return False      
    #print("LAST_KEY:" + last_key)
    if gamemode_btn.get_label()=="遊戲模式":      
      return True    
    
    #thekey = chr(event.Ascii)
    # KeyID = 91 = Lwinkey
    # 2019-07-19
    # 增加，如果是肥模式，且輸入的字>=1以上，按下 esc 鍵，會把字消除  
    if event.MessageName == "key down" and is_ucl() == True and len(play_ucl_label) >=1 and event.Key == "Escape":
      #debug_print("2019-07-19 \n 增加，如果是肥模式，且輸入的字>=1以上，按下 esc 鍵，會把字消除)");
      play_ucl_label = ""
      type_label_set_text()
      return False
    if event.MessageName == "key down" and (event.KeyID == 91 or event.KeyID == 92):
      flag_is_win_down = True
      debug_print("Debug event A")
    if event.MessageName == "key up" and (event.KeyID == 91 or event.KeyID == 92):
      flag_is_win_down = False
      debug_print("Debug event B")
    if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift"):
      if flag_is_shift_down==False:
        flag_is_play_otherkey=False
        flag_shift_down_microtime = my.microtime()      
      flag_is_shift_down=True
      debug_print("Debug event CC")
    if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #hm.UnhookMouse()
      if flag_is_shift_down==False:
        flag_is_play_otherkey=False
        flag_shift_down_microtime = my.microtime()      
      flag_is_shift_down=True
      
      #hm.HookMouse()            
      debug_print("Debug event C") 
    if event.MessageName == "key down" and (event.Key == "Lcontrol" or event.Key == "Rcontrol"):  # and config['DEFAULT']['CTRL_SP'] == "1"
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #2021-03-22 修正英/全時，複製、貼上，按著 Ctrl + 任意鍵 有問題
      #hm.UnhookMouse()        
      flag_is_ctrl_down=True      
      #hm.HookMouse()            
      debug_print("Debug event Ctrl C 1")         
    if event.MessageName == "key up" and (event.Key == "Lcontrol" or event.Key == "Rcontrol"): #  and config['DEFAULT']['CTRL_SP'] == "1"
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #2021-03-22 修正英/全時，複製、貼上，按著 Ctrl + 任意鍵 有問題
      #hm.UnhookMouse()                  
      flag_is_ctrl_down=False      
      #hm.HookMouse()            
      debug_print("Debug event Ctrl C 2")
      return True
    if event.MessageName == "key down" and event.Key == "Capital":
      flag_is_capslock_down=True
      flag_is_play_capslock_otherkey=False
      debug_print("Debug event E")
      return True
    if event.MessageName == "key down" and event.Key != "Capital":
      flag_is_play_capslock_otherkey=True
      debug_print("Debug event F")
    if event.MessageName == "key up" and event.Key == "Capital":
      flag_is_capslock_down=False
      flag_is_play_capslock_otherkey=False
      debug_print("Debug event E")
    if event.MessageName == "key down" and (event.Key != "Lshift" and event.Key != "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      debug_print("Debug event D")
      flag_is_play_otherkey=True   
    
    if flag_is_capslock_down == True and flag_is_play_capslock_otherkey == True:
      # 2019-03-06 增加，如果是 肥 模式，且輸入字是 backspace 且框有字根，就跳過這個 True
      if event.Key == "Back" and is_ucl()==True and len(play_ucl_label) >= 1:
        debug_print("Debug 2019-03-06 CapsLock + backspace")
        pass
      else:  
        return True
    if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift"):
      flag_is_shift_down=False
               
    if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      debug_print("Debug event G")
      debug_print("event.MessageName:"+event.MessageName)
      debug_print("event.Ascii:"+str(event.Ascii))
      debug_print("event.KeyID:"+str(event.KeyID))
      debug_print("flag_is_play_otherkey:"+str(flag_is_play_otherkey))
      debug_print("flag_is_shift_down:"+str(flag_is_shift_down))        
      debug_print("flag_is_capslock_down:"+str(flag_is_capslock_down))
      debug_print("flag_is_play_capslock_otherkey:"+str(flag_is_play_capslock_otherkey))
      flag_is_shift_down=False
      #hm.UnhookMouse()
      debug_print("Press shift")
      
      #2021-03-20 如果 microtime() - flag_shift_down_microtime>=500 flag_is_play_otherkey = true
      st = my.microtime() - flag_shift_down_microtime
      debug_print("st: %d " % (st))
      if st>=500:
         flag_is_play_otherkey = True
      # 不可是右邊的2、4、6、8      
      #toAlphaOrNonAlpha()
      if flag_is_play_otherkey==False and (event.Ascii > 40 or event.Ascii < 37) :
        toggle_ucl()
        debug_print("Debug15")        
        debug_print("Debug14")
  
      #toAlphaOrNonAlpha()
      return True
    if event.MessageName == "key down" and event.Ascii==32 and flag_is_shift_down==True:
      # Press shift and space
      # switch 半/全
      hf_btn_click(hf_btn)
      flag_is_play_otherkey=True
      flag_is_shift_down=False    
      debug_print("Debug13")
      return False            
    if is_ucl():
      #debug_print("is ucl")    
      if event.MessageName == "key down" and flag_is_win_down == True : # win key
        return True
      #2018-05-05要考慮右邊數字鍵的 . 
      if event.MessageName == "key down" and ( event.Ascii>=48 and event.Ascii <=57) or (event.Key=="Decimal" and event.Ascii==46) : #0~9 . 
        if len(ucl_find_data)>=1 and int(chr(event.Ascii)) < len(ucl_find_data):
          # send data        
          data = ucl_find_data[int(chr(event.Ascii))]
          #print(ucl_find_data)
          
          senddata(data)
          show_sp_to_label(data.decode('utf-8'))
          #print(data)
          #快選用的
          #print(data)        
          debug_print("Debug12")
          return False
        else:
          if len(event.Key) == 1 and is_hf(None)==False:
            #k = widen(event.Key)
            kac = event.Ascii          
            k = widen(chr(kac))
            debug_print("event.Key to Full:%s %s" % (event.Key,k))
            senddata(k)
            debug_print("Debug11")
            return False
          
          debug_print("Debug10")
          #2017-10-24要考慮右邊數字鍵的狀況
          #2018-05-05要考慮右邊數字鍵的 .
          # event.Ascii==46 or (event.Key=="Decimal" and event.Ascii==46)
          # 先出小點好了
          if is_hf(None)==False and ( event.Ascii==49 or event.Ascii==50 or event.Ascii==51 or event.Ascii==52 or event.Ascii==53 or event.Ascii==54 or event.Ascii==55 or event.Ascii==56 or event.Ascii==57 or event.Ascii==47 or event.Ascii==42 or event.Ascii==45 or event.Ascii==43 or event.Ascii==48):
            kac = event.Ascii        
            k = widen(chr(kac))
            #if event.Ascii==46:
            #  senddata("a")
            #else:
            senddata(k)
            debug_print("Debug100")
            return False
          else:  
            return True                    
      if event.MessageName == "key down" and ( (event.Ascii>=65 and event.Ascii <=90) or (event.Ascii>=97 and event.Ascii <=122) or event.Ascii==44 or event.Ascii==46 or event.Ascii==39 or event.Ascii==91 or event.Ascii==93):
        # 這裡應該是同時按著SHIFT的部分
        flag_is_play_otherkey=True
        if flag_is_shift_down==True:
          if len(event.Key) == 1 and is_hf(None)==False:
            #k = widen(event.Key)
            kac = event.Ascii
            if kac>=65 and kac<=90:
              kac=kac+32
            else:
              kac=kac-32
            k = widen(chr(kac))
            debug_print("285 event.Key to Full:%s %s" % (event.Key,k))
            senddata(k)
            debug_print("Debug9")
            return False
          debug_print("Debug8")
          return True
        else:
          # Play ucl
          #print("Play UCL")
          #print(thekey)
          play_ucl(chr(event.Ascii))
          debug_print("Debug7")
          return False    
      if event.MessageName == "key down" and ( event.Ascii == 8 ): # ←      
        if my.strlen(play_ucl_label) <= 0:                    
          play_ucl_label=""
          play_ucl("")
          debug_print("Debug6")
          return True
        else:
          play_ucl_label = play_ucl_label[:-1]
          type_label_set_text()
          debug_print("Debug5")        
          return False       
      if event.MessageName == "key down" and event.Key=="Space" and config['DEFAULT']['CTRL_SP']=="1": # check ctrl + space
          if flag_is_ctrl_down == True:
            toggle_ucl()
            return False
      if event.MessageName == "key down" and event.Key=="Space": #空白
        # Space                          
        if len(ucl_find_data)>=1:        
          #丟出第一個字                
          text = ucl_find_data[0]
          if same_sound_last_word=="":
            same_sound_last_word=text
          #] my.utf8tobig5("好的")
          
          if is_need_use_pinyi==True:
            #使用同音字
            debug_print("Debug use pinyi")
            use_pinyi(same_sound_last_word)
          else:
            senddata(text)
            show_sp_to_label(text)
          debug_print("Debug4")
          return False 
        elif len(ucl_find_data)==0 and len(play_ucl_label)!=0:
          #無此字根時，按到空白鍵
          debug_print("Debug11")
          play_ucl_label=""
          ucl_find_data=[]
          type_label_set_text()
          return False 
        else:
          #沒字時直接出空白
          debug_print("Debug1")
          if is_hf(None)==False:        
            kac = event.Ascii        
            k = widen(chr(kac))
            senddata(k)
            debug_print("Debug23")
            return False
          else:
            return True
      elif event.MessageName == "key down" and ( event.Ascii==58 or event.Ascii==59 or event.Ascii==123 or event.Ascii==125 or event.Ascii==40 or event.Ascii==41 or event.Ascii==43 or event.Ascii==126 or event.Ascii==33 or event.Ascii==64 or event.Ascii==35 or event.Ascii==36 or event.Ascii==37 or event.Ascii==94 or event.Ascii==38 or event.Ascii==42 or event.Ascii==95 or event.Ascii==60 or event.Ascii==62 or event.Ascii==63 or event.Ascii==34 or event.Ascii==124 or event.Ascii==47 or event.Ascii==45) : # : ;｛｝（）＋～！＠＃＄％＾＆＊＿＜＞？＂｜／－
        #修正 肥/全 時，按分號、冒號只出半型的問題
        if is_hf(None)==False:        
          kac = event.Ascii        
          k = widen(chr(kac))
          senddata(k)
          debug_print("Debug22")
          return False
        else:
          debug_print("Debug22OK")
          return True     
      else:                  
        return True            
        
    else:
      debug_print("DDDDDDDDD: event.Key: " + event.Key + "\nDDDDDDDDD: event.KeyID: " + str(event.KeyID) + "\nDDDDDDDDD: event.MessageName: " +  event.MessageName )
      debug_print("flag_is_shift_down:"+str(flag_is_shift_down))
      debug_print("flag_is_ctrl_down:"+str(flag_is_ctrl_down))
      debug_print("Debug3")  
      debug_print(event.KeyID)
      # 2018-03-27 此部分修正「英/全」時，按Ctrl A 無效的問題，或ctrl+esc等問題
      # 修正enter、winkey 在「英/全」的狀況
      if event.MessageName == "key down" and event.KeyID == 13:
        return True
      if event.MessageName == "key down" and ( event.KeyID == 91 or event.KeyID == 92): #winkey
        flag_is_win_down=True
        return True
      # 修正  在「英/全」的狀況，按下 esc (231 + 27 ) 無效的問題
      if event.MessageName == "key down" and ( event.KeyID == 231 or event.KeyID == 27):
        flag_is_win_down=False
        debug_print("Fix 23+27")
        return True                
      if event.MessageName == "key down" and flag_is_win_down == True : # win key
        flag_is_win_down=False
        return True          
      #if event.MessageName == "key down" and ( event.KeyID == 231 or event.KeyID == 162 or event.KeyID == 163):
      #  flag_is_ctrl_down=True
      #  debug_print("Ctrl key")
      #  return True
      #if flag_is_ctrl_down == True:
      #  flag_is_ctrl_down=False
      #  return True       
      if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift"):      
        flag_is_shift_down=True
        flag_is_play_otherkey=False      
        debug_print("Debug331")                
      if event.MessageName == "key down" and (event.Key != "Lshift" and event.Key != "Rshift"): 
        flag_is_play_otherkey=True                                                                               
        debug_print("Debug332")                
      if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift"):
        debug_print("Debug333")
        #shift
        flag_is_shift_down=False
        debug_print("Press shift")
      if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
        if flag_is_play_otherkey==False:
          toggle_ucl()
          debug_print("Debug315")    
        debug_print("Debug314")
        return True
                
      if event.MessageName == "key down" and event.Key=="Space" and config['DEFAULT']['CTRL_SP']=="1": # check ctrl + space
        if flag_is_ctrl_down == True:
          toggle_ucl()
          return False
      #2021-03-22 修正 英/全 模式下，按 CTRL + 任意鍵，也是穿透的問題
      if is_hf(None)==False and event.MessageName == "key down" and flag_is_ctrl_down == True:
        return True        
      #if event.MessageName == "key up" and len(event.Key) == 1 and is_hf(None)==False:
      #  k = widen(event.Key)
      #  print("335 event.Key to Full:%s %s" % (event.Key,k))
      #  senddata(k)
      #  return False
      #if len(event.Key) == 1 and is_hf(None)==False and event.KeyID !=0 and event.KeyID !=145 and event.KeyID !=162:
      #  k = widen(event.Key)      
      #  senddata(k) 
      debug_print("Debug3: %s" % (event.Transition))
      if event.KeyID==8 or event.KeyID==20 or event.KeyID==45 or event.KeyID==46 or event.KeyID==36 or event.KeyID==33 or event.KeyID==34 or event.KeyID==35 or event.KeyID==160 or event.KeyID==161 or event.KeyID==9 or event.KeyID == 37 or event.KeyID == 38 or event.KeyID == 39 or event.KeyID == 40 or event.KeyID == 231 or event.KeyID == 162 or event.KeyID == 163: #↑←→↓
        return True
      if event.MessageName == "key down" and len( str(chr(event.Ascii)) ) == 1 and is_hf(None)==False and event.Injected == 0 :
        k = widen( str(chr(event.Ascii)) )
        #print("ｋｋｋｋｋｋｋｋｋｋｋｋｋｋｋK:%s" % k)
        senddata(k)
        return False
      return True    
  except Exception as e:
    # 理論上不會發生，也不該發生
    debug_print("KeyPressed")
    debug_print(e)
    return True
      
#程式主流程
#功能說明


# create a hook manager
hm = pyHook.HookManager()
#hm.UnhookMouse();
# watch for all mouse events
hm.KeyAll = OnKeyboardEvent
debug_print(dir(hm))
# set the hook
hm.HookKeyboard()
# wait forever

# watch for all mouse events
# 2021-03-19 改成只Hook MouseAllButtons，MouseAll 好像會造成lag
# From : http://pyhook.sourceforge.net/doc_1.5.0/
#hm.MouseAll = OnMouseEvent
#hm.MouseAllButtons = OnMouseEvent
# set the hook
# 改成按到 shift 才 hook
#hm.HookMouse()

        
#win=gtk.Window(type=gtk.WINDOW_POPUP)
win=gtk.Window(type=gtk.WINDOW_POPUP)
win.set_modal(True)
win.set_resizable(False)



#win.move(screen_width-700,int(screen_height*0.87))
win.move( int(config["DEFAULT"]["X"]) , int(config["DEFAULT"]["Y"]))
#always on top
win.set_keep_above(True)
win.set_keep_below(False)
win.set_skip_taskbar_hint(False)  
win.set_skip_pager_hint(False)
win.set_decorated(False)
win.set_accept_focus(False)
win.set_icon_name(None)

win.add_events( gdk.BUTTON_PRESS_MASK)
win.connect ('button-press-event', winclicked)


vbox = gtk.VBox(False)

hbox=gtk.HBox()
vbox.pack_start(hbox, False)

uclen_btn=gtk.Button("肥")
uclen_label=uclen_btn.get_child()
uclen_label.modify_font(pango.FontDescription(GUI_FONT_22))
uclen_btn.connect("clicked",uclen_btn_click)
uclen_btn.set_size_request(int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))
hbox.add(uclen_btn)

hf_btn=gtk.Button("半")
hf_label=hf_btn.get_child()
hf_label.modify_font(pango.FontDescription(GUI_FONT_22))
hf_btn.connect("clicked",hf_btn_click)
hf_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40) )
hbox.add(hf_btn)

type_label=gtk.Label("")
type_label.modify_font(pango.FontDescription(GUI_FONT_22))
type_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
type_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*100) ,int( float(config['DEFAULT']['ZOOM'])*40) )
type_label.set_alignment(xalign=0.1, yalign=0.5) 
f_type = gtk.Frame()
f_type.add(type_label)
hbox.add(f_type)

word_label=gtk.Label("")
word_label.modify_font(pango.FontDescription(GUI_FONT_20))
word_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*350),int( float(config['DEFAULT']['ZOOM'])*40))
word_label.set_alignment(xalign=0.05, yalign=0.5)
f_word = gtk.Frame()
f_word.add(word_label)
hbox.add(f_word)

# 加一個簡繁互換的
simple_btn=gtk.Button("")
simple_btn.set_size_request(0,int( float(config['DEFAULT']['ZOOM'])*40))
simple_label=simple_btn.get_child()
simple_label.modify_font(pango.FontDescription(GUI_FONT_16))
#simple_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
#simple_label.set_justify(gtk.JUSTIFY_CENTER)
#simple_label.set_alignment(xalign=0.05, yalign=0.5)
f_word = gtk.Frame()
f_word.add(simple_btn)
hbox.add(f_word)


gamemode_btn=gtk.Button("正常模式")
gamemode_label=gamemode_btn.get_child()
gamemode_label.modify_font(pango.FontDescription(GUI_FONT_12))
gamemode_btn.connect("clicked",gamemode_btn_click)
gamemode_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*80),int( float(config['DEFAULT']['ZOOM'])*40))
hbox.add(gamemode_btn)

x_btn=gtk.Button("╳")
x_label=x_btn.get_child()
x_label.modify_font(pango.FontDescription(GUI_FONT_14))
x_btn.connect("clicked",x_btn_click)
x_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*40),int( float(config['DEFAULT']['ZOOM'])*40))
hbox.add(x_btn)



win.add(vbox)

# 2019-10-20 加入 trayicon
def message(data=None):
  "Function to display messages to the user."
  
  msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL,
    gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
  msg.run()
  msg.destroy()

# From : https://github.com/gevasiliou/PythonTests/blob/master/TrayAllClicksMenu.py
class TrayIcon(gtk.StatusIcon):
    def __init__(self):
      global VERSION
      global PWD
      global UCL_PIC_BASE64
      gtk.StatusIcon.__init__(self)
      #self.set_from_icon_name('help-about')
      #debug_print(PWD+"\\UCLLIU.png")
      # base64.b64decode
      # From : https://sourceforge.net/p/matplotlib/mailman/message/20449481/
      raw_data = base64.decodestring(UCL_PIC_BASE64)
      #debug_print(gtk.gdk.Pixbuf)
      w = 16
      h = 16
      img_pixbuf = gtk.gdk.pixbuf_new_from_data(
              raw_data, gtk.gdk.COLORSPACE_RGB, True, 8, w, h, w*4)

      self.set_from_pixbuf(img_pixbuf)
      self.set_tooltip("肥米輸入法：%s" % (VERSION))
      self.set_has_tooltip(True)
      self.set_visible(True)
      self.connect("button-press-event", self.on_click)

    def m_about(self,data=None):  # if i ommit the data=none section python complains about too much arguments passed on greetme
      message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
      message.set_position(gtk.WIN_POS_CENTER_ALWAYS)
      message.set_keep_above(True)
      _msg_text = about_uclliu()       
      message.set_markup( _msg_text )
      #toAlphaOrNonAlpha()
      message.show()
      toAlphaOrNonAlpha()  
      response = message.run()
      #toAlphaOrNonAlpha()
      debug_print("Show Version")
      debug_print(response)
      #print(gtk.ResponseType.BUTTONS_OK)
      if response == -5 or response == -4:
        #message.hide()
        message.destroy()
        #toAlphaOrNonAlpha()  
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()
        #return False
    def m_sp_switch(self,data=None):
      global config
      if config['DEFAULT']['SP'] == "0":        
        config['DEFAULT']['SP']="1"
      else:
        config['DEFAULT']['SP']="0"
      #切換後，都要存設定
      saveConfig()
    def m_ctrlsp_switch(self,data=None):
      global config
      if config['DEFAULT']['CTRL_SP'] == "0":        
        config['DEFAULT']['CTRL_SP']="1"
      else:
        config['DEFAULT']['CTRL_SP']="0"
      #切換後，都要存設定
      saveConfig()            
    def m_pm_switch(self,data=None):
      global config
      #is_play_music
      if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "0":
         config['DEFAULT']['PLAY_SOUND_ENABLE'] = "1"
      else:
         config['DEFAULT']['PLAY_SOUND_ENABLE'] = "0"
      #切換後，都要存設定
      saveConfig()
    def m_game_switch(self,data=None):
      global gamemode_btn_click
      global gamemode_btn
      gamemode_btn_click(gamemode_btn)      
    def m_quit(self,data=None):
      self.set_visible(False)      
      x_btn_click(self)
    def m_output_type(self,data=None,kind="DEFAULT"):
      global DEFAULT_OUTPUT_TYPE
      debug_print(kind)
      DEFAULT_OUTPUT_TYPE=kind
    def m_none(self,data=None):
      return False
    def on_click(self,data,event): #data1 and data2 received by the connect action line 23
      #print ('self :', self)
      #print('data :',data)
      #print('event :',event)
      btn=event.button #Bby controlling this value (1-2-3 for left-middle-right) you can call other functions.
      #debug_print('event.button :',btn)
      time=gtk.get_current_event_time() # required by the popup. No time - no popup.
      #debug_print ('time:', time)

      global menu
      global menu_items
      global gamemode_btn
      global DEFAULT_OUTPUT_TYPE
      global config
      #debug_print(dir(menu))
      menu.set_visible(False)
      #menu = gtk.Menu()
      for i in range(0,len(menu_items)):
        menu.remove(menu_items[i])
      menu_items=[]
      menu_items.append(gtk.MenuItem("1.關於肥米輸入法"))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items[len(menu_items)-1].connect("activate", self.m_about) #added by gv - it had nothing before
      
      if gamemode_btn.get_label()=="正常模式":        
        menu_items.append(gtk.MenuItem("2.切換至「遊戲模式」"))
      else:
        menu_items.append(gtk.MenuItem("2.切換至「正常模式」"))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items[len(menu_items)-1].connect("activate", self.m_game_switch) #added by gv - it had nothing before

      menu_items.append(gtk.MenuItem("4.選擇出字模式"))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items[len(menu_items)-1].connect("activate", self.m_none)
      #print(dir(menu_items[len(menu_items)-1]))
      # From : https://www.twblogs.net/a/5beb3c312b717720b51efe87
      sub_menu = gtk.Menu()
      sub_menu_items = []
      is_o = ""
      if DEFAULT_OUTPUT_TYPE=="DEFAULT":
        is_o = "●"
      else:
        is_o = "　"      
      sub_menu_items.append(gtk.MenuItem("【%s】正常出字模式" % (is_o)))
      sub_menu.append( sub_menu_items[len(sub_menu_items)-1] )
      sub_menu_items[len(sub_menu_items)-1].connect("activate", self.m_output_type,"DEFAULT")
      
      if DEFAULT_OUTPUT_TYPE=="BIG5":
        is_o = "●"
      else:
        is_o = "　"
      sub_menu_items.append(gtk.MenuItem("【%s】BIG5模式" % (is_o)))
      sub_menu.append( sub_menu_items[len(sub_menu_items)-1] )
      sub_menu_items[len(sub_menu_items)-1].connect("activate", self.m_output_type,"BIG5")
      
      if DEFAULT_OUTPUT_TYPE=="PASTE":
        is_o = "●"
      else:
        is_o = "　"
      sub_menu_items.append(gtk.MenuItem("【%s】複製貼上模式" % (is_o)))
      sub_menu.append( sub_menu_items[len(sub_menu_items)-1] )
      sub_menu_items[len(sub_menu_items)-1].connect("activate", self.m_output_type,"PASTE")
      
      menu_items[len(menu_items)-1].set_submenu(sub_menu)
      #sub_menu.show_all()
      #sub_menu.popup(None, None, None, btn, 2)
      #menu_items[len(menu_items)-1].connect("activate", self.m_game_switch) #added by gv - it had nothing before
      
      if config['DEFAULT']['CTRL_SP'] == "1":
        menu_items.append(gtk.MenuItem("4.【●】使用 CTRL+SPACE 切換輸入法"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_ctrlsp_switch)
      else:
        menu_items.append(gtk.MenuItem("4.【　】使用 CTRL+SPACE 切換輸入法"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_ctrlsp_switch)
      
      if config['DEFAULT']['SP'] == "1":
        menu_items.append(gtk.MenuItem("5.【●】顯示短根"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_sp_switch)
      else:
        menu_items.append(gtk.MenuItem("5.【　】顯示短根"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_sp_switch)
      
      if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1":
        menu_items.append(gtk.MenuItem("6.【●】打字音"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_pm_switch)
      else:
        menu_items.append(gtk.MenuItem("6.【　】打字音"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_pm_switch)
                        
      menu_items.append(gtk.MenuItem(""))
      menu.append( menu_items[len(menu_items)-1] )
      
      menu_items.append(gtk.MenuItem("離開(Quit)"))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items[len(menu_items)-1].connect("activate", self.m_quit)

      #add space
      menu_items.append(gtk.MenuItem(""))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items.append(gtk.MenuItem(""))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items.append(gtk.MenuItem(""))
      
      
      menu.show_all()      
      menu.popup(None, None, None, btn, 2) #button can be hardcoded (i.e 1) but time must be correct.      
      #menu.reposition()
      #print(dir(menu))

  #message("Status Icon Left Clicked")
  #make_menu(event_button, event_time)
# 生成肥圖片
#if my.is_file(PWD+"\\UCLLIU.png") == False:
#  my.file_put_contents(PWD+"\\UCLLIU.png",my.base64_decode(UCL_PIC_BASE64))  
menu_items = []
menu = gtk.Menu()  
tray = TrayIcon()

#icon.set_visible(True)
# Create menu

 


win.show_all()
simple_btn.set_visible(False)

if config["DEFAULT"]["SHORT_MODE"] == "1":
  run_short()
else:
  run_long()  
  


win.set_focus(None)

# 初使化按二次
#uclen_btn_click(uclen_btn)
#uclen_btn_click(uclen_btn)

#set_interval(1)

#gtk.main()
updateGUI_Step = 0
def updateGUI():
  global updateGUI_Step
  #global is_shutdown
  while gtk.events_pending():
    gtk.main_iteration(False)
  updateGUI_Step = updateGUI_Step + 1
  if updateGUI_Step % 100 == 0:
    updateGUI_Step = 0
    toAlphaOrNonAlpha()
while True:
  time.sleep(0.01)
  #debug_print("gg")
  updateGUI()      
pythoncom.PumpMessages()     

#mainloop()
  
 
