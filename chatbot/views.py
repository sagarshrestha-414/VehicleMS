

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import json
import random
import time
import requests
import hashlib
from django.conf import settings

class VehicleServiceChatbot:
    def __init__(self):
        self.service_menu = """
        🚗 **Complete Auto Care Services** 🚗

        🔧 **Maintenance Services**:
        - Oil Changes (Conventional: $39.99 | Synthetic: $69.99)
        - Tire Services (Rotation: $24.99 | Balancing: $29.99)
        - Brake Services (Pads: $129.99/axle | Rotors: $249.99/axle)
        - Battery Testing & Replacement
        - AC Recharging & Repair

        🔍 **Diagnostics**:
        - Engine Light Diagnostics: $49.99
        - Computer System Scan
        - Electrical System Check

        🛠️ **Other Services**:
        - Fluid Flushes (Coolant, Transmission)
        - Filter Replacements
        - Suspension Repairs

        📅 **Book Appointment**: Call ☎️ 555-1234 or visit autocare.example.com
        """

        self.local_triggers = [
            'hi', 'hello', 'hey', 'service', 'offer',
            'appointment', 'schedule', 'book', 'hour',
            'time', 'open', 'close', 'where', 'location',
            'address', 'breakdown', 'emergency', 'tow'
        ]

        self.local_responses = {
            # Greetings
            'greeting': [
                "Hello! Welcome to AutoCare. How can we assist with your vehicle today?",
                "Hi there! Ready to service your vehicle? Here's what we offer:\n" + self.service_menu,
                "Welcome! We provide complete vehicle care services. What do you need today?"
            ],
            
            # Service Info
            'service': self.service_menu,
            'services': self.service_menu,
            'offer': self.service_menu,
            
            # Appointments
            'appointment': "📅 Book appointments:\n- Online: autocare.example.com\n- Phone: ☎️ 555-1234\n- In-person: 123 Auto Care Lane",
            'schedule': "We're open for service:\nMon-Fri: 7:30am-6pm\nSat: 8am-4pm\nWalk-ins welcome!",
            'book': "To book your service:\n1. Call ☎️ 555-1234\n2. Visit our website\n3. Stop by our shop",
            
            # Hours
            'hour': "🕒 Service Hours:\nMon-Fri: 7:30am-6pm\nSat: 8am-4pm\nSun: Closed",
            'time': "Our technicians are available:\nWeekdays: 7:30am-6pm\nSaturdays: 8am-4pm",
            'open': "We're open:\nWeekdays: 7:30am-6pm\nSaturdays: 8am-4pm\nClosed Sundays",
            
            # Location
            'where': "📍 Find us at:\n123 Auto Care Lane\nVehicle City, VC 12345\n(Behind the gas station)",
            'location': "Our shop is located at:\n123 Auto Care Lane\nVehicle City, VC 12345\nFree parking available!",
            'address': "Mailing & Service Address:\nAutoCare Center\n123 Auto Care Lane\nVehicle City, VC 12345",
            
            # Emergency
            'emergency': "🚨 **24/7 Roadside Assistance**\nTowing: 555-TOWING\nLockout: 555-LOCK\nJumpstart: 555-JUMP",
            'breakdown': "For breakdowns:\n1. Pull over safely\n2. Call our 24/7 line: 555-HELP\n3. We'll dispatch assistance",
            'tow': "Need a tow? Call our partners:\n- QuickTow: 555-TOW1\n- SafeHaul: 555-TOW2\nWe offer 10% discount for clients!"
        }

        # Comprehensive vehicle technical keywords
        self.vehicle_keywords = [
            # Vehicle Types
            'vehicle', 'auto', 'automobile', 'car', 'truck', 'suv', 'van', 
            'motorcycle', 'sedan', 'coupe', 'hatchback', 'convertible', 'wagon',
            'jeep', 'pickup', 'minivan', 'crossover', 'sports car', 'luxury car',
            'electric vehicle', 'ev', 'hybrid', 'diesel', 'gasoline', '4x4',
            'awd', 'fwd', 'rwd', 'commercial vehicle', 'fleet vehicle',
            
            # Engine Systems (150+ terms)
            'engine', 'motor', 'internal combustion', 'cylinder', 'piston',
            'crankshaft', 'camshaft', 'valve', 'valvetrain', 'timing belt',
            'timing chain', 'tensioner', 'spark plug', 'ignition', 'coil',
            'distributor', 'turbo', 'turbocharger', 'supercharger', 'blower',
            'oil pump', 'oil filter', 'oil pan', 'dipstick', 'fuel injector',
            'fuel pump', 'fuel filter', 'throttle', 'throttle body', 'carburetor',
            'intake', 'intake manifold', 'exhaust', 'exhaust manifold', 'header',
            'catalytic converter', 'muffler', 'resonator', 'o2 sensor',
            'egr', 'pcv', 'vacuum line', 'gasket', 'seal', 'bearing',
            'flywheel', 'harmonic balancer', 'water pump', 'thermostat',
            'radiator', 'coolant', 'antifreeze', 'heater core', 'hose',
            'serpentine belt', 'v belt', 'pulley', 'idler pulley',
            'engine block', 'cylinder head', 'head gasket', 'valve cover',
            'rocker arm', 'pushrod', 'lifter', 'cam follower', 'timing cover',
            'knock sensor', 'map sensor', 'maf sensor', 'iat sensor',
            'crank sensor', 'cam sensor', 'oil pressure sensor', 'coolant temp sensor',
            'engine mount', 'torque mount', 'dogbone mount',
            
            # Transmission (50+ terms)
            'transmission', 'trans', 'clutch', 'gear', 'gearbox', 'shift',
            'shifter', 'automatic', 'manual', 'stick shift', 'cvt',
            'dual clutch', 'dsg', 'torque converter', 'flexplate',
            'drivetrain', 'differential', 'diff', 'transfer case',
            'drive shaft', 'propeller shaft', 'cv joint', 'axle',
            'halfshaft', 'u joint', 'clutch master cylinder',
            'clutch slave cylinder', 'clutch pedal', 'shift fork',
            'synchro', 'gear oil', 'transmission fluid', 'atf',
            'shift solenoid', 'valve body', 'tcm', 'transmission control module',
            
            # Electrical Systems (100+ terms)
            'battery', 'alternator', 'starter', 'solenoid', 'fuse',
            'fusebox', 'relay', 'wiring', 'harness', 'ecu', 'pcm',
            'ecm', 'computer', 'sensor', 'actuator', 'light',
            'headlight', 'taillight', 'brake light', 'turn signal',
            'hazard light', 'fog light', 'daytime running light',
            'bulb', 'led', 'halogen', 'xenon', 'hid', 'dome light',
            'map light', 'license plate light', 'reverse light',
            'instrument cluster', 'gauge', 'speedometer', 'tachometer',
            'odometer', 'fuel gauge', 'temp gauge', 'oil pressure gauge',
            'voltmeter', 'warning light', 'check engine light',
            'abs light', 'airbag light', 'traction control light',
            'stability control light', 'tpms light', 'maintenance light',
            'glow plug', 'ignition switch', 'key fob', 'remote',
            'immobilizer', 'alarm', 'horn', 'wiper', 'washer',
            'window motor', 'window regulator', 'power seat',
            'heated seat', 'ventilated seat', 'steering wheel controls',
            'bluetooth', 'infotainment', 'navigation', 'radio',
            'speaker', 'amplifier', 'subwoofer', 'antenna',
            'backup camera', 'parking sensor', 'blind spot monitor',
            'lane departure', 'adaptive cruise', 'auto high beams',
            
            # Brakes (50+ terms)
            'brake', 'braking', 'caliper', 'rotor', 'disc', 'drum',
            'pad', 'shoe', 'brake fluid', 'dot 3', 'dot 4', 'dot 5',
            'master cylinder', 'brake booster', 'brake line',
            'brake hose', 'proportioning valve', 'abs', 'anti-lock',
            'traction control', 'stability control', 'parking brake',
            'emergency brake', 'e-brake', 'hand brake', 'brake pedal',
            'brake light switch', 'wheel cylinder', 'brake dust',
            'brake noise', 'brake pulsation', 'brake drag',
            'brake fade', 'brake warning light', 'pad wear sensor',
            'brake bleed', 'brake flush', 'brake job',
            
            # Suspension/Steering (80+ terms)
            'suspension', 'shock', 'shock absorber', 'strut',
            'coilover', 'spring', 'coil spring', 'leaf spring',
            'air suspension', 'control arm', 'a arm', 'ball joint',
            'tie rod', 'tie rod end', 'rack', 'pinion', 'steering',
            'steering wheel', 'steering column', 'steering shaft',
            'steering gear', 'steering box', 'steering pump',
            'steering fluid', 'power steering', 'electric steering',
            'alignment', 'wheel alignment', 'toe', 'camber', 'caster',
            'sway bar', 'stabilizer bar', 'end link', 'bushing',
            'subframe', 'knuckle', 'hub', 'wheel bearing',
            'cv axle', 'drive axle', 'strut mount', 'bump stop',
            'jounce bumper', 'ride height', 'leveling system',
            'load leveling', 'suspension warning', 'clunk',
            'rattle', 'bottoming out', 'nose dive', 'body roll',
            'vague steering', 'pulling', 'drift', 'wander',
            
            # Tires/Wheels (50+ terms)
            'tire', 'tyre', 'wheel', 'rim', 'alloy', 'steel wheel',
            'hubcap', 'wheel cover', 'center cap', 'lug nut',
            'wheel bolt', 'tire pressure', 'psi', 'inflation',
            'underinflation', 'overinflation', 'rotation',
            'balancing', 'alignment', 'tread', 'tread depth',
            'treadwear', 'traction', 'summer tire', 'winter tire',
            'all-season', 'all weather', 'run flat', 'spare tire',
            'donut', 'tire chain', 'snow chain', 'stud', 'studded',
            'valve stem', 'tpms', 'tire pressure monitoring',
            'tire wear', 'cupping', 'feathering', 'camber wear',
            'toe wear', 'center wear', 'edge wear', 'patchy wear',
            'bulge', 'bubble', 'sidewall', 'tire repair', 'plug',
            'patch', 'tire change', 'mount', 'demount',
            
            # Fluids/Lubricants (30+ terms)
            'oil', 'engine oil', 'motor oil', 'synthetic oil',
            'conventional oil', 'high mileage oil', 'oil change',
            'oil filter', 'coolant', 'antifreeze', 'transmission fluid',
            'atf', 'gear oil', 'differential fluid', 'transfer case fluid',
            'brake fluid', 'power steering fluid', 'washer fluid',
            'wiper fluid', 'adblue', 'def', 'diesel exhaust fluid',
            'grease', 'lubricant', 'penetrating oil', 'assembly lube',
            'fluid leak', 'oil leak', 'coolant leak', 'fluid level',
            'dipstick', 'overflow tank', 'reservoir',
            
            # Problems/Symptoms (100+ terms)
            'noise', 'sound', 'whine', 'whining', 'squeal', 'squealing',
            'squeak', 'squeaking', 'chirp', 'chirping', 'rattle',
            'rattling', 'clunk', 'clunking', 'knock', 'knocking',
            'ping', 'pinging', 'tick', 'ticking', 'click', 'clicking',
            'tap', 'tapping', 'grind', 'grinding', 'scrape', 'scraping',
            'screech', 'howl', 'howling', 'hum', 'humming', 'buzz',
            'buzzing', 'vibration', 'shake', 'shaking', 'shimmy',
            'wobble', 'pulsation', 'judder', 'surge', 'hesitation',
            'stumble', 'miss', 'misfire', 'stall', 'stalling',
            'rough idle', 'loping idle', 'high idle', 'low idle',
            'hunting idle', 'die', 'dying', 'no start', 'crank no start',
            'hard start', 'slow crank', 'click no start', 'turn over',
            'flooded', 'backfire', 'afterfire', 'pop', 'popping',
            'bang', 'banging', 'explosion', 'detonation', 'pre-ignition',
            'pinging', 'spark knock', 'run on', 'dieseling',
            'overheat', 'overheating', 'hot', 'running hot', 'temp',
            'temperature', 'cool', 'running cool', 'cold', 'warm up',
            'smoke', 'smoking', 'white smoke', 'blue smoke',
            'black smoke', 'gray smoke', 'steam', 'burning smell',
            'oil smell', 'gas smell', 'coolant smell', 'rotten egg smell',
            'leak', 'leaking', 'drip', 'dripping', 'puddle', 'wet spot',
            'consumption', 'oil consumption', 'coolant loss',
            'fluid loss', 'loss of power', 'lack of power', 'sluggish',
            'bog', 'bogging', 'flat spot', 'dead spot', 'hesitation',
            'stumble', 'surge', 'bucking', 'jerking', 'shudder',
            'vibration', 'shake', 'shimmy', 'wander', 'drift', 'pull',
            'lead', 'torque steer', 'brake pull', 'alignment',
            'steering wheel off center', 'loose steering',
            'vague steering', 'tight steering', 'hard steering',
            'no power steering', 'groan', 'moan', 'whir', 'whirring',
            
            # Maintenance/Service (100+ terms)
            'service', 'maintenance', 'repair', 'fix', 'diagnose',
            'diagnosis', 'troubleshoot', 'troubleshooting', 'inspect',
            'inspection', 'check', 'scan', 'code', 'dtc', 'diagnostic',
            'tune', 'tune up', 'adjust', 'adjustment', 'calibrate',
            'calibration', 'reset', 'relearn', 'initialize', 'program',
            'flash', 'update', 'recall', 'tsb', 'technical service bulletin',
            'recall', 'warranty', 'recall work', 'campaign', 'service bulletin',
            'oil change', 'filter change', 'fluid change', 'flush',
            'transmission flush', 'coolant flush', 'brake flush',
            'power steering flush', 'fuel system cleaning', 'injector cleaning',
            'throttle body cleaning', 'carbon cleaning', 'decarbonization',
            'walnut blast', 'induction service', 'fuel treatment',
            'engine treatment', 'seafoam', 'fuel injector cleaner',
            'tune up', 'spark plug change', 'wire change', 'coil change',
            'cap and rotor', 'distributor', 'ignition service',
            'timing belt', 'timing chain', 'water pump', 'serpentine belt',
            'accessory belt', 'belt change', 'pulley', 'tensioner',
            'gasket', 'seal', 'rear main seal', 'valve cover gasket',
            'head gasket', 'intake gasket', 'exhaust gasket',
            'thermostat', 'coolant temp sensor', 'oxygen sensor',
            'o2 sensor', 'air fuel ratio sensor', 'maf sensor',
            'map sensor', 'crank sensor', 'cam sensor', 'knock sensor',
            'wheel speed sensor', 'abs sensor', 'tpms sensor',
            'battery', 'alternator', 'starter', 'fuse', 'relay',
            'bulb', 'light', 'headlight', 'taillight', 'brake light',
            'turn signal', 'horn', 'wiper', 'washer', 'tire',
            'rotation', 'balance', 'alignment', 'brake', 'pad',
            'rotor', 'caliper', 'shoe', 'drum', 'master cylinder',
            'wheel cylinder', 'brake line', 'hose', 'suspension',
            'shock', 'strut', 'spring', 'control arm', 'ball joint',
            'tie rod', 'rack', 'pinion', 'wheel bearing', 'cv axle',
            'drive shaft', 'u joint', 'center support bearing',
            'exhaust', 'muffler', 'catalytic converter', 'o2 sensor',
            'hanger', 'bracket', 'mount', 'engine mount',
            'transmission mount', 'dogbone mount', 'torque mount',
            'ac', 'air conditioning', 'compressor', 'condenser',
            'evaporator', 'receiver drier', 'expansion valve',
            'orifice tube', 'refrigerant', 'freon', 'r134a', 'r1234yf',
            'ac charge', 'ac recharge', 'ac service', 'heater',
            'heater core', 'blend door', 'actuator', 'climate control',
            'auto climate', 'dual zone', 'rear ac', 'rear heat',
            'defroster', 'defogger', 'vent', 'duct', 'filter',
            'cabin filter', 'air filter', 'fuel filter', 'trans filter',
            'oil filter', 'pcv valve', 'egr valve', 'thermostat',
            'coolant', 'antifreeze', 'water pump', 'radiator',
            'hose', 'heater hose', 'radiator hose', 'bypass hose',
            'overflow tank', 'reservoir', 'cap', 'radiator cap',
            'pressure cap', 'cooling system', 'overheat',
            'overheating', 'running hot', 'temp', 'temperature',
            'gauge', 'warning light', 'check engine light',
            'service engine soon', 'maintenance required',
            'oil life', 'oil change', 'tire rotation', 'brake service',
            'fluid service', 'multi-point inspection', 'safety inspection',
            'emissions', 'smog', 'state inspection', 'annual inspection',
            'pre-purchase inspection', 'used car inspection',
            'diagnostic fee', 'labor', 'parts', 'estimate',
            'quote', 'warranty', 'extended warranty', 'aftermarket',
            'oem', 'original equipment', 'genuine parts',
            'aftermarket parts', 'performance parts', 'upgrade',
            'mod', 'modification', 'custom', 'tune', 'chip',
            'programmer', 'flash', 'ecu tune', 'pcm flash',
            'horsepower', 'torque', 'performance', 'mpg',
            'fuel economy', 'gas mileage', 'range', 'electric range',
            'charging', 'charger', 'level 1', 'level 2', 'dc fast charge',
            'battery health', 'battery capacity', 'degradation',
            'regeneration', 'regen', 'dpf', 'def', 'adblue',
            'diesel particulate filter', 'scr', 'selective catalytic reduction',
            'emissions system', 'check engine light', 'cel',
            'diagnostic trouble code', 'dtc', 'code reader',
            'scan tool', 'obd', 'obd2', 'obd ii', 'port',
            'connector', 'interface', 'software', 'app',
            'mobile app', 'vehicle health', 'maintenance reminder',
            'service interval', 'schedule', 'log', 'history',
            'record', 'receipt', 'invoice', 'work order',
            'service writer', 'technician', 'mechanic', 'advisor',
            'shop', 'dealership', 'independent', 'chain',
            'franchise', 'mobile mechanic', 'house call',
            'roadside', 'assistance', 'towing', 'flatbed',
            'wrecker', 'recovery', 'jump start', 'battery jump',
            'boost', 'jumper cables', 'portable jump starter',
            'tire change', 'flat tire', 'spare', 'donut',
            'tire repair', 'plug', 'patch', 'tire inflator',
            'air compressor', 'tire pressure', 'psi',
            'lockout', 'keys locked in', 'key fob', 'remote',
            'transponder', 'chip key', 'smart key', 'proximity',
            'push button start', 'ignition', 'cylinder',
            'fuel delivery', 'out of gas', 'empty', 'fuel',
            'gas', 'petrol', 'diesel', 'def', 'adblue',
            'wrong fuel', 'misfuel', 'contamination',
            'water in fuel', 'bad gas', 'old gas', 'stale',
            'varnish', 'gum', 'deposit', 'carbon', 'build up',
            'sludge', 'varnish', 'gunk', 'dirt', 'debris',
            'contaminant', 'particle', 'metal', 'shaving',
            'fragment', 'chip', 'crack', 'fracture', 'break',
            'snap', 'shear', 'strip', 'round', 'wear',
            'groove', 'score', 'scratch', 'pit', 'pitting',
            'corrosion', 'rust', 'oxidation', 'scale',
            'discoloration', 'stain', 'spot', 'blemish',
            'defect', 'failure', 'malfunction', 'problem',
            'issue', 'concern', 'complaint', 'symptom',
            'condition', 'state', 'status', 'operation',
            'performance', 'behavior', 'characteristic',
            'quality', 'attribute', 'property', 'aspect',
            'factor', 'element', 'component', 'part',
            'assembly', 'module', 'unit', 'system',
            'subsystem', 'section', 'area', 'location',
            'position', 'orientation', 'alignment',
            'adjustment', 'setting', 'configuration',
            'calibration', 'specification', 'tolerance',
            'clearance', 'gap', 'play', 'movement',
            'motion', 'travel', 'stroke', 'throw',
            'rotation', 'revolution', 'cycle', 'phase',
            'stage', 'step', 'process', 'procedure',
            'method', 'technique', 'approach', 'strategy',
            'plan', 'schedule', 'timing', 'sequence',
            'order', 'priority', 'importance', 'urgency',
            'severity', 'criticality', 'impact', 'effect',
            'consequence', 'result', 'outcome', 'solution',
            'fix', 'repair', 'replacement', 'adjustment',
            'service', 'maintenance', 'inspection',
            'diagnosis', 'troubleshooting', 'testing',
            'verification', 'validation', 'confirmation',
            'approval', 'authorization', 'clearance',
            'release', 'completion', 'finish', 'done',
            'ready', 'available', 'operational', 'functional',
            'working', 'running', 'driving', 'operating',
            'performing', 'behaving', 'responding',
            'reacting', 'acting', 'functioning', 'operating',
            'performing', 'serving', 'fulfilling', 'meeting',
            'satisfying', 'complying', 'conforming', 'adhering',
            'following', 'observing', 'maintaining', 'keeping',
            'preserving', 'protecting', 'conserving', 'saving',
            'extending', 'prolonging', 'enhancing', 'improving',
            'upgrading', 'optimizing', 'maximizing', 'increasing',
            'boosting', 'raising', 'elevating', 'enhancing',
            'strengthening', 'fortifying', 'reinforcing',
            'supporting', 'sustaining', 'maintaining', 'preserving',
            'protecting', 'conserving', 'saving', 'extending',
            'prolonging', 'enhancing', 'improving', 'upgrading',
            'optimizing', 'maximizing', 'increasing', 'boosting',
            'raising', 'elevating', 'enhancing', 'strengthening',
            'fortifying', 'reinforcing', 'supporting', 'sustaining',
            'maintaining', 'preserving', 'protecting', 'conserving',
            'saving', 'extending', 'prolonging', 'enhancing',
            'improving', 'upgrading', 'optimizing', 'maximizing',
            'increasing', 'boosting', 'raising', 'elevating',
            'enhancing', 'strengthening', 'fortifying', 'reinforcing',
            'supporting', 'sustaining', 'maintaining', 'preserving',
            'protecting', 'conserving', 'saving', 'extending',
            'prolonging', 'enhancing', 'improving', 'upgrading',
            'optimizing', 'maximizing', 'increasing', 'boosting',
            'raising', 'elevating', 'enhancing', 'strengthening',
            'fortifying', 'reinforcing', 'supporting', 'sustaining'

        ]

    def _generate_cache_key(self, message):
        """Generate consistent cache key for messages"""
        return f"chat_response_{hashlib.md5(message.encode()).hexdigest()}"

    def get_local_response(self, message):
        """Handle all basic queries instantly"""
        message_lower = message.lower().strip()
        
        if any(greeting in message_lower for greeting in ['hi', 'hello', 'hey']):
            return random.choice(self.local_responses['greeting'])
            
        for trigger, response in self.local_responses.items():
            if trigger != 'greeting' and trigger in message_lower:
                return response
                
        return None

    def get_ai_response(self, message):
        """Optimized for fast technical responses with caching"""
        cache_key = self._generate_cache_key(message)
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": f"""<|system|>
                    As an auto expert, provide concise answers:
                    - 1 sentence problem identification
                    - Top 1-2 likely causes
                    - Urgency level (❗Low/❗❗Medium/❗❗❗High)
                    - Recommended action
                    Max 3 sentences. If unsure, recommend visit.
                    Services: {self.service_menu}
                    </s>
                    <|user|>{message}</s>
                    <|assistant|>""",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_ctx": 1024,  # Reduced for speed
                        "num_gpu": 1
                    }
                },
                timeout=15  # Faster timeout
            )
            response.raise_for_status()
            ai_response = response.json().get('response')
            
            # Cache successful responses
            if ai_response and len(ai_response) > 10:  # Don't cache empty/short responses
                cache.set(cache_key, ai_response, timeout=3600)  # Cache for 1 hour
            
            return ai_response
        except requests.exceptions.Timeout:
            return self._get_fallback_response(message)
        except Exception as e:
            print(f"AI Error: {e}")
            return self._get_fallback_response(message)

    def _get_fallback_response(self, message):
        """Smart fallback responses based on message content"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['brake', 'stop', 'pedal']):
            return "🚨 Urgent brake issue detected! Call ☎️ 555-1234 immediately"
        elif any(word in message_lower for word in ['engine', 'overheat', 'smoke']):
            return "⚠️ Engine concern! Please call ☎️ 555-1234 now"
        return "For expert diagnosis, visit our shop at 123 Auto Care Lane"

    def should_use_ai(self, message):
        """Determine if query requires technical AI response"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.vehicle_keywords)

    def process_query(self, message):
        """Optimized query routing with fast failover"""
        message_lower = message.lower()
        
        # Immediate local responses for basic queries
        local_response = self.get_local_response(message)
        if local_response and not any(keyword in message_lower for keyword in self.vehicle_keywords):
            return local_response
            
        # AI responses for technical queries
        return self.get_ai_response(message)

chatbot = VehicleServiceChatbot()

@require_POST
@csrf_exempt
def chat_api(request):
    """Optimized API endpoint with caching and fast responses"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
            
        start_time = time.time()
        response = chatbot.process_query(user_message)
        response_time = time.time() - start_time
        
        # Service detection
        suggested_services = []
        if response:
            response_lower = response.lower()
            service_triggers = {
                'oil': 'Oil Change',
                'tire': 'Tire Service',
                'rotation': 'Tire Service',
                'balance': 'Tire Service',
                'brake': 'Brake Service',
                'battery': 'Battery Check',
                'diagnos': 'Diagnostic'
            }
            
            for trigger, service in service_triggers.items():
                if trigger in response_lower:
                    suggested_services.append(service)
        
        return JsonResponse({
            'response': response,
            'response_time': f"{response_time:.2f}s",
            'is_technical': chatbot.should_use_ai(user_message),
            'suggested_services': list(set(suggested_services))  # Remove duplicates
        })
        
    except Exception as e:
        return JsonResponse({
            'response': "Our systems are busy. Please call ☎️ 555-1234",
            'status': 'error',
            'error': str(e)
        }, status=500)
    


    