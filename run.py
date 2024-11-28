"""
Main Module for the FomoRadio
"""
import time
from src.config import configurations as cf
from src.utils import json_loader
from src.memory import MemoryClient
from src.data_collectors import TwitterClient


# Loading Configurations
llm_config = json_loader("./src/config/llm_config.json")
radio_show = json_loader("./src/config/radio_show.json")
rj_personas = json_loader("./src/config/rj_persona.json")


# Loading Memory for personas
for each_persona in rj_personas:
    each_persona["memory"] = MemoryClient(llm_config)
    print("Memory Initialized for {host_name}".format(host_name=each_persona.get("host_name")))


while True:
    # Collecting the data from multiple sources
    twitter_client = TwitterClient(cf.x_bearer_token, cf.x_radio_handle, cf.x_influencers)
    contents = twitter_client.process()
    print(f"Got {len(contents)} contents from {twitter_client.source}")

    # Loading Contents to Personas
    memories = MemoryClient.content_to_memory(contents)
    for each_persona in rj_personas:
        each_persona['memory'].load_memory(memories)
        print("Loaded Memory for {host_name}".format(host_name=each_persona.get("host_name")))

    # Summarizing the contents from the past 15 minutes

