from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===========================
#       BOOK DATA (TEXT)
# ===========================

# Дар ин ҷо матни китобҳоро ворид мекунед.
# Барои мисол, ман дар ҳар синф "Саҳифаи X" навиштам.
# Шумо метавонед ба ҷои он матни китобро гузоред.

books = {
    "class5": {
        "title": "Адабиёти синфи 5",
        "pages": ["АДАБИЁТИ ШИФОҲИ ФАРҚИ АДАБИЁТИ ШИФОҲИ АЗ КИТОБИ Адабиёти бадей асосан ду навъ мешавад: а) адабиёти шифоҳӣ; б) адабиёти китобӣ. Дар чомеа аввал адабиёти шифоҳӣ, яъне фолклор замонҳое, ки ҳанӯз хат вучуд надошт, пайдо шуда буд. Одамон гаму шодӣ, орзую омоли хешро даҳонӣ, бадоҳатан дар наклу ривоятҳо, афсонаю асотирҳо, суруду таронаҳо баён мекарданд. Ин гуфтаҳо аз авлод ба авлод, аз насл ба насл, аз аср ба аср гузашта такмил меёфтанд ва оҳиста-оҳиста жанру намудхои адабиёти шифоҳӣ шакл мегирифтанд. Баробари пайдоиши хат адабиёти китобӣ ҳам оғоз меёбад. Ва ашхоси босавод адабиёти шифохиро ҷамъ намуда ба шакли китоб омода месозанд. Бештари асарҳои халкӣ бо ҳамин роху восита то замони мо омада расидаанд. Адабиёти шифоҳӣ моли халқ аст. Яъне, сохиби наклу ривоят, афсона, суруду таронаҳо мову шумо ҳастем. Имрӯз низ халқ асар эҷод мекунад ва эҷодиёти онҳо дар маҷмӯаҳои дастҷамъй ба табъ мерасанд. Адабиёти китобӣ эҷоди ашхоси муайянанд, ки дар замону макони мушаххас зиндагӣ карда, асар эчод намудаанд. Масалан, устод Рӯдакиро гирем. У дар соли 858 ба дунё омада, соли 941 вафот кардааст. Ва ў қасидаи "Шикоят аз пири", "Модари май" ва асарҳои дигарро офаридааст. Ин андешаро нисбати Восеъ ва нақлу ривоят ва суруду таронаҳое, ки дар ҳаққи ў гуфта шудаанд, баён карда наметавонем. Зеро наклу ривоят ва суруду таронаҳоро шахсони номаълум, яъне халқ эъҷод кардааст. Адабиёти шифоҳӣ аз лиҳози забон ва тарзи баён ҳам аз адабиёти китобӣ фарқ мекунад. Забони асарҳои халкӣ сода, фаҳмо буда, мардум онро зуд қабул мекунанд. Ибораорой, истифодаи калимаю ибораҳои душворфаҳм ва бегона дар онҳо дида намешавад, вале дар адабиёти китобӣ зиёдтар ба назар мерасад. "]
    },
    "class6": {
        "title": "Адабиёти синфи 6",
        "pages": ["Саҳифаи 1 " ]
    },
    "class7": {
        "title": "Адабиёти синфи 7",
        "pages": ["Саҳифаи " + str(i) for i in range(1, 4001)]
    },
    "class8": {
        "title": "Адабиёти синфи 8",
        "pages": ["Саҳифаи " + str(i) for i in range(1, 4001)]
    },
    "class9": {
        "title": "Адабиёти синфи 9",
        "pages": ["Саҳифаи " + str(i) for i in range(1, 4001)]
    },
    "class10": {
        "title": "Адабиёти синфи 10",
        "pages": ["Саҳифаи " + str(i) for i in range(1, 4001)]
    },
    "class11": {
        "title": "Адабиёти синфи 11",
        "pages": ["Саҳифаи " + str(i) for i in range(1, 4001)]
    }
}

# ===========================
#       START MENU
# ===========================

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📘 Синфи 5", callback_data="open_class5")],
        [InlineKeyboardButton("📘 Синфи 6", callback_data="open_class6")],
        [InlineKeyboardButton("📘 Синфи 7", callback_data="open_class7")],
        [InlineKeyboardButton("📘 Синфи 8", callback_data="open_class8")],
        [InlineKeyboardButton("📘 Синфи 9", callback_data="open_class9")],
        [InlineKeyboardButton("📘 Синфи 10", callback_data="open_class10")],
        [InlineKeyboardButton("📘 Синфи 11", callback_data="open_class11")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Китобхонаи электронӣ*\nСинфи худро интихоб кунед:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# ===========================
#       PAGE HANDLER
# ===========================

async def open_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    book_id = query.data.replace("open_", "")
    context.user_data["book_id"] = book_id
    context.user_data["page"] = 0

    await show_page(query, context)


async def show_page(query, context):
    book_id = context.user_data["book_id"]
    page = context.user_data["page"]

    book = books[book_id]
    total_pages = len(book["pages"])

    text = f"📖 *{book['title']}*\n\n"
    text += book["pages"][page]

    keyboard = [
        [
            InlineKeyboardButton("⬅️", callback_data="prev") if page > 0 else InlineKeyboardButton(" ", callback_data="none"),
            InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="none"),
            InlineKeyboardButton("➡️", callback_data="next") if page < total_pages - 1 else InlineKeyboardButton(" ", callback_data="none")
        ],
        [InlineKeyboardButton("🔙 Бозгашт", callback_data="back_to_menu")]
    ]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ===========================
#    CALLBACKS FOR BUTTONS
# ===========================

async def callback_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "next":
        context.user_data["page"] += 1
        await show_page(query, context)
    elif query.data == "prev":
        context.user_data["page"] -= 1
        await show_page(query, context)
    elif query.data == "back_to_menu":
        await query.edit_message_text(
            "📚 *Китобхонаи электронӣ*\nСинфи худро интихоб кунед:",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    else:
        await open_book(update, context)

# ===========================
#        BOT RUN
# ===========================

TOKEN = "8280566276:AAHQjwIexpzVqeBVKpZZPdZvKFhYEu4-EN0"  # TOKEN-и худро гузоред

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(callback_buttons))

app.run_polling()
