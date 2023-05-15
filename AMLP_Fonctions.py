import pandas as pd 
import re 
import emoji
import numpy as np


def get_emoji_regexp():
    # Sort emoji by length to make sure multi-character emojis are
    # matched first
    emojis = sorted(emoji.EMOJI_DATA, key=len, reverse=True)
    pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
    return re.compile(pattern)

def remove_emojis(text):
    import emoji
    # remove emojis from the text
    text = get_emoji_regexp().sub(r'', text)
    return text


def Clean_Data(data,cmt_col,Commter_name_col):
    
    data=pd.DataFrame(data=data, index=None, columns=[Commter_name_col,cmt_col])
    df=data
    # replace any value in the names column that appears in the comments column with an empty string
    for name in df[Commter_name_col]:
      df[cmt_col] = df[cmt_col].str.replace(name, '')

    pattern = re.compile(
                     u'[\U0001F600-\U0001F64F]'   # emoticons
                     u'|[\U0001F300-\U0001F5FF]'  # symbols & pictographs
                     u'|[\U0001F680-\U0001F6FF]'  # transport & map symbols
                     u'|[\U0001F1E0-\U0001F1FF]'  # flags (iOS)
                     r'|\#\w+'                    # hashtag
                     r'|(\w)\1+'                  # elongated words
                     r'|(https?://\S+|www\.\S+|\S+\.\S+)' # links
                     r'(?:(?!http|www)[\S])+[.][a-z]{2,4}(?:\/[\S]+)?\/?')
              
    # Apply the regex to the 'text' column to remove all emojis

    df[cmt_col] = df[cmt_col].str.replace(pattern, '')
    df=df.replace('',np.nan)
    df=df.replace(' ',np.nan)
    df=df.dropna(axis=0)
    return df

def remove_symbols(cmt):
    # Remove all non-alphanumeric characters from the string
    output_cmt = re.sub(r'\W+', ' ', cmt)
    return output_cmt


from deep_translator import GoogleTranslator
def translate_char(cmt):
    
    if any(char in 'abcdefghijklmnopqrstuvwxyz' for char in cmt.lower()):
        name_translated = GoogleTranslator('fr', 'ar').translate(cmt)
        return name_translated
    else:
        return cmt


