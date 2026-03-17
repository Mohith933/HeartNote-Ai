import requests
from datetime import datetime


# ------------------------------------------
# TONE STYLES
# ------------------------------------------
TONE_MAP = {
    "soft": "Use short sentences. Use simple words. Keep emotions light and calm.",
    "balanced": "Use clear and direct sentences. Stay grounded. No dramatic language.",
    "deep": "Use short sentences. Mention one physical reaction (e.g., heavy chest, quiet room). Avoid abstract words."
}






# ------------------------------------------
# TEMPLATES
# ------------------------------------------

LETTER_TEMPLATE = """
Letter

Write a short personal letter based only on this real event:

{content}

STRICT RULES:
- 50–60 words only
- Exactly 3–4 sentences
- Do NOT invent new characters or events
- Focus only on the writer's internal feeling
- If the input is vague, do not invent details. Keep it simple.
- No advice
- No life lessons
- No clichés
- Tone style: {tone}

Format:

Dear You,
"""






JOURNAL_TEMPLATE = """
Journal

Write a personal journal entry about this real event:
{content}

STRICT RULES:
- 50–70 words only
- Exactly 4–6 sentences
- Mention one specific detail from the moment
- No advice
- No philosophy
- If the input is vague, keep it general and do not invent events
- Tone style: {tone}
- Simple, honest English

Format:

Date: {date}
Write as if this happened today.
"""




POEM_TEMPLATE = """
Poem

Write a short emotional poem based only on:
{content}

STRICT RULES:
- Exactly 4 short lines
- Use concrete words (hands, room, chair, rain, glass)
- No rhyming
- No abstract philosophy
- If input is vague, keep imagery simple
- Tone style: {tone}

Respond ONLY with the poem.
"""


REFLECTION_TEMPLATE = """
Reflection

Write a personal reflection based strictly on this real moment:
{content}

STRICT RULES:
- 40–60 words only
- Exactly 3–5 sentences
- Mention one concrete detail
- No advice
- No life lessons
- No general statements about life
- If input is vague, do not invent events
- Tone style: {tone}

Respond ONLY with the reflection.
"""



STORY_TEMPLATE = """
Story

Write a very short emotional story based only on:
{content}

STRICT RULES:
- Exactly 2–3 sentences
- Focus on one small physical action
- No moral lesson
- No philosophical ending
- If input is vague, keep it minimal
- Tone style: {tone}

Respond ONLY with the story.
"""





# ------------------------------------------
# LLM SERVICE (GEMINI ONLY)
# ------------------------------------------
class LLM_Service:

    def __init__(self):
        pass

    # -------------------------
    # Gemini API call
    # -------------------------
    def call_ollama(self, prompt, model="llama3.2:3b"):
        url = "http://localhost:11434/api/generate"
        payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
       "options": {"temperature": 0.5,"top_p": 0.9}
        }
        try:
            response = requests.post(url, json=payload)
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"⚠️ Ollama error: {str(e)}"


    # -------------------------
    # Router
    # -------------------------
    def generate(self, mode, text, tone="soft"):
        tone_style = TONE_MAP.get(tone, TONE_MAP["soft"])
        mode = mode.lower().strip()

        # Select template
        prompt = self.build_prompt(mode, text, tone_style)
        safe, result = self.safety_filter(text)
        if not safe:
            return result


        if prompt is None:
            return "⚠️ Unknown mode."

        return self.call_ollama(prompt, model="llama3.2:3b")

    # -------------------------
    # Template selection
    # -------------------------
    def build_prompt(self, mode, text, tone):
        if mode == "letter":
            return LETTER_TEMPLATE.format(content=text, tone=tone)
        
        

        elif mode == "journal":
            date_str = datetime.now().strftime("%d/%m/%Y")
            return JOURNAL_TEMPLATE.format(date=date_str, content=text, tone=tone)

        elif mode == "poem":
            return POEM_TEMPLATE.format(content=text, tone=tone)
        elif mode == "reflection":
            return REFLECTION_TEMPLATE.format(content=text, tone=tone)

        elif mode == "story":
            return STORY_TEMPLATE.format(content=text, tone=tone)
        return None
    

    def safety_filter(self, text):
        text_lower = text.lower().strip()

    # --------------------------------------
    # BAD WORD BLOCK
    # --------------------------------------
        bad_words = [
            "fuck", "bitch", "shit", "asshole",
            "bastard", "slut", "dick", "pussy",
            "kill you", "hurt you"  # generic abuse
        ]
        for w in bad_words:
            if w in text_lower:
                return False, "⚠️ Your input contains unsafe or harmful language. Please rewrite it more respectfully."

        selfharm_patterns = [
        "kill myself",
        "kill me",
        "i want to die",
        "end my life",
        "i want to disappear",
        "i hurt myself",
        "self harm",
        "i can't live",
        "no reason to live",
    ]
        for pattern in selfharm_patterns:
            if pattern in text_lower:
                return False, (
                "⚠️ HeartNote AI cannot continue this request.\n"
                "You are feeling something heavy.\n"
                "Here is a gentle, safe message instead:\n\n"
                "• You deserve care.\n"
                "• You are not alone.\n"
                "• Your feelings matter.\n"
            )
            
        return True, text

