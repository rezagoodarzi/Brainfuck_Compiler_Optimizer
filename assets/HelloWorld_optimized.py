mem = [0] * 10000
p = 0
mem[p+1] += 8
p += 1
mem[p+-1] += mem[p] * 9
mem[p] = 0
print(chr(mem[p+-1]), end="")
mem[p] += 4
mem[p+-1] += mem[p] * 7
mem[p] = 0
mem[p+-1] += 1
print(chr(mem[p+-1]), end="")
mem[p+-1] += 7
print(chr(mem[p+-1]), end="")
print(chr(mem[p+-1]), end="")
mem[p+-1] += 3
print(chr(mem[p+-1]), end="")
mem[p+1] += 6
p += 1
mem[p+-1] += mem[p] * 7
mem[p] = 0
mem[p+-1] += 2
print(chr(mem[p+-1]), end="")
mem[p+-1] -= 12
print(chr(mem[p+-1]), end="")
mem[p] += 6
mem[p+-1] += mem[p] * 9
mem[p] = 0
mem[p+-1] += 1
print(chr(mem[p+-1]), end="")
print(chr(mem[p+-2]), end="")
mem[p+-2] += 3
print(chr(mem[p+-2]), end="")
mem[p+-2] -= 6
print(chr(mem[p+-2]), end="")
mem[p+-2] -= 8
print(chr(mem[p+-2]), end="")
mem[p+1] += 4
p += 1
mem[p+-1] += mem[p] * 8
mem[p] = 0
mem[p+-1] += 1
print(chr(mem[p+-1]), end="")
p -= 1