# -*- coding: utf-8 -*-

"""
**Math Delimiters Replacer**

- an addon to replace block equation delimiters ($$) with \[ and \]
and to replace inline equation delimiters ($) with \( and \)

Copyright: (c) 2023-2027 Achyut Morang <achyut.morang@gmail.com> 
License: MIT License <https://opensource.org/license/mit/>
"""


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
import re
from anki.utils import stripHTML

# Config

def getConfig():
    return mw.addonManager.getConfig(__name__)

# Format Function

def replaceMathDelimiters(editor):
    # Get a reference to the editor's web view
    web_view = editor.web
    
    # Fetch the selected plain text content
    selected_text = web_view.selectedText()

    # Format the selected text as a raw multiline string
    selected_text = r"""{}""".format(selected_text.encode("unicode-escape").decode())

    # Replace block equation delimiters ($$) with \[ and \]
    modified_text = re.sub(r"\$\$([\s\S]*?)\$\$", r"\\\[\1\\\]", selected_text, flags=re.DOTALL)

    # Replace inline equation delimiters ($) with \( and \)
    modified_text = re.sub(r"\$([\s\S]*?)\$", r"\\\(\1\\\)", modified_text, flags=re.DOTALL)

    # Preserve newline breaks in the modified text
    modified_text = modified_text.replace("\\n", "<br>")
    
    # Replace \begin and \end with \[ and \]
    modified_text = re.sub(r'\\begin{(\w+)}|\\end{(\w+)}', lambda m: r'\[' if m.group().startswith(r'\begin') else r'\]', modified_text)

    # Execute JavaScript to replace the selected text with modified text
    replace_selected_text_script = f"""
    document.execCommand('insertHtml', false, `{modified_text}`);
    """
    web_view.page().runJavaScript(replace_selected_text_script)
     


def createReplaceDelimitersButton(editor):
    editor._links['replaceDelimiters'] = replaceMathDelimiters
    # QShortcut(QKeySequence("Ctrl+D"), editor.widget, activated=lambda s=editor: replaceMathDelimiters(s))
    return '''<button tabindex=-1 class="linkb" title="Replace Math Delimiters"
                type="button" onclick="pycmd('replaceDelimiters');return false;">\(...\)</button>'''


def onSetupButtons(buttons, editor):
    buttons.append(createReplaceDelimitersButton(editor))
    return buttons


addHook("setupEditorButtons", onSetupButtons)
