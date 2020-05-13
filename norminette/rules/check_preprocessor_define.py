from rules import Rule
from lexer import Lexer, TokenError
from scope import *


class CheckPreprocessorDefine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        i = 0
        if context.check_token(i, "DEFINE") is False:
            return False, 0
        val = context.peek_token(i).value.split("define")[1]
        content = Lexer(val)
        tkns = content.get_tokens()
        i = 1
        while tkns[i] in ["TAB", "SPACE"]:
            i += 1
        if tkns[i].type == "IDENTIFIER" and tkns[i].value.isupper() is False:
            context.new_error("MACRO_NAME_CAPITAL", context.peek_token(0))
        if len(tkns) == i + 1 and context.filetype == 'h':
            protection = context.filename.upper().split('/')[-1].replace('.', '_')
            if context.scope.header_protection == 0:
                if tkns[1].value == protection:
                    context.scope.header_protection = 1
                elif tkns[1].value != protection:
                    context.new_error("HEADER_PROT_NAME", context.peek_token(i))
        i += 1
        if context.filetype == 'h' and context.scope.header_protection != 1:
            context.new_error("HEADER_PROT_ALL", context.peek_token(0))
        while len(tkns) > i and tkns[i] in ["TAB", "SPACE"]:
            i += 1
        i += 1
        if len(tkns) > i and tkns[i].type in ["STRING", "CONSTANT"] is False:
            context.new_error("PREPROC_CONSTANT", context.peek_token(0))
        i += 1
        return False, 0
