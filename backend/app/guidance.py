"""Sanitized public guidance engine for Digital Krishna AI.

This module demonstrates:

- English, Hindi, and Hinglish responses
- Transparent concern classification
- Structured practical guidance
- Safety-oriented support messaging
- Separation of generated reflection from verified scripture

It contains no API keys, private endpoints, or user records.
"""

from __future__ import annotations

from uuid import uuid4

from .schemas import (
    GuidanceRequest,
    GuidanceResponse,
    PracticalStep,
    ScriptureSource,
)


CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Academic stress": (
        "study",
        "studies",
        "exam",
        "marks",
        "college",
        "school",
        "focus",
        "पढ़ाई",
        "परीक्षा",
        "अंक",
        "ध्यान",
        "padhai",
        "pariksha",
    ),
    "Career uncertainty": (
        "career",
        "job",
        "future",
        "profession",
        "internship",
        "placement",
        "नौकरी",
        "भविष्य",
        "करियर",
        "naukri",
        "bhavishya",
    ),
    "Anger and frustration": (
        "angry",
        "anger",
        "frustrated",
        "irritated",
        "गुस्सा",
        "क्रोध",
        "नाराज़",
        "gussa",
        "krodh",
    ),
    "Fear and worry": (
        "fear",
        "afraid",
        "worried",
        "anxious",
        "nervous",
        "डर",
        "चिंता",
        "घबराहट",
        "dar",
        "chinta",
    ),
    "Motivation and discipline": (
        "motivation",
        "lazy",
        "discipline",
        "procrastinate",
        "unmotivated",
        "आलस",
        "अनुशासन",
        "प्रेरणा",
        "aalas",
        "prerna",
    ),
    "Decision-making": (
        "decision",
        "choose",
        "choice",
        "confused",
        "निर्णय",
        "चुनाव",
        "उलझन",
        "nirnay",
    ),
}


SAFETY_MARKERS: tuple[str, ...] = (
    "immediate danger",
    "not safe",
    "emergency",
    "urgent danger",
    "someone may hurt me",
    "तुरंत खतरा",
    "मैं सुरक्षित नहीं",
    "आपातकाल",
    "turant khatra",
    "safe nahi",
)


CATEGORY_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "General reflection": "General reflection",
        "Academic stress": "Academic stress",
        "Career uncertainty": "Career uncertainty",
        "Anger and frustration": "Anger and frustration",
        "Fear and worry": "Fear and worry",
        "Motivation and discipline": "Motivation and discipline",
        "Decision-making": "Decision-making",
    },
    "hi": {
        "General reflection": "सामान्य आत्मचिंतन",
        "Academic stress": "पढ़ाई का दबाव",
        "Career uncertainty": "करियर की अनिश्चितता",
        "Anger and frustration": "क्रोध और निराशा",
        "Fear and worry": "भय और चिंता",
        "Motivation and discipline": "प्रेरणा और अनुशासन",
        "Decision-making": "निर्णय लेना",
    },
    "hinglish": {
        "General reflection": "General reflection",
        "Academic stress": "Padhai ka pressure",
        "Career uncertainty": "Career uncertainty",
        "Anger and frustration": "Gussa aur frustration",
        "Fear and worry": "Dar aur chinta",
        "Motivation and discipline": "Motivation aur discipline",
        "Decision-making": "Decision-making",
    },
}


def normalize_text(value: str) -> str:
    """Return lowercase text with repeated whitespace removed."""

    return " ".join(value.lower().split())


def classify_concern(message: str) -> str:
    """Classify a concern through transparent keyword matching."""

    normalized = normalize_text(message)

    best_category = "General reflection"
    best_score = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in normalized)

        if score > best_score:
            best_category = category
            best_score = score

    return best_category


def requires_safety_response(message: str) -> bool:
    """Check for a limited set of immediate-safety expressions."""

    normalized = normalize_text(message)

    return any(marker in normalized for marker in SAFETY_MARKERS)


def build_english_content(category: str) -> dict[str, object]:
    """Create an English guidance response."""

    responses: dict[str, dict[str, object]] = {
        "Academic stress": {
            "acknowledgement": (
                "Academic pressure can make every task feel heavier. "
                "You do not need to solve everything at once."
            ),
            "explanation": (
                "Clarity often returns when attention moves from the final "
                "result to the next responsible action within your control."
            ),
            "steps": [
                (
                    "Choose one task",
                    "Select one small topic or assignment instead of trying "
                    "to complete everything together.",
                ),
                (
                    "Use a focused session",
                    "Work for 25 minutes, take a short pause, and then decide "
                    "whether to continue.",
                ),
                (
                    "Measure effort",
                    "Record the effort you made instead of judging yourself "
                    "only by the result.",
                ),
            ],
            "question": (
                "What is the smallest useful study action you can take now?"
            ),
        },
        "Career uncertainty": {
            "acknowledgement": (
                "Uncertainty about the future can feel uncomfortable, "
                "especially when you feel pressure to choose perfectly."
            ),
            "explanation": (
                "A career is usually shaped through skills, experiments, "
                "feedback, and responsible decisions rather than one perfect "
                "prediction."
            ),
            "steps": [
                (
                    "List your strengths",
                    "Write three skills you already possess and one skill "
                    "you want to improve.",
                ),
                (
                    "Run a small experiment",
                    "Complete one project, course, application, or conversation "
                    "that gives you real information.",
                ),
                (
                    "Review the evidence",
                    "Base your next decision on what you learned rather than "
                    "only on fear or comparison.",
                ),
            ],
            "question": (
                "What small experiment could give you useful career evidence "
                "this week?"
            ),
        },
        "Anger and frustration": {
            "acknowledgement": (
                "Anger often appears when something feels unfair, blocked, "
                "or outside your control."
            ),
            "explanation": (
                "Pausing before acting gives you space to choose a response "
                "that protects your values and relationships."
            ),
            "steps": [
                (
                    "Pause the reaction",
                    "Step away briefly before replying or making an important "
                    "decision.",
                ),
                (
                    "Name the concern",
                    "Write what happened, what you expected, and what you need.",
                ),
                (
                    "Choose a calm response",
                    "Return when you can speak clearly without insulting or "
                    "threatening anyone.",
                ),
            ],
            "question": "What need or expectation is underneath your anger?",
        },
        "Fear and worry": {
            "acknowledgement": (
                "Worry can make uncertain possibilities feel like confirmed "
                "outcomes."
            ),
            "explanation": (
                "Separating what is known from what is imagined can reduce "
                "confusion and reveal the next useful action."
            ),
            "steps": [
                (
                    "Separate facts from predictions",
                    "Write what you know for certain and what your mind is "
                    "predicting.",
                ),
                (
                    "Ground your attention",
                    "Take a slow breath and notice your surroundings.",
                ),
                (
                    "Take one controllable action",
                    "Choose one practical step related to the real situation.",
                ),
            ],
            "question": (
                "Which part of this situation is actually within your control?"
            ),
        },
        "Motivation and discipline": {
            "acknowledgement": (
                "Low motivation does not mean you are incapable. The task may "
                "be unclear, too large, or disconnected from a routine."
            ),
            "explanation": (
                "Discipline becomes easier when the first action is small, "
                "specific, and repeated consistently."
            ),
            "steps": [
                (
                    "Reduce the starting point",
                    "Make the first task small enough to begin in five minutes.",
                ),
                (
                    "Create a fixed cue",
                    "Connect the task to a regular time, place, or activity.",
                ),
                (
                    "Track consistency",
                    "Record whether you started, even when the session was short.",
                ),
            ],
            "question": "How can you make the first step easier to begin?",
        },
        "Decision-making": {
            "acknowledgement": (
                "Confusion often grows when several choices contain both "
                "benefits and risks."
            ),
            "explanation": (
                "A thoughtful decision considers values, evidence, likely "
                "consequences, and what can be corrected later."
            ),
            "steps": [
                (
                    "Define the decision",
                    "Write the exact choice you are trying to make.",
                ),
                (
                    "Compare consequences",
                    "List the likely short-term and long-term effects.",
                ),
                (
                    "Check your values",
                    "Choose the option that supports honesty, responsibility, "
                    "and sustainable progress.",
                ),
            ],
            "question": (
                "Which option best matches the person you want to become?"
            ),
        },
    }

    return responses.get(
        category,
        {
            "acknowledgement": (
                "It is understandable to seek clarity when your thoughts and "
                "emotions feel difficult to organise."
            ),
            "explanation": (
                "Reflection becomes more useful when the situation is separated "
                "into facts, feelings, values, and the next practical action."
            ),
            "steps": [
                (
                    "Describe the situation",
                    "Write what happened without judging yourself.",
                ),
                (
                    "Name what matters",
                    "Identify the value or responsibility involved.",
                ),
                (
                    "Choose one next action",
                    "Take one small step that is safe, honest, and achievable.",
                ),
            ],
            "question": (
                "What is one responsible action available to you today?"
            ),
        },
    )


def build_hindi_content() -> dict[str, object]:
    """Create a general Hindi guidance response."""

    return {
        "acknowledgement": (
            "आपकी स्थिति कठिन लग सकती है, लेकिन आपको सब कुछ एक साथ "
            "सुलझाने की आवश्यकता नहीं है।"
        ),
        "explanation": (
            "जब हम परिणाम की चिंता से ध्यान हटाकर अपने नियंत्रण में मौजूद "
            "अगले सही कदम पर रखते हैं, तब स्पष्टता बढ़ती है।"
        ),
        "steps": [
            (
                "स्थिति स्पष्ट करें",
                "जो हुआ है उसे लिखें और अनुमान को तथ्य से अलग करें।",
            ),
            (
                "एक छोटा कदम चुनें",
                "ऐसा कार्य चुनें जिसे आप आज सुरक्षित रूप से पूरा कर सकें।",
            ),
            (
                "शांत होकर समीक्षा करें",
                "कार्य के बाद देखें कि आपने क्या सीखा।",
            ),
        ],
        "question": "आज आपके नियंत्रण में कौन-सा एक उपयोगी कदम है?",
    }


def build_hinglish_content() -> dict[str, object]:
    """Create a general Hinglish guidance response."""

    return {
        "acknowledgement": (
            "Yeh situation difficult lag sakti hai, lekin aapko sab kuch "
            "ek saath solve karne ki zarurat nahi hai."
        ),
        "explanation": (
            "Result ki tension se focus hata kar apne control wale next "
            "responsible step par dhyaan dena clarity badha sakta hai."
        ),
        "steps": [
            (
                "Situation clear karo",
                "Facts ko assumptions se alag karke situation likho.",
            ),
            (
                "Ek small step choose karo",
                "Aaj ka ek safe aur achievable action decide karo.",
            ),
            (
                "Review karo",
                "Action ke baad dekho ki kya seekha.",
            ),
        ],
        "question": "Aaj aapke control mein kaunsa ek useful step hai?",
    }


def generate_guidance(request: GuidanceRequest) -> GuidanceResponse:
    """Generate one structured public demonstration response."""

    category = classify_concern(request.message)

    if request.language == "hi":
        content = build_hindi_content()
    elif request.language == "hinglish":
        content = build_hinglish_content()
    else:
        content = build_english_content(category)

    safety_note: str | None = None

    if requires_safety_response(request.message):
        if request.language == "hi":
            safety_note = (
                "यदि आप अभी सुरक्षित नहीं हैं, तो तुरंत किसी भरोसेमंद वयस्क, "
                "स्थानीय आपातकालीन सेवा या योग्य सहायता प्रदाता से संपर्क करें।"
            )
        elif request.language == "hinglish":
            safety_note = (
                "Agar aap abhi safe nahi hain, turant kisi trusted adult, "
                "local emergency service, ya qualified support provider se "
                "contact karein."
            )
        else:
            safety_note = (
                "If you are not currently safe, contact a trusted adult, "
                "local emergency service, or qualified support provider now."
            )

    practical_steps = [
        PracticalStep(title=title, description=description)
        for title, description in content["steps"]
    ]

    displayed_category = CATEGORY_LABELS[request.language].get(
        category,
        category,
    )

    return GuidanceResponse(
        request_id=str(uuid4()),
        category=displayed_category,
        language=request.language,
        acknowledgement=str(content["acknowledgement"]),
        scripture=ScriptureSource(
            status="none",
            reference=None,
            original_text=None,
            translation=None,
            review_note=(
                "No reviewed scripture record is attached in this sanitized "
                "public demonstration response."
            ),
        ),
        explanation=str(content["explanation"]),
        practical_steps=practical_steps,
        reflection_question=str(content["question"]),
        safety_note=safety_note,
    )
