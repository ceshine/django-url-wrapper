# This file is partly extracted and modified from twitter-text-python project:
# <https://github.com/BonsaiDen/twitter-text-python>
import re

AT_SIGNS = ur'[@\uff20]'
UTF_CHARS = ur'a-z0-9_\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff'
SPACES = ur'[\u0020\u00A0\u1680\u180E\u2002-\u202F\u205F\u2060\u3000]'

# Hashtags
HASHTAG_EXP = ur'(^|[^0-9A-Z&/]+)(#|\uff03)([0-9A-Z_]*[A-Z_]+[%s]*)' % UTF_CHARS
HASHTAG_REGEX = re.compile(HASHTAG_EXP, re.IGNORECASE)

# URLs
PRE_CHARS = ur'(?:[^/"\':!=]|^|\:)'
DOMAIN_CHARS = ur'([\.-]|[^\s_\!\.])+\.[a-z]{2,}(?::[0-9]+)?'
PATH_CHARS = ur'(?:[\.,]?[%s!\*\'\(\);:=\+\$/%s#\[\]\-_,~@])' % (UTF_CHARS, '%')
QUERY_CHARS = ur'[a-z0-9!\*\'\(\);:&=\+\$/%#\[\]\-_\.,~]'

# Valid end-of-path chracters (so /foo. does not gobble the period).
# 1. Allow ) for Wikipedia URLs.
# 2. Allow =&# for empty URL parameters and other URL-join artifacts
PATH_ENDING_CHARS = r'[%s\)=#/]' % UTF_CHARS
QUERY_ENDING_CHARS = '[a-z0-9_&=#]'

URL_REGEX = re.compile('((%s)((https?://|www\\.)(%s)(\/%s*%s?)?(\?%s*%s)?))'
                       % (PRE_CHARS, DOMAIN_CHARS, PATH_CHARS,
                          PATH_ENDING_CHARS, QUERY_CHARS, QUERY_ENDING_CHARS),
                       re.IGNORECASE)

class ParseResult:
    '''A class containing the results of a parsed Tweet.
       Attributes:
       - urls:
       A list containing all the valid urls in the Tweet.
       - html
       A string containg formatted HTML.
       
       '''
    
    def __init__(self, urls, html):
        self.urls = urls
        self.html = html



class Parser:
    def __init__(self, max_url_length=30):
        self._max_url_length = max_url_length

    def parse(self, text, html=True):
        '''Parse the text and return a ParseResult instance.'''
        self._urls = []
        
        
        parsed_html = self._html(text) if html else self._text(text)
        return ParseResult(self._urls, parsed_html)

    def _text(self, text):
        '''Parse a Tweet without generating HTML.'''
        URL_REGEX.sub(self._parse_urls, text)
        return None
    
    def _html(self, text):
        '''Parse a Tweet and generate HTML.'''
        return URL_REGEX.sub(self._parse_urls, text)

    # Internal parser stuff ----------------------------------------------------
    def _parse_urls(self, match):
        '''Parse URLs.'''
        
        mat = match.group(0)
        
        # Fix a bug in the regex concerning www...com and www.-foo.com domains
        # TODO fix this in the regex instead of working around it here
        if match.group(5)[0] in '.-':
            return mat
        
        # Check for urls without http(s)
        pos = mat.find('http')
        if pos != -1:
            pre, url = mat[:pos], mat[pos:]
            full_url = url
        
        # Find the www and force http://
        else:
            pos = mat.lower().find('www')
            pre, url = mat[:pos], mat[pos:]
            full_url = 'http://%s' % url
        
        self._urls.append(url)
        
        if self._html:
            return '%s%s' % (pre, self.format_url(full_url,
                                       self._shorten_url(escape(url))))


    def _shorten_url(self, text):
        '''Shorten a URL and make sure to not cut of html entities.'''
        
        if len(text) > self._max_url_length:
            text = text[0:self._max_url_length - 3]
            amp = text.rfind('&')
            close = text.rfind(';')
            if amp != -1 and (close == -1 or close < amp):
                text = text[0:amp]
            
            return text + '...'
        
        else:
            return text
    
    # User defined formatters --------------------------------------------------
    def format_url(self, url, text):
        '''Return formatted HTML for a url.'''
        return '<a href="%s" class="wrapped_url">%s</a>' % (escape(url), text)

# Simple URL escaper
def escape(text):
    '''Escape some HTML entities.'''
    return ''.join({'&': '&amp;', '"': '&quot;',
                    '\'': '&apos;', '>': '&gt;',
                    '<': '&lt;'}.get(c, c) for c in text)
