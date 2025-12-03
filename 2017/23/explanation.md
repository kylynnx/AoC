# Explanation

Let us put some annotations on the input instructions for the jumps:

```
set b 65
set c b
jnz a 2  ----------+
jnz 1 5 -----------|--+
mul b 100 <--------+  |
sub b -100000         |
set c b               |
sub c -17000          |
set f 1 <-------------+--+
set d 2                  |
set e 2 <--------+       |
set g d <-----+  |       |
mul g e       |  |       |
sub g b       |  |       |
jnz g 2 ---+  |  |       |
set f 0    |  |  |       |
sub e -1 <-+  |  |       |
set g e       |  |       |
sub g b       |  |       |
jnz g -8 -----+  |       |
sub d -1         |       |
set g d          |       |
sub g b          |       |
jnz g -13 -------+       |
jnz f 2 --+              |
sub h -1  |              |
set g b <-+              |
sub g c                  |
jnz g 2                  |
jnz 1 3 ---> HALT        |
sub b -17                |
jnz 1 -23 ---------------+
```

Now lets dissect what this program does. First of all we can see that the program nicely divides into two parts. First
of which are these lines:

```
set b 65
set c b
jnz a 2  ----------+
jnz 1 5 -----------|--> Second Part>
mul b 100 <--------+
sub b -100000
set c b
sub c -17000
```

Translating this to python code, assuming this is a function gives us:

```python
def setup(a: int) -> tuple[int, int]:
    b = 65
    c = b

    if a != 0:
        b *= 100
        b += 100000
        c = b + 17000
    
    return b, c
```

So this first part only sets up two integer values `b` and `c` for use in the looping function described by the other
instructions. Taking the outermost instructions:

```
set f 1 <--+
...        |
jnz 1 -23 -+
```

which results in this python function for the time being:

```python
def loop():
    while True:
        f = 1
```

Analysing a few more lines inbetween:

```
set f 1 <------+
set d 2        |
set e 2 <---+  |  
...         |  |
sub d -1    |  |
set g d     |  |
sub g b     |  |
jnz g -13 --+  |
...            |
jnz 1 -23 -----+
```

Naively translated to python that reads:

```python
def loop(b: int):
    while True:
        f = 1
        d = 2
        while True:
            e = 2
            d += 1
            g = b - d
            if g == 0:
                break
```

Meaning the second loop increases `d` until `d == b` and then breaks. In other words:

```python
def loop(b: int):
    while True:
        f = 1
        for d in range(2, b):
            e = 2
```

By the same logic the loop within that:

```
set e 2
set g d <-----+
mul g e       |
sub g b       |
...           |
set g e       |
sub g b       |
jnz g -8 -----+
```

adds:

```python
def loop(b: int):
    while True:
        f = 1
        for d in range(2, b):
            for e in range(2, b):
                g = d * e - b
```


Within these two loops this check is being performed:

```
jnz g 2 ---+
set f 0    |
sub e -1 <-+
```

Meaning if `g` is `0`, `f` is increased by one. Note the previously `g` was set to the product `d * e`. Putting it into
our loop:

```python
def loop(b: int):
    while True:
        f = 1
        for d in range(2, b):
            for e in range(2, b):
                if d * e == b:
                    f = 0
```

Let us have another look at the rest of the outermost loop:

```
set f 1 <----------------+
...                      |
jnz f 2 --+              |
sub h -1  |              |
set g b <-+              |
sub g c                  |
jnz g 2                  |
jnz 1 3 ---> HALT        |
sub b -17                |
jnz 1 -23 ---------------+
```

After our loop if `f` is zero `h` is increased by one. Then if `b == c` the program halts. Otherwise `b` is increased
by `17` and the main loop starts over. Finally, we can replace the outer `while True` loop by a `for`-loop:

```python
def loop(b: int, c: int):
    h = 0

    while b <= c:
        f = 1
        for d in range(2, b):
            for e in range(2, b):
                if d * e == b:
                    f = 0
        if f == 0:
            h += 1

        b += 17

    return h
```

# Conclusion

Rewriting these function with names and adding the main function:

```python
def limits(use_large_limits: bool) -> tuple[int, int]:
    start = 65
    end = start

    if use_large_limits:
        start *= 100
        start += 100000
        end = start + 17000
    
    return start, end


def count_composite_numbers(start: int, end: int, step = 17) -> int:
    composite_numbers = 0
    
    for number in range(start, end + 1, step):
        f = 1
        for d in range(2, number):
            for e in range(2, number):
                if d * e == number:
                    f = 0
        if f == 0:
            composite_numbers += 1
    
    return composite_numbers


def main(a: int):
    start, end = limits(a == 1)
    print(count_composite_numbers(start, end))
```

The main loop goes through all combinations of two numbers `d` and `e`, where each is between `2` and `number`. If the
product of the two numbers of any combination equals the number `f` is set to `0`. After that loop if `f` was changed,
`h` is increased. Thus, register `h` counts the number of composite numbers between `start` and `end`. The above loop
can be optimized more (see actual solution).


## Part 1

As we can see the iteration contains **one** `mul` instruction. In part one `a` is initialized with `0`, meaning `b`
and `c` both start with the same value. The count loop is only being run once, checking all combinations of numbers
smaller than the initial value of `b` starting at `2` without respecting the order. So the `mul` instruction is
called `(b - 2)^2` times.


## Part 2

As part 2 starts with `a = 1` the result is the number of composite numbers as explained above.
