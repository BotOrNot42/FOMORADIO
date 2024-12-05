"""
Main Module for the FomoRadio
"""
from typing import Tuple, Dict, List
from datetime import datetime
from uuid import uuid4
import pytz
from utils.logger import custom_logger
from config import configuration as cf
from utils import json_loader, save_file, dir_checker
from activities import wait_for_next_show
from memory import MemoryClient
from data_collectors import TwitterClient
from script_generators import ScriptClient, LLMClient
from tts_transformers import TTSClient
from converters import mp3_to_mp4_converter
from consumers import TwitterConsumerClient

# Logger Module
logger = custom_logger("Fomo-FW")
logger.info("Fomo Framework started")

# Create Logs and Media Directory
logger.info("Logger directory initialized")
dir_checker(cf.LOG_FOLDER)
logger.info("Media directory initialized")
dir_checker(cf.MEDIA_FOLDER)


def initialize() -> Tuple[Dict, Dict, Dict, Dict]:
    """
    Initializes the configurations
    :return: Set of 4 configurations (Show, Memory, Fomo, Persona)
    """
    show_config = json_loader("config/show_config.json")
    logger.info("Show configurations loaded")
    memory_config = json_loader("config/memory_config.json")
    logger.info("Memory configurations loaded")
    fomo_config = json_loader("config/fomo_config.json")
    logger.info("Memory configurations loaded")
    persona_config = json_loader("config/persona_config.json")
    logger.info("Persona configurations loaded")
    return show_config, memory_config, fomo_config, persona_config


def load_memory(rj_personas: List, memory_config: Dict) -> List:
    """
    Memory Initializer for the personas given the contents
    :param rj_personas: List of persona's performing the show
    :param memory_config: Configurations for the memory
    :return: Lisf of personas with loaded memory
    """
    for each_persona in rj_personas:
        each_persona["memory"] = MemoryClient(memory_config)
        host_name = each_persona.get("host_name")
        logger.info("Memory Initialized for %s", host_name)
    return rj_personas


def data_collectors():
    """
    Data Collectors to collect the data. If collected from multiple sources, then
    should be given a tuple of records and its sources.
    :return: Contents from Collectors with its source information
    """
    twitter_client = TwitterClient(
        cf.x_bearer_token, cf.x_radio_handle, cf.x_influencers
    )
    return twitter_client.process(), twitter_client.source


def memory_updater(contents: List, persona_config: List) -> List:
    """
    Updates the memory based on the contents
    :param contents: fragments to be updated in the memory
    :param persona_config: persona of the rjs
    :return: List of persona's with updated memory fragments
    """
    memories = MemoryClient.content_to_memory(contents)
    for each_persona in persona_config:
        each_persona["memory"].load_memory(memories)
        host_name = each_persona.get("host_name")
        logger.info("Memory Updated for %s", host_name)
    return persona_config


def main():
    """
    Main Module of Fomo Framework :)
    """
    # Variables needed for the framework to run
    episode_count = 1
    rj_index = 0
    wait_time = None
    max_retries = 5
    # Initializing the modules
    show_config, memory_config, fomo_config, persona_config = initialize()
    persona_config = load_memory(persona_config.get("personas"), memory_config)
    # Starting the infinite loop
    while True:
        # Exit condition if the data collection keeps going on
        if max_retries == 0:
            logger.info("No content found. Skipping the show")
            wait_for_next_show(360, logger)
            max_retries = 5
            continue

        # Collecting the data from multiple sources
        contents, source = data_collectors()
        spoken_users = [i.get("user") for i in contents]
        logger.info("Got %d contents from %s", len(contents), source)
        if len(contents) == 0:
            max_retries -= 1
            logger.info("Trying different logic to fetch content")
            continue

        # Loading Contents to Personas
        persona_config = memory_updater(contents, persona_config)

        # Iterating through shows
        for each_show in show_config.get("shows"):
            # Loop variables
            unique_id = uuid4().hex[:8]
            wait_time = each_show.get("wait_time")

            # Filtering the RJs for that particular show
            filter_rjs = [
                i
                for i in persona_config
                if i.get("show_id") == each_show.get("show_id")
            ]
            current_rj_index = rj_index % len(filter_rjs)
            next_rj_index = (rj_index + 1) % len(filter_rjs)
            llm_client, llm_interact = LLMClient(
                fomo_config.get("llm")
            ).initialize_client()

            # Generating the show script
            current_time = datetime.now(pytz.UTC).strftime("%I:%M %p UTC")
            script_client = ScriptClient(
                spoken_users,
                each_show,
                filter_rjs[current_rj_index],
                filter_rjs[next_rj_index].get("host_name"),
            )
            script_prompt = script_client.generate_prompt(source, current_time)
            generated_script = llm_interact(llm_client, script_prompt)
            current_rj_name = filter_rjs[current_rj_index].get("host_name")
            cleaned_script = generated_script.replace("\n", " ")
            logger.info("Script for %s - %s", current_rj_name, cleaned_script)

            # Generating the content for posting
            content_prompt = script_client.generate_content(source)
            generated_content = llm_interact(llm_client, content_prompt)
            cleaned_content = generated_content.replace("\n", " ")
            logger.info("Content for %s - %s", current_rj_name, cleaned_content)

            # Generating the audio
            current_rj_voice = filter_rjs[current_rj_index].get("voice_id")
            tts_client, tts_interact = TTSClient(
                fomo_config.get("tts"), cf.tts_api_key
            ).initialize_client()
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            radio_name = show_config.get("radio_name").replace(" ", "")
            show_id = each_show.get("show_id")
            file_name = (
                f"{cf.MEDIA_FOLDER}/{radio_name}-{show_id}-{unique_id}-{timestamp}"
            )
            audio_generator = tts_interact(
                tts_client, generated_script, current_rj_voice
            )
            is_audio_saved, audio_errors = save_file(
                audio_generator, f"{file_name}.mp3"
            )
            if is_audio_saved:
                logger.info("Audio File saved as %s.mp3", file_name)
            else:
                logger.error("Generating audio file failed due to %s", audio_errors)

            # Generating video file
            show_details = (
                f"{each_show.get('name')} | Host: {current_rj_name}  | "
                f"Episode: {episode_count} | {current_time}"
            )
            is_video_saved, video_errors = mp3_to_mp4_converter(
                fomo_config.get("mp4"),
                f"{file_name}.mp3",
                f"{file_name}.mp4",
                cf.TEMP_VIDEO_FILE,
                show_details,
                show_config.get("radio_name")
            )
            if is_video_saved:
                logger.info("Video File saved as %s.mp4", file_name)
            else:
                logger.error("Generating video file failed due to %s", video_errors)

            # Consuming the created media
            twitter_consumer_client = TwitterConsumerClient(
                cf.x_api_key,
                cf.x_api_secret,
                cf.x_access_token,
                cf.x_access_token_secret,
            )
            is_tweeted, posting_errors = twitter_consumer_client.post_tweet_with_media(
                generated_content, f"{file_name}.mp4"
            )
            if is_tweeted:
                logger.info("Content consumed by %s", twitter_consumer_client.source)
            else:
                logger.error("Posting content failed due to %s", posting_errors)

            # Iterating through multiple rjs for a single show
            rj_index += 1
        wait_for_next_show(wait_time, logger)


if __name__ == "__main__":
    main()
