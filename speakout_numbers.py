from num2words import num2words

def _get_decpoint(lang):
    # different variants
    decpoints = { 
        "de" : ",",
    }
    
    # value for languate exists?
    if lang in decpoints:
        return decpoints[lang]
    
    # return default value
    return "."

def _get_ordpoint(lang):
    # different variants
    ordpoints = { 
        "de" : ".",
    }
    
    # value for languate exists?
    if lang in ordpoints:
        return ordpoints[lang]
    
    # return default value
    return "."


def speakout_numbers(text, lang, decpoint=None, ordpoint=None):
    if decpoint is None:
        decpoint = _get_decpoint(lang)
    if ordpoint is None:
        ordpoint = _get_ordpoint(lang)
        
    result = ""
    for i in range(0,len(text)):
        char = text[i]
        if char>='0' and char<='9':
            # search for end of number
            dec_found=False
            cont = True
            has_ordpoint = False
            end_idx=i+1
            text_len=len(text)
            while cont:
                char = text[end_idx] if end_idx<text_len else ''
                if char>='0' and char<='9':
                    end_idx+=1
                    continue
                if char==decpoint and not dec_found:
                    end_idx+=1
                    dec_found=True
                    continue
                cont=False
                if char==ordpoint:
                    has_ordpoint = True
                    end_idx+=1
            
            number = text[i:end_idx]
            
            if number[-1] == decpoint:
                # number must not finish with only decpoint!
                end_idx-=1
                number = text[i:end_idx]
                
            # convert decpoint to dot, otherwise conversion would fail
            number = number.replace(decpoint,".")
            if has_ordpoint:
                # remove last char (ord-point) and convert using "ordinal"
                number_text=num2words(number[:-1], lang=lang, to='ordinal')
            else:
                # "normal" conversion
                number_text=num2words(number, lang=lang)
            
            # go into recurse
            # current result + converted-text + rest of text recurse processed
            return result + number_text + speakout_numbers(text[end_idx:], lang, decpoint=",", ordpoint=".")
        
        # add to result and continue
        result += char
    
    # fallback: no number was found, just return the connected string
    return result  
