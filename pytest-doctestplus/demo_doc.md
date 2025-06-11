# Are all these run as tests?

All below is executed in one pytest case.

## Basic python example

```python
>>> 21 * 2
42

```

## Multi line python

A code block can have multiple command, each with `>>>`.
Then if an output is expected, put it there without prefix.
If a single command has multiple lines, continue with `...`.

```bash
>>> x = 0
>>> x
0
>>> if x == 0:
...   print(x)
0

```

## Context across code blocks

We can also use the `x` later:

```python
>>> x
0
>>> x = 1
>>> x
1

```

## This fails

It is the last, because executing the code blocks stops at the first failing one, I think.

```python
>>> 21 * 2
43

```

(this fails ❌)
