import openai
import os
import json
from Email.schemas import IntroEmailInfo

openai.api_key = os.getenv("OPENAI_KEY")
MAX_TOKENS = 400
# model 1 MODEL = "curie:ft-personal-2023-08-10-07-08-10"

# MODEL = "curie:ft-personal-2023-08-12-18-00-04"
# MODEL = "curie:ft-personal-2023-08-12-18-15-36"


async def generateIntroEmail(IntroEmailInfo: IntroEmailInfo):
    sender_name = (
        f" Name is {IntroEmailInfo.senderName}" if IntroEmailInfo.senderName else ""
    )
    sender_email = (
        f" Email is {IntroEmailInfo.senderEmail}" if IntroEmailInfo.senderEmail else ""
    )
    sender_company = (
        f" Works at {IntroEmailInfo.senderCompany}"
        if IntroEmailInfo.senderCompany
        else ""
    )

    vendor_name = f" Name is {IntroEmailInfo.vendorName}"
    vendor_email = f" Name is {IntroEmailInfo.vendorEmail}"
    vendor_company = f" Name is {IntroEmailInfo.vendorCompany}"

    sender_prompt = f"The talent executive (sender) information is as follows, {sender_name}, {sender_email}, {sender_company}"
    vendor_propmpt = f"The vendor (receiver) information is as follows, {vendor_name}, {vendor_email}, {vendor_company}"

    prompt = f"Write me an Introductory email. The sender is a talent executive who works at a staffing firm.{sender_prompt}. {vendor_propmpt}. Write me 200 words and no more than 1 paragraph. Return just the JSON string."

    temp = {
        "subject": "Exploring Potential Partnership Opportunities",
        "body": "Dear [Receivers Name],\n\nI hope this email finds you well. My name is [Your Name], and I am a Talent Executive at [Your Staffing Firms Name]. I have been following the impressive work of [Receivers Company Name] for some time now, and I am truly impressed by the innovative solutions and services your company provides to clients.\n\nAs a staffing firm that prides itself on connecting businesses with exceptional talent, we are always seeking to collaborate with industry leaders who share our commitment to excellence. I believe that there could be valuable synergies between our organizations, and I am excited to explore the possibility of establishing a partnership that can benefit both our clients and our respective teams.\n\nI would greatly appreciate the opportunity to connect with you and discuss how we might be able to create a mutually beneficial arrangement. Please let me know a convenient time for a brief call or meeting. Thank you for considering this proposal, and I look forward to the opportunity to connect.\n\nBest regards,\n\n[Your Name]\nTalent Executive\n[Your Staffing Firms Name]\n[Your Contact Information]",
    }

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates emails for staffing companies.",
        },
        {
            "role": "user",
            "content": "Write me an Introductory email. The sender is a talent executive who works at a staffing firm and the receiver is a vendor company executive. Write me 150 words and no more than 1 paragraph. Return a valid JSON string",
        },
        {
            "role": "assistant",
            "content": '{"subject": "Exploring Potential Partnership Opportunities","body": "Dear [Receivers Name],\n\nI hope this email finds you well. My name is [Your Name], and I am a Talent Executive at [Your Staffing Firms Name]. I have been following the impressive work of [Receivers Company Name] for some time now, and I am truly impressed by the innovative solutions and services your company provides to clients.\n\nAs a staffing firm that prides itself on connecting businesses with exceptional talent, we are always seeking to collaborate with industry leaders who share our commitment to excellence. I believe that there could be valuable synergies between our organizations, and I am excited to explore the possibility of establishing a partnership that can benefit both our clients and our respective teams.\n\nI would greatly appreciate the opportunity to connect with you and discuss how we might be able to create a mutually beneficial arrangement. Please let me know a convenient time for a brief call or meeting. Thank you for considering this proposal, and I look forward to the opportunity to connect.\n\nBest regards,\n\n[Your Name]\nTalent Executive\n[Your Staffing Firms Name]\n[Your Contact Information]"}"',
        },
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    if "choices" in response and len(response["choices"]) > 0:
        return response["choices"][0]["message"]["content"]
    raise Exception(
        "Error: [AIUtils/generateIntroEmail], faulty openai response. Try again."
    )
