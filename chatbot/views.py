from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import random
import time

class VehicleServiceChatbot:
    def __init__(self):
        self.service_menu = """
        Our services include:
        - Oil Changes (Conventional/Synthetic)
        - Tire Rotations & Balancing
        - Brake Services
        - Engine Diagnostics
        - Battery Checks
        - AC Recharging
        Which service are you interested in?"""
        
        self.price_guide = {
            'oil': {
                'conventional': "$39.99",
                'synthetic': "$69.99",
                'full synthetic': "$89.99"
            },
            'tire': {
                'rotation': "$24.99",
                'balance': "$29.99",
                'alignment': "$79.99"
            },
            'brake': {
                'pads': "$129.99 per axle",
                'rotors': "$249.99 per axle",
                'full service': "$399.99"
            }
        }

    def process_query(self, message):
        message = message.lower().strip()
        
        # Greetings
        if any(greeting in message for greeting in ['hi', 'hello', 'hey']):
            return random.choice([
                "Hello! Welcome to AutoCare. How can we assist with your vehicle today?",
                "Hi there! What service does your vehicle need?"
            ])
        
        # Services
        if 'service' in message or 'offer' in message:
            return self.service_menu
            
        # Oil changes
        if 'oil' in message:
            if 'synthetic' in message:
                type_ = 'full synthetic' if 'full' in message else 'synthetic'
                return f"Our {type_} oil change costs {self.price_guide['oil'][type_]} (includes filter)"
            return f"Conventional oil change: {self.price_guide['oil']['conventional']}\nSynthetic available for {self.price_guide['oil']['synthetic']}"
        
        # Tires
        if any(tire_word in message for tire_word in ['tire', 'tyre']):
            if 'rotat' in message:
                return f"Tire rotation: {self.price_guide['tire']['rotation']}"
            if 'balanc' in message:
                return f"Tire balancing: {self.price_guide['tire']['balance']}"
            if 'align' in message:
                return f"Wheel alignment: {self.price_guide['tire']['alignment']}"
            return "We offer:\n- Rotations\n- Balancing\n- Alignments\nWhich tire service do you need?"
        
        # Brakes
        if 'brake' in message:
            if 'pad' in message:
                return f"Brake pad replacement: {self.price_guide['brake']['pads']}"
            if 'rotor' in message:
                return f"Brake rotor replacement: {self.price_guide['brake']['rotors']}"
            return f"Complete brake service: {self.price_guide['brake']['full service']}"
        
        # Appointments
        if any(word in message for word in ['appointment', 'schedule', 'book']):
            return "Book online at autocare.example.com or call 555-1234"
        
        # Hours/Location
        if any(word in message for word in ['hour', 'time', 'when', 'open']):
            return "We're open:\nMon-Fri: 7:30am-6pm\nSat: 8am-4pm\nSun: Closed"
        
        if any(word in message for word in ['where', 'location', 'address']):
            return "📍 123 Auto Care Lane\nVehicle City, VC 12345"
        
        # Emergency
        if any(word in message for word in ['breakdown', 'emergency', 'tow']):
            return "🚨 For emergencies:\n24/7 Towing: 555-TOWING\nRoadside Assistance: 555-HELP"
        
        # Default
        return "I can help with:\n- Service pricing\n- Appointments\n- Service details\nWhat do you need?"

chatbot = VehicleServiceChatbot()

@require_POST
@csrf_exempt
def chat_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Simulate processing delay
        time.sleep(0.5)
        
        response = chatbot.process_query(user_message)
        return JsonResponse({'response': response})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)