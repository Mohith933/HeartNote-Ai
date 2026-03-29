import requests
from datetime import datetime
import os
import time



# ------------------------------------------
# TONE STYLES
# ------------------------------------------
TONE_MAP = {
    "soft": "Write gently. Keep it simple and warm.",
    "balanced": "Write naturally. Keep it honest and clear.",
    "deep": "Write with emotional weight. Use one real detail. Keep sentences short."
}






# ------------------------------------------
# TEMPLATES
# ------------------------------------------

LETTER_TEMPLATE = """
Write a short personal letter based only on this real event:
{content}

Rules:
- 50–60 words
- 3–4 sentences
- No new events or characters
- No advice or life lessons
- Focus only on internal feelings
- Tone: {tone}
- End naturally. Do not cut mid-sentence.

Start directly as a personal letter. Do not use placeholders.

Return only the letter.
"""






JOURNAL_TEMPLATE = """
Write a journal entry about this real event:
{content}

Rules:
- 50–70 words
- 4–6 sentences
- Mention one concrete detail
- No advice or philosophy
- Tone: {tone}
- End naturally. Do not cut mid-sentence.

Start with:
Date: {date}

Return only the journal entry.
"""




# POEM_TEMPLATE = """
# Write a short poem based only on:
# {content}

# Rules:
# - Exactly 4 short lines
# - Concrete imagery only
# - No rhyming
# - Tone: {tone}

# Return only the poem.
# """


REFLECTION_TEMPLATE = """
Write a short reflection based only on:
{content}

Rules:
- 40–60 words
- 3–5 sentences
- Mention one concrete detail
- No advice or general life statements
- Tone: {tone}
- End naturally. Do not cut mid-sentence.

Return only the reflection.
"""



# STORY_TEMPLATE = """
# Write a very short story based only on:
# {content}

# Rules:
# - 2–3 sentences
# - Focus on one small physical action
# - No moral or philosophical ending
# - Tone: {tone}

# Return only the story.
# """




# ------------------------------------------
# LLM SERVICE (GEMINI ONLY)
# ------------------------------------------
class LLM_Service:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")


    # ------------------------------------------
    # GEMINI CALL
    # ------------------------------------------
    def call_gemini(self, prompt, model="flash"):

        # Model selection
        if model == "pro":
            model_name = "gemini-1.5-pro"
        else:
            model_name = "gemini-2.5-flash"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.9,
                "maxOutputTokens": 300
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()

            # ✅ safer extraction
            return data.get("candidates", [{}])[0]\
                       .get("content", {})\
                       .get("parts", [{}])[0]\
                       .get("text", "⚠️ No response").strip()

        except Exception as e:
            return f"⚠️ Gemini error: {str(e)}"


    # ------------------------------------------
    # MAIN GENERATE FUNCTION
    # ------------------------------------------
    def generate(self, mode, text, tone="soft"):

        tone_style = TONE_MAP.get(tone, TONE_MAP["soft"])
        mode = mode.lower().strip()

        # Safety first
        safe, result = self.safety_filter(text)
        if not safe:
            return result

        # Build prompt
        prompt = self.build_prompt(mode, text, tone_style)

        if prompt is None:
            return "⚠️ Unknown mode."

        # 🔥 SMART MODEL SWITCHING
        if tone == "deep":
            model_type = "pro"     # better emotional depth
        else:
            model_type = "flash"   # faster

        return self.call_gemini(prompt, model=model_type)


    # ------------------------------------------
    # PROMPT BUILDER
    # ------------------------------------------
    def build_prompt(self, mode, text, tone):

        if mode == "letter":
            return LETTER_TEMPLATE.format(content=text, tone=tone)

        elif mode == "journal":
            date_str = datetime.now().strftime("%d/%m/%Y")
            return JOURNAL_TEMPLATE.format(date=date_str, content=text, tone=tone)

        elif mode == "reflection":
            return REFLECTION_TEMPLATE.format(content=text, tone=tone)

        else:
            return None   # ✅ important fallback


    # ------------------------------------------
    # SAFETY FILTER
    # ------------------------------------------
    def safety_filter(self, text):

        text_lower = text.lower().strip()

        bad_words = [
            "fuck", "bitch", "shit", "asshole",
            "bastard", "slut", "dick", "pussy",
            "kill you", "hurt you"
        ]

        for w in bad_words:
            if w in text_lower:
                return False, "⚠️ Please rewrite without harmful language."

        selfharm_patterns = [
            "kill myself", "kill me", "i want to die",
            "end my life", "i want to disappear",
            "i hurt myself", "self harm",
            "i can't live", "no reason to live"
        ]

        for pattern in selfharm_patterns:
            if pattern in text_lower:
                return False, (
                    "⚠️ I can’t continue this.\n\n"
                    "You deserve care.\n"
                    "You are not alone.\n"
                    "Your feelings matter."
                )

        return True, text