const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { applyTheme } = require("/root/.claude/skills/synced/ff77adec-22ca-4fcc-ad0d-e5bfdc9df599_9f3d0612-1348-4498-b31e-8662570811d7/pptx/scripts/apply_theme.js");

const IMG = p => path.join(__dirname, "img", p);
const OUT = process.argv[2] || path.join(__dirname, "ZelenyKrug_presentation.pptx");
const VIDEO = path.join(__dirname, "..", "video", "ZelenyKrug_reklama.mp4");

const THEME = {
  name: "Зелёный Круг",
  headFontFace: "Times New Roman",
  bodyFontFace: "Times New Roman",
  colors: {
    dk1: "14271C", lt1: "FFFFFF", dk2: "1F5136", lt2: "F6F1E4",
    accent1: "5DBB63", accent2: "F4A93B", accent3: "1F5136", accent4: "C6EBCF",
    accent5: "5E6E63", accent6: "E8505B", hlink: "1F5136", folHlink: "5E6E63",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "Зелёный Круг — айдентика бренда";
pres.author = "Бачинский И.В., Мельников А.Н., Бахшинян Д.А.";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---------- Макеты ----------
pres.defineSlideMaster({
  title: "COVER",
  background: { path: IMG("bg_dark.jpg") },
  objects: [],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: "F6F1E4" },
  objects: [
    { image: { path: IMG("icon_color.png"), x: 0.6, y: 0.5, w: 0.5, h: 0.5 } },
    { text: { text: "Зелёный Круг · айдентика бренда", options: { x: 0.6, y: 7.0, w: 5, h: 0.3, fontSize: 10, color: C.accent5, margin: 0 } } },
    { placeholder: { options: { name: "title", type: "title", x: 1.25, y: 0.42, w: 11.4, h: 0.68, fontSize: 32, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "DARK",
  background: { color: "1F5136" },
  objects: [
    { image: { path: IMG("favicon.png"), x: 0.6, y: 0.5, w: 0.5, h: 0.5 } },
    { text: { text: "Зелёный Круг · айдентика бренда", options: { x: 0.6, y: 7.0, w: 5, h: 0.3, fontSize: 10, color: C.accent4, margin: 0 } } },
    { placeholder: { options: { name: "title", type: "title", x: 1.25, y: 0.42, w: 11.4, h: 0.68, fontSize: 32, bold: true, color: C.background2, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
});

const shadow = () => ({ type: "outer", color: "14271C", blur: 14, offset: 4, angle: 90, opacity: 0.12 });
function card(s, x, y, w, h, fill = C.background1, name = "card") {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.22, fill: { color: fill }, line: { color: fill, width: 0 }, shadow: shadow(), objectName: name });
}
function fitImg(file, pw, ph, boxW, boxH) { // вписать картинку в рамку с сохранением пропорций
  const r = Math.min(boxW / pw, boxH / ph);
  return { w: pw * r, h: ph * r };
}
function txt(s, text, o) { s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: C.text1, valign: "top" }, o)); }
function bullets(s, items, o) {
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: { indent: 14 }, breakLine: i < items.length - 1 } })),
    Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: C.text1, valign: "top", paraSpaceAfter: 6 }, o));
}
function heading(s, text, o) { txt(s, text, Object.assign({ fontSize: 18, bold: true, color: C.text2, h: 0.4 }, o)); }

// ---------- 1. Обложка ----------
pres.addSection({ title: "Обложка" });
let s = pres.addSlide({ masterName: "COVER", sectionTitle: "Обложка" });
txt(s, "Комплексное задание по компьютерной графике · пр. 11–12", { x: 0.8, y: 0.75, w: 7, h: 0.35, fontSize: 14, color: C.accent4 });
s.addImage({ path: IMG("logo_cream.png"), x: 0.7, y: 1.75, w: 6.6, h: 6.6 * 200 / 640, altText: "Логотип Зелёный Круг" });
txt(s, "Разработка цифровой айдентики бренда", { x: 0.8, y: 4.0, w: 6.9, h: 0.5, fontSize: 22, bold: true, color: C.background2 });
txt(s, "Сервис доставки продуктов в многоразовой таре", { x: 0.8, y: 4.6, w: 6.9, h: 0.4, fontSize: 18, color: C.accent4 });
s.addText([
  { text: "Работу выполнили студенты группы 2ИСИП-925:", options: { color: C.accent4, breakLine: true } },
  { text: "Бачинский И.В., Мельников А.Н., Бахшинян Д.А.", options: { bold: true, breakLine: true } },
  { text: "Проверила: Чеботарева Ю.А.", options: { color: C.accent4 } },
], { isTextBox: true, x: 0.8, y: 5.55, w: 6.6, h: 1.1, margin: 0, fontSize: 14, color: C.background2, valign: "top", paraSpaceAfter: 4 });
s.addShape(pres.shapes.OVAL, { x: 7.75, y: 1.0, w: 5.0, h: 5.0, fill: { color: C.accent4 }, line: { color: C.accent4, width: 0 }, objectName: "mascot circle" });
s.addShape(pres.shapes.OVAL, { x: 7.5, y: 0.75, w: 5.5, h: 5.5, fill: { type: "none" }, line: { color: C.accent2, width: 4 }, objectName: "ring" });
s.addImage({ path: IMG("mascot_front_transparent.png"), x: 7.65, y: 0.95, w: 5.2, h: 5.2, altText: "3D-талисман Кругляш" });
s.addNotes("Тема работы: айдентика для вымышленной компании «Зелёный Круг» — сервиса доставки продуктов в многоразовой стеклянной таре.");

// ---------- 2. Логотип ----------
pres.addSection({ title: "Логотип" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Логотип" });
s.addText("Логотип", { placeholder: "title" });
card(s, 0.6, 1.45, 7.5, 2.75);
s.addImage({ path: IMG("logo_horizontal.png"), x: 0.95, y: 1.75, w: 6.8, h: 6.8 * 438 / 1400, altText: "Горизонтальный логотип" });
card(s, 0.6, 4.45, 3.6, 2.35);
s.addImage({ path: IMG("logo_vertical.png"), x: 1.85, y: 4.6, w: 1.1, h: 1.1 * 1663 / 1400, altText: "Вертикальный логотип" });
txt(s, "вертикальный", { x: 0.6, y: 6.42, w: 3.6, h: 0.3, fontSize: 11, color: C.accent5, align: "center" });
card(s, 4.5, 4.45, 3.6, 2.35, C.text2);
s.addImage({ path: IMG("logo_cream.png"), x: 4.75, y: 5.0, w: 3.1, h: 3.1 * 200 / 640, altText: "Логотип на тёмном фоне" });
txt(s, "на тёмном фоне", { x: 4.5, y: 6.42, w: 3.6, h: 0.3, fontSize: 11, color: C.accent4, align: "center" });
txt(s, "Логотип — визуальное обозначение бренда, по которому компанию узнают с первого взгляда. Наш логотип — комбинированный: знак + шрифтовая часть.",
  { x: 8.5, y: 1.45, w: 4.25, h: 1.2, fontSize: 14, color: C.accent5 });
heading(s, "Концепция знака", { x: 8.5, y: 2.85, w: 4.25 });
bullets(s, [
  "Разомкнутое кольцо — путь тары по кругу: доставили, вернули, помыли, наполнили",
  "Лист вырастает из конца кольца: забота о природе и свежесть продуктов",
  "Внутри — многоразовая банка с круглой этикеткой, главный герой сервиса",
  "Шрифт — Inter Display Black: плотный, дружелюбный, хорошо читается в мелком размере",
], { x: 8.5, y: 3.35, w: 4.25, h: 3.4 });
s.addNotes("Логотип адаптивный: горизонтальная версия для шапки сайта и бланков, вертикальная — для упаковки и квадратных форматов. Все версии сделаны в векторе (SVG), текст переведён в кривые.");

// ---------- 3. Упрощённые и монохромные ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Логотип" });
s.addText("Упрощённые и монохромные версии", { placeholder: "title" });
heading(s, "Значок для сайта и соцсетей", { x: 0.6, y: 1.45, w: 6 });
const icons = [["favicon.png", "Favicon"], ["avatar_social.png", "Аватар соцсетей"], ["icon_color.png", "Знак без текста"]];
icons.forEach(([f, cap], i) => {
  const x = 0.6 + i * 2.25;
  card(s, x, 2.0, 2.0, 2.3);
  s.addImage({ path: IMG(f), x: x + 0.3, y: 2.2, w: 1.4, h: 1.4, altText: cap });
  txt(s, cap, { x, y: 3.8, w: 2.0, h: 0.3, fontSize: 12, color: C.accent5, align: "center" });
});
card(s, 0.6, 4.6, 6.5, 2.15);
txt(s, "Favicon в реальном размере", { x: 0.9, y: 4.8, w: 5.9, h: 0.3, fontSize: 12, color: C.accent5 });
[[48, 0.9], [32, 2.0], [16, 2.85]].forEach(([px, x]) => {
  const inch = px / 48 * 0.7;
  s.addImage({ path: IMG(`favicon_${px}.png`), x, y: 5.35 + (0.7 - inch) / 2, w: inch, h: inch, altText: `favicon ${px}px` });
  txt(s, `${px}px`, { x: x - 0.1, y: 6.2, w: inch + 0.2, h: 0.3, fontSize: 11, color: C.accent5, align: "center" });
});
txt(s, "Упрощённый знак без мелких деталей (этикетки и блика) остаётся узнаваемым даже на вкладке браузера.",
  { x: 3.6, y: 5.25, w: 3.25, h: 1.2, fontSize: 12, color: C.text1 });
heading(s, "Монохром для печати", { x: 7.5, y: 1.45, w: 5 });
card(s, 7.5, 2.0, 5.25, 2.3, "FFFFFF");
s.addImage({ path: IMG("logo_mono_black.png"), x: 7.75, y: 2.35, w: 4.75, h: 4.75 * 438 / 1400, altText: "Чёрный монохромный логотип" });
card(s, 7.5, 4.6, 5.25, 2.15, "000000");
s.addImage({ path: IMG("logo_mono_white.png"), x: 7.75, y: 4.9, w: 4.75, h: 4.75 * 438 / 1400, altText: "Белый монохромный логотип" });
s.addNotes("Монохромные версии — для печати в одну краску, штампов, гравировки на крышках банок.");

// ---------- 4. Палитра ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Логотип" });
s.addText("Концепция и выбор цветовой палитры", { placeholder: "title" });
const pal = [
  ["1F5136", "Хвойный", "#1F5136", "F6F1E4", "Основной цвет бренда. Природа, надёжность и спокойствие. Фоны, логотип, текст заголовков."],
  ["5DBB63", "Свежая зелень", "#5DBB63", "14271C", "Свежесть продуктов и рост. Лист в знаке, крышки банок, иконки, акценты интерфейса."],
  ["F6F1E4", "Льняной", "#F6F1E4", "14271C", "Натуральные материалы: лён, крафт, стекло. Светлые фоны сайта, этикетки, бланки."],
  ["F4A93B", "Тыквенный", "#F4A93B", "14271C", "Тёплый акцент: аппетит и энергия. Кнопки призыва к действию, бейджи, промо."],
];
pal.forEach(([hex, name, code, tc, desc], i) => {
  const x = 0.6 + i * 3.1;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.5, w: 2.85, h: 2.6, rectRadius: 0.22, fill: { color: hex }, line: { color: hex === "F6F1E4" ? "DCD5C2" : hex, width: 1 }, shadow: shadow(), objectName: name });
  txt(s, name, { x: x + 0.25, y: 3.2, w: 2.4, h: 0.4, fontSize: 18, bold: true, color: tc });
  txt(s, code, { x: x + 0.25, y: 3.6, w: 2.4, h: 0.3, fontSize: 13, color: tc });
  txt(s, desc, { x, y: 4.35, w: 2.85, h: 1.3, fontSize: 13, color: C.text1 });
});
card(s, 0.6, 5.85, 12.15, 0.95, C.accent4);
txt(s, "Пропорция в макетах: ~60% льняной и белый, ~30% хвойный, ~10% зелень и тыквенный. Тёмно-зелёный и льняной дают контраст 9:1 — текст читается легко.",
  { x: 0.9, y: 6.0, w: 11.6, h: 0.65, fontSize: 14, color: C.text2, valign: "middle" });
s.addNotes("Палитра из четырёх цветов: два зелёных — природа и свежесть, льняной — натуральные материалы, тыквенный — тёплый акцент для кнопок.");

// ---------- 5. Талисман ----------
pres.addSection({ title: "Талисман" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Талисман" });
s.addText("Талисман — 3D-персонаж Кругляш", { placeholder: "title" });
s.addImage({ path: IMG("mascot_hero.jpg"), x: 0.6, y: 1.35, w: 5.45, h: 5.45, altText: "3D-рендер талисмана Кругляша" });
txt(s, "Талисман — персонаж, который олицетворяет компанию: делает бренд «живым», вызывает эмоции и помогает его запомнить.",
  { x: 6.45, y: 1.4, w: 6.3, h: 0.75, fontSize: 13, color: C.accent5 });
heading(s, "Имя: Кругляш", { x: 6.45, y: 2.3, w: 4 });
bullets(s, [
  "Характер: добродушный и хозяйственный. Помнит каждую банку «в лицо» и радуется, когда она возвращается домой",
  "Образ: стеклянная банка с зелёной крышкой, на которой вырос росток — у вещи началась новая жизнь",
  "Связь с брендом: Кругляш сам прошёл по кругу десятки раз, поэтому он живое доказательство, что многоразовая тара работает",
], { x: 6.45, y: 2.75, w: 4.05, h: 3.6, fontSize: 13 });
s.addImage({ path: IMG("gif_3d_povorot.gif"), x: 10.75, y: 2.4, w: 2.0, h: 2.0, altText: "Анимация поворота 3D-модели" });
txt(s, "3D-модель со всех сторон", { x: 10.6, y: 4.5, w: 2.3, h: 0.5, fontSize: 11, color: C.accent5, align: "center" });
txt(s, "Модель собрана из базовых форм со сглаживанием: скруглённые цилиндры, эллипсоиды, капсулы.", { x: 10.6, y: 5.0, w: 2.3, h: 1.4, fontSize: 11, color: C.accent5, align: "center" });
s.addNotes("Цель — не реализм, а узнаваемость и шарм. Персонаж повторяет форму банки из логотипа, поэтому связан с фирменным стилем.");

// ---------- 6. Мудборд ----------
pres.addSection({ title: "Сайт" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Сайт" });
s.addText("Мудборд", { placeholder: "title" });
s.addImage({ path: IMG("moodboard.jpg"), x: 0.6, y: 1.35, w: 8.8, h: 5.5, altText: "Мудборд бренда" });
heading(s, "Настроение", { x: 9.8, y: 1.4, w: 3 });
bullets(s, ["Свежо, честно, по-соседски", "Натуральные фактуры: стекло, лён, крафт", "Плоские иллюстрации с тёмным контуром", "Мягкий 3D для персонажа", "Много воздуха, крупные скругления"],
  { x: 9.8, y: 1.85, w: 2.95, h: 3.6, fontSize: 13 });
s.addNotes("Мудборд задаёт визуальное направление сайта до начала вёрстки.");

// ---------- 7. UI Kit ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Сайт" });
s.addText("Стилевое руководство (UI Kit)", { placeholder: "title" });
s.addImage({ path: IMG("uikit.jpg"), x: 0.6, y: 1.35, w: 6.85, h: 6.85 * 1284 / 1600, altText: "UI Kit" });
heading(s, "Что входит", { x: 7.85, y: 1.4, w: 4.9 });
bullets(s, [
  "Цвета с HEX-кодами и ролями",
  "Типографика: H1–H3, основной текст и подписи",
  "Кнопки: основная, акцентная, вторичная, текстовая, иконка; состояния default / hover / disabled",
  "Поля ввода: обычное, в фокусе, с ошибкой, поиск",
  "Чипы, теги, переключатели, чекбоксы, счётчик количества, уведомление",
  "Карточка товара и набор иконок",
], { x: 7.85, y: 1.85, w: 4.9, h: 3.8, fontSize: 14 });
card(s, 7.85, 5.7, 4.9, 1.1, C.accent4);
txt(s, "Все кнопки — «таблетки» со скруглением 999px: форма повторяет круг из логотипа.", { x: 8.1, y: 5.8, w: 4.4, h: 0.9, fontSize: 13, color: C.text2, valign: "middle" });

// ---------- 8. Главная страница desktop ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Сайт" });
s.addText("Главная страница сайта — Desktop 1440 px", { placeholder: "title" });
s.addImage({ path: IMG("site_a.jpg"), x: 0.6, y: 1.35, w: 4.5, h: 4.5 * 1800 / 1440, altText: "Главная страница, верхняя часть" });
s.addImage({ path: IMG("site_b.jpg"), x: 5.3, y: 1.35, w: 4.5 * 1440 / 1440, h: 4.5 * 1752 / 1440, altText: "Главная страница, нижняя часть" });
heading(s, "Структура страницы", { x: 10.15, y: 1.4, w: 2.6 });
s.addText([
  "Шапка: логотип, меню, поиск, корзина",
  "Первый экран: оффер, 2 кнопки, 3D-талисман",
  "«Как это работает» — 4 шага",
  "Каталог с фильтрами-чипами",
  "Блок «Наш круг» с цифрами",
  "Подписка на рассылку",
  "Подвал с контактами",
].map((t, i, a) => ({ text: t, options: { bullet: { indent: 14 }, breakLine: i < a.length - 1 } })),
  { isTextBox: true, x: 10.15, y: 1.85, w: 2.6, h: 4.6, margin: 0, fontSize: 13, color: C.text1, valign: "top", paraSpaceAfter: 8 });
s.addNotes("Макет главной страницы для экрана 1440 px. Страница длинная, поэтому показана двумя частями: слева верх, справа низ.");

// ---------- 9. Мобильная версия ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Сайт" });
s.addText("Адаптация под мобильную версию — 390 px", { placeholder: "title" });
const phW = 2.75, phH = phW * 920 / 466;
s.addImage({ path: IMG("phone1.png"), x: 0.9, y: 1.3, w: phW, h: phH, altText: "Мобильная версия: первый экран" });
s.addImage({ path: IMG("phone2.png"), x: 4.0, y: 1.3, w: phW, h: phH, altText: "Мобильная версия: как это работает" });
heading(s, "Что изменилось на мобильном", { x: 7.4, y: 1.45, w: 5.3 });
bullets(s, [
  "Меню спрятано в «бургер», поиск — в иконку",
  "Заголовок уменьшен с 76 до 42 px, текст сокращён",
  "Кнопки растянуты на всю ширину — по ним легко попасть пальцем",
  "Талисман встал между заголовком и текстом, чтобы первый экран оставался ярким",
  "Цифры собраны в одну компактную плашку",
  "Шаги «Как это работает» — вертикальным списком",
  "Снизу таб-бар с основными разделами",
], { x: 7.4, y: 1.95, w: 5.3, h: 4.8, fontSize: 14 });

// ---------- 10. Видео ----------
pres.addSection({ title: "Медиа" });
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Медиа" });
s.addText("Рекламный видеоролик · 24 секунды", { placeholder: "title" });
s.addMedia({ type: "video", path: VIDEO, x: 0.6, y: 1.45, w: 8.0, h: 4.5, cover: "data:image/jpeg;base64," + fs.readFileSync(IMG("poster.jpg")).toString("base64") });
txt(s, "Нажмите на видео, чтобы воспроизвести · 1920×1080, со звуком", { x: 0.6, y: 6.1, w: 8, h: 0.3, fontSize: 11, color: C.accent4 });
heading(s, "Раскадровка", { x: 9.0, y: 1.45, w: 3.8, color: C.background2 });
const scenes = [
  ["0–4 с", "Кольцо рисуется, вырастает лист, падает банка: собирается логотип"],
  ["4–9 с", "«Продукты в стекле. Без пластика» и фирменные иллюстрации"],
  ["9–14 с", "Кругляш машет и знакомится со зрителем"],
  ["14–20 с", "Схема «Заказ → Доставка → Возврат → Мойка»"],
  ["20–24 с", "Логотип, сайт и промо «−10% на первый заказ»"],
];
scenes.forEach(([t, d], i) => {
  const y = 1.95 + i * 0.9;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.0, y, w: 0.95, h: 0.42, rectRadius: 0.21, fill: { color: C.accent2 }, line: { color: C.accent2, width: 0 }, objectName: "time " + t });
  txt(s, t, { x: 9.0, y, w: 0.95, h: 0.42, fontSize: 11, bold: true, color: C.text1, align: "center", valign: "middle" });
  txt(s, d, { x: 10.1, y: y - 0.02, w: 2.7, h: 0.85, fontSize: 12, color: C.background2 });
});
txt(s, "Переходы между сценами — круговая шторка (мотив круга). Музыка — короткий акустический луп.", { x: 0.6, y: 6.45, w: 8, h: 0.4, fontSize: 11, color: C.accent4 });

// ---------- 11. Гифки и стикеры ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Медиа" });
s.addText("Гифки и стикеры для соцсетей", { placeholder: "title" });
const gifs = ["gif_privet.gif", "gif_splyu.gif", "gif_lyublyu.gif", "gif_krug.gif"];
gifs.forEach((g, i) => s.addImage({ path: IMG(g), x: 0.6 + i * 2.15, y: 1.35, w: 1.95, h: 2.6, altText: "Анимированный стикер " + (i + 1) }));
s.addImage({ path: IMG("gif_3d_povorot.gif"), x: 9.25, y: 1.35, w: 2.6, h: 2.6, altText: "3D-гифка талисмана" });
txt(s, "GIF-анимации: привет · сплю · люблю · тара по кругу · 3D-поворот", { x: 0.6, y: 4.05, w: 11, h: 0.3, fontSize: 12, color: C.accent5 });
const st = ["sticker_privet.png", "sticker_nyam.png", "sticker_lyublyu.png", "sticker_vozvrat.png", "sticker_splyu.png", "sticker_wow.png"];
st.forEach((f, i) => s.addImage({ path: IMG(f), x: 0.55 + i * 2.05, y: 4.35, w: 2.1, h: 2.1, altText: "Стикер " + (i + 1) }));
txt(s, "Стикерпак для Telegram и ВКонтакте: PNG 512×512 с белой обводкой", { x: 0.6, y: 6.5, w: 11, h: 0.3, fontSize: 12, color: C.accent5 });

// ---------- 12. Мокапы ----------
pres.addSection({ title: "Мокапы и дополнительно" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Мокапы и дополнительно" });
s.addText("Мокапы: фирменный бланк и визитка", { placeholder: "title" });
s.addImage({ path: IMG("mockup_stationery.jpg"), x: 0.6, y: 1.35, w: 7.6, h: 4.75, altText: "Мокап бланка и визиток" });
s.addImage({ path: IMG("mockup_cards.jpg"), x: 8.5, y: 1.35, w: 4.25, h: 4.25 * 1200 / 1800, altText: "Мокап визиток" });
txt(s, "Бланк A4: логотип и контакты в шапке, крупный знак-водяной знак, нижний колонтитул с паттерном.", { x: 0.6, y: 6.25, w: 7.6, h: 0.6, fontSize: 13 });
txt(s, "Визитка 90×50 мм: лицевая сторона — знак на фоне паттерна, оборот — контакты на льняном фоне.", { x: 8.5, y: 4.3, w: 4.25, h: 1.0, fontSize: 13 });
card(s, 8.5, 5.45, 4.25, 1.35, C.accent4);
txt(s, "Обе стороны визитки и бланк сделаны в векторе и готовы к печати.", { x: 8.75, y: 5.55, w: 3.8, h: 1.15, fontSize: 13, color: C.text2, valign: "middle" });

// ---------- 13. Упаковка ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Мокапы и дополнительно" });
s.addText("Дополнительно: дизайн упаковки в 3D", { placeholder: "title" });
s.addImage({ path: IMG("pack_3d.jpg"), x: 0.6, y: 1.35, w: 8.0, h: 4.5, altText: "3D-рендер упаковки" });
txt(s, "Банки с этикетками и крафтовая коробка доставки. Этикетка натянута на 3D-цилиндр как текстура.", { x: 0.6, y: 6.0, w: 8, h: 0.7, fontSize: 13 });
heading(s, "Развёртки этикеток", { x: 9.0, y: 1.4, w: 3.8 });
["label_jar_grechka.png", "label_jar_ovsyanka.png", "label_jar_mindal.png"].forEach((f, i) =>
  s.addImage({ path: IMG(f), x: 9.0, y: 1.9 + i * 0.8, w: 3.75, h: 3.75 / 6, altText: "Этикетка " + (i + 1) }));
s.addImage({ path: IMG("box_front.png"), x: 9.0, y: 4.35, w: 2.3, h: 2.3 * 560 / 800, altText: "Печать на коробке" });
txt(s, "Сзади на этикетке — «Верни банку, получи бонус»", { x: 11.45, y: 4.4, w: 1.35, h: 1.6, fontSize: 11, color: C.accent5 });

// ---------- 14. Паттерны ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Мокапы и дополнительно" });
s.addText("Дополнительно: фирменные паттерны", { placeholder: "title" });
s.addImage({ path: IMG("pattern_preview.png"), x: 0.6, y: 1.35, w: 5.9, h: 5.9 * 9 / 16, altText: "Светлый паттерн" });
s.addImage({ path: IMG("pattern_dark_preview.png"), x: 6.85, y: 1.35, w: 5.9, h: 5.9 * 9 / 16, altText: "Тёмный паттерн" });
s.addImage({ path: IMG("pattern_tile.png"), x: 0.6, y: 4.95, w: 1.85, h: 1.85, altText: "Раппорт паттерна" });
txt(s, "Раппорт (повторяющийся фрагмент) собран из элементов логотипа: знак, лист, кольцо, точки-зёрна.", { x: 2.75, y: 5.0, w: 4.4, h: 0.9, fontSize: 13 });
heading(s, "Где используется", { x: 7.5, y: 4.95, w: 5 });
bullets(s, ["Фон блоков на сайте и в ролике", "Лицевая сторона визитки, колонтитул бланка", "Тишью-бумага и скотч для коробок доставки"], { x: 7.5, y: 5.4, w: 5.25, h: 1.4, fontSize: 13 });

// ---------- 15. Иллюстрации ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Мокапы и дополнительно" });
s.addText("Дополнительно: фирменные иллюстрации", { placeholder: "title" });
const ills = [["ill_jars.png", 800, 760, "Крупы в банках"], ["ill_milk.png", 800, 760, "Молоко в стекле"], ["ill_bag.png", 800, 760, "Эко-сумка"], ["ill_courier.png", 880, 720, "Курьер на велосипеде"]];
ills.forEach(([f, pw, ph, cap], i) => {
  const x = 0.6 + i * 3.1;
  card(s, x, 1.4, 2.85, 3.15);
  const d = fitImg(f, pw, ph, 2.5, 2.4);
  s.addImage({ path: IMG(f), x: x + (2.85 - d.w) / 2, y: 1.55 + (2.4 - d.h) / 2, w: d.w, h: d.h, altText: cap });
  txt(s, cap, { x, y: 4.05, w: 2.85, h: 0.3, fontSize: 12, color: C.accent5, align: "center" });
});
heading(s, "Иконки «Как это работает»", { x: 0.6, y: 4.85, w: 5 });
["icon_order.png", "icon_deliver.png", "icon_return.png", "icon_wash.png"].forEach((f, i) => {
  s.addShape(pres.shapes.OVAL, { x: 0.6 + i * 1.45, y: 5.35, w: 1.25, h: 1.25, fill: { color: C.background1 }, line: { color: C.background1, width: 0 }, objectName: "icon circle" });
  s.addImage({ path: IMG(f), x: 0.75 + i * 1.45, y: 5.5, w: 0.95, h: 0.95, altText: "Иконка" });
});
txt(s, "Единый приём: плоская заливка из палитры, тёмно-зелёный контур одной толщины, мягкое пятно-подложка. Иллюстрации используются на сайте, в рекламе и соцсетях.",
  { x: 6.6, y: 5.35, w: 6.15, h: 1.3, fontSize: 13 });

// ---------- 16. Финал ----------
pres.addSection({ title: "Финал" });
s = pres.addSlide({ masterName: "COVER", sectionTitle: "Финал" });
txt(s, "Спасибо за внимание!", { x: 0.8, y: 2.4, w: 7.5, h: 1.0, fontSize: 48, bold: true, color: C.background2 });
txt(s, "Тара едет по кругу — присоединяйтесь", { x: 0.8, y: 3.45, w: 7.5, h: 0.5, fontSize: 20, color: C.accent4 });
s.addImage({ path: IMG("logo_cream.png"), x: 0.8, y: 5.3, w: 3.6, h: 3.6 * 200 / 640, altText: "Логотип" });
s.addImage({ path: IMG("gif_privet.gif"), x: 8.9, y: 1.0, w: 3.6, h: 4.8, altText: "Кругляш машет" });

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
