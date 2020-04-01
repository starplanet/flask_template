# -*- coding: utf-8 -*-

from html.parser import HTMLParser

acceptable_elements = {
    'a', 'abbr', 'acronym', 'address', 'area', 'article', 'aside', 'audio', 'b', 'big', 'blockquote',
    'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'command',
    'datagrid', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'em',
    'event-source', 'fieldset', 'figcaption', 'figure', 'footer', 'font', 'form', 'header', 'h1',
    'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'input', 'ins', 'keygen', 'kbd', 'label',
    'legend', 'li', 'm', 'map', 'menu', 'meter', 'multicol', 'nav', 'nextid', 'ol', 'output',
    'optgroup', 'option', 'p', 'pre', 'progress', 'q', 's', 'samp', 'section', 'select', 'small',
    'sound', 'source', 'spacer', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'tbody', 'td',
    'textarea', 'time', 'tfoot', 'th', 'thead', 'tr', 'tt', 'u', 'ul', 'var', 'video'
}


class MyHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(MyHTMLParser, self).__init__(*args, **kwargs)

        self.elements = set()

    def handle_starttag(self, tag, attrs):
        self.elements.add(tag)

    def handle_endtag(self, tag):
        self.elements.add(tag)


def is_html(text):
    parser = MyHTMLParser()
    parser.feed(text)
    return bool(parser.elements.intersection(acceptable_elements))
