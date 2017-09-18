from django.forms import formset_factory
from django.views.generic import FormView, ListView, CreateView
from django.views.generic.edit import CreateView, ModelFormMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django import forms
from .models import Choice, Question, Village, Remark, Resident
from .forms import VillageForm, RemarkForm, ResidentForm
from random import randint

def getRainTable():
    return (
        (1 ,'恋多き娘　メイ'),
        (2 ,'双子の赤　レディア'),
        (3 ,'双子の青　ヴィノール'),
        (4 ,'見習い　ミレイユ'),
        (5 ,'訓練生　ルファ'),
        (6 ,'教官　アミル'),
        (7 ,'落第生　クラット'),
        (8 ,'飛び級　シュカ'),
        (9 ,'看板娘　サリィ'),
        (10,'若店主　エト'),
        (11,'領主の娘　ロッテ'),
        (12,'領主の末娘　エリィゼ'),
        (13,'町娘　コレット'),
        (14,'異国の旅人　イル'),
        (15,'女装癖　ノクロ'),
        (16,'隠密修行　ミナオ'),
        (17,'受信中　ギュル'),
        (18,'自己愛者　チサ'),
        (19,'用心棒　アルビーネ'),
        (20,'悪ガキ　ジュスト'),
        (21,'鍛冶屋　ジャン'),
        (22,'仮面紳士　マスケラ'),
        (23,'童話読み　モカ'),
        (24,'中毒　カイン　'),
        (25,'自称王子　アールグレイ'),
        (26,'図書館長　ジョセフ'),
        (27,'女中　リーリ'),
        (28,'怪談好き　アーニャ'),
        (29,'修道女　イリア'),
        (30,'踊り子　メリッサ'),
        (31,'詠み手　ポラリス'),
        (32,'冒険家　ウィル'),
        (33,'射手　キリク'),
        (34,'技師　レネ'),
        (35,'染物師　サムファ'),
        (36,'商人　アルカ'),
        (37,'建築家　フェン'),
        (38,'噂好き　トルテ'),
        (39,'小説家　エラリー'),
        (40,'観測者　マリーベル'),
        (41,'詐欺師　ネッド'),
        (42,'彫師　ランス'),
        (43,'探究者　エドワーズ'),
        (44,'泣き虫　ティナ'),
        (45,'盲目　テレーズ'),
        (46,'転寝　オデット'),
        (47,'作曲家　ケーリー'),
        (48,'接客業　スイートピー'),
        (49,'毒舌家　セルマ'),
        (50,'家令　ユーリ　'),
        (51,'雪国の作家　エレオノーラ'),
        (52,'雪国の少女　リディヤ'),
        (53,'本屋　クレイグ'),
        (54,'郵便屋　パーシー'),
        (55,'装飾工　メリル'),
        (56,'植物学者　シニード'),
        (57,'酒飲み　ハイヴィ'),
        (58,'調香師　チュレット'),
        (59,'薬草摘み　ソーヤ'),
        (60,'治療中　スー'),
        (61,'昆虫博士　ニコル'),
        (62,'綾取り　ツリガネ'),
        (63,'蒐集家　ダァリヤ'),
        (64,'研究者　トロイ'),
        (65,'歌い手　ナデージュ'),
        (66,'占星術師　ヘロイーズ'),
        (67,'学術士　ヒューゴ　'),
        (68,'演者　ヤーニカ'),
        (69,'煙草売り　ヌァヴェル'),
        (70,'火薬師　ヨアン'),
        (71,'花屋　マイダ'),
        (72,'パン屋　デボラ'),
        (73,'庭師　アーリック'),
        (74,'写真家　ヴィンセント'),
        (75,'司祭　ドワイト'),
        (76,'好奇心　エメット'),
        (77,'泣き女　シーナ'),
        (78,'代書人　クレム'),
        (79,'掏摸　セス'),
        (80,'煙突掃除　ミケル'),
    )

def getJewelTable():
    return (
        (1, '水晶　クリスタ'),
        (2, '黒曜石　オブシウス'),
        (3, '柘榴石　グラニエ'),
        (4, '紫水晶　アメジスタ'),
        (5, '水宝玉　ミレーネ'),
        (6, '金剛石　リアント'),
        (7, '翠玉　エメリア'),
        (8, '真珠　パーヴィス'),
        (9, '紅玉　ルービナ'),
        (10,'橄欖石　ガラーシャ'),
        (11,'青玉　フィーラ'),
        (12,'蛋白石　オルコット'),
        (13,'黄玉　パズィ'),
        (14,'土耳古石　ギュルセル'),
        (15,'藍銅鉱　アズ'),
        (16,'縞瑪瑙　イクシオン'),
        (17,'月長石　ルナ'),
        (18,'日長石　ソル'),
        (19,'ユークレース　ファシリア'),
        (20,'炎瑪瑙　フィエゴ'),
        (21,'金緑石　アレクシア'),
        (22,'黄水晶　トール'),
        (23,'瑠璃　ルリ'),
        (24,'曹珪灰石　エルマール'),
        (25,'紅柱石　アンダルシア'),
        (26,'藍玉　ハルム'),
        (27,'深海珊瑚　コーラリア'),
        (28,'蒼鉛　ヴィスマルト'),
        (29,'黒玉　クロヒメ'),
        (30,'菊石　アントニオ'),
        (31,'黒蛋白石　オペラ'),
        (32,'黄鉄鉱　リット'),
        (33,'天青石　セレスティア'),
        (34,'閃亜鉛鉱　ファル'),
        (35,'モルガン石　ミーナ'),
        (36,'金緑石　クロード'),
        (37,'猫目石　キャシー'),
        (38,'孔雀石　マラク'),
        (39,'空色縞瑪瑙　シエロ'),
        (40,'紅玉髄　カルナス'),
        (41,'菫青石　アイラ'),
        (42,'針水晶　ルチル'),
        (43,'菱苦土石　ハウエラ'),
        (44,'翡翠　フェイ'),
        (45,'燐葉石　フィオレ'),
        (46,'緑柱石　ヘリオス'),
        (47,'ユーディアル石　ディアナ'),
        (48,'白蝶貝　ハク'),
        (49,'透輝石　ステラ'),
        (50,'チャロ石　シェニ　'),
        (51,'珪孔雀石　クラリス'),
        (52,'黝輝石　エリシオ'),
        (53,'曹灰硼石　ウェディ'),
        (54,'曹灰長石　ヴラド'),
        (55,'雷鳥卵石　エッカ'),
        (56,'蛍石　シャオ'),
        (57,'虹瑪瑙　イリス'),
        (58,'輝安鉱　ツルギ'),
        (59,'血玉石　メアリー'),
        (60,'煙水晶　キーツ'),
        (61,'葡萄石　リプリィ'),
        (62,'風信子石　ジル'),
    )

def getRainBigTable():
    return (
        (1, '恋多き娘　メイ'),
        (2, '双子の赤　レディア'),
        (3, '双子の青　ヴィノール'),
        (4, '見習い　ミレイユ'),
        (5, '訓練生　ルファ'),
        (6, '教官　アミル'),
        (7, '落第生　クラット'),
        (8, '飛び級　シュカ'),
        (9, '看板娘　サリィ'),
        (10,'若店主　エト'),
        (11,'領主の娘　ロッテ'),
        (12,'領主の末娘　エリィゼ'),
        (13,'町娘　コレット'),
        (14,'異国の旅人　イル'),
        (15,'女装癖　ノクロ'),
        (16,'隠密修行　ミナオ'),
        (17,'受信中　ギュル'),
        (18,'自己愛者　チサ'),
        (19,'用心棒　アルビーネ'),
        (20,'悪ガキ　ジュスト'),
        (21,'鍛冶屋　ジャン'),
        (22,'仮面紳士　マスケラ'),
        (23,'童話読み　モカ'),
        (24,'中毒　カイン　'),
        (25,'自称王子　アールグレイ'),
        (26,'図書館長　ジョセフ'),
        (27,'女中　リーリ'),
        (28,'怪談好き　アーニャ'),
        (29,'修道女　イリア'),
        (30,'踊り子　メリッサ'),
        (31,'詠み手　ポラリス'),
        (32,'冒険家　ウィル'),
        (33,'射手　キリク'),
        (34,'技師　レネ'),
        (35,'染物師　サムファ'),
        (36,'商人　アルカ'),
        (37,'建築家　フェン'),
        (38,'噂好き　トルテ'),
        (39,'小説家　エラリー'),
        (40,'観測者　マリーベル'),
        (41,'詐欺師　ネッド'),
        (42,'彫師　ランス'),
        (43,'探究者　エドワーズ'),
        (44,'泣き虫　ティナ'),
        (45,'盲目　テレーズ'),
        (46,'転寝　オデット'),
        (47,'作曲家　ケーリー'),
        (48,'接客業　スイートピー'),
        (49,'毒舌家　セルマ'),
        (50,'家令　ユーリ　'),
        (51,'装飾工　メリル'),
        (52,'植物学者　シニード'),
        (53,'酒飲み　ハイヴィ'),
        (54,'調香師　チュレット'),
        (55,'薬草摘み　ソーヤ'),
        (56,'治療中　スー'),
        (57,'昆虫博士　ニコル'),
        (58,'綾取り　ツリガネ'),
        (59,'蒐集家　ダァリヤ'),
        (60,'研究者　トロイ'),
        (61,'歌い手　ナデージュ'),
        (62,'占星術師　ヘロイーズ'),
        (63,'学術士　ヒューゴ　'),
        (64,'演者　ヤーニカ'),
        (65,'煙草売り　ヌァヴェル'),
        (66,'火薬師　ヨアン'),
        (67,'花屋　マイダ'),
        (68,'パン屋　デボラ'),
        (69,'庭師　アーリック'),
        (70,'写真家　ヴィンセント'),
        (71,'司祭　ドワイト'),
        (72,'好奇心　エメット'),
        (73,'泣き女　シーナ'),
        (74,'代書人　クレム'),
        (75,'掏摸　セス'),
        (76,'煙突掃除　ミケル'),
        (77,'受付人　マシュー'),
        (78,'裏稼業　ロー'),
        (80,'夜光性　シェーラ'),
    )

def getEnsouTable():
    return (
        (1 ,'ピアノ　アリシア'),
        (2 ,'ギター　ルース'),
        (3 ,'草笛　エフェル'),
        (4 ,'ハープ　コウィスカ'),
        (5 ,'板胡　シア'),
        (6 ,'ツィター　シルビア'),
        (7 ,'レインスティック　ベルスーズ'),
        (8 ,'角笛　オルファン'),
        (9 ,'アルプホルン　カルーア'),
        (10,'宮太鼓　マコト'),
        (11,'チェロ　ミリッツァ'),
        (12,'口笛　ケルイズ'),
        (13,'フルート　リベラ'),
        (14,'カスタネット　ムティリュ'),
        (15,'カスタネット　ネスカ'),
        (16,'ハーモニカ　テイト'),
        (17,'三味線　クオン'),
        (18,'トロンボーン　ノール'),
        (19,'セルパン　カサドル'),
        (20,'スティールパン　シャンティ'),
        (21,'クラリネット　コトワ'),
        (22,'タンバリン　シェシャ'),
        (23,'シタール　モハーナ'),
        (24,'手拍子　ブリジット'),
        (25,'手拍子　エディ'),
        (26,'ヴィオラ　ルネッタ'),
        (27,'汽笛　シズキ'),
        (28,'オーボエ　アニタ'),
        (29,'平太鼓　コズエ'),
        (30,'シンバル　ソルム'),
        (31,'ブズーキ　エイレーネ'),
        (32,'シュリンクス　クリロフ'),
        (33,'ハンドベル　ヤシロ'),
        (34,'トライアングル　クロエ'),
        (35,'エレキギター　ジョゼ'),
        (36,'キーボード　リル'),
        (37,'ベース　ヴェルナー'),
        (38,'アコーディオン　ドロテア'),
        (39,'音叉　エミリオ'),
        (40,'バードコール　ヴァレリー'),
    )

def getRandomCharacterImgURL(ID):
    if ID == 'rain':
        return 'rain/{}.png'.format(str(randint(1,80)).zfill(2))
    elif ID == 'rainBig':
        return 'rainBig/{}.png'.format(str(randint(1,80)).zfill(2))
    elif ID == 'jewel':
        return 'jewel/{}_n.png'.format(str(randint(1,62)).zfill(2))
    elif ID == 'ensou':
        return 'ensou/{}.png'.format(str(randint(1,40)).zfill(3))
    else:
        return 'rain/01.png'

def getCharacterImgURL(ID,no):
    if ID == 'rain':
        return 'rain/{}.png'.format(str(no).zfill(2))
    elif ID == 'rainBig':
        return 'rainBig/.png'.format(str(no).zfill(2))
    elif ID == 'jewel':
        return 'jewel/{}_n.png'.format(str(no).zfill(2))
    elif ID == 'ensou':
        return 'ensou/{}.png'.format(str(no).zfill(3))
    else:
        return 'rain/01.png'

def getCharacterName(ID):
    if ID == 'rain':
        return '霧雨降る街'
    elif ID == 'rainBig':
        return '霧雨降る街(BIG)'
    elif ID == 'jewel':
        return '宝石箱《Jewel Box》'
    elif ID == 'ensou':
        return '演奏会'
    else:
        return 'undefined'

def getCharacterTable(ID):
    if ID == 'rain':
        return getRainTable()
    elif ID == 'rainBig':
        return getRainBigTable()
    elif ID == 'jewel':
        return getJewelTable()
    elif ID == 'ensou':
        return getEnsouTable()
    else:
        return ((1,'エラーが発生しました'),)

class VillageIndex(CreateView):
    model = Village, Resident
    form_class = VillageForm
    template_name = 'werewolf/index.html'
    success_url = reverse_lazy('werewolf:index')

    def form_valid(self, form):
        form.instance.auther = self.request.user.username
        form.instance.character_name = getCharacterName(form.cleaned_data['character'])
        form.instance.character_img_url = getRandomCharacterImgURL(form.cleaned_data['character'])
        print(form.instance.character_img_url)
        return super(VillageIndex, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = Village.objects.filter(palflag=0,endflag=0, delflag=0).order_by('-created_date')
        return context

class VillagePalIndex(CreateView):
    model = Village, Resident
    form_class = VillageForm
    template_name = 'werewolf/pal.html'
    success_url = reverse_lazy('werewolf:pal')

    def form_valid(self, form):
        form.instance.auther = self.request.user.username
        form.instance.character_name = getCharacterName(form.cleaned_data['character'])
        form.instance.character_img_url = getRandomCharacterImgURL(form.cleaned_data['character'])
        print(form.instance.character_img_url)
        return super(VillagePalIndex, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = Village.objects.filter(palflag=1,endflag=0, delflag=0).order_by('-created_date')
        return context

def VillageRemarks(request):
    ArticleFormSet = formset_factory(ArticleForm)
    BookFormSet = formset_factory(BookForm)
    if request.method == 'POST':
        article_formset = ArticleFormSet(request.POST, request.FILES, prefix='articles')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if article_formset.is_valid() and book_formset.is_valid():
            # do something with the cleaned_data on the formsets.
            pass
    else:
        article_formset = ArticleFormSet(prefix='articles')
        book_formset = BookFormSet(prefix='books')
    return render(request, 'manage_articles.html', {
        'article_formset': article_formset,
        'book_formset': book_formset,
    })

class VillageResidentForm(CreateView):
    model = Resident
    form_class = ResidentForm
    template_name = 'werewolf/village.html'

    def get_success_url(self):
        return reverse_lazy('werewolf:village', args=(self.kwargs['village_id'],))

    def form_valid(self, form):
        form.instance.resident = self.request.user
        form.instance.village_id = self.kwargs['village_id']
        form.instance.character = randint(1,80)
        return super(VillageRemarks, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['remark_list'] = Remark.objects.filter(delflag=0,village=self.kwargs['village_id']).order_by('-date')
        return context

class VillageRemarkForm(CreateView):
    model = Remark
    form_class = RemarkForm
    template_name = 'werewolf/village.html'

    def get_success_url(self):
        return reverse_lazy('werewolf:village', args=(self.kwargs['village_id'],))

    def form_valid(self, form):
        form.instance.user = self.request.user.username
        form.instance.user_id = self.request.user
        form.instance.village_id = self.kwargs['village_id']
        form.instance.character = randint(1,80)
        form.instance.character_img_url = "rain/" + str(form.instance.character).zfill(2) + ".png"
        return super(VillageRemarks, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['remark_list'] = Remark.objects.filter(delflag=0,village=self.kwargs['village_id']).order_by('-date')
        return context

class VillageLog(ListView):
    model = Village
    template_name = 'werewolf/log.html'
    queryset = Village.objects.filter(endflag=1, delflag=0).order_by('-created_date')

def VillageView(request, village_id):
    this_village = Village.objects.get(id=village_id)
    if request.method == 'POST':
        if 'remark' in request.POST:
            remark_form = RemarkForm(request.POST)
            if remark_form.is_valid():
                post = remark_form.save(commit=False)
                post.user_id = request.user
                post.user = request.user.username
                post.village_id = village_id
                resident_self = Resident.objects.get(village=village_id, resident=request.user)
                post.character = resident_self.character
                post.charaset = resident_self.charaset
                post.character_img_url = getCharacterImgURL(post.charaset, post.character)
                post.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
        elif 'resident' in request.POST:
            resident_form = ResidentForm(request.POST)
            resident_form.fields['character'].choices = getCharacterTable(this_village.character)
            if resident_form.is_valid():
                post = resident_form.save(commit=False)
                post.resident = request.user
                post.village_id = village_id
                post.charaset = this_village.character
                post.character_img_url = getCharacterImgURL(post.charaset, post.character)
                post.save()
                return HttpResponseRedirect(reverse('werewolf:village', args=(village_id,)))
    else:
        resident_form = ResidentForm()
        resident_form.fields['character'].choices = getCharacterTable(this_village.character)
        resident_list = Resident.objects.filter(village=village_id)
        context = {
            'remark_form': RemarkForm(),
            'resident_form': resident_form,
            'remark_list': Remark.objects.filter(delflag=0,village=village_id).order_by('-date')[:100],
            'resident_list': resident_list,
        }
        try:
            context['myselfinfo'] = resident_list.get(resident=request.user)
            context['isResident'] = True
            context['icon_url'] = context['myselfinfo'].character_img_url
        except:
            context['isResident'] = False
            context['icon_url'] = this_village.character_img_url
    return render(request, 'werewolf/village.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'werewolf/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'werewolf/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'werewolf/detail.html', {
            'question': question,
            'error_message': "投票先を選択してください",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('werewolf:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'werewolf/results.html', {'question': question})
