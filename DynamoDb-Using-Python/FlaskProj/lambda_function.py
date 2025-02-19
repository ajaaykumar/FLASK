"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
import requests
import boto3

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to alexa voice student details"
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_Student_Response(intent):
    session_attributes = {}
    card_title = "StudentDetails"
    
    kid = intent['slots']['RollNo']['value']
    print('===>',kid)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StudentDetails')
    resource = table.scan()
    data = resource['Items']
    
    smarks = 0
    for x in data:
        if str(kid) == x['Student_Id'] :
            sname = x['Student_name']
            slocation = x['Location']
            smarks = x['Marks']
    if  smarks != 0:
        speech_output = str(kid)+" Student details are student name "+ sname + " Location " + slocation + " Marks " +smarks + " %"
        reprompt_text = str(kid)+" Student details are student name "+ sname + " Location " + slocation + " Marks " +smarks + " %"
    
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
       
    else:
        speech_output = str(kid)+" student Doesn't Exist"
        reprompt_text = str(kid)+" student Doesn't Exist"
        should_end_session = False 
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        

def get_FeeDetails_response(intent):
    session_attributes = {}
    card_title = "FeeDetails"
    
    sid = intent['slots']['fRollno']['value']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StudentDetails')
    resource = table.scan()
    details = resource['Items']
    
    fee = 0
    for detail in details:
        if str(sid) == detail['Student_Id']:
            fee = detail['Fee_Details']
            
    if  fee != 0:        
        speech_output = str(sid)+" Fee details are "+str(fee)+' rupees '
        reprompt_text = str(sid)+" Fee details are "+str(fee)+' rupees '
            
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    else:
        speech_output = str(sid)+" student Doesn't Exist"
        reprompt_text = str(sid)+" student Doesn't Exist"
            
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_mobilenumber_response(intent):
    session_attributes = {}
    card_title = "mobilenumber"
    
    fid = intent['slots']['aRollNo']['value']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StudentDetails')
    resource = table.scan()
    data = resource['Items']
    
    mobile = 0
    for x in data:
        if x['Student_Id'] == str(fid):
            mobile = x['Mobile Number']
            
    if mobile != 0:
        speech_output = str(fid) + " Mobile number is " + str(mobile)
        reprompt_text = str(fid) + " Mobile number is " + str(mobile)
        
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    else:
        speech_output = str(fid)+" student Doesn't Exist"
        reprompt_text = str(fid)+" student Doesn't Exist"
        
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_HighestMarks_response():
    session_attributes = {}
    card_title = "HighestMarks"
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StudentDetails')
    resource = table.scan()
    data = resource['Items']
    lst = []
    for x in data:
        lst.append(x['Marks'])
    maxum = max(lst)
    
    for x in data:
        if x['Marks'] == maxum:
            name = x['Student_name']
            id = x['Student_Id']
            
            speech_output = "Highest Marks are "+ str(maxum)+ "%" + " student name is " + str(x['Student_name'])
            reprompt_text = "This is else condition"
            
            should_end_session = False
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StudentDetails":
        return get_Student_Response(intent)
    
    elif intent_name == "FeeDetails":
        return get_FeeDetails_response(intent)
    
    elif intent_name == "mobilenumber":
        return get_mobilenumber_response(intent)
    
    elif intent_name == "HighestMarks":
        return get_HighestMarks_response()
        
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

