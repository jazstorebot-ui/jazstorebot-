import os
import asyncio
import subprocess
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ====== 🔧 ТАНЗИМ ======
BOT_TOKEN = "8550449462:AAHozKMKDtayXrK5XuADce-miEM_RAHszyw"
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

SUPPORTED_FORMATS = ["mp4", "avi", "mkv", "mov", "flv", "ts", "webm"]

# ====== 🚀 ФУНКСИЯҲО ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎬 Табдил додани видео", callback_data="convert")],
        [InlineKeyboardButton("ℹ️ Маълумот", callback_data="info")],
    ]
    await update.message.reply_text(
        "👋 Салом! Ман *Video Converter Bot* ҳастам.\n\n"
        "🎥 Ман метавонам файлҳои видеоро ба форматҳои гуногун табдил диҳам.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "convert":
        await query.message.reply_text("📤 Лутфан видеоро фирист, ки мехоҳӣ табдил диҳам.")
    elif query.data == "info":
        await query.message.reply_text(
            "ℹ️ *Маълумот дар бораи бот:*\n\n"
            "🎯 Форматҳои дастгиришаванда:\n"
            "`" + ", ".join(SUPPORTED_FORMATS).upper() + "`\n\n"
            "💡 Танҳо видеоро фирист ва форматро интихоб кун.",
            parse_mode="Markdown",
        )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document
    if not video:
        await update.message.reply_text("😕 Файли видео ёфт нашуд.")
        return

    # Санҷиши андоза
    if video.file_size > 100 * 1024 * 1024:
        await update.message.reply_text("⚠️ Файл аз 100MB зиёд аст. Лутфан видеои хурдтар фирист.")
        return

    # Боргирӣ
    msg = await update.message.reply_text("⬇️ Боргирии видео...")
    file = await context.bot.get_file(video.file_id)
    input_path = os.path.join(DOWNLOAD_DIR, video.file_name or "input_video")
    await file.download_to_drive(input_path)
    await msg.edit_text("✅ Видео боргирӣ шуд!")

    # Менюи форматҳо
    keyboard = [
        [InlineKeyboardButton(fmt.upper(), callback_data=f"format_{fmt}")]
        for fmt in SUPPORTED_FORMATS
    ]
    await update.message.reply_text(
        f"🎞 Файли гирифташуда: `{os.path.basename(input_path)}`\n\n"
        "Формати баромадро интихоб кун 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    context.user_data["input_path"] = input_path


async def format_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    fmt = query.data.replace("format_", "")
    input_path = context.user_data.get("input_path")

    if not input_path or not os.path.exists(input_path):
        await query.message.reply_text("❌ Файл ёфт нашуд. Аз аввал видеоро фирист.")
        return

    output_path = os.path.splitext(input_path)[0] + f".{fmt}"

    msg = await query.message.reply_text(f"⚙️ Табдилдиҳӣ оғоз шуд ба формат `{fmt.upper()}` ...", parse_mode="Markdown")

    # Иҷрои FFmpeg
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k", output_path,
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    _, stderr = await process.communicate()

    if process.returncode == 0 and os.path.exists(output_path):
        await msg.edit_text("✅ Табдилдиҳӣ анҷом ёфт! Файли тайёр ⬇️")
        await query.message.reply_video(video=open(output_path, "rb"))
        os.remove(input_path)
        os.remove(output_path)
    else:
        await msg.edit_text(
            "⚠️ Хатогӣ ҳангоми табдилдиҳӣ:\n\n"
            f"```\n{stderr.decode()[-400:]}\n```",
            parse_mode="Markdown",
        )

# ====== 🔄 ОҒОЗИ БОТ ======

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(convert|info)$"))
    app.add_handler(CallbackQueryHandler(format_selected, pattern="^format_"))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    print("🤖 Бот фаъол шуд!")
    app.run_polling()

if __name__ == "__main__":
    main()
