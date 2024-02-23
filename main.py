import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()


client = openai.OpenAI()

model = "gpt-3.5-turbo-16k"

# Create a new assistant
#personal_trainer_assistant = client.beta.assistants.create(
#name = "Personal Trainer Assistant",
#instructions= """You are a personal trainer and Specialize in calisthenics and bodyweight exercises. You are also inspireed by Dave Asprey's bio hacking expirements excersizes and routines. His knowledge of nutrition is  what you recommend most to clients""",
#model = model,
#)
#assistant_id = personal_trainer_assistant.id    
#print(personal_trainer_assistant.id)

#=== Hardcode our ids===
assistant_id ="asst_FKNHmFkJC5tG9aLXNNjSqSJ9"
thread_id ="thread_VOM41oMN99UaltLCajO1dmks"

#=== Thread ===
#thread = client.beta.threads.create(
#messages=[
    #    {
   #     "role": "user",
  #      "content": "I'm looking to get in shape and I'm interested in calisthenics. What do you recommend?"
 #       }
#    ]
#)
#thread_id = thread.id
#print(thread_id)
message = "What are the best excersizes for building muscle and strength?"
message = client.beta.threads.messages.create(
    thread_id, 
    role="user",
      content=message
      )

#=== Run our assistant ===
run = client.beta.threads.runs.create(
    assistant_id = assistant_id,
    thread_id = thread_id,
    instructions=" address the user as Chuck Norris"

)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")

                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)