import openai
import os
import json
from Email.schemas import IntroEmailInfo, ReplyEmailInfo

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


async def generateReply(ReplyEmailInfo: ReplyEmailInfo):
    prompt = (
        f"Make the receiver book a slot on my calendar. Meeting Link: {ReplyEmailInfo.meetingLink}"
        if ReplyEmailInfo.meetingLink
        else ""
    )
    prompt = (
        f"{prompt}. {ReplyEmailInfo.extraNotes}"
        if ReplyEmailInfo.extraNotes
        else prompt
    )
    prompt = f"The sender is a talent executive who works at a staffing firm and the receiver is a vendor company executive.{prompt}"
    if ReplyEmailInfo.isMeFollowUp:
        if ReplyEmailInfo.prevSender:
            prompt = f"The name of the sender is {ReplyEmailInfo.prevSender.name} and his/her email is {ReplyEmailInfo.prevSender.address}. {prompt}"
        prompt = f"Write me a followup to my email. The sender had sent an email to the receiver to build a professional relationship. This is the sender's email:'{ReplyEmailInfo.prevBodySent}'The receiver has not replied to the email. Write me 200 words and no more than 1 paragraph. {prompt}"
    else:
        prompt = f"Write me a reply to this email. The sender had sent an email to the receiver to build a professional relationship. This is the receiver's reply: '{ReplyEmailInfo.prevBodySent}'. write me 200 words and no more than 1 paragraph. {prompt}"

    prompt = f"Write subject and body of an email. Return the subject and body in a JSON format. {prompt}."
    # TODO: add extra messages so open ai will follow that while sending reply.
    # increase temperature.
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates emails for staffing companies. And returns the sibject and body seperately in a json format.",
        }
    ]

    if ReplyEmailInfo.isMeFollowUp:
        messages += [
            {
                "role": "user",
                "content": "Write subject and body of an email. Return the subject and body in a JSON format. Write me a followup to my email. The sender had sent an email to the receiver to build a professional relationship. This is the sender's email:'Dear [Receivers Name],\n\nI hope this email finds you well. My name is [Your Name], and I am a Talent Executive at [Your Staffing Firms Name]. I have been following the impressive work of [Receivers Company Name] for some time now, and I am truly impressed by the innovative solutions and services your company provides to clients.\n\nAs a staffing firm that prides itself on connecting businesses with exceptional talent, we are always seeking to collaborate with industry leaders who share our commitment to excellence. I believe that there could be valuable synergies between our organizations, and I am excited to explore the possibility of establishing a partnership that can benefit both our clients and our respective teams.\n\nI would greatly appreciate the opportunity to connect with you and discuss how we might be able to create a mutually beneficial arrangement. Please let me know a convenient time for a brief call or meeting. Thank you for considering this proposal, and I look forward to the opportunity to connect.\n\nBest regards,\n\n[Your Name]\nTalent Executive\n[Your Staffing Firms Name]\n[Your Contact Information]'. The receiver has not replied to the email. Write me 200 words and no more than 1 paragraph. The name of the sender is sam and his/her email is sam@gmail.com. The sender is a talent executive who works at a staffing firm and the receiver is a vendor company executive.. important vendor.",
            },
            {
                "role": "assistant",
                "content": '{"subject":"Follow-up: Exploring Collaboration Opportunities","body":"Dear [Receiver name],\n\nI hope this message finds you well. I wanted to follow up on my previous email as I haven\'t received a response. I understand that you have a busy schedule, and I appreciate your time. I\'m genuinely excited about the potential for collaboration between Careersasha and your esteemed company.\n\nTo make scheduling easier, I\'ve set up a dedicated calendar where you can choose a convenient time slot for our meeting. Please visit Meeting Calendar to select a time that works best for you. Your insights and perspective are highly valuable, and I believe a conversation between us could lead to fruitful opportunities for both organizations.\n\nI look forward to the possibility of connecting and exploring how we can create synergies that benefit our clients and teams. Thank you for considering this, and I\'m eager to hear from you soon.\n\nBest regards,\nShreyas Bhujbal\nTalent Executive\nCareersasha\nEmail: shreyasbhujbal@careersasha.com\nPhone: (Your Contact Number)"}',
            },
        ]
    else:
        messages += [
            {
                "role": "user",
                "content": "Write subject and body of an email. Return the subject and body in a JSON format. Write me a reply to this email. The sender had sent an email to the receiver to build a professional relationship. This is the receiver's reply: 'Hey, I'm busy, please dont bother me.'. write me 200 words and no more than 1 paragraph. The sender is a talent executive who works at a staffing firm and the receiver is a vendor company executive.. important vendor.",
            },
            {
                "role": "assistant",
                "content": '{"subject": "Reply to your email","body": "Dear [Senders Name],\n\nI hope this email finds you well. I wanted to take a moment to apologize for any inconvenience caused by my response earlier. I understand that you are a busy individual, and I respect your time and commitments.\n\nAs the Talent Executive at [Staffing Firm Name], I value relationships with important vendors like yourself. The success of our staffing operations relies on collaborating with credible partners, and I believe that our organizations can benefit greatly from working together.\n\nI apologize if my previous email came across as bothersome. If there are any specific times or methods of communication that are more convenient for you, please let me know, and I will be happy to adjust accordingly. I am confident that by joining forces, we can create mutually beneficial opportunities and achieve great results.\n\nThank you for your understanding, and I look forward to the possibility of building a strong professional relationship with you.\n\nBest regards,\n[Receivers Name]\n[Receivers Title]\n[Staffing Firm Name]"}',
            },
        ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    if "choices" in response and len(response["choices"]) > 0:
        return response["choices"][0]["message"]["content"]
    raise Exception(
        "Error: [AIUtils/generateIntroEmail], faulty openai response. Try again."
    )
