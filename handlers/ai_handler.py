from aiogram.types import ReplyKeyboardRemove

from db.sql import DataBase
from main import dp, bot
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import get_main_keyboard
from keyboards.ai_keyboard import AIState

from aiogram.types import FSInputFile, Message
from languages.translator import to_user_lang, to_bot_lang, ImagePath

db = DataBase('my_database.db')


@dp.message(AIState.ai)
async def conversation(message: Message, state: FSMContext):

    if to_bot_lang(message.text.lower()) == "back":
        keyboard = await get_main_keyboard(message.from_user.id)
        lang = await db.get_lang(message.from_user.id)
        lang = lang[0][0]
        await bot.send_message(
            message.chat.id,
            text=to_user_lang("Thank you. Bye!", lang),
            # reply_markup=low_keyboard.as_markup()
            reply_markup=ReplyKeyboardRemove()
        )

        await message.answer_photo(
            photo=FSInputFile(f"{ImagePath}Catalog.jpg"),
            caption='',
            reply_markup=keyboard.as_markup()
        )
        await state.clear()
    else:
        lang = await db.get_lang(message.from_user.id)
        lang = lang[0][0]
        response = conversation.predict(human_input=message.text)
        message_hist = {'human': message.text, 'AI': response}
        chat_history.append(message_hist)
        await bot.send_message(message.chat.id, text=to_user_lang(response, lang))


from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

system_prompt = """
       you are shop consultant. You should consultate 
       about products below. You can search info only in this description 
       Use short phrases. If you are asked about something else except products, 
       you should answer 'I don't know this info, I am just consultant'
       
       Products:
       1) LibidoProst: A herbal preparation with a preventive and healing effect, well tolerated and safe for the body,\
        does not have a toxic load with prolonged use, is a reliable aid in general strengthening of the body. \
        The drug has a complex therapeutic effect on the genitourinary system.
       2) EnergyFit: A herbal preparation with a preventive and healing effect, well tolerated and safe for the body,\
        does not cause toxic load with long-term use, is a reliable aid in general strengthening of the body.
        
        """

model = 'llama3-8b-8192'
conversational_memory_length = 40

memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history",
                                        return_messages=True)

# session state variable
chat_history = []

# Initialize Groq Langchain chat object and conversation
groq_chat = ChatGroq(
    groq_api_key="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",
    model_name=model
)

# Construct a chat prompt template using various components
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=system_prompt
        ),  # This is the persistent system prompt that is always included at the start of the chat.

        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.

        HumanMessagePromptTemplate.from_template(
            "{human_input}"
        ),  # This template is where the user's current input will be injected into the prompt.
    ]
)

# Create a conversation chain using the LangChain LLM (Language Learning Model)
conversation = LLMChain(
    llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
    prompt=prompt,  # The constructed prompt template.
    verbose=False,  # Enables verbose output, which can be useful for debugging.
    memory=memory,  # The conversational memory object that stores and manages the conversation history.
    # retriever=None
)