from llama_index import StorageContext, load_index_from_storage

from llama_index.llms import OpenAI


class Engine:
    def __init__(self, storage = '/home/phongtnh/Face_Makeup/storage', users_data = "", context_data = ""):
        
        # Init chat engine from index created for local storage
        storage_context = StorageContext.from_defaults(persist_dir=storage)
        index = load_index_from_storage(storage_context)
        self.chat_engine = index.as_chat_engine()


        # System prompt
        system_prompt_text = open("/home/phongtnh/Face_Makeup/sample/system_prompt.txt", "r")
        self.system_prompt = system_prompt_text.read()
        system_prompt_text.close()

        # Personalized data
        self.users_data = users_data
        self.context_data = context_data

    def create_advice(self): 
        instruction_1 = ". First you will receive a description of this user such as: "
        instruction_2 = ". You will output a detailed makeup guide that matches user and his/her purposes:"
        split = "\n---\n"
        query = f'''
                    "#INSTRUCTION\n" + 
                    {self.system_prompt} +  {instruction_1} + 
                    {split} + 
                    {self.users_data} + 
                    {split} + 
                    "PURPOSES \n" + 
                    {self.context_data} + 
                    {split} + 
                    {instruction_2}
                '''
        """
        Query look like this:
        #INSTRUCTION
        I want you to act as a makeup artist. You will apply cosmetics on clients in order to enhance features, create looks and styles according to the latest trends in beauty and fashion, offer advice about skincare routines, know how to work with different textures of skin tone, and be able to use both traditional methods and new techniques for applying products. First you will receive a description of this user such as: 
        ---
        #USER
        This Asian woman has a dark skin
        ---
        #PURPOSES
        Wedding, hot weather, active
        ---
        You will output a detailed makeup guide that matches user and his/her purposes: 
        """
        
        resp = OpenAI().complete(query)
        self.guide = resp.text
        return self.guide
    
    def create_advice_with_prod(self):
        query = f'''
                    {self.system_prompt} + 
                    "\n----\n" + 
                    {self.guide} + 
                    "\n---\n" + 
                    "Based on the guide above, adding product details and reasons to use it over other products" + 
                    "\n---\n" 
                '''

        response = self.chat_engine.chat(query)
        self.advice = response.response
        return self.advice
