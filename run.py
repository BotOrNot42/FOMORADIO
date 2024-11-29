"""
Main Module for the FomoRadio
"""
from src.utils.logger import custom_logger
from src.config import configurations as cf
from src.utils import json_loader
from src.activities import wait_for_next_show
from src.memory import MemoryClient
from src.data_collectors import TwitterClient
from src.script_generators import ScriptClient, LLMClient

# Loading Configurations
radio_show = json_loader("./src/config/radio_show.json")
memory_config = json_loader("./src/config/memory_config.json")
llm_config = json_loader("./src/config/llm_config.json")
rj_personas = json_loader("./src/config/rj_persona.json")


# Logger
logger = custom_logger(radio_show.get("radio_name"))
logger.info("Configurations loaded")
logger.info("Fomo Framework started")

# Loading Memory for personas
for each_persona in rj_personas:
    each_persona["memory"] = MemoryClient(memory_config)
    host_name = each_persona.get("host_name")
    logger.info(f"Memory Initialized for {host_name}")


rj_index = 0
while True:
    # Collecting the data from multiple sources
    twitter_client = TwitterClient(cf.x_bearer_token, cf.x_radio_handle, cf.x_influencers)
    contents = twitter_client.process()
    logger.info(f"Got {len(contents)} contents from {twitter_client.source}")
    if len(contents) == 0:
        logger.info(f"Trying different logic to fetch content")
        continue

    # Loading Contents to Personas
    memories = MemoryClient.content_to_memory(contents)
    for each_persona in rj_personas:
        each_persona['memory'].load_memory(memories)
        host_name = each_persona.get("host_name")
        logger.info(f"Memory Updated for {host_name}")

    # Generating scripts based on the memories
    spoken_users = [i.get("user") for i in contents]
    wait_time = None
    for each_show in radio_show.get("shows"):
        wait_time = each_show.get("wait_time")
        filter_rjs = [
            i for i in rj_personas if i.get("show_id") == each_show.get("show_id")
        ]
        current_rj_index = rj_index % len(filter_rjs)
        next_rj_index = (rj_index + 1) % len(filter_rjs)
        script_client = ScriptClient(
            spoken_users,
            each_show,
            filter_rjs[current_rj_index],
            filter_rjs[next_rj_index].get("host_name")
        )
        prompt = script_client.generate_prompt(twitter_client.source)
        llm_client = LLMClient(llm_config)
        client, interact = llm_client.initialize_client()
        response = interact(client, prompt)
        current_rj_name = filter_rjs[current_rj_index].get("host_name")
        cleaned_response = response.replace('\n', ' ')
        logger.info(f"Script for {current_rj_name} - {cleaned_response}")
        rj_index += 1

    wait_for_next_show(wait_time, logger)
