import asyncio
import sys
from datetime import datetime

from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapterSettings, BotFrameworkAdapter, TurnContext
from botbuilder.schema import Activity, ActivityTypes

from config import Config
from bot import Bot


# Crean el loop y la instancia de flask
Loop = asyncio.get_event_loop()
App = Flask(__name__)

App.config.from_object(Config)


# Creando el adaptador del bot
SETTINGS = BotFrameworkAdapterSettings(App.config["APP_ID"], App.config["APP_PASSWORD"])
ADAPTER = BotFrameworkAdapter(SETTINGS)


# Capturando todos los errores
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] error no capturado: {error}", file=sys.stderr)

    # Enviar mensaje al usuario
    await context.send_activity("Oh, oh. Al parecer tengo un error.")
    await context.send_activity("Por favor, corrígeme")

    if context.activity.channel_id == 'emulator':
        # se crea una actividad conteniendo info del error
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error"
        )
        # Se muestra la actividad en el Bot Framework Emulator
        await context.send_activity(trace_activity)

ADAPTER.on_turn_error = on_error

BOT = Bot()


@App.route('/api/messages', methods=['POST'])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = (
        request.headers["Authorization"] if "Authorization" in request.headers else ""
    )

    try:
        task = Loop.create_task(
            ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        )
        Loop.run_until_complete(task)
        return Response(status=201)
    except Exception as exception:
        raise exception


if __name__ == "__main__":
    try:
        App.run(
            debug=False,
            port=App.config["PORT"]
        )
    except Exception as exception:
        raise exception
