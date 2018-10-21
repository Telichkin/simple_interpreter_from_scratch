RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'

token_expressions = (
    (r'[ \n\t]+', None),  # Whitespaces are nothing
    (r'#[^\n]*', None),  # Comments are nothing
    (r'\:=', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'=', RESERVED),
    (r'!=', RESERVED),
    (r'\band\b', RESERVED),
    (r'\bor\b', RESERVED),
    (r'\bnot\b', RESERVED),
    (r'\brepeat\b', RESERVED),
    (r'\btimes\b', RESERVED),
    (r'\bif\b', RESERVED),
    (r'\bthen\b', RESERVED),
    (r'\belse\b', RESERVED),
    (r'\bwhile\b', RESERVED),
    (r'\bdo\b', RESERVED),
    (r'\bend\b', RESERVED),

    (r'[0-9]+', INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),  # This regexp matches all symbols above, so it should be the last regexp
)
