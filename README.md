# Template code generator

This is a personal template engine for code/config generation.

The template engine MUST be transparent and provide little to no abstraction to the user.

This also a research project, to understand how to implement a code
generator that can be integrated into a build system AND stay fast.

## Usage

### Terminology

- Implementation language: The language the parser is implemented in
- Host language: The language the engine is running on
- Target language: The language of template output (rarely useful term)

```
 <template parser> -> <generated generator in host language> -> <template output>
```

### Showcase

The code inside `{%` and `%}` is statements in host language, `{{` and
`}}` is for expressions. No need to learn a DSL to use the template, use
the language you already know.

The example below generate fizzbuzz at template time.
```python
{% for i in range(1, 21): %}
{% if False: %}
{% elif 0 == i % 15: %}
print("FizzBuzz")
{% elif 0 == i % 3: %}
print("Fizz")
{% elif 0 == i % 5: %}
print("Buzz")
{% else: %}
print({{ i }})
{% end %}
{% end %}
```

Expands to this:

```python
print(1)
print(2)
print("Fizz")
print(4)
print("Buzz")
print("Fizz")
print(7)
print(8)
print("Fizz")
print("Buzz")
print(11)
print("Fizz")
print(13)
print(14)
print("FizzBuzz")
print(16)
print(17)
print("Fizz")
print(19)
print("Buzz")
```

<!-- vim: set spell: -->
