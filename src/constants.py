FONT_PATH = './src/fonts/rabiohead.ttf'
SIGNATURE_FONT_PATH = './src/fonts/PWsignaturefont.ttf'
WORD_PER_LINE = 110
BLUE_INK = '#0047AB'
DEFAULT_FONT_SIZE=10
SIGNATURE_FONT_SIZE=30
LINE_HEIGHT=20
CONTENT_WRAP_WIDTH=100

OUTPUT_FILE_NAME = 'medical-document.pdf'

MESSAGES = {
    "START": "Hello there! \nI can help you create a medical certificate, Type 'I am sick' to begin",
    "HELP": """
        Type "I am sick" to begin
     """,
     "NAME": "Okay, let's create a medical for you.\nWhat's your name?",
     "AGE": "Nice to meet you, {name}! How old are you?",
     "DISEASE": "Okay Great, and what health issue you want to mention. Write in 2-3 words",
     "START_DATE": "Got it. What's the start date for your absence?\nPlease mention date in 'dd-mm-yyyy' format",
     "END_DATE": "Got it. What's the end date for your absence?\nPlease mention date in 'dd-mm-yyyy' format",
     "END": "Awesome, you are all done. I am processing your medical",
     "CANCEL": "Bye! I hope we can talk again soon.",
     "INVALID_AGE": "Please enter a valid age"
}

templates = [
    {
        'location': 'src/templates/doctor-template-1.pdf',
        'width': 595,
        'height': 842,
        'placement': {
            'doctorName': {
                'x': 90,
                'y': 805,
                'fontSize': 24,
                'fontWeight': 'bold',
                'color': '#975ca4'
            },
            'doctorSpecification': {
                'x': 90,
                'y': 785,
                'fontSize': 12,
                'fontWeight': 'bold',
                'color': '#656161'
            },
            'hospitalInfo': {
                'x': 350,
                'y': 45,
                'fontSize': 10,
                'fontWeight': 'bold',
                'color': '#656161'
            },
            'date': {
                'x': 478,
                'y': 788,
                'fontSize': 11,
                'fontWeight': 'bold',
                'color': '#656161'
            },
            'content': {
                'x': 40,
                'y': 720,
                'fontSize': 16,
                'fontWeight': 'bold',
                'color': BLUE_INK,
                'width': 500,
                'height': 600,
            },
        }
    }
]

content = '''
To Whom It May Concern,

This is to certify that [Your Name], [Age], was under my care on [Date] due to a bee sting incident. The patient presented with significant pain and discomfort as a result of the bee sting and was unable to attend work on that day.

Medical Assessment:

The patient's symptoms are consistent with a bee sting, including localized pain, swelling, and possible allergic reactions. As a responsible measure for their health and safety, it is advisable for the patient to refrain from engaging in strenuous activities, including office work, during the recovery period.

Recommendations:

Rest: The patient requires adequate rest to allow the body to heal and recover from the effects of the bee sting.
Pain Management: Prescribed medications for pain relief as per the attached prescription.
Follow-up Care: It is recommended that the patient follows up with their primary care physician for further evaluation and management if symptoms persist or worsen.
Sick Leave Duration:
[Your Name] is advised to take [number of days] off from work to ensure proper rest and recovery. The duration of sick leave may be extended based on the patient's condition and response to treatment.

Work Excuse:
Due to the severity of the bee sting and associated pain, [Your Name] was medically unfit to attend work on [Date].

Please feel free to contact me if further clarification or information is required.

Warm regards,
'''