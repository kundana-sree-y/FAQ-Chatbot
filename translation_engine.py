
import re

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

MODEL_NAME = "facebook/nllb-200-distilled-600M"

# Common language codes supported by NLLB.
LANGUAGES = {
    "en": ("eng_Latn", "English"),
    "te": ("tel_Telu", "Telugu"),
    "hi": ("hin_Deva", "Hindi"),
    "ta": ("tam_Taml", "Tamil"),
    "kn": ("kan_Knda", "Kannada"),
    "ml": ("mal_Mlym", "Malayalam"),
    "bn": ("ben_Beng", "Bengali"),
    "mr": ("mar_Deva", "Marathi"),
    "gu": ("guj_Gujr", "Gujarati"),
    "pa": ("pan_Guru", "Punjabi"),
    "ur": ("urd_Arab", "Urdu"),
    "es": ("spa_Latn", "Spanish"),
    "fr": ("fra_Latn", "French"),
    "de": ("deu_Latn", "German"),
    "it": ("ita_Latn", "Italian"),
    "pt": ("por_Latn", "Portuguese"),
    "ru": ("rus_Cyrl", "Russian"),
    "ar": ("arb_Arab", "Arabic"),
    "zh-cn": ("zho_Hans", "Chinese"),
    "ja": ("jpn_Jpan", "Japanese"),
    "ko": ("kor_Hang", "Korean"),
    "tr": ("tur_Latn", "Turkish"),
    "id": ("ind_Latn", "Indonesian"),
    "th": ("tha_Thai", "Thai"),
    "vi": ("vie_Latn", "Vietnamese"),
    "sw": ("swh_Latn", "Swahili"),
}

SCRIPT_PATTERNS = [
    (r"[\u0C00-\u0C7F]", "te"),       # Telugu
    (r"[\u0900-\u097F]", "hi"),       # Devanagari
    (r"[\u0B80-\u0BFF]", "ta"),       # Tamil
    (r"[\u0C80-\u0CFF]", "kn"),       # Kannada
    (r"[\u0D00-\u0D7F]", "ml"),       # Malayalam
    (r"[\u0980-\u09FF]", "bn"),       # Bengali
    (r"[\u0A80-\u0AFF]", "gu"),       # Gujarati
    (r"[\u0A00-\u0A7F]", "pa"),       # Punjabi
    (r"[\u0600-\u06FF]", "ur"),       # Arabic/Urdu script
    (r"[\u3040-\u30FF]", "ja"),       # Japanese
    (r"[\uAC00-\uD7AF]", "ko"),       # Korean
    (r"[\u4E00-\u9FFF]", "zh-cn"),    # Chinese
    (r"[\u0400-\u04FF]", "ru"),       # Cyrillic
    (r"[\u0E00-\u0E7F]", "th"),       # Thai
]


class TranslationEngine:

    def __init__(self):
        print("Loading CampusAI translation model...")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print("Translation device:", self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        self.model.to(self.device)
        self.model.eval()

        print("Translation model loaded successfully.")

    def detect_language(self, text):

        # Detect languages that use distinctive writing systems first.
        for pattern, language_code in SCRIPT_PATTERNS:
            if re.search(pattern, text):
                return language_code

        try:
            detected = detect(text)
            if detected in LANGUAGES:
                return detected
        except Exception:
            pass

        return "en"

    def translate(self, text, source_code, target_code):

        if not text.strip():
            return text

        if source_code == target_code:
            return text

        if source_code not in LANGUAGES or target_code not in LANGUAGES:
            raise ValueError("This language is not configured in CampusAI.")

        source_nllb = LANGUAGES[source_code][0]
        target_nllb = LANGUAGES[target_code][0]

        self.tokenizer.src_lang = source_nllb

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)

        target_id = self.tokenizer.convert_tokens_to_ids(target_nllb)

        with torch.no_grad():
            translated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=target_id,
                max_length=512,
                num_beams=4
            )

        return self.tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True
        )[0]


_engine = None


def get_translation_engine():

    global _engine

    if _engine is None:
        _engine = TranslationEngine()

    return _engine
