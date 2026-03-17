import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"



# -----------------------------------------------------
# TONE DEPTH MAP
# -----------------------------------------------------
DEPTH_TONE = {
    "light": "simple, gentle, easy-to-understand emotional language",
    "medium": "clear, honest, emotionally calm language",
    "deep": "deep but simple emotions, clear words, no complex vocabulary"
}

SUPPORTED_LANGUAGES = {
    "en": "English",
    "english": "English",
    "hi": "Hindi",
    "hindi": "Hindi"
}


# -----------------------------------------------------
# SIMPLE EMOTIONAL TEMPLATES FOR 8 MODES
# -----------------------------------------------------

DASHBOARD_REFLECTION = """
You are HeartNote Reflection Writer.

Write the response in {language}.

Write a simple, emotional reflection that feels human and relatable.

INPUT:
- Topic: {name}
- Feeling: {desc}
- Tone: {tone}

RULES:
- Two paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Use simple, clear language
-If the input is vague, do not invent new events.
Keep the writing simple and general.
-- Do not include realizations or life conclusions.
- Focus only on the moment.
- Avoid complex or poetic vocabulary
- Emotional but natural tone
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- No advice
- No motivation
- No emojis

Generate only the reflection.
"""


DASHBOARD_LETTER = """
You are HeartNote Letter Writer.

Write the response in {language}.

INPUT:
Recipient: {name}
Feeling: {desc}
Tone depth: {tone}

RULES:
- Write exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Use simple, clear emotional language
- Gentle and honest tone
- Avoid dramatic phrases.
- Avoid emotional clichés.
- Emotional but natural, not dramatic
- Avoid complex or rare words
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- No advice
- No moralizing
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- No judgement
- No motivational tone
- No lists
- No emojis

Format:
Start with:
Dear You,
"""




DASHBOARD_POEM = """
You are HeartNote Poem Writer.

Write the response in {language}.

Write a gentle emotional poem inspired by:
{name} — {desc}

RULES:
- 5–7 short lines
- Free verse
- Calm, emotional, human language
- Focus on feeling, not explanation
- No advice
- Use physical images (hands, room, light, chair, rain)
- Avoid abstract words like destiny, forever, soul, heartache.
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- No motivation
- No emojis

Generate only the poem.
"""

DASHBOARD_STORY = """
You are HeartNote Story Writer.

Write the response in {language}.

Write a short emotional micro-story inspired by:
{name} — {desc}

RULES:
- 45–70 words
- One emotional moment
- Simple, human language
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- Soft emotional ending
- End with a small physical detail instead of a life conclusion.
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- No advice
- No lessons
- No emojis

Generate only the story.
"""


DASHBOARD_JOURNAL = """
You are HeartNote Journal Writer.

Write the response in {language}.

Write a calm emotional journal entry.

INPUT:
- Topic/person: {name}
- Feeling: {desc}

RULES:
- Write exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- Do not begin with “Today was…”
- Reflective, neutral tone
- No advice
- No lessons
- No emojis
- No signature

Format:
Start with:
Date: {date}

<journal entry>

"""

DASHBOARD_MESSAGES = """
You are HeartNote Message Writer.

Write the response in {language}.

Write a short emotional message someone might want to send.

INPUT:
- Person: {name}
- Feeling: {desc}
- Tone depth: {tone}

RULES:
- 1–2 short paragraphs
- Total length: 25–45 words
- Simple, natural language
- Honest but calm tone
- Focus on what the person wants to say
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- No advice
- No life lessons
- No emojis

Generate only the message.
"""

DASHBOARD_MEMORIES = """
You are HeartNote Memory Writer.

Write the response in {language}.

Write a short emotional memory reflection.

INPUT:
- Memory topic: {name}
- Feeling: {desc}
- Tone depth: {tone}

RULES:
- Exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Focus on a past moment
- Describe a small detail or scene
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- No advice
- No life lessons
- No motivational tone
- No emojis

Generate only the memory reflection.
"""

DASHBOARD_CHECKIN = """
You are HeartNote Gentle Check-In Writer.

Write the response in {language}.

Write a short weekly emotional reflection based on the user's writing theme.

INPUT:
- Focus: {name}
- Feeling context: {desc}

RULES:
- Write exactly 2 short paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Calm, reflective tone
- Focus on awareness, not advice
- Do NOT give solutions or guidance
- Do NOT sound like therapy
- Avoid dramatic or poetic language
- Use simple human words
-If the input is vague, do not invent events.
Keep the reflection general.
- Do NOT use phrases like:
  “everything happens for a reason”
  “stay strong”
  “life lesson”
  “ups and downs”
- No advice
- No motivation
- No emojis

Goal:
A quiet moment of emotional awareness.

Generate only the reflection.
"""




# -----------------------------------------------------
# LLM SERVICE
# -----------------------------------------------------
class Dashboard_LLM_Service:

    def __init__(self, model=MODEL_NAME):
        self.model = model

    # -------------------------------------------------
    # MAIN GENERATE
    # -------------------------------------------------
    def generate(self, mode, name, desc, depth, language):
        mode = (mode or "").lower().strip()
        depth = (depth or "light").lower().strip()
        raw_lang = (language or "en").lower().strip()
        language = SUPPORTED_LANGUAGES.get(raw_lang, "English")
        tone = DEPTH_TONE.get(depth, DEPTH_TONE["light"])

        # 1️⃣ Safety filter (ONLY for bad words / self-harm)
        safe, safe_message = self.safety_filter(desc)
        if not safe:
            return {
                "response": safe_message,
                "blocked": True,
                "is_fallback":False
            }

        # 2️⃣ Template selection
        template = self.get_template(mode)
        if not template:
            return {
                "response": "This writing mode is not available right now.",
                "blocked": False,
                'is_fallback':True
            }

        # 3️⃣ Prompt build
        date = datetime.now().strftime("%d/%m/%Y")

        try:
            prompt = template.format(
                name=name,
                desc=desc,
                tone=tone,
                depth=depth,
                language=language,
                date=date
            )
        except Exception:
            prompt = template.format(name=name, desc=desc, tone=tone,language=language)

        full_prompt = f"[LANG={language}]\n{prompt}"

        # 4️⃣ Ollama call (GUARANTEED STRING RETURN)
        try:
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {"temperature": 0.6}
            }

            res = requests.post(OLLAMA_URL, json=payload, timeout=30)
            res.raise_for_status()

            raw = res.json().get("response")

            # ✅ HARD GUARANTEE
            if not isinstance(raw, str) or not raw.strip():
                return {
                "response": (
                "The words feel quiet right now.\n\n"
                "Some feelings take a moment before they find language."
                ),
        "blocked": False,
        "is_fallback": True
    }


            return {
    "response": raw.strip(),
    "blocked": False,
    "is_fallback": False
}


        except Exception:
            return {
        "response": (
            "The thoughts are still forming.\n\n"
            "Please try again in a moment."
        ),
        "blocked": False,
        "is_fallback": False
    }


    # -------------------------------------------------
    # TEMPLATE ROUTER
    # -------------------------------------------------
    def get_template(self, mode):
        return {
            "reflection": DASHBOARD_REFLECTION,
            "letters": DASHBOARD_LETTER,
            "poems": DASHBOARD_POEM,
            "story": DASHBOARD_STORY,
            "journal": DASHBOARD_JOURNAL,
            "messages": DASHBOARD_MESSAGES,
            "memories": DASHBOARD_MEMORIES,
            "checkin": DASHBOARD_CHECKIN

        }.get(mode)

    # -------------------------------------------------
    # SAFETY FILTER (MINIMAL)
    # -------------------------------------------------
    def safety_filter(self, text):
        t = (text or "").lower()

        bad_words = [
            "fuck", "bitch", "shit", "asshole",
            "bastard", "slut", "dick", "pussy"
        ]
        for w in bad_words:
            if w in t:
                return False, "⚠️ Please rewrite using respectful language."

        selfharm = [
            "kill myself", "i want to die", "end my life",
            "self harm", "no reason to live"
        ]
        for s in selfharm:
            if s in t:
                return False, (
                    "⚠️ HeartNote AI cannot generate this.\n\n"
                    "• You matter.\n"
                    "• You are not alone.\n"
                    "• Support is available."
                )

        return True, text