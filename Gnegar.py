# -*- coding: utf-8 -*-

import re
import sys

text = ""
fix_dashes = True
fix_three_dots = True
fix_english_quotes = True
fix_hamzeh = True
hamzeh_with_yeh = True
cleanup_zwnj = False
fix_spacing_for_braces_and_quotes = True
fix_arabic_numbers = True
fix_english_numbers = True
fix_misc_non_persian_chars = True
fix_perfix_spacing = True
fix_suffix_spacing = True
aggresive = True
cleanup_kashidas = True
cleanup_extra_marks = True
cleanup_spacing = True


def cleanup(text):
    """
    This is the main function who call other functions if need!
    """
    if fix_dashes:
        text = fix_dashes_func(text)

    if fix_three_dots:
        text = fix_three_dots_func(text)

    if fix_english_quotes:
        text = fix_english_quotes_func(text)

    if fix_hamzeh:
        text = fix_hamzeh_func(text)

    if cleanup_zwnj:
        text = cleanup_zwnj_func(text)

    if fix_misc_non_persian_chars:
        text = char_validator(text)

    if fix_arabic_numbers:
        text = fix_arabic_numbers_func(text)

    if fix_english_numbers:
        text = fix_english_numbers_func(text)

    if fix_perfix_spacing:
        text = fix_perfix_spacing_func(text)
        
    if fix_suffix_spacing:
        text = fix_suffix_spacing_func(text)

    if aggresive:
        text = aggresive_func(text)

    if fix_spacing_for_braces_and_quotes:
        text = fix_spacing_for_braces_and_quotes_func(text)
      
    if cleanup_spacing:
        text = cleanup_spacing_func(text)

    return text
        
def fix_dashes_func(text):
    text = re.sub(r'-{3}', r'—', text)
    text = re.sub(r'-{2}', r'–', text)
    return text

def fix_three_dots_func(text):
    """
    This function will replace three dots with ellipsis
    """
    text = re.sub(r'\s*\.{3,}', r'…', text)
    return text

def fix_english_quotes_func(text):
    """
    This function will replace English quotes with their persian equivalent
    """
    text.replace('“‌', '"')
    text.replace('”', '"')
    text = re.sub(r"([\"'`]+)(.+?)(\1)", r'«\2»', text)
    return text

def fix_hamzeh_func(text):
    """
    This function will replace end of any word which finished with 'ه ی' with
    'هٔ' or 'ه‌ی'(if hamzeh_with_yeh == True)
    """
    if hamzeh_with_yeh:
        text = re.sub(r'(\S)(ه[\s]+[یي])(\s)',r'\1ه‌ی\3', text)
    else:
        text = re.sub(r'(\S)(ه[\s]+[یي])(\s)',r'\1هٔ\3', text)
    return text

def cleanup_zwnj_func(text):
    '''
    This function will remove unnecessary zwnj that are succeeded/preceded by a space
    '''
    text = re.sub(r'\s+|\s+', r' ', text)
    return text

def char_validator(text):
    """
    This function will change invalid characters to validate ones.
    it uses char_translator function to do it.
    """
    bad_chars  = ",;%يةك"
    good_chars = "،؛٪یهک"
    text = char_translator(bad_chars, good_chars, text)
    return text

def fix_arabic_numbers_func(text):
    """
    This function will translate Arabic numbers to their Persian equivalants.
    it uses char_translator function to do it.
    """
    persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
    arabic_numbers = "١٢٣٤٥٦٧٨٩٠"
    text = char_translator(arabic_numbers, persian_numbers, text)
    return text

def fix_english_numbers_func(text):
    """
    This function will translate English numbers to their Persian equivalants.
    it will avoid to do this translation at a English string!
    it uses char_translator function to do it.
    """
    persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
    english_numbers = "1234567890"
    text = char_translator(english_numbers, persian_numbers, text)

    #Followilng commands will help Negar to avoid chang english numbers in strings
    #like 'Text12', 'Text_12' & other string like this
    text = re.sub(r'[a-z\-_]{2,}[۰-۹]+|[۰-۹]+[a-z\-_]{2,}',
                       lambda m:
                       char_translator(persian_numbers, english_numbers,  m.group()),
                       text)
    return text
        
            
def fix_perfix_spacing_func(text):
    """
    Put zwnj between word and prefix (mi* nemi*)
    there's a possible bug here: می and نمی could separate nouns and not prefix
    """
    text = re.sub(r"\s*(ن?می)\s+",r' \1‌', text)
    return text

def fix_suffix_spacing_func(text):
    text = re.sub(r'\s+(تر(ی(ن)?)?|ها(ی)?)\s*', r'‌\1 ', text)
    return text

def aggresive_func(text):
    """
    Aggressive Editing
    """
    # replace more than one ! or ? mark with just one
    if cleanup_extra_marks:
        text = re.sub(r'(!){2,}', r'\1', text)
        text = re.sub(r'(؟){2,}', r'\1', text)
        
    # should remove all kashida
    if cleanup_kashidas:
        text = re.sub(r'ـ+', "", text)
    return text
        
def fix_spacing_for_braces_and_quotes_func(text):
    """
    This function will fix the braces and quotes spacing problems.
    """
    # ()[]{}""«» should have one space before and one virtual space after (inside)
    text = re.sub(r'[ ‌]*(\()\s*([^)]+?)\s*?(\))[ ‌]*', r' \1‌\2‌\3 ', text)
    text = re.sub(r'[ ‌]*(\[)\s*([^)]+?)\s*?(\])[ ‌]*', r' \1‌\2‌\3 ', text)
    text = re.sub(r'[ ‌]*(\{)\s*([^)]+?)\s*?(\})[ ‌]*', r' \1‌\2‌\3 ', text)
    text = re.sub(r'[ ‌]*(“)\s*([^)]+?)\s*?(”)[ ‌]*', r' \1‌\2‌\3 ', text)
    text = re.sub(r'[ ‌]*(«)\s*([^)]+?)\s*?(»)[ ‌]*', r' \1‌\2‌\3 ', text)
    # : ; , ! ? an their persian equivalents should have one space after and no space before
    text = re.sub(r'[ ‌ ]*([:;,؛،.؟!]{1})[ ‌ ]*',r'‌\1 ', text)
    text = re.sub(r'([۰-۹]+):\s+([۰-۹]+)', r'\1:\2', text)
    # should fix inside spacing for () [] {} "" «»
    text = re.sub(r'(\()\s*([^)]+?)\s*?(\))', r'\1\2\3', text)
    text = re.sub(r'(\[)\s*([^)]+?)\s*?(\])', r'\1\2\3', text)
    text = re.sub(r'(\{)\s*([^)]+?)\s*?(\})', r'\1\2\3', text)
    text = re.sub(r'(“)\s*([^)]+?)\s*?(”)', r'\1\2\3', text)
    text = re.sub(r'(«)\s*([^)]+?)\s*?(»)', r'\1\2\3', text)
    return text

def fix_LTRM_RTLM_func(text):
    """
    This function will fix 'ltr mark/rtl mark' problem in the text
    """
    test = re.search(r'([\(\)\)\(])[a-z]', text)
    text = re.sub(r'(\()([a-z])(\))', r'\1‎\2\3‎', text)
    return text
    
def cleanup_spacing_func(text):
    text = re.sub(r'[ ]+', r' ', text)
    text = re.sub(r'([\n]+)[ ‌]', r'\1', text)
    return text


def char_translator(fromchar, tochar, whichstring):
    """
    This function will translate the 'whichstring' character by character from
    'fromchar' to 'tochar'. My old function is writed after this. in this new
    function I can return the newstring, but I can't check the length of fromchar
    and tochar! Why? I don't know!
    """
    newstring = whichstring
    for i in range(len(fromchar)):
        newstring = re.sub(fromchar[i], tochar[i], newstring)
    return newstring

        

def gnegarPython( ):
    xModel = XSCRIPTCONTEXT.getDocument()

    #the writer controller impl supports the css.view.XSelectionSupplier interface
    xSelectionSupplier = xModel.getCurrentController()

    #see section 7.5.1 of developers' guide
    xIndexAccess = xSelectionSupplier.getSelection()
    count = xIndexAccess.getCount();
    if(count>=1):  #ie we have a selection
        i=0
    while i < count :
            xTextRange = xIndexAccess.getByIndex(i);
            #print "string: " + xTextRange.getString();
            theString = xTextRange.getString();
            xTextRange.setString(cleanup(theString));
            xSelectionSupplier.select(xTextRange);
            i+= 1

    return None

g_exportedScripts = gnegarPython,

