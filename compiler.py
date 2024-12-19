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

def opt_clearloop(ir):
    """Replaces clear loops ([-] and [+]) with single instructions."""

    optimized = []

    for op in ir:
        optimized.append(op)
        if (op.__class__ == Close and
            len(optimized) > 2 and
            optimized[-2].__class__ in (Sub, Add) and
            optimized[-2].x == 1 and
            optimized[-2].offset == 0 and
            optimized[-3].__class__ == Open):
            # last 3 ops are [-] or [+] so replace with Clear
            optimized.pop(-1)
            optimized.pop(-1)
            optimized[-1] = Clear(0)

    return optimized
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

def opt_cancel(ir):
    """Cancels out adjacent Add, Sub and Left Right.

    E.g., ++++-->>+-<<< is equivalent to +<.
    """

    opposite = {Add: Sub,
                Sub: Add,
                Left: Right,
                Right: Left}
    optimized = []

    for op in ir:
        if len(optimized) == 0:
            optimized.append(op)
            continue
        prev = optimized[-1]
        if prev.__class__ == opposite.get(op.__class__) and \
           getattr(prev, 'offset', 0) == getattr(op, 'offset', 0):
            x = prev.x - op.x
            if x < 0:
                optimized[-1] = op._replace(x=-x)
            elif x > 0:
                optimized[-1] = prev._replace(x=x)
            else:
                optimized.pop(-1)
        else:
            optimized.append(op)

    return optimized

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
             Copy: 'mem[p+%(off)d] += mem[p]',
             Mul: 'mem[p+%(off)d] += mem[p] * %(factor)d',
             ScanLeft: 'while mem[p] != 0: p -= 1',
             ScanRight: 'while mem[p] != 0: p += 1'}

    woff = {Add: 'mem[p+%(offset)d] += %(x)d',
            Sub: 'mem[p+%(offset)d] -= %(x)d',
            In: 'mem[p+%(offset)d] = ord(input()[0])',
            Out: 'print(chr(mem[p+%(offset)d]), end="")',
            Clear: 'mem[p+%(offset)d] = 0'}

    lines = ['mem = [0] * 65536', 'p = 0']
    indent_level = 0

    for op in ir:
        if isinstance(op, Close):
            indent_level -= 1

        line = (woff if getattr(op, 'offset', 0) else plain)[op.__class__] % op._asdict()
        lines.append('    ' * indent_level + line)

        if isinstance(op, Open):
            indent_level += 1

    return '\n'.join(lines)

def execute_brainfuck_file(file_path):
    """
    Reads Brainfuck code from a file, compiles it to Python code, and executes it.
    """
    with open(file_path, 'r') as f:
        brainfuck_code = f.read()

    try:
        ir = bf_to_ir(brainfuck_code)
        print(ir)
        optimized_ir = opt_cancel(ir)
        print(optimized_ir)
        python_code = ir_to_python(optimized_ir)
        with open("output.py", 'w') as f:
            f.write(python_code)
        #exec(python_code)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    file_path = "program.bf"
    execute_brainfuck_file(file_path)

