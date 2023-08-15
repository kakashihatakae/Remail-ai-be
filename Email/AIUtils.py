import openai
import os

from Email.schemas import JobDescription

# TODO: move api_key to a more secure location
openai.api_key = os.getenv("OPENAI_KEY")
MAX_TOKENS = 400
# model 1 MODEL = "curie:ft-personal-2023-08-10-07-08-10"

# MODEL = "curie:ft-personal-2023-08-12-18-00-04"
MODEL = "curie:ft-personal-2023-08-12-18-15-36"


async def generateEmail(JobDescription: JobDescription):
    location = (
        f"Location: {JobDescription.location}." if JobDescription.location else ""
    )
    onsite_remote = (
        f"Onsite/Remote: {JobDescription.onsite_remote}."
        if JobDescription.onsite_remote
        else ""
    )
    duration = (
        f"Duration: {JobDescription.duration}." if JobDescription.duration else ""
    )
    contract_type = (
        f"Contract Type: {JobDescription.contract_type}."
        if JobDescription.contract_type
        else ""
    )
    visa = f"Visa: {JobDescription.visa}." if JobDescription.visa else ""
    experience = (
        f"Location: {JobDescription.experience}." if JobDescription.experience else ""
    )
    rate = f"Rate: {JobDescription.rate}." if JobDescription.rate else ""
    skills = f"Skills: {JobDescription.skills}."

    prompt = f"Write me one signle email for one single position to be sent to a condidate for a requirement for {JobDescription.title}.{location}{onsite_remote}{duration}{contract_type}{visa}{experience}{rate}{skills}->"
    response = openai.Completion.create(
        model=MODEL, prompt=prompt, temperature=0.3, max_tokens=MAX_TOKENS
    )
    if response["choices"]:
        return response["choices"][0]["text"]
