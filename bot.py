from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount


class Bot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("¡Bienvenido!")
                await turn_context.send_activity("Escribe tu saludo")

    async def on_message_activity(self, turn_context: TurnContext):
        grettings = ['hello', 'hola', 'hey', 'oe', 'que onda', 'dag']
        grettings_ask = ['que tal', 'que tal?', '¿qué tal?', '¿que tal?', 'cómo estas?', 'como estas?', 'como estas', '¿como estas?', '¿cómo estas?']
        grettings_ask_response = ['bien', 'mas o menos', 'más o menos', 'mal', 'tenemos salud']
        byes = ['bye', 'adios', 'adiós', 'hasta luego', 'nos vemos', 'hasta la próxima', 'hasta la proxima']
        text = turn_context.activity.text
        response = 'Ups! Al parecer eso no es un saludo :('

        if text.lower() in grettings:
            response = 'Hola, que tal?'

        if text.lower() in grettings_ask:
            response = 'De maravilla, y tú?'

        if text.lower() in byes:
            response = 'Hasta luego'

        if text.lower() in grettings_ask_response:
            response = 'que bien, vamos por unas hamburguesas?'

        return await turn_context.send_activity(MessageFactory.text(f"{response}"))
