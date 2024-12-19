from collections import namedtuple

# These map directly to the 8 regular brainfuck instructions. The
# exception is the offset parameter, which would be 0 in regular
# brainfuck, but can here indicate an offset from the current cell at
# which the operation should be applied.
Add = namedtuple('Add', ['x', 'offset'])
Sub = namedtuple('Sub', ['x', 'offset'])
Right = namedtuple('Right', ['x'])
Left = namedtuple('Left', ['x'])
In = namedtuple('In', ['offset'])
Out = namedtuple('Out', ['offset'])
Open = namedtuple('Open', [])
Close = namedtuple('Close', [])

# These are extensions to the regular 8
Clear = namedtuple('Clear', ['offset'])
Copy = namedtuple('Copy', ['off'])
Mul = namedtuple('Mul', ['off', 'factor'])
ScanLeft = namedtuple('ScanLeft', [])
ScanRight = namedtuple('ScanRight', [])


def bf_to_ir(brainfuck):
    """Translates brainfuck to IR."""

    simplemap = {'+': Add(1, 0),
                 '-': Sub(1, 0),
                 '>': Right(1),
                 '<': Left(1),
                 ',': In(0),
                 '.': Out(0),
                 '[': Open(),
                 ']': Close()}

    return [simplemap[c] for c in brainfuck if c in simplemap]


def ir_to_python(ir):
    """Translates IR into a Python program."""

    plain = {Add: 'mem[p] += %(x)d',
             Sub: 'mem[p] -= %(x)d',
             Right: 'p += %(x)d',
             Left: 'p -= %(x)d',
             Open: 'while mem[p]:',
             Close: '',
             In: 'mem[p] = ord(input()[0])',
             Out: 'print(chr(mem[p]), end="")',
             Clear: 'mem[p] = 0',
             Mul: 'mem[p+%(off)d] += mem[p] * %(factor)d',
             ScanLeft: 'while mem[p] != 0: p -= 1',
             ScanRight: 'while mem[p] != 0: p += 1'}

    woff = {Add: 'mem[p+%(offset)d] += %(x)d',
            Sub: 'mem[p+%(offset)d] -= %(x)d',
            In: 'mem[p+%(offset)d] = ord(input()[0])',
            Out: 'print(chr(mem[p+%(offset)d]), end="")',
            Clear: 'mem[p+%(offset)d] = 0'}

    lines = ['mem = [0] * 10000', 'p = 0']
    indent_level = 0

    for op in ir:
        if isinstance(op, Close):
            indent_level -= 1

        line = (woff if getattr(op, 'offset', 0) else plain)[op.__class__] % op._asdict()
        lines.append('    ' * indent_level + line)

        if isinstance(op, Open):
            indent_level += 1

    return '\n'.join(lines)
