CODE_EXTENSIONS = frozenset({
    '.py', '.java', '.js', '.cpp', '.c', '.rb', '.go', '.php',
    '.html', '.css', '.swift', '.ts', '.sh', '.pl', '.r',
    '.cs', '.bat', '.scala', '.lua', '.rust', '.kotlin', '.vb',
    '.sql', '.yaml', '.dockerfile', '.m', '.swift',
    '.d', '.user', '.clj', '.coffee', '.groovy', '.f90', '.asm',
    '.hs', '.erl', '.ex', '.elm', '.fs', '.fsx', '.ml', '.mli',
    '.jl', '.nim', '.pas', '.purs', '.re', '.v', '.vhd', '.vhdl',
    '.zig', '.odin', '.dart', '.tcl', '.awk', '.sed', '.ps1',
    '.jsx', '.tsx', '.vue', '.svelte', '.pug', '.jade', '.ejs',
    '.hbs', '.handlebars', '.mustache', '.twig', '.haml', '.scss',
    '.less', '.styl', '.sass', '.stylus'
})

def is_code_file(filename: str) -> bool:
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in CODE_EXTENSIONS)

def get_code_extensions() -> tuple[str, ...]:
    return tuple(sorted(CODE_EXTENSIONS))