
import aiohttp
import config
import uuid
import json



LANGS = [
    {'lang_code': 'af', 'lang_title': 'Afrikaans'},
    {'lang_code': 'sq', 'lang_title': 'Albanian'},
    {'lang_code': 'am', 'lang_title': 'Amharic'},
    {'lang_code': 'ar', 'lang_title': 'Arabic'},
    {'lang_code': 'hy', 'lang_title': 'Armenian'},
    {'lang_code': 'az', 'lang_title': 'Azerbaijani'},
    {'lang_code': 'eu', 'lang_title': 'Basque'},
    {'lang_code': 'be', 'lang_title': 'Belarusian'},
    {'lang_code': 'bn', 'lang_title': 'Bengali'},
    {'lang_code': 'bs', 'lang_title': 'Bosnian'},
    {'lang_code': 'bg', 'lang_title': 'Bulgarian'},
    {'lang_code': 'ca', 'lang_title': 'Catalan'},
    {'lang_code': 'ceb', 'lang_title': 'Cebuano'},
    {'lang_code': 'zh-CN', 'lang_title': 'Chinese (Simplified)'},
    {'lang_code': 'zh', 'lang_title': 'Chinese'},
    {'lang_code': 'zh-Hans', 'lang_title': 'Chinese (Simplified)'},
    {'lang_code': 'zh-TW', 'lang_title': 'Chinese (Traditional)'},
    {'lang_code': 'zh-Hant', 'lang_title': 'Chinese (Traditional)'},
    {'lang_code': 'co', 'lang_title': 'Corsican'},
    {'lang_code': 'hr', 'lang_title': 'Croatian'},
    {'lang_code': 'cs', 'lang_title': 'Czech'},
    {'lang_code': 'da', 'lang_title': 'Danish'},
    {'lang_code': 'nl', 'lang_title': 'Dutch'},
    {'lang_code': 'en', 'lang_title': 'English'},
    {'lang_code': 'eo', 'lang_title': 'Esperanto'},
    {'lang_code': 'et', 'lang_title': 'Estonian'},
    {'lang_code': 'fi', 'lang_title': 'Finnish'},
    {'lang_code': 'fr', 'lang_title': 'French'},
    {'lang_code': 'fy', 'lang_title': 'Frisian'},
    {'lang_code': 'gl', 'lang_title': 'Galician'},
    {'lang_code': 'ka', 'lang_title': 'Georgian'},
    {'lang_code': 'de', 'lang_title': 'German'},
    {'lang_code': 'el', 'lang_title': 'Greek'},
    {'lang_code': 'gu', 'lang_title': 'Gujarati'},
    {'lang_code': 'ht', 'lang_title': 'Haitian Creole'},
    {'lang_code': 'ha', 'lang_title': 'Hausa'},
    {'lang_code': 'haw', 'lang_title': 'Hawaiian'},
    {'lang_code': 'he', 'lang_title': 'Hebrew'},
    {'lang_code': 'iw', 'lang_title': 'Hebrew'},
    {'lang_code': 'hi', 'lang_title': 'Hindi'},
    {'lang_code': 'hmn', 'lang_title': 'Hmong'},
    {'lang_code': 'hu', 'lang_title': 'Hungarian'},
    {'lang_code': 'is', 'lang_title': 'Icelandic'},
    {'lang_code': 'ig', 'lang_title': 'Igbo'},
    {'lang_code': 'id', 'lang_title': 'Indonesian'},
    {'lang_code': 'in', 'lang_title': 'Indonesian'},
    {'lang_code': 'ga', 'lang_title': 'Irish'},
    {'lang_code': 'it', 'lang_title': 'Italian'},
    {'lang_code': 'ja', 'lang_title': 'Japanese'},
    {'lang_code': 'jv', 'lang_title': 'Javanese'},
    {'lang_code': 'kn', 'lang_title': 'Kannada'},
    {'lang_code': 'kk', 'lang_title': 'Kazakh'},
    {'lang_code': 'km', 'lang_title': 'Khmer'},
    {'lang_code': 'rw', 'lang_title': 'Kinyarwanda'},
    {'lang_code': 'ko', 'lang_title': 'Korean'},
    {'lang_code': 'ku', 'lang_title': 'Kurdish'},
    {'lang_code': 'ky', 'lang_title': 'Kyrgyz'},
    {'lang_code': 'lo', 'lang_title': 'Lao'},
    {'lang_code': 'la', 'lang_title': 'Latin'},
    {'lang_code': 'lv', 'lang_title': 'Latvian'},
    {'lang_code': 'lt', 'lang_title': 'Lithuanian'},
    {'lang_code': 'lb', 'lang_title': 'Luxembourgish'},
    {'lang_code': 'mk', 'lang_title': 'Macedonian'},
    {'lang_code': 'mg', 'lang_title': 'Malagasy'},
    {'lang_code': 'ms', 'lang_title': 'Malay'},
    {'lang_code': 'ml', 'lang_title': 'Malayalam'},
    {'lang_code': 'mt', 'lang_title': 'Maltese'},
    {'lang_code': 'mi', 'lang_title': 'Maori'},
    {'lang_code': 'mr', 'lang_title': 'Marathi'},
    {'lang_code': 'mn', 'lang_title': 'Mongolian'},
    {'lang_code': 'my', 'lang_title': 'Myanmar (Burmese)'},
    {'lang_code': 'ne', 'lang_title': 'Nepali'},
    {'lang_code': 'no', 'lang_title': 'Norwegian'},
    {'lang_code': 'ny', 'lang_title': 'Nyanja (Chichewa)'},
    {'lang_code': 'or', 'lang_title': 'Odia (Oriya)'},
    {'lang_code': 'ps', 'lang_title': 'Pashto'},
    {'lang_code': 'fa', 'lang_title': 'Persian'},
    {'lang_code': 'pl', 'lang_title': 'Polish'},
    {'lang_code': 'pt', 'lang_title': 'Portuguese'},
    {'lang_code': 'pa', 'lang_title': 'Punjabi'},
    {'lang_code': 'ro', 'lang_title': 'Romanian'},
    {'lang_code': 'ru', 'lang_title': 'Russian'},
    {'lang_code': 'sm', 'lang_title': 'Samoan'},
    {'lang_code': 'gd', 'lang_title': 'Scots Gaelic'},
    {'lang_code': 'sr', 'lang_title': 'Serbian'},
    {'lang_code': 'st', 'lang_title': 'Sesotho'},
    {'lang_code': 'sn', 'lang_title': 'Shona'},
    {'lang_code': 'sd', 'lang_title': 'Sindhi'},
    {'lang_code': 'si', 'lang_title': 'Sinhala'},
    {'lang_code': 'sk', 'lang_title': 'Slovak'},
    {'lang_code': 'sl', 'lang_title': 'Slovenian'},
    {'lang_code': 'so', 'lang_title': 'Somali'},
    {'lang_code': 'es', 'lang_title': 'Spanish'},
    {'lang_code': 'su', 'lang_title': 'Sundanese'},
    {'lang_code': 'sw', 'lang_title': 'Swahili'},
    {'lang_code': 'sv', 'lang_title': 'Swedish'},
    {'lang_code': 'tl', 'lang_title': 'Tagalog (Filipino)'},
    {'lang_code': 'tg', 'lang_title': 'Tajik'},
    {'lang_code': 'ta', 'lang_title': 'Tamil'},
    {'lang_code': 'tt', 'lang_title': 'Tatar'},
    {'lang_code': 'te', 'lang_title': 'Telugu'},
    {'lang_code': 'th', 'lang_title': 'Thai'},
    {'lang_code': 'tr', 'lang_title': 'Turkish'},
    {'lang_code': 'tk', 'lang_title': 'Turkmen'},
    {'lang_code': 'uk', 'lang_title': 'Ukrainian'},
    {'lang_code': 'ur', 'lang_title': 'Urdu'},
    {'lang_code': 'ug', 'lang_title': 'Uyghur'},
    {'lang_code': 'uz', 'lang_title': 'Uzbek'},
    {'lang_code': 'vi', 'lang_title': 'Vietnamese'},
    {'lang_code': 'cy', 'lang_title': 'Welsh'},
    {'lang_code': 'xh', 'lang_title': 'Xhosa'},
    {'lang_code': 'yi', 'lang_title': 'Yiddish'},
    {'lang_code': 'ji', 'lang_title': 'Yiddish'},
    {'lang_code': 'yo', 'lang_title': 'Yoruba'},
    {'lang_code': 'zu', 'lang_title': 'Zulu'}
]





async def paste(content: str, ext: str = "txt"):
    api_url = "https://api.github.com/gists/e08f0a195acf449983815ee7bc3fde4e"
    headers = {
        "Authorization": f"Bearer {config.GIST_TOKEN}",
        "accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    id = f"{uuid.uuid4()}.{ext}"
    payload = {
        "files": {
            id: {
                "content": content
            }
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, data=json.dumps(payload)) as response:
                if response.status != 200:
                    return "Pasting failed"
                results = await response.json()
                files = results['files']
                paste = files.get(id, None)
                paste_url = f"https://gist.github.com/NandhaxD/e08f0a195acf449983815ee7bc3fde4e#file-{id.replace('.', '-')}"
                raw_url = paste['raw_url']
                return f"<b><emoji id=5271604874419647061>🔗</emoji> <a href='{raw_url}'>Pasted link</a></b>"
    except Exception as e:
        return "Pasting failed"
