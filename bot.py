from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

from dbcontext import DbContext

db = DbContext('intents.db')


class Bot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("¡Bienvenido!")
                await turn_context.send_activity("Escribe tu saludo")

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text

        response_index = self.check_keyword(text, self.get_keyword_list())
        response = self.get_response(response_index)

        return await turn_context.send_activity(MessageFactory.text(f"{response}"))

    def check_keyword(self, word, keyword_list):
        for item in keyword_list:
            if word in item:
                return item[1]

        return -1

    def get_keyword_list(self):
        result = db.read(f"select * from keyword")

        return result

    def get_response(self, intype):
        result = db.read(f"select value from response where intype_id=?", query_params=[intype])

        if result and len(result) > 0:
            return result[0][0]
        else:
            return 'Ups! Al parecer eso no es un saludo :('
