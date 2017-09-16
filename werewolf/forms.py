from django import forms
from .models import Village, Remark, Resident

class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = '村の名前を入力'

class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'form-control'

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ('character',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['character'].widget.attrs['class'] = 'form-control'
        self.fields['character'].widget.attrs['placeholder'] = 'キャラクターを選択'

    rain = (
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

    character = forms.ChoiceField(widget=forms.Select, choices=rain)
