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
def get_key():
    conf = mw.addonManager.getConfig(__name__)
    return conf.get("hotkey", "") if conf else ""
# Format Function
def format_key(k):
    return QKeySequence(k).toString(QKeySequence.NativeText)


def replaceMathDelimiters(editor):
    # Get a reference to the editor's web view
    web_view = editor.web
    
    # Fetch the selected plain text content
    selected_text = web_view.selectedText()

    # Format the selected text as a raw multiline string
    selected_text = r"""{}""".format(selected_text.encode("unicode-escape").decode())

    # Remove the selected text from the editor using Ctrl+X
    cut_selected_text_script = """
    document.execCommand('cut', false);
    """
    web_view.page().runJavaScript(cut_selected_text_script)

    # Replace block equation delimiters ($$) with \[ and \]
    modified_text = re.sub(r"\$\$([\s\S]*?)\$\$", r"\\\[\1\\\]", selected_text, flags=re.DOTALL)

    # Replace inline equation delimiters ($) with \( and \)
    modified_text = re.sub(r"\$([\s\S]*?)\$", r"\\\(\1\\\)", modified_text, flags=re.DOTALL)

    # Preserve newline breaks in the modified text
    modified_text = modified_text.replace("\\n", "<br>")
    
    # Replace \begin and \end with \[ and \]
    # modified_text = re.sub(r'\\begin{(\w+)}|\\end{(\w+)}', lambda m: r'\[' if m.group().startswith(r'\begin') else r'\]', modified_text)

    # Insert the modified text at the cursor position
    insert_modified_text_script = f"""
    document.execCommand('insertText', false, `{modified_text}`);
    """
    web_view.page().runJavaScript(insert_modified_text_script)
     

def setupEditorButtonsFilter(buttons, editor):
    key = get_key()
    b = editor.addButton(
            os.path.join(os.path.dirname(__file__), "rmd.png"),
            "replaceMathDelimiters",
            replaceMathDelimiters,
            tip=f"Replace Math Delimiters ({format_key(key)})",
            keys=key
        )
    buttons.append(b)
    return buttons

addHook("setupEditorButtons", setupEditorButtonsFilter)



