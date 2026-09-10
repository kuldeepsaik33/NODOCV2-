
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# NODOC v2 - Offline Smart Health Assistant
# Academic prototype. Uses symptom-pattern matching and provides
# general medication information, supportive care, and red flags.
# It is not a diagnostic or prescribing system.

CONDITIONS = {
    # Respiratory / ENT
    "common cold": {"keys": ["runny nose","sneezing","stuffy nose","sore throat","cold"], "care":"Rest, fluids, warm liquids and saline nasal care.", "med":"OTC cold-symptom products may be used only according to their label and age restrictions.", "ayur":"Warm fluids; ginger/tulsi tea may be used as a traditional comfort measure.", "red":"Breathing difficulty, chest pain, confusion, blue/grey lips, or severe worsening."},
    "influenza-like illness": {"keys": ["flu","fever","chills","body ache","muscle ache","cough"], "care":"Rest, fluids and monitor temperature.", "med":"OTC fever/pain medicines may provide symptom relief when label directions are followed.", "ayur":"Warm fluids and rest; traditional remedies should not replace medical evaluation.", "red":"Breathing difficulty, persistent severe symptoms, dehydration, confusion, or high-risk patient."},
    "allergic rhinitis": {"keys": ["sneezing","itchy nose","runny nose","allergy","itchy eyes"], "care":"Avoid known triggers and consider saline nasal care.", "med":"Non-prescription antihistamine or nasal products may be options; follow the package label.", "ayur":"Saline nasal cleansing can be supportive when performed safely.", "red":"Severe breathing difficulty, facial swelling, or rapidly worsening reaction."},
    "sinusitis": {"keys": ["sinus","facial pain","facial pressure","blocked nose","nasal congestion"], "care":"Fluids, rest and saline nasal care may help.", "med":"Symptom-relief medicines can be considered according to label directions; persistent cases need clinician assessment.", "ayur":"Warm fluids and gentle steam may provide comfort.", "red":"Eye swelling, severe headache, confusion, vision changes, or severe illness."},
    "sore throat": {"keys": ["sore throat","throat pain","painful swallowing"], "care":"Warm fluids, hydration and throat soothing measures.", "med":"OTC pain-relief products may help when used according to the label.", "ayur":"Warm salt-water gargling may provide comfort.", "red":"Difficulty breathing, inability to swallow fluids, drooling, or neck swelling."},
    "bronchitis-like cough": {"keys": ["persistent cough","chesty cough","mucus cough","phlegm"], "care":"Fluids, rest and avoid smoke/irritants.", "med":"Cough medicines vary by age and symptoms; use only products appropriate for the user's age and label.", "ayur":"Warm fluids may soothe the throat.", "red":"Coughing blood, chest pain, severe breathing difficulty, or blue/grey lips."},
    "asthma symptom flare": {"keys": ["wheezing","asthma","tight chest","shortness of breath"], "care":"Move away from triggers and follow an existing clinician-provided asthma action plan.", "med":"Use prescribed rescue medication only according to the patient's existing plan.", "ayur":"Do not substitute herbal remedies for prescribed asthma treatment.", "red":"Severe or rapidly worsening breathing difficulty, inability to speak normally, blue/grey lips."},
    # GI
    "indigestion": {"keys": ["indigestion","heartburn","acid reflux","acidity","burning chest"], "care":"Smaller meals and avoiding known trigger foods may help.", "med":"OTC antacid/acid-reducing products have age and interaction restrictions; follow the label.", "ayur":"Avoid heavy meals; warm water may be comforting.", "red":"Severe chest pain, vomiting blood, black stools, fainting, or persistent symptoms."},
    "gas / bloating": {"keys": ["gas","bloating","bloat","flatulence"], "care":"Eat slowly, hydrate and consider smaller meals.", "med":"Some OTC gas-relief products exist; follow label directions and age restrictions.", "ayur":"Gentle warm fluids may be soothing.", "red":"Severe abdominal pain, repeated vomiting, distension with inability to pass stool/gas."},
    "constipation": {"keys": ["constipation","hard stool","difficulty passing stool"], "care":"Increase fluids and dietary fiber gradually; stay physically active.", "med":"OTC laxatives have different indications and age restrictions; use label directions and seek advice for persistent symptoms.", "ayur":"Fiber-rich foods and adequate fluids are supportive.", "red":"Severe pain, vomiting, blood in stool, or inability to pass stool/gas with swelling."},
    "diarrhea": {"keys": ["diarrhea","loose stools","watery stool"], "care":"Focus on oral rehydration and fluids; eat light foods as tolerated.", "med":"Oral rehydration solution is important; anti-diarrheal medicines are not suitable for everyone, especially some children.", "ayur":"Rice-based light foods and fluids can be supportive.", "red":"Severe dehydration, blood in stool, persistent vomiting, fainting, or severe abdominal pain."},
    "nausea": {"keys": ["nausea","feeling sick","queasy"], "care":"Small sips of fluid and small meals may help.", "med":"Anti-nausea medicines require age/condition checks; consult a pharmacist/clinician if persistent.", "ayur":"Ginger-containing food or tea may help some people.", "red":"Repeated vomiting, severe pain, blood, dehydration, confusion."},
    "vomiting": {"keys": ["vomiting","throwing up"], "care":"Take frequent small sips of oral fluids and monitor hydration.", "med":"Medication depends on the cause and age; avoid self-prescribing.", "ayur":"Small amounts of clear fluids may be supportive.", "red":"Blood/coffee-ground vomit, severe pain, dehydration, confusion, or repeated vomiting."},
    "food poisoning pattern": {"keys": ["food poisoning","vomiting and diarrhea","diarrhea and vomiting"], "care":"Hydration and rest are priorities.", "med":"Oral rehydration is useful; antibiotics should not be self-started.", "ayur":"Simple foods and fluids can be supportive.", "red":"Blood in stool, severe dehydration, high fever, severe pain, or worsening illness."},
    # Skin
    "acne": {"keys": ["acne","pimples","blackheads"], "care":"Gentle cleansing and avoid picking lesions.", "med":"OTC acne products can contain benzoyl peroxide or salicylic acid; follow product directions and age warnings.", "ayur":"Gentle skin care; avoid unverified irritant preparations.", "red":"Severe painful lesions, scarring, or widespread reaction."},
    "eczema pattern": {"keys": ["eczema","dry itchy skin","itchy rash","dry skin"], "care":"Use fragrance-free moisturiser and avoid known irritants.", "med":"OTC moisturisers are commonly used; steroid creams require appropriate use and professional advice for some ages/areas.", "ayur":"Gentle moisturising and trigger avoidance are supportive.", "red":"Rapid spreading, fever, pus, facial swelling, or breathing difficulty."},
    "contact dermatitis": {"keys": ["contact rash","irritation rash","rash after product","skin irritation"], "care":"Stop the suspected irritant and gently wash the area.", "med":"Simple moisturisers may help; medication depends on severity and location.", "ayur":"Avoid the trigger; use gentle, fragrance-free skin care.", "red":"Facial swelling, breathing difficulty, blistering over large areas."},
    "fungal skin infection pattern": {"keys": ["ringworm","fungal rash","athlete's foot","itchy circular rash"], "care":"Keep affected skin clean and dry and avoid sharing towels.", "med":"OTC antifungal products exist for some uncomplicated skin infections; follow label directions.", "ayur":"Keep the area dry; do not rely on herbal products as a substitute for proven treatment.", "red":"Extensive infection, diabetes/immunosuppression, facial/genital involvement, or rapid worsening."},
    # Pain / general
    "tension headache": {"keys": ["tension headache","band-like headache","stress headache"], "care":"Hydrate, rest, reduce screen strain and manage stress.", "med":"OTC pain-relief medicines may help some adults when label directions are followed and contraindications are absent.", "ayur":"Relaxation, hydration and gentle neck/shoulder stretching may help.", "red":"Sudden worst-ever headache, weakness, confusion, fainting, seizure, or injury."},
    "migraine pattern": {"keys": ["migraine","throbbing headache","light sensitivity","nausea headache"], "care":"Rest in a quiet/dim room, hydrate and avoid known triggers.", "med":"OTC pain-relief options may help some people; recurrent migraine warrants medical assessment.", "ayur":"Quiet rest and hydration may provide supportive relief.", "red":"New severe headache, neurological deficits, fever with stiff neck, or sudden onset."},
    "back strain": {"keys": ["back pain","lower back pain","back strain"], "care":"Gentle movement and avoiding prolonged bed rest can help uncomplicated strain.", "med":"OTC pain-relief products have important contraindications; follow the label.", "ayur":"Gentle stretching and warm compresses may be supportive.", "red":"Weakness/numbness, loss of bladder/bowel control, fever, major trauma."},
    "muscle strain": {"keys": ["muscle strain","pulled muscle","muscle pain"], "care":"Relative rest and gradual return to activity; protect the painful area.", "med":"OTC pain-relief options may be appropriate for some people according to label directions.", "ayur":"Gentle stretching after the acute phase may be supportive.", "red":"Severe swelling, deformity, inability to use the limb, or major trauma."},
    "menstrual cramps": {"keys": ["period pain","menstrual cramps","period cramps"], "care":"Heat, hydration and gentle activity may help.", "med":"OTC pain-relief medicines can help some people but have age, pregnancy and medical-condition restrictions.", "ayur":"Warm compresses and gentle movement can be supportive.", "red":"Very heavy bleeding, fainting, severe new pain, or possible pregnancy."},
    # Eye / ear
    "conjunctivitis pattern": {"keys": ["pink eye","red eye","eye discharge","itchy red eye"], "care":"Avoid touching/rubbing eyes and wash hands frequently.", "med":"Treatment depends on cause; antibiotics are not appropriate for every red eye.", "ayur":"Clean hands and gentle hygiene; avoid putting unsterile substances in the eye.", "red":"Vision loss, severe eye pain, light sensitivity, injury, or chemical exposure."},
    "earache": {"keys": ["ear pain","earache"], "care":"Keep the ear dry and avoid inserting objects into it.", "med":"Pain-relief medicines may provide symptom relief when label directions are followed.", "ayur":"Warm compress outside the ear may be comforting.", "red":"Severe pain, swelling behind ear, discharge with severe illness, hearing loss, or dizziness."},
    "dental pain": {"keys": ["toothache","tooth pain","dental pain"], "care":"Gentle oral hygiene and arrange dental assessment.", "med":"OTC pain-relief products may help temporarily; antibiotics should not be self-started.", "ayur":"Warm salt-water rinsing may provide temporary comfort.", "red":"Facial/neck swelling, difficulty swallowing/breathing, fever, or rapidly worsening pain."},
    # Urinary
    "urinary tract infection pattern": {"keys": ["uti","burning urination","painful urination","frequent urination"], "care":"Hydrate normally and seek clinical testing when UTI is suspected.", "med":"Antibiotic treatment requires appropriate diagnosis and prescription; do not self-start leftover antibiotics.", "ayur":"Adequate fluids may be supportive but do not replace testing/treatment.", "red":"Fever with flank/back pain, vomiting, pregnancy, blood in urine, or severe illness."},
    "kidney stone pattern": {"keys": ["kidney stone","flank pain","colicky side pain"], "care":"Seek medical assessment, especially for severe pain.", "med":"Pain treatment depends on severity and medical history; evaluation may be needed.", "ayur":"Hydration may be supportive unless a clinician has advised fluid restriction.", "red":"Fever, inability to urinate, severe uncontrolled pain, vomiting."},
    # Common chronic/recognition patterns
    "high blood pressure pattern": {"keys": ["high bp","high blood pressure"], "care":"Arrange proper blood-pressure measurement and medical follow-up.", "med":"Do not start, stop, or change blood-pressure medicine without clinician guidance.", "ayur":"Heart-healthy diet, activity and sleep are supportive.", "red":"Very high reading with chest pain, severe headache, weakness, confusion, or breathing difficulty."},
    "type 2 diabetes symptom pattern": {"keys": ["high sugar","frequent urination and thirst","excess thirst and urination"], "care":"Arrange blood glucose testing and clinical evaluation.", "med":"Diabetes medicines require diagnosis and individualized prescribing.", "ayur":"Balanced diet and physical activity can support health; herbal products may interact with medicines.", "red":"Confusion, severe weakness, vomiting, deep/rapid breathing, or altered consciousness."},
}

# Add additional named patterns to bring the prototype above 100 searchable entries.
EXTRA = [
"allergic conjunctivitis","dry eye","blepharitis","stye","mouth ulcer","gingivitis",
"bad breath","tonsillitis pattern","laryngitis pattern","hoarse voice","snoring",
"sleep difficulty","jet lag","mild dehydration","heat exhaustion","sunburn","minor burn",
"minor cut","minor bruise","sprain","tendinitis","neck strain","joint pain","knee pain",
"foot pain","heel pain","plantar fasciitis pattern","shin splints","leg cramps",
"cold sore","mouth thrush pattern","dandruff","hives","insect bite","mild sun rash",
"scalp irritation","dry lips","nail fungal pattern","warts","corns","callus",
"hair dandruff","motion sickness","travel nausea","mild dizziness","vertigo pattern",
"fainting warning pattern","palpitations warning pattern","chest pain warning pattern",
"shortness of breath warning pattern","swollen legs warning pattern","anemia symptom pattern",
"iron deficiency symptom pattern","vitamin deficiency symptom pattern","fatigue pattern",
"insomnia pattern","stress symptoms","mild anxiety symptoms","low mood symptoms",
"panic-like symptoms","seasonal allergy","dust allergy","pet allergy","food allergy warning",
"bee sting reaction","mild sun headache","heat cramps","sore muscles after exercise",
"exercise fatigue","dehydration after exercise","acid reflux pattern","gastritis pattern",
"stomach ache","abdominal cramps","loss of appetite","mild constipation","hemorrhoid pattern",
"anal fissure pattern","motion-related headache","screen strain","dry throat","postnasal drip",
"nasal congestion","loss of smell","loss of taste","ear fullness","ringing in ears",
"mild hearing difficulty","hoarse cough","dry cough","night cough","morning cough",
"phlegm cough","viral sore throat","viral fever pattern","body ache","chills pattern",
"mild viral illness","hand foot mouth pattern","chickenpox-like rash","measles-like rash warning",
"jaundice warning pattern","severe abdominal pain warning","menstrual irregularity",
"premenstrual symptoms","vaginal itching warning","vaginal discharge warning",
"testicular pain warning","prostate urinary symptoms","erectile difficulty",
"pregnancy warning pattern","postpartum warning pattern","breast pain warning",
"breast lump warning","pelvic pain warning","ovarian cyst symptom pattern",
"endometriosis symptom pattern","pcos symptom pattern","thyroid symptom pattern",
"low blood sugar warning","high blood sugar warning","dehydration warning",
"allergic reaction warning","anaphylaxis warning","stroke warning pattern",
"heart attack warning pattern","seizure warning pattern","meningitis warning pattern",
"appendicitis warning pattern","internal bleeding warning pattern","sepsis warning pattern"
]

for name in EXTRA:
    CONDITIONS.setdefault(name, {
        "keys": [name.replace(" pattern","").replace(" warning","")],
        "care": "This prototype recognizes this symptom/condition pattern. Arrange appropriate medical evaluation for diagnosis and management.",
        "med": "Medication depends on the confirmed cause, age, medical history and other medicines. Use only appropriately labelled OTC products or clinician/pharmacist advice.",
        "ayur": "Use only evidence-aware supportive measures and avoid replacing necessary medical care with unverified remedies.",
        "red": "Seek urgent care for severe, rapidly worsening, or unusual symptoms."
    })

KV = r"""
#:import dp kivy.metrics.dp
BoxLayout:
    orientation: "vertical"
    padding: dp(14)
    spacing: dp(10)

    canvas.before:
        Color:
            rgba: .96,.98,1,1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "NODOC"
        font_size: "30sp"
        bold: True
        color: .05,.25,.45,1
        size_hint_y: None
        height: dp(45)

    Label:
        text: "Offline Smart Health Assistant • v2"
        font_size: "14sp"
        color: .25,.30,.35,1
        size_hint_y: None
        height: dp(25)

    TextInput:
        id: age
        hint_text: "Age"
        input_filter: "int"
        multiline: False
        size_hint_y: None
        height: dp(46)

    Spinner:
        id: gender
        text: "Select sex / gender"
        values: ["Male", "Female", "Other"]
        size_hint_y: None
        height: dp(46)

    TextInput:
        id: symptoms
        hint_text: "Describe symptoms (example: fever, cough, sore throat)"
        multiline: True
        size_hint_y: None
        height: dp(100)

    Button:
        text: "ANALYZE SYMPTOMS"
        size_hint_y: None
        height: dp(50)
        background_normal: ""
        background_color: .08,.42,.72,1
        on_release: app.check_symptoms()

    ScrollView:
        do_scroll_x: False
        Label:
            id: result
            text: app.result_text
            text_size: self.width - dp(16), None
            size_hint_y: None
            height: self.texture_size[1] + dp(25)
            valign: "top"
            padding: dp(8),dp(8)
            color: .08,.10,.12,1

    Label:
        text: "Academic prototype • Offline • Information is not a diagnosis or personalized prescription."
        font_size: "10sp"
        color: .45,.45,.45,1
        size_hint_y: None
        height: dp(30)
"""

class NODOCApp(App):
    result_text = StringProperty("Enter age, sex/gender and symptoms, then tap ANALYZE SYMPTOMS.")

    def check_symptoms(self):
        raw_age = self.root.ids.age.text.strip()
        gender = self.root.ids.gender.text
        symptoms = self.root.ids.symptoms.text.lower().strip()

        if not raw_age or gender == "Select sex / gender" or not symptoms:
            self.result_text = "Please enter age, select sex/gender, and describe the symptoms."
            return

        try:
            age = int(raw_age)
        except ValueError:
            self.result_text = "Please enter a valid age."
            return

        if age < 0 or age > 120:
            self.result_text = "Please enter an age between 0 and 120."
            return

        matches = []
        for name, item in CONDITIONS.items():
            score = sum(1 for k in item["keys"] if k in symptoms)
            if score:
                matches.append((score, name, item))

        matches.sort(key=lambda x: x[0], reverse=True)

        if not matches:
            self.result_text = (
                "NO STRONG MATCH FOUND\n\n"
                "NODOC could not match the reported symptoms to its offline prototype database.\n\n"
                "Try describing the main symptoms more specifically. If symptoms are severe or worsening, seek professional medical care."
            )
            return

        top = matches[:5]
        out = ["NODOC ANALYSIS", "=" * 28, f"Profile: Age {age} • {gender}\n"]
        out.append("LIKELY SYMPTOM/CONDITION PATTERNS")
        for i, (score, name, item) in enumerate(top, 1):
            confidence = min(95, 50 + score * 15)
            out.append(f"\n{i}. {name.title()}  • Match: {confidence}%")
            out.append(f"   Self-care: {item['care']}")
            out.append(f"   Medication information: {item['med']}")
            out.append(f"   Ayurvedic/supportive: {item['ayur']}")
            out.append(f"   WARNING: {item['red']}")

        if age < 18:
            age_note = "Age note: pediatric medication decisions should be checked with a parent/guardian and qualified clinician/pharmacist."
        elif age >= 65:
            age_note = "Age note: older adults may have higher medication sensitivity and interactions; pharmacist/clinician review is important."
        else:
            age_note = "Age note: age can affect medicine choice and safety; follow product-specific age restrictions."

        out.append("\n" + age_note)
        out.append(
            "\n\nIMPORTANT\n"
            "NODOC is an offline academic prototype. Match percentages are software scores, not clinical probabilities. "
            "Medication information is general reference information, not a personalized prescription or dosage calculation. "
            "Do not use NODOC to delay emergency care."
        )
        self.result_text = "\n".join(out)

if __name__ == "__main__":
    NODOCApp().run()
