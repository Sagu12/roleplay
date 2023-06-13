import os
from langchain.memory import ConversationBufferWindowMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from src.prediction.services.v1.get_template_queries import template_fitness_coach_gpt3
from dotenv import load_dotenv
import pandas as pd
import re

# Load environment variables
load_dotenv(r"src/prediction/env/.env")
api_key = os.getenv("openai_api_key")

class MissTm:
    def __init__(self):
        # Read and preprocess emoji data
        self.df = pd.read_csv(r'src/prediction/models/emojis.txt', sep='\t')
        self.df = self.df[["EMOJI", 'EMOJI NAME']]
        self.df['EMOJI NAME'] = self.df['EMOJI NAME'].str.lower()
        self.df['EMOJI NAME'] = ':' + self.df['EMOJI NAME'] + ':'

        # Initialize conversation memories and language model chains
        self.conversation_memories = {}
        self.language_model_chains = {}

    async def draft_fitnesscoach_message(self, input_prompt, user_id):
        try:
            # Check if user has a conversation memory and language model chain
            if user_id not in self.conversation_memories:
                self.conversation_memories[user_id] = ConversationBufferWindowMemory(k=2)
                prompt_template = PromptTemplate(input_variables=["history", "human_input"], template=template_fitness_coach_gpt3)
                self.language_model_chains[user_id] = LLMChain(
                    llm=OpenAI(openai_api_key=api_key),
                    prompt=prompt_template,
                    verbose=False,
                    memory=self.conversation_memories[user_id],
                )
            
            # Retrieve the conversation memory and language model chain for the user
            memory = self.conversation_memories[user_id]
            llm_chain = self.language_model_chains[user_id]
            
            # Generate response from the language model
            result = llm_chain.predict(human_input=input_prompt)
            result = result.replace('_', ' ')
            
            # Replace emoji names with actual emojis
            for index, row in self.df.iterrows():
                meaning = row['EMOJI NAME']
                emoji = row['EMOJI']
                result = result.replace(meaning, emoji)
            
            # Replace unnecessary subtext with a space
            modified_text = re.sub(r":\w+:", '', result).strip()
            modified_text = re.sub(r'\s+', ' ', modified_text).strip()
            
            # Remove person identifier from the response
            final_output = modified_text.replace('[PersonG #]:', '')
            
            return {"response": final_output}
        except:
            return {"response": "fitness trainer error"}
