import pygame
import sys
import os
import random
import asyncio # أضفنا هذا للمتصفح
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# --- الدالة السحرية لرؤية الصور داخل ملف الـ EXE أو الموقع ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
WIDTH, HEIGHT = 1300, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mathio game") # تم تصليح القوس هنا

# الألوان
BG_COLOR = (10, 15, 25)
GOLD, WHITE, GREEN, RED, BLUE = (212, 175, 55), (245, 245, 245), (46, 204, 113), (231, 76, 60), (31, 58, 147)

def get_font(size):
    p = "C:/Windows/Fonts/tahoma.ttf"
    # للمتصفح سنستخدم الخط الافتراضي إذا لم يجد تاهوما
    return pygame.font.Font(p, size) if os.path.exists(p) else pygame.font.SysFont("arial", size)

font_title, font_sub, font_text, font_ui = get_font(36), get_font(26), get_font(19), get_font(21)
def ar(text): return get_display(reshape(str(text)))

def draw_text_wrapped(surface, text, x_end, y_start, max_width, font, color):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    y = y_start
    for line in lines:
        if line.strip() == "": continue
        rendered = font.render(ar(line), True, color)
        surface.blit(rendered, (x_end - rendered.get_width(), y))
        y += font.get_linesize() + 7
    return y

# --- تحميل الصور ---
images = {}
for name in ['digestive', 'circulatory', 'respiratory', 'skeletal']:
    found = False
    for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG']:
        path = resource_path(name + ext)
        if os.path.exists(path):
            try:
                images[name] = pygame.transform.scale(pygame.image.load(path), (420, 420))
                found = True
                break
            except: continue

# --- المحتوى والأسئلة (كما هي في كودك) ---
lessons = [
    {"title": "الجهاز الهضمي: ميكانيكا الكيموس (1/2)", "img": "digestive", "content": ["تبدأ رحلة الغذاء في الفم، حيث يتم التنسيق بين الأسنان واللسان لإجراء الهضم الميكانيكي، بينما تفرز الغدد اللعابية إنزيم الأميليز الذي يبدأ في تفكيك النشا المعقد إلى سكريات ثنائية. ينتقل الطعام عبر المريء بواسطة الحركة الدودية وصولاً للمعدة. في المعدة، تفرز الخلايا الجدارية حمض الهيدروكلوريك HCl الذي يخفض الأس الهيدروجيني لقتل البكتيريا وتنشيط البيبسين لتبدأ عملية هضم البروتينات المعقدة وتحويلها لسلاسل ببتيدية."]},
    {"title": "الجهاز الهضمي: الامتصاص والملحقات (2/2)", "img": "digestive", "content": ["ينتقل الكيموس للأمعاء الدقيقة حيث تفرز العصارة الصفراء من الكبد لتفتيت الدهون ميكانيكياً. الأمعاء الدقيقة تحتوي على ملايين الخملات التي تزيد مساحة سطح الامتصاص بشكل هائل لتمرير المغذيات للدم. في الأمعاء الغليظة، يتم استخلاص الماء وتنتج البكتيريا النافعة فيتامين K وB12. الكبد يعمل كمصفاة للسموم ومخزن للجليكوجين، مما يحافظ على استقرار مستويات الطاقة والسكر في جسم الإنسان طوال اليوم."]},
    {"title": "الجهاز الدوري: كهرباء القلب (1/2)", "img": "circulatory", "content": ["القلب مضخة عضلية رباعية الحجرات. تبدأ الإشارة الكهربائية من العقدة الجيب أذينية (SA Node)، لتنتشر في الأذينين ثم البطينين. الجانب الأيمن يستقبل الدم غير المؤكسج ويضخه للرئتين، بينما الجانب الأيسر يضخ الدم المؤكسج لكافة أنحاء الجسم عبر الأورطي. الصمامات تضمن سريان الدم في اتجاه واحد وتمنع الارتجاع. عضلة القلب تعتمد في تغذيتها على الشرايين التاجية التي تحيط بها كالتاج وتوفر الأكسجين المستمر."]},
    {"title": "الجهاز الدوري: الأوعية والدم (2/2)", "img": "circulatory", "content": ["الشرايين تحمل الدم الغني بالأكسجين بجدران سميكة، بينما تعيد الأوردة الدم عبر صمامات تمنع تأثير الجاذبية. يتكون الدم من بلازما وخلايا حمراء تحمل الهيموجلوبين لنقل الأكسجين، وصفائح دموية للتجلط، وخلايا بيضاء للمناعة. الجهاز الليمفاوي يعيد السوائل المفقودة من الشعيرات الدموية إلى الأوردة الكبرى، مما يحافظ على ضغط الجسم المثالي 120/80، وهو نتاج توازن قوة القلب ومقاومة الأوعية الدموية الطرفية."]},
    {"title": "الجهاز التنفسي: ممرات الهواء (1/2)", "img": "respiratory", "content": ["يبدأ التنفس من الأنف الذي يرطب ويدفئ الهواء. لسان المزمار يغلق الحنجرة أثناء البلع لمنع الاختناق. القصبة الهوائية مبطنة بأهداب مجهرية تطرد الشوائب، ومدعمة بحلقات غضروفية لتبقى مفتوحة. تتفرع المسالك وصولاً للحويصلات الرئوية، وهي المواقع النهائية لتبادل الغازات. الرئة اليمنى تتكون من 3 فصوص واليسرى من فصين لتفسح مجالاً للقلب، ويغلفهما غشاء البلورا الذي يحميهما ويقلل الاحتكاك أثناء التنفس."]},
    {"title": "الجهاز التنفسي: تبادل الغازات (2/2)", "img": "respiratory", "content": ["يحدث تبادل الغازات عبر جدران الحويصلات الرقيقة بالانتشار البسيط. سائل السيرفاكتانت يغلف الحويصلات ليمنع انهيارها. الحجاب الحاجز هو المحرك الأساسي؛ بانقباضه يتوسع الصدر ويقل الضغط فيندفع الهواء للداخل (شهيق). ينتقل معظم ثاني أكسيد الكربون في الدم كأيونات بيكربونات. النخاع المستطيل في الدماغ يراقب حموضة الدم ويزيد معدل التنفس عند ارتفاع CO2، لضمان وصول الأكسجين للميتوكوندريا لإنتاج طاقة ATP الحيوية."]},
    {"title": "الجهاز الهيكلي: هندسة العظام (1/2)", "img": "skeletal", "content": ["يتكون الهيكل العظمي من 206 عظمة توفر الدعامة. العظام أنسجة حية تخزن الكالسيوم والفوسفور. النخاع العظمي الأحمر هو المصنع لإنتاج خلايا الدم. الخلايا البانية تبني العظم، بينما الهادمة تعيد تدويره. يتكون الهيكل المحوري من 80 عظمة تشمل الجمجمة والعمود الفقري والقفص الصدري، والسمحاق هو الغشاء الخارجي للعظم الغني بالأعصاب المسؤولة عن نقل إشارات الألم الحادة والمركزة عند حدوث الكسور العظمية المختلفة."]},
    {"title": "الجهاز الهيكلي: المفاصل (2/2)", "img": "skeletal", "content": ["المفاصل الزلالية توفر مدى واسعاً من الحركة وتستخدم السائل السينوفي لتقليل الاحتكاك. الغضاريف تعمل كوسائد لامتصاص الصدمات وحماية العظام من التآكل. الأربطة تربط العظام ببعضها، بينما تنقل الأوتار قوة العضلات للعظام لتحريك الجسم. فيتامين D ضروري لتقوية العظام ضد الهشاشة. العمود الفقري يحمي الحبل الشوكي، بينما الهيكل الطرفي (126 عظمة) يمنحنا القدرة على المشي والركض والتفاعل الميكانيكي الدقيق مع البيئة."]}
]

q_bank = [
    {"q": "أي إنزيم يبدأ هضم النشا في الفم؟", "o": ["الأميليز", "الليباز", "البيبسين"], "a": "الأميليز"},
    {"q": "ما وظيفة حمض HCl في المعدة؟", "o": ["تنشيط البيبسين", "هضم الدهون", "امتصاص الماء"], "a": "تنشيط البيبسين"},
    {"q": "أين تقع خملات الامتصاص؟", "o": ["الأمعاء الدقيقة", "المعدة", "المرئ"], "a": "الأمعاء الدقيقة"},
    {"q": "ماذا تنتج البكتيريا في الأمعاء الغليظة؟", "o": ["فيتامين K", "حمض HCl", "الأكسجين"], "a": "فيتامين K"},
    {"q": "ما هو منظم النبض الطبيعي في القلب؟", "o": ["العقدة SA", "العقدة AV", "ألياف بيركنجي"], "a": "العقدة SA"},
    {"q": "أي وعاء يحمل الدم بضغط عالٍ جداً؟", "o": ["الشرايين", "الأوردة", "الشعيرات"], "a": "الشرايين"},
    {"q": "ما وظيفة صمامات الأوردة؟", "o": ["منع ارتداد الدم", "زيادة الضغط", "نقل الغذاء"], "a": "منع ارتداد الدم"},
    {"q": "ما هو ناقل الأكسجين الأساسي في الدم؟", "o": ["الهيموجلوبين", "الألبومين", "البلازما"], "a": "الهيموجلوبين"},
    {"q": "ما وظيفة لسان المزمار؟", "o": ["حماية القصبة الهوائية", "إصدار الصوت", "البلع"], "a": "حماية القصبة الهوائية"},
    {"q": "لماذا القصبة مدعمة بحلقات غضروفية؟", "o": ["لتبقى مفتوحة", "لإنتاج اللعاب", "للهضم"], "a": "لتبقى مفتوحة"},
    {"q": "ما وظيفة سائل السيرفاكتانت؟", "o": ["منع انكماش الحويصلات", "قتل الميكروبات", "ترطيب الهواء"], "a": "منع انكماش الحويصلات"},
    {"q": "كيف يدخل الهواء للرئتين بالشهيق؟", "o": ["ضغط سلبي", "نقل نشط", "جاذبية"], "a": "ضغط سلبي"},
    {"q": "أين تصنع خلايا الدم في الجسم؟", "o": ["نخاع العظام", "الطحال", "الكبد"], "a": "نخاع العظام"},
    {"q": "ما الوظيفة الأساسية للغضاريف؟", "o": ["تقليل الاحتكاك", "تخزين الكالسيوم", "الحركة"], "a": "تقليل الاحتكاك"},
    {"q": "ما الذي يربط العضلة بالعظم مباشرة؟", "o": ["الأوتار", "الأربطة", "المفاصل"], "a": "الأوتار"},
    {"q": "كم عدد عظام الهيكل المحوري؟", "o": ["80 عظمة", "206 عظمة", "126 عظمة"], "a": "80 عظمة"},
    {"q": "ما المادة التي تفتت الدهون ميكانيكياً؟", "o": ["العصارة الصفراء", "البيبسين", "الأميليز"], "a": "العصارة الصفراء"},
    {"q": "أين يقع الصمام الميترالي؟", "o": ["الجانب الأيسر للقلب", "في الرئة", "في الكبد"], "a": "الجانب الأيسر للقلب"},
    {"q": "كيف ينتقل معظم CO2 في الدم؟", "o": ["أيونات بيكربونات", "غاز ذائب", "على الهيموجلوبين"], "a": "أيونات بيكربونات"},
    {"q": "ما اسم الغشاء المحيط بالرئة؟", "o": ["البلورا", "التامور", "السمحاق"], "a": "البلورا"},
    {"q": "ما هو المفصل الأكثر حرية في الحركة؟", "o": ["الزلالي", "الليفي", "الغضروفي"], "a": "الزلالي"},
    {"q": "ما دور خلايا Osteoblasts؟", "o": ["بناء العظم", "هدم العظم", "تخزين الدم"], "a": "بناء العظم"},
    {"q": "ما طول المريء تقريباً في البالغين؟", "o": ["25 سم", "10 سم", "50 سم"], "a": "25 سم"},
    {"q": "أي بطين يضخ الدم للرئتين؟", "o": ["الأيمن", "الأيسر", "كلاهما"], "a": "الأيمن"},
    {"q": "ما الجزء المسؤول عن التحكم في التنفس؟", "o": ["النخاع المستطيل", "القلب", "المعدة"], "a": "النخاع المستطيل"},
    {"q": "ما اسم الغشاء الخارجي للعظم؟", "o": ["السمحاق", "الغضروف", "النخاع"], "a": "السمحاق"},
    {"q": "ما نسبة البلازما في الدم تقريباً؟", "o": ["55%", "45%", "10%"], "a": "55%"},
    {"q": "أين يخزن السكر الزائد (الجليكوجين)؟", "o": ["الكبد", "المعدة", "الكلية"], "a": "الكبد"},
    {"q": "ما وظيفة الجهاز الليمفاوي؟", "o": ["إعادة السوائل المفقودة", "هضم السكر", "تجلط الدم"], "a": "إعادة السوائل المفقودة"},
    {"q": "ما الفيتامين الضروري لامتصاص الكالسيوم؟", "o": ["فيتامين D", "فيتامين C", "فيتامين B"], "a": "فيتامين D"}
]

# --- دالة التشغيل الرئيسية المعدلة للويب ---
async def main():
    state, idx, correct, wrong, q_idx, waiting, feedback = "STUDY", 0, 0, 0, 0, False, ""
    fb_col = WHITE
    random.shuffle(q_bank)
    current_options = []
    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)
        buttons = []
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if state == "STUDY":
                    if e.key == pygame.K_RIGHT and idx < len(lessons)-1: idx += 1
                    elif e.key == pygame.K_LEFT and idx > 0: idx -= 1
                    elif e.key == pygame.K_SPACE: 
                        state, q_idx, correct, wrong = "QUIZ", 0, 0, 0
                        random.shuffle(q_bank)
                        current_options = list(q_bank[q_idx]["o"])
                        random.shuffle(current_options)
                elif state == "QUIZ" and waiting:
                    q_idx += 1
                    if q_idx >= 30: state = "RESULT"
                    else: 
                        waiting, feedback = False, ""
                        current_options = list(q_bank[q_idx]["o"])
                        random.shuffle(current_options)
                elif state == "RESULT" and e.key == pygame.K_SPACE: state, idx = "STUDY", 0

            if e.type == pygame.MOUSEBUTTONDOWN and state == "QUIZ" and not waiting:
                # سنحسب الـ buttons لاحقاً في الرسم
                pass 

        if state == "STUDY":
            curr = lessons[idx]
            screen.blit(font_title.render(ar(curr["title"]), True, GOLD), (WIDTH-650, 40))
            if curr["img"] in images: screen.blit(images[curr["img"]], (50, 200))
            y_pos = 200
            for paragraph in curr["content"]:
                y_pos = draw_text_wrapped(screen, paragraph, WIDTH - 50, y_pos, 720, font_text, WHITE) + 15
            nav = font_ui.render(ar(f"صفحة {idx+1}/8 | (أسهم) تنقل | (مسطرة) بدء الامتحان"), True, BLUE)
            screen.blit(nav, (WIDTH//2 - nav.get_width()//2, HEIGHT-60))

        elif state == "QUIZ":
            stats = font_ui.render(ar(f"صح: {correct} | خطأ: {wrong} | سؤال: {q_idx+1}/30"), True, GOLD)
            screen.blit(stats, (50, 30))
            draw_text_wrapped(screen, q_bank[q_idx]["q"], WIDTH//2 + 350, 180, 800, font_sub, WHITE)
            
            for i, opt in enumerate(current_options):
                r = pygame.Rect(WIDTH//2 - 350, 350 + i*120, 700, 95)
                pygame.draw.rect(screen, BLUE, r, border_radius=15)
                txt = font_ui.render(ar(opt), True, WHITE)
                screen.blit(txt, txt.get_rect(center=r.center))
                buttons.append((r, opt))
                
                # كشف الضغط على الزر
                if pygame.mouse.get_pressed()[0]:
                    m_pos = pygame.mouse.get_pos()
                    if r.collidepoint(m_pos) and not waiting:
                        if opt == q_bank[q_idx]["a"]:
                            correct += 1; feedback = "إجابة صحيحة يا دكتور!"; fb_col = GREEN
                        else:
                            wrong += 1; feedback = f"خطأ! الإجابة: {q_bank[q_idx]['a']}"; fb_col = RED
                        waiting = True

            if waiting:
                msg = font_sub.render(ar(feedback), True, fb_col)
                screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 820))

        elif state == "RESULT":
            res_txt = "ممتاز يا دكتور! نجحت بتفوق" if correct >= 24 else "تحتاج لمراجعة الشرح مرة أخرى"
            screen.blit(font_title.render(ar(res_txt), True, GREEN if correct >= 24 else RED), (WIDTH//2 - 300, 350))
            screen.blit(font_sub.render(ar(f"النتيجة النهائية: {correct} من 30"), True, WHITE), (WIDTH//2 - 150, 450))
            screen.blit(font_text.render(ar("اضغط مسطرة للعودة للبداية"), True, GOLD), (WIDTH//2 - 120, 600))

        pygame.display.flip()
        await asyncio.sleep(0) # السطر السحري للمتصفح
        clock.tick(30)

if __name__ == "__main__":
    asyncio.run(main())