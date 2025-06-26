# climate_discord_bot.py
# Bot de Discord sobre cambio climático
# Realizado por [Tu Nombre]
# Fecha: [Pon la fecha aquí]

import discord
from discord.ext import commands, tasks
import random
import asyncio
import datetime

# Prefijo para los comandos, ejemplo: !hola, !clima, etc.
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Necesario para leer el contenido de los mensajes

# Creamos la instancia del bot
bot = commands.Bot(command_prefix="!", intents=intents, description="Bot educativo sobre cambio climático")

# Lista de tips ecológicos para el comando !tip y otros usos
eco_tips = [
    "Apaga las luces cuando no las necesites para ahorrar energía.",
    "Reduce el consumo de agua cerrando la llave mientras te cepillas los dientes.",
    "Recicla y reutiliza envases siempre que puedas.",
    "Usa el transporte público o bicicleta en vez de coche para reducir emisiones.",
    "Planta un árbol, ayuda a limpiar el aire y da sombra.",
    "Prefiere productos locales para disminuir la huella de carbono.",
    "Evita el uso de plásticos de un solo uso.",
    "Desconecta los aparatos eléctricos que no utilices.",
    "Apoya campañas de limpieza en tu comunidad.",
    "Utiliza focos LED en lugar de incandescentes.",
    "Compra ropa de segunda mano para reducir la huella textil.",
    "Evita el desperdicio de alimentos aprovechando sobras.",
    "Utiliza bolsas reutilizables en vez de bolsas plásticas.",
    "Consume menos carne y más productos vegetales.",
    "Ahorra papel utilizando medios digitales.",
    "Comparte el auto siempre que puedas.",
    "Apoya energías limpias y renovables.",
    "Cuida los ecosistemas locales.",
    "Educa a otros sobre la importancia del medio ambiente.",
    "No tires basura en la calle ni en ríos o lagos.",
    "Aprovecha la luz natural durante el día.",
    "Cierra cortinas por la noche para conservar el calor.",
    "Lava la ropa con agua fría siempre que sea posible.",
    "No dejes cargadores conectados si no los usas.",
    "Separa residuos orgánicos de los inorgánicos.",
    "Haz composta con tus desechos orgánicos.",
    "Repara objetos antes de desecharlos.",
    "No compres productos con exceso de embalaje.",
    "Participa en reforestaciones locales."
]

# Lista de noticias simuladas para el comando !noticia
noticias = [
    {
        "titulo": "Récord de temperatura global en 2025",
        "contenido": "El año 2025 ha registrado el año más cálido desde que se tienen registros.",
        "url": "https://ejemplo.com/noticia-temperatura"
    },
    {
        "titulo": "Nuevo informe del IPCC alerta sobre el deshielo",
        "contenido": "El deshielo en el Ártico avanza más rápido de lo esperado según el nuevo informe del IPCC.",
        "url": "https://ejemplo.com/noticia-ipcc"
    },
    {
        "titulo": "Innovaciones en energías renovables",
        "contenido": "Científicos desarrollan paneles solares más eficientes y económicos.",
        "url": "https://ejemplo.com/noticia-renovables"
    },
    {
        "titulo": "Ciudades implementan transporte eléctrico",
        "contenido": "Más ciudades adoptan autobuses eléctricos para reducir la contaminación urbana.",
        "url": "https://ejemplo.com/noticia-transporte"
    },
    {
        "titulo": "Nuevas reservas naturales en América Latina",
        "contenido": "Latinoamérica crea nuevas áreas protegidas para conservar la biodiversidad.",
        "url": "https://ejemplo.com/noticia-reservas"
    },
    {
        "titulo": "Prohibición mundial de plásticos de un solo uso",
        "contenido": "Más de 50 países se unen para prohibir los plásticos de un solo uso.",
        "url": "https://ejemplo.com/noticia-plasticos"
    },
    {
        "titulo": "Aumento de energías limpias en la matriz global",
        "contenido": "Las energías solar y eólica alcanzan un nuevo récord de producción.",
        "url": "https://ejemplo.com/noticia-energias"
    }
]

# Glosario de términos de cambio climático
glosario = {
    "efecto invernadero": "Fenómeno natural por el cual ciertos gases en la atmósfera retienen el calor y mantienen la temperatura de la Tierra.",
    "huella de carbono": "Cantidad total de gases de efecto invernadero emitidos directa o indirectamente por una persona, organización, evento o producto.",
    "deshielo": "Derretimiento de masas de hielo, como polos y glaciares, causado principalmente por el aumento de la temperatura global.",
    "IPCC": "Panel Intergubernamental sobre Cambio Climático, organismo científico internacional que evalúa el cambio climático.",
    "emisiones": "Liberación de gases contaminantes a la atmósfera, principalmente dióxido de carbono (CO2), metano (CH4) y óxidos de nitrógeno (NOx).",
    "energía renovable": "Energía obtenida de fuentes naturales, virtualmente inagotables, como el sol, el viento y el agua.",
    "deforestación": "Tala o destrucción de bosques y selvas, generalmente causada por actividades humanas.",
    "biodegradable": "Material que puede descomponerse de manera natural por la acción de organismos vivos.",
    "compostaje": "Proceso biológico de descomposición de materia orgánica para obtener abono natural.",
    "calentamiento global": "Aumento sostenido de la temperatura media global de la Tierra debido a la actividad humana."
}

# Frases motivacionales o inspiradoras para el comando !frase
frases = [
    "El planeta no es una herencia de nuestros padres, sino un préstamo de nuestros hijos.",
    "Pequeñas acciones, grandes cambios.",
    "El cambio empieza en ti.",
    "Cuidar la naturaleza es cuidar la vida.",
    "No heredamos la Tierra de nuestros antepasados, la tomamos prestada de nuestros hijos.",
    "El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor momento es ahora.",
    "Cada acción cuenta en la lucha contra el cambio climático.",
    "Si cuidas el planeta, el planeta cuidará de ti.",
    "Aún estamos a tiempo de hacer la diferencia.",
    "No hay Planeta B."
]

# ---------------------- PREGUNTAS Y RESPUESTAS OPCIÓN MÚLTIPLE ----------------------

quiz_questions = [
    {
        "pregunta": "¿Qué es el efecto invernadero?",
        "opciones": [
            "a) Un tipo de planta tropical.",
            "b) El calentamiento de la Tierra por la acumulación de gases que retienen el calor.",
            "c) Un edificio de cristal para plantas."
        ],
        "correcta": "b"
    },
    {
        "pregunta": "¿Cuál es el gas de efecto invernadero más abundante producido por el ser humano?",
        "opciones": [
            "a) Vapor de agua",
            "b) Metano",
            "c) Dióxido de carbono"
        ],
        "correcta": "c"
    },
    {
        "pregunta": "¿Qué sector contribuye más a las emisiones de gases de efecto invernadero?",
        "opciones": [
            "a) Agricultura",
            "b) Generación de energía",
            "c) Transporte"
        ],
        "correcta": "b"
    },
    {
        "pregunta": "¿Qué año se considera el más cálido registrado hasta ahora?",
        "opciones": [
            "a) 2016",
            "b) 2020",
            "c) 1998"
        ],
        "correcta": "a"
    },
    {
        "pregunta": "¿Qué organismo internacional publica informes sobre cambio climático?",
        "opciones": [
            "a) OMS",
            "b) IPCC",
            "c) ONUDI"
        ],
        "correcta": "b"
    },
    {
        "pregunta": "¿Cuál es la principal causa del aumento del nivel del mar?",
        "opciones": [
            "a) Terremotos",
            "b) El deshielo de los polos y glaciares",
            "c) Erupciones volcánicas"
        ],
        "correcta": "b"
    },
    {
        "pregunta": "¿Cómo podemos reducir nuestra huella de carbono?",
        "opciones": [
            "a) Usando energías renovables",
            "b) Usando más autos",
            "c) Talando bosques"
        ],
        "correcta": "a"
    },
    {
        "pregunta": "¿Qué es la deforestación?",
        "opciones": [
            "a) La tala masiva de árboles en los bosques",
            "b) La plantación de nuevos árboles",
            "c) El reciclaje de papel"
        ],
        "correcta": "a"
    },
    {
        "pregunta": "¿Qué acuerdo internacional busca limitar el calentamiento global a menos de 2°C?",
        "opciones": [
            "a) Protocolo de Montreal",
            "b) Acuerdo de París",
            "c) Convenio de Basilea"
        ],
        "correcta": "b"
    },
    {
        "pregunta": "¿Qué animal polar está en peligro por el deshielo?",
        "opciones": [
            "a) El pingüino emperador",
            "b) El oso polar",
            "c) El lobo ártico"
        ],
        "correcta": "b"
    },
    {
        "pregunta": "¿Qué es una energía renovable?",
        "opciones": [
            "a) Una fuente de energía que se obtiene de recursos naturales inagotables",
            "b) Una energía creada por combustibles fósiles",
            "c) Energía proveniente de baterías desechables"
        ],
        "correcta": "a"
    },
    {
        "pregunta": "¿Cuál es el principal efecto del aumento de CO2 en la atmósfera?",
        "opciones": [
            "a) El calentamiento global",
            "b) La lluvia ácida",
            "c) La reducción del oxígeno"
        ],
        "correcta": "a"
    },
    {
        "pregunta": "¿Qué podemos hacer para ahorrar agua?",
        "opciones": [
            "a) Dejar la llave abierta mientras nos cepillamos los dientes",
            "b) Cerrar la llave mientras nos cepillamos los dientes",
            "c) Lavar el auto todos los días"
        ],
        "correcta": "b"
    },
    {
        "pregunta": "¿Por qué es importante reciclar?",
        "opciones": [
            "a) Para reducir la contaminación y el uso de recursos naturales",
            "b) Para gastar más energía",
            "c) Para llenar los basureros"
        ],
        "correcta": "a"
    },
    {
        "pregunta": "¿Qué significa ‘huella ecológica’?",
        "opciones": [
            "a) El impacto ambiental que dejamos por nuestro consumo",
            "b) El tamaño de nuestro pie",
            "c) Una huella en la playa"
        ],
        "correcta": "a"
    }
]

# ---------------------- CONTROL DE QUIZ EN CURSO POR USUARIO ----------------------
quiz_in_progress = {}

@bot.command(name="quiz")
async def quiz(ctx):
    """Inicia un quiz de 15 preguntas de opción múltiple."""
    user_id = ctx.author.id
    if quiz_in_progress.get(user_id, False):
        await ctx.send("Ya tienes un quiz en curso. Escribe !quizstop para cancelar o termina el actual.")
        return
    quiz_in_progress[user_id] = True
    await ctx.send("📝 **Quiz de cambio climático**\nResponde cada pregunta escribiendo **a**, **b** o **c** en el chat. ¡Tienes 30 segundos para cada una!\n(Escribe `!quizstop` para cancelar tu quiz en cualquier momento)")

    questions = random.sample(quiz_questions, 15)
    score = 0

    def check(m):
        return (
            m.author == ctx.author
            and m.channel == ctx.channel
            and (m.content.lower() in ['a', 'b', 'c'] or m.content.lower() == '!quizstop')
        )

    for i, q in enumerate(questions):
        opciones_texto = "\n".join(q["opciones"])
        await ctx.send(f"**Pregunta {i+1} de 15:**\n{q['pregunta']}\n{opciones_texto}")
        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
            if msg.content.lower() == '!quizstop':
                await ctx.send("Quiz cancelado. ¡Vuelve a intentarlo cuando quieras!")
                quiz_in_progress.pop(user_id, None)
                return
            respuesta_usuario = msg.content.strip().lower()
            if respuesta_usuario == q["correcta"]:
                await ctx.send("✅ ¡Correcto!")
                score += 1
            else:
                correcta_texto = q["opciones"][ord(q["correcta"])-ord('a')]
                await ctx.send(f"❌ Incorrecto. La respuesta correcta era: **{q['correcta']}) {correcta_texto[3:]}**")
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tiempo agotado. Siguiente pregunta.")
    await ctx.send(f"🎉 ¡Quiz terminado! Tu puntaje final: {score} de 15.")
    quiz_in_progress.pop(user_id, None)

@bot.command(name="quizstop")
async def quizstop(ctx):
    """Cancela el quiz en curso para el usuario."""
    user_id = ctx.author.id
    if quiz_in_progress.get(user_id, False):
        quiz_in_progress.pop(user_id, None)
        await ctx.send("Tu quiz ha sido cancelado.")
    else:
        await ctx.send("No tienes ningún quiz en curso.")

# ---------------------- COMANDOS EXTRA PARA EXTENDER FUNCIONALIDAD ----------------------

@bot.command(name="glosario")
async def glosario_cmd(ctx, *, termino: str = None):
    """Muestra la definición de un término relacionado al cambio climático."""
    if not termino:
        await ctx.send("Por favor, especifica el término que quieres buscar. Ejemplo: `!glosario efecto invernadero`")
        return
    clave = termino.strip().lower()
    definicion = glosario.get(clave)
    if definicion:
        await ctx.send(f"**{clave.capitalize()}**: {definicion}")
    else:
        await ctx.send(f"No encontré el término '{termino}'. Usa solo palabras clave, por ejemplo: 'IPCC', 'huella de carbono', 'biodegradable'...")

@bot.command(name="frase")
async def frase(ctx):
    """Envía una frase inspiradora/motivacional sobre el medio ambiente."""
    f = random.choice(frases)
    await ctx.send(f"🌳 {f}")

@bot.command(name="tipdelosabado")
async def tipdelosabado(ctx):
    """Envía un tip ecológico especial para los sábados."""
    if datetime.datetime.utcnow().weekday() == 5:
        consejo = random.choice(eco_tips)
        await ctx.send(f"🌱 [Tip especial de sábado]: {consejo}")
    else:
        await ctx.send("Este comando solo está disponible los sábados. ¡Vuelve ese día para recibir un tip especial!")

@bot.command(name="cuentaregresiva")
async def cuentaregresiva(ctx, minutos: int = 1):
    """Inicia una cuenta regresiva y te avisa al terminar (máx 60 min)."""
    if minutos < 1 or minutos > 60:
        await ctx.send("Puedes poner entre 1 y 60 minutos.")
        return
    await ctx.send(f"⏳ ¡Cuenta regresiva iniciada! Te avisaré en {minutos} minuto(s).")
    await asyncio.sleep(minutos*60)
    await ctx.send(f"⏰ ¡{ctx.author.mention} Tu cuenta regresiva de {minutos} minuto(s) ha terminado!")

@bot.command(name="top_tips")
async def top_tips(ctx, cantidad: int = 5):
    """Muestra una lista de los mejores tips ecológicos."""
    if cantidad < 1 or cantidad > len(eco_tips):
        cantidad = 5
    selected = random.sample(eco_tips, cantidad)
    tips_text = "\n".join([f"- {tip}" for tip in selected])
    await ctx.send(f"🌱 **Top {cantidad} tips ecológicos:**\n{tips_text}")

@bot.command(name="datos")
async def datos(ctx):
    """Muestra datos curiosos sobre el cambio climático."""
    curiosidades = [
        "El nivel del mar ha subido más de 20 centímetros en el último siglo.",
        "Cada año se pierden aproximadamente 13 millones de hectáreas de bosque.",
        "La década de 2010-2019 fue la más cálida jamás registrada.",
        "Más del 90% del calor adicional generado por el cambio climático es absorbido por los océanos.",
        "Los eventos climáticos extremos han aumentado en frecuencia e intensidad.",
        "La producción de alimentos representa el 25% de las emisiones globales de gases de efecto invernadero."
    ]
    c = random.choice(curiosidades)
    await ctx.send(f"🌡️ Dato curioso: {c}")

@bot.command(name="recordatorio")
async def recordatorio(ctx, minutos: int = 10):
    """Te envía un recordatorio ecológico en X minutos (máx 180)."""
    if minutos < 1 or minutos > 180:
        await ctx.send("Elige un valor entre 1 y 180 minutos.")
        return
    await ctx.send(f"⏰ Te enviaré un recordatorio ecológico en {minutos} minutos.")
    await asyncio.sleep(minutos * 60)
    consejo = random.choice(eco_tips)
    await ctx.send(f"{ctx.author.mention} ¡Hora de tu recordatorio ecológico! 🌱 {consejo}")

@bot.command(name="infoipcc")
async def infoipcc(ctx):
    """Da información sobre el IPCC."""
    texto = (
        "El IPCC (Panel Intergubernamental sobre Cambio Climático) es un organismo internacional creado en 1988 "
        "por la ONU para evaluar la información científica relacionada con el cambio climático. "
        "El IPCC no realiza investigaciones propias, sino que recopila y evalúa estudios realizados en todo el mundo."
    )
    await ctx.send(texto)

@bot.command(name="energias")
async def energias(ctx):
    """Muestra una lista de energías renovables con una breve explicación."""
    energias = [
        ("Solar", "Aprovecha la energía del sol mediante paneles fotovoltaicos o térmicos."),
        ("Eólica", "Utiliza la fuerza del viento para generar electricidad."),
        ("Hidráulica", "Genera energía a partir de corrientes o caídas de agua."),
        ("Geotérmica", "Aprovecha el calor interno de la Tierra."),
        ("Biomasa", "Obtiene energía de materia orgánica como residuos agrícolas o forestales."),
        ("Mareomotriz", "Utiliza el movimiento de las mareas y olas.")
    ]
    emb = discord.Embed(title="⚡ Tipos de energías renovables", color=discord.Color.gold())
    for nombre, desc in energias:
        emb.add_field(name=nombre, value=desc, inline=False)
    await ctx.send(embed=emb)

# ---------------------- CICLO AUTOMÁTICO DE TIPS ----------------------
canal_tips_id = None  # Puedes poner aquí el ID de un canal para tips automáticos

@tasks.loop(hours=12)
async def enviar_tip_automatico():
    global canal_tips_id
    if canal_tips_id is not None:
        canal = bot.get_channel(canal_tips_id)
        if canal:
            consejo = random.choice(eco_tips)
            await canal.send(f"🌱 [Tip automático]: {consejo}")

@bot.command(name="activar_tips_auto")
@commands.has_permissions(administrator=True)
async def activar_tips_auto(ctx, canal_id: int = None):
    """Activa el envío automático de tips ecológicos cada 12 horas en un canal."""
    global canal_tips_id
    if canal_id is None:
        canal_id = ctx.channel.id
    canal_tips_id = canal_id
    enviar_tip_automatico.start()
    await ctx.send("✅ Tips automáticos activados para este canal.")

@bot.command(name="desactivar_tips_auto")
@commands.has_permissions(administrator=True)
async def desactivar_tips_auto(ctx):
    """Desactiva los tips automáticos."""
    global canal_tips_id
    canal_tips_id = None
    enviar_tip_automatico.cancel()
    await ctx.send("❌ Tips automáticos desactivados.")

# ---------------------- EVENTOS Y COMANDOS ORIGINALES ----------------------

@bot.event
async def on_ready():
    print(f"[INFO] Bot conectado como {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        await member.send(f"¡Bienvenido/a a {member.guild.name}! 🌱 Recuerda cuidar el planeta. Escribe !hola para empezar.")
    except Exception as e:
        print(f"[WARN] No se pudo enviar mensaje de bienvenida a {member}.")

@bot.command(name="hola")
async def hola(ctx):
    await ctx.send("¡Hola! 👋 Soy un bot educativo sobre el cambio climático. Escribe !ayuda para ver lo que puedo hacer.")

@bot.command(name="clima")
async def clima(ctx):
    embed = discord.Embed(
        title="🌎 Cambio Climático",
        description="El cambio climático es uno de los mayores retos de nuestro tiempo.",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Temperatura Global",
        value="La temperatura global ha aumentado aproximadamente 1.1°C desde la era preindustrial.",
        inline=False
    )
    embed.add_field(
        name="Consecuencias",
        value="Fenómenos como olas de calor, deshielo y aumento del nivel del mar son cada vez más frecuentes.",
        inline=False
    )
    embed.set_footer(text="Fuente: IPCC y organismos ambientales internacionales")
    await ctx.send(embed=embed)

@bot.command(name="tip")
async def tip(ctx):
    consejo = random.choice(eco_tips)
    await ctx.send(f"🌱 Tip ecológico: {consejo}")

@bot.command(name="noticia")
async def noticia(ctx):
    n = random.choice(noticias)
    embed = discord.Embed(
        title=f"📰 {n['titulo']}",
        description=n['contenido'],
        url=n['url'],
        color=discord.Color.blue()
    )
    embed.set_footer(text="Esta es una noticia simulada para el proyecto.")
    await ctx.send(embed=embed)

@bot.command(name="adminmsg")
@commands.has_permissions(administrator=True)
async def adminmsg(ctx, *, mensaje=None):
    if mensaje is None:
        await ctx.send("Debes escribir el mensaje que quieres enviar, por ejemplo: !adminmsg Este es un anuncio.")
    else:
        await ctx.send(f"📢 [Mensaje de administración]: {mensaje}")

@adminmsg.error
async def adminmsg_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos para usar este comando.")


@bot.command(name="ayuda")
async def ayuda(ctx):
    embed = discord.Embed(
        title="🤖 Comandos del Bot de Cambio Climático",
        description="Aquí tienes una lista de comandos disponibles:",
        color=discord.Color.teal()
    )
    embed.add_field(name="!hola", value="El bot te saluda.", inline=False)
    embed.add_field(name="!clima", value="Información general sobre el cambio climático.", inline=False)
    embed.add_field(name="!tip", value="Recibe un consejo ecológico al azar.", inline=False)
    embed.add_field(name="!noticia", value="Lee una noticia simulada sobre el clima.", inline=False)
    embed.add_field(name="!quiz", value="Responde un quiz de 15 preguntas de opción múltiple.", inline=False)
    embed.add_field(name="!quizstop", value="Cancela el quiz si lo necesitas.", inline=False)
    embed.add_field(name="!frase", value="Recibe una frase inspiradora sobre el medio ambiente.", inline=False)
    embed.add_field(name="!glosario [término]", value="Definición de un término de cambio climático.", inline=False)
    embed.add_field(name="!top_tips [n]", value="Muestra los mejores tips ecológicos.", inline=False)
    embed.add_field(name="!tipdelosabado", value="Tip especial para los sábados.", inline=False)
    embed.add_field(name="!datos", value="Dato curioso sobre el cambio climático.", inline=False)
    embed.add_field(name="!recordatorio [min]", value="Recibe un recordatorio ecológico en X minutos.", inline=False)
    embed.add_field(name="!infoipcc", value="Información sobre el IPCC.", inline=False)
    embed.add_field(name="!energias", value="Tipos de energías renovables.", inline=False)
    embed.add_field(name="!cuentaregresiva [min]", value="Inicia una cuenta regresiva ecológica.", inline=False)
    embed.add_field(name="!activar_tips_auto [id]", value="(Admin) Tips automáticos cada 12h en un canal.", inline=False)
    embed.add_field(name="!desactivar_tips_auto", value="(Admin) Desactiva los tips automáticos.", inline=False)
    embed.add_field(name="!adminmsg", value="(Solo admins) El bot repite tu mensaje para anuncios.", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ Ese comando no existe. Escribe !ayuda para ver los comandos.")
    else:
        print(f"[ERROR] {error}")

if __name__ == "__main__":
    print("[INFO] Iniciando el bot...")
    bot.run("pon tu token aquí")  # Reemplaza con tu token de bot de Discord