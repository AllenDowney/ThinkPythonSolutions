---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Title
Chapter 1

## Quiz Type
Formative

<!-- #region -->
### Question
Which of these types is used to represent a number with a fraction part?
- [ ] `int`
- [ ] `real`
- [ ] `string`
- [X] `float`


### Rationale
- `int` values can only be integers.
- Python does not have a type called `real`.
- `string` values contain a sequence of characters.
- `float` values represent floating-point numbers, which can have a fraction part.

<!-- #endregion -->

<!-- #region -->
### Question
Which of these is a legal expression?

- [ ] `'1' / '2'`
- [ ] `'1' * '2'`
- [ ] `'1' / 2`
- [X] `'1' * 2`


### Rationales
- The division operator does not work with strings.
- With the multiplication operator, the first value can be a string, but the second cannot.  
- The division operator does not work with strings.
- When the first operator is a string, the multiplication operator repeats the string, so the result is `'11'`.

<!-- #endregion -->

### Question
Which of these is the general word for any value used in a mathematical operation like addition or multiplication?

- [ ] term
- [ ] factor
- [ ] divisor
- [X] operand

### Rationale
- A "term" is a value used in addition, but it is not the general word for any value used in an operation.
- A "factor" is a value used in multiplication, but it is not the general word for any value used in an operation.
- A "divisor" is one of the values used in division, but it is not the general word for any value used in an operation.
- An "operand" is a value used in an operation.


### Question
On the internet, people sometimes argue about the value of an ambiguous mathematical expression like $8 ÷ 2(2+2)$. How do we write this expression in Python?

- [ ] `8 ÷ 2 (2 + 2)`
- [ ] `8 / 2 (2 + 2)`
- [ ] `8 ÷ 2 * (2 + 2)`
- [X] `8 / 2 * (2 + 2)`

### Rationale
- The operator for division is `/`, not `÷`. Also, there is no implicit multiplication in Python -- you have to use the `*` operator.
- There is no implicit multiplication in Python -- you have to use the `*` operator.
- The operator for division is `/`, not `÷`.
- An alternative is to put `8 / 2` in parentheses so the order of operations is clear. 



# Title
Chapter 2

## Quiz Type
Formative

<!-- #region -->
### Question
Which of these is a legal variable name?
- [ ] `2pi`
- [ ] `question?`
- [ ] `import`
- [X] `is_even`



### Rationale
- `2pi` is not a legal variable name because it starts with a number.
- `question?` is not a legal variable name because only letters, numbers, and the underscore character, `_`, are allowed.
- `import` is not a legal variable name because it is one of Python's keywords.
- `is_even` is a legal variable name because letters, numbers, and the underscore character, `_`, are allowed.
<!-- #endregion -->

### Question
Which of these is NOT a correct way to raise `2` to the third power?
- [ ] `2 * 2 * 2` 
- [ ] `2 ** 3`
- [ ] `math.pow(2, 3)`
- [X] `2 ^ 3`

### Rationale
- Multiplication is a correct way to raise `2` to the third power.
- The exponentiation operator, `**`,  is a correct way to raise `2` to the third power.
- The `pow` function in the `math` module is a correct way to raise `2` to the third power.
- In some languages, the `^` operator is used for exponentiation, but in Python it means something else.


<!-- #region -->
### Question
When you call a function, what are the values that appear in parentheses?
- [ ] assignments
- [ ] comments
- [ ] exceptions
- [X] arguments


### Rationale 
- An assignment is a statement that assigns a value to a variable.
- A comment is text you add to a program to explain how it works.
- An exception is an error detected while a program is running.
- The values you pass to a function are called arguments.

<!-- #endregion -->

<!-- #region -->
### Question
If a program runs without producing an error message, but it does not do the right thing, what kind of error is that?
- [ ] syntax error
- [ ] runtime error
- [ ] exception
- [X] semantic error


### Rationale
- A syntax error produces an error message.
- A runtime error produces an error message.
- An exception produces an error message.
- A semantic error is when a program runs, but does the wrong thing.

<!-- #endregion -->

# Title
Chapter 3

## Quiz Type
Formative

<!-- #region -->
### Question
When you define a function, what are the variables that appear in parentheses?
- [ ] arguments
- [ ] local variables
- [ ] function objects
- [X] parameters



### Rationale
- An argument is a value you provide when you call a function.
- A local variable is a variable that gets assigned a value inside a function.
- A function object is the result of defining a new function.
- A parameter is a variable that gets a value when the function is called.

<!-- #endregion -->

<!-- #region -->
### Question
Which kind of statement can be used to run a line of code more than once?
- [ ] assignment statement
- [ ] import statement
- [ ] print statement
- [X] `for` statement


### Rationale
- An assignment statement assigns a value to a variable.
- An import statement makes it possible to use functions in a module.
- A print statement displays the value of an expression.
- A `for` statement can run a line of code, or multiple lines, more than once.

<!-- #endregion -->

<!-- #region -->
### Question
What is wrong with this function, if anything?

```
def bottle_line(n, suffix):
    print(n)
    print('bottles of beer')
    print(suffix)
```

- [ ] Instead of `def`, the first word should be `define`.
- [ ] You can't have more than one parameter in parentheses.
- [ ] Only the first statement of the body should be indented.
- [X] There are no errors in this function.


### Rationale
- `def` is the right keyword to define a new function, although some other languages use `define`.
- You can have any number of parameters in parentheses, including none.
- All of the statements in the body of the function should be indented.
- There is nothing wrong with this function.

<!-- #endregion -->

# Title
Chapter 4

## Quiz Type
Formative

<!-- #region -->
### Question
What is wrong with this function, if anything?

```
def square(length):
    for i in range(4):
        forward(50)
        left(90)
```

- [ ] The indentation of the statements in the `for` loop is incorrect.
- [ ] It does not bring the Turtle back to where it started.
- [ ] There are no errors in this function.
- [X] It always draws the same size square, regardless of `length`.


### Rationale
- The indentation in this function is correct.
- The `Turtle` ends where it started, facing in the same direction.
- There is an error!
- The size is always `50` -- the value of `length` is never used.

<!-- #endregion -->

<!-- #region -->
### Question
What is it called when you put working statements into a new function definition?
- [ ] generalization
- [ ] indentation
- [ ] debugging
- [X] encapsulation


### Rationale
- Generalization is when you add a parameter to a function to make it more general.
- You might have to indent the statements when you put them in a function definition, but that's not what the whole process is called.
- If the statements are working, they don't have to be debugged.
- Encapsulation is the process of transforming a sequence of statements into a function definition.

<!-- #endregion -->

<!-- #region -->
### Question
Here are two versions of the `circle` function. 

```
def circle(radius):
    circumference = 2 * math.pi * radius
    n = 30
    length = circumference / n
    polygon(n, length)

def circle(radius):
    arc(radius,  360)
```

What can we say about these functions?

- [ ] They have the same implementation, but different interfaces.
- [ ] They have the same interface _and_ the same implementation.
- [ ] They have neither the same interface nor the same implementation.
- [X] They have the same interface, but different implementations.


### Rationale
- They take the same parameter and have the same effect, so they have the same interface -- but they accomplish the effect in different ways, so they have different implementations.
- They take the same parameter and have the same effect, so they have the same interface -- but they accomplish the effect in different ways, so they have different implementations.
- They take the same parameter and have the same effect, so they have the same interface -- but they accomplish the effect in different ways, so they have different implementations.
- They take the same parameter and have the same effect, so they have the same interface -- but they accomplish the effect in different ways, so they have different implementations.

<!-- #endregion -->

# Title
Chapter 5

## Quiz Type
Formative

<!-- #region -->
### Question
What is the result of these assignment statements?

```
a = 25 // 10
b = 25 % 10
```
- [ ] `a` is `2.5` and `b` is `5`
- [ ] `a` is `2` and `b` is `250`
- [ ] `a` is `2.5` and `b` is `250`
- [X] `a` is `2` and `b` is `5`


### Rationale
- The `//` operator does integer division, so `25 // 10` is `2`.
- The `%` operator computes the remainder after division, so `25 % 10` is `5`.
- The `//` operator does integer division, so `25 // 10` is `2`, and the `%` operator computes the remainder after division, so `25 % 10` is `5`.
- The `//` operator does integer division and the `%` operator computes the remainder after division.

<!-- #endregion -->

<!-- #region -->
### Question
What is the result of these statements?
```
x = 5
print(x > 5)
print(x <= 5)
```
- [ ] They print the values `True` and `True`
- [ ] They print the values `True` and `False`
- [ ] They print the values `False` and `False`
- [X] They print the values `False` and `True`


### Rationale
- If `x` is `5`, `x > 5` is the same as `5 > 5`, which is `False`.
- If `x` is `5`, `x > 5` is the same as `5 > 5`, which is `False`; also, `x <= 5` is the same as `5 <= 5`, which is `True`.
- If `x` is `5`, `x <= 5` is the same as `5 <= 5`, which is `True`.
- If `x` is `5`, `x > 5` is `False` and `x <= 5` is `True`.

<!-- #endregion -->

<!-- #region -->
### Question
What is the result of calling this function?
```
def hello():
    print('hello')
    hello()
```
- [ ] It prints `hello` once.
- [ ] It prints `hello` forever.
- [ ] It causes an error the first time `hello` tries to call itself.
- [X] It prints `hello` many times and then causes an error.


### Rationale
- After it prints `hello` once, it calls itself, which prints `hello` many times and then causes a `RecursionError`.
- After printing `hello` many times, it causes a `RecursionError`.
- After printing `hello` many times, it causes a `RecursionError`.
- After printing `hello` many times, it causes a `RecursionError`.

<!-- #endregion -->

<!-- #region -->
### Question
What kind of operator is `or`?
- [ ] arithmetic
- [ ] bitwise
- [ ] relational
- [X] logical


### Rationale
- `or` is a logical operator, along with `and` and `not`.
- `or` is a logical operator, along with `and` and `not`.
- `or` is a logical operator, along with `and` and `not`.
- `or` is a logical operator, along with `and` and `not`.

<!-- #endregion -->

# Title
Chapter 6

## Quiz Type
Formative

<!-- #region -->
### Question
What is the return value if we call this function with the value `3`?

```
def collatz(x):
    if x % 2 == 0:
        return x // 2
    else:
        return x * 3 + 1
```

- [ ] `1`
- [ ] `1.5`
- [ ] It causes an error.
- [X] `10`


### Rationale
- Because `3 % 2` is `1`, the second branch of the conditional runs.
- Because `3 % 2` is `1`, the second branch of the conditional runs. Also, because `//` does integer division, `3 // 2` is `1`.
- This function works. Because `3 % 2` is `1`, the second branch of the conditional runs, and the result is `3 * 3 + 1`, which is `10`.
- Because `3 % 2` is `1`, the second branch of the conditional runs, and the result is `3 * 3 + 1`, which is `10`.

<!-- #endregion -->

<!-- #region -->
### Question
What do we call a function that does not print anything or have any effect other than a return value?
- [ ] recursive
- [ ] dead code
- [ ] incremental
- [X] pure function


### Rationale
- A recursive function calls itself, but it might print something or have some other effect.
- Dead code is code that can never run, often because it appears after a `return` statement.
- Incremental development is a way of writing programs by making small changes and testing.
- A pure function does not print anything or have any effect other than a return value.

<!-- #endregion -->

<!-- #region -->
### Question
What is the result of calling this function with the values `x=1.5` and `y=1.6`?

```
def is_close(x, y):
    return abs(x - y) < 0.2
```
- [ ] There is a syntax error.
- [ ] There is a runtime error.
- [ ] `False`
- [X] `True`


### Rationale
- The syntax of the function is correct.
- The function is correct as long as the values of `x` and `y` are numbers.
- The absolute difference between `1.5` and `1.6` is `0.1`, which is less than `0.2`.
- The absolute difference between `1.5` and `1.6` is `0.1`, which is less than `0.2`.

<!-- #endregion -->

# Title
Chapter 7

## Quiz Type
Formative

<!-- #region -->
### Question
This function is supposed to return `True` if `word` contains with `'A'` or `'a'`, and `False` otherwise. But it doesn't work -- What's wrong?

```
def has_a(word):
    for letter in word.lower():
        if letter == 'a':
            return True
        else:
            return False
        return False
```

- [ ] The first line of the for statement has a syntax error.
- [ ] It only checks for lowercase `'a'`, not uppercase `'A'`.
- [ ] It causes a runtime error if `word` is an empty string.
- [X] It only checks the first letter of `word`.


### Rationale
- The syntax of the function is correct.
- It uses `lower` to convert `word` to lowercase, so if uppercase `'A'` is in the string, it would be found.
- If `word` is an empty string, the body of the loop never runs and the function returns `False`, which is correct.
- Both branches of the conditional have `return` statements, so this function ends after checking the first letter.

<!-- #endregion -->

<!-- #region -->
### Question
Which of these is a legal way to increment `x`, assuming it has already been assigned a value.
- [ ] `x++`
- [ ] `x + 1 = x`
- [ ] `x = +1`
- [X] `x = x + 1`


### Rationale
- Some programming languages use the `++` operator to increment a variable, but not Python.
- The left side of an assignment can't be an expression like `x + 1`.
- The value `+1` is the same as `1`, so this statement assigns the value `1` to`x`.
- This is a legal way to update the value of `x`.

<!-- #endregion -->

<!-- #region -->
### Question
What does this function do?

```
def check(word, letters):
    for letter in word.lower():
        if letter in letters.lower():
            return False
    return True
```
- [ ] Returns `True` if any of the letters in `letters` appear in `word`.
- [ ] Returns `True` if any of the letters in `word` appear in `letter`.
- [ ] Returns `True` if none of the letters in `word` appear in `letter`.
- [X] Returns `True` if none of the letters in `letters` appear in `word`.


### Rationale
- It only returns `True` if it gets to the end of `word` and exits the loop having found none of the letters in `letters`.
- It only returns `True` if it gets to the end of `word` and exits the loop having found none of the letters in `letters`.
- It only returns `True` if it gets to the end of `word` and exits the loop having found none of the letters in `letters`.
- It returns `True` if it gets to the end of `word` and exits the loop having found none of the letters in `letters`.

<!-- #endregion -->

# Title
Chapter 8

## Quiz Type
Formative

<!-- #region -->
### Question
What is the result of this comparison: `'Orange' < 'apple'`?
- [ ] `False`
- [ ] Syntax error
- [ ] Runtime error, because you can't compare apples and oranges.
- [X] `True`


### Rationale
- When we compare characters the uppercase `'O'` comes before the lowercase `'a'`.
- The syntax is correct.
- It's legal to compare any two strings.
- Because when we compare characters the uppercase `'O'` comes before the lowercase `'a'`.

<!-- #endregion -->

<!-- #region -->
### Question
Which of these is the correct way to invoke the `lower` method on a string called `s`?
- [ ] lower(s)
- [ ] string.lower(s)
- [ ] s.lower(string)
- [X] s.lower()


### Rationale
- The `lower` method can only be invoked on a string using dot notation.
- The `lower` method can only be invoked on a string using dot notation.
- The `lower` method doesn't take an argument in parentheses.
- This is the correct syntax for invoking a method on an object.

<!-- #endregion -->

<!-- #region -->
### Question
If we use the `search` function in the `re` module, which of the following strings matches this pattern: `r'ab?c$'`?
- [ ] `'ab?c$'`
- [ ] `'abcd'`
- [ ] `'abbc'`
- [X] `'zac'`


### Rationale
- The question mark, `?`, and dollar sign, `$`, are special characters that change the behavior of the pattern -- they should not appear in the string.
- The pattern `c$` requires the letter `c` at the end of the string.
- The pattern `b?` means that `b` is optional, but it cannot be repeated.
- It's OK to have extra letters at the beginning, and the `b` is not required.

<!-- #endregion -->

# Title
Chapter 9

## Quiz Type
Formative

<!-- #region -->
### Question
What is the value of `t` after running these statements?

```
t = [1, 2, 3]
t.pop(1)
t.append(2)
t.remove(3)
```
- [ ] `[2, 2]`
- [ ] `[1, 3]`
- [ ] `[1, 2, 3]`
- [X] `[1, 2]`


### Rationale
- `t.pop(1)` removes the second element, which is `2`.
- After `t.pop(1)` removes the second element, `t.append(2)` adds `2` to the end of the list, and `t.remove(3)` removes `3`.
- `t.pop(1)` removes the second element, which is `2`. `t.append(2)` adds `2` to the end of the list, and `t.remove(3)` removes `3`.
- `t.pop(1)` removes the second element, which is `2`. `t.append(2)` adds `2` to the end of the list, and `t.remove(3)` removes `3`.

<!-- #endregion -->

<!-- #region -->
### Question
What is the value of `b` after running these statements?

```
a = [1, 2, 3]
b = a
a.remove(2)
```
- [ ] `[1, 2]`
- [ ] `[1, 2, 3]`
- [ ] Runtime error
- [X] `[1, 3]`


### Rationale
- `a.remove(2)` removes the value `2` from the list.
- `a` and `b` refer to the same object, so when we modify `a`, the value of `b` also changes.
- These statements run without causing an error.
- `a` and `b` refer to the same object, so when we modify `a`, the value of `b` also changes.

<!-- #endregion -->

<!-- #region -->
### Question
What can we say about two lists created like this:

```
a = [1, 2, 3]
b = [1, 2, 3]
```


- [ ] They are equivalent and identical.
- [ ] They are identical but not equivalent.
- [ ] They are not equivalent and not identical.
- [X] They are equivalent but not identical.


### Rationale
- `a` and `b` refer to different lists, so they are not identical.
- `a` and `b` refer to lists with the same value, so they are equivalent, but they refer to different lists, so they are not identical.
- `a` and `b` refer to lists with the same value, so they are equivalent, but they refer to different lists, so they are not identical.
- `a` and `b` refer to lists with the same value, so they are equivalent, but they refer to different lists, so they are not identical.

<!-- #endregion -->

# Title
Chapter 10

## Quiz Type
Formative


### Question
What is the value of the dictionary `d` after these statements run?

```
d = {'a': 1, 'b': 2}
d['a'] = 3
```

- [ ] `{'a': 1, 'b': 2, 'a': 3}`
- [ ] `{'a': 1, 'b': 2}`
- [ ] These statements cause a runtime error
- [X] `{'a': 3, 'b': 2}`

### Rationale
- Each key can only appear once in a dictionary.
- The second assignment statement changes the value associated with the key `'a'`.
- This code runs without causing an error.
- The second assignment statement updates the value associated with the key `'a'`.


<!-- #region -->
### Question
What is the value of the dictionary `d` after running these statements?

```
d = {'a': 1, 'b': 2}
d['c'] += 1
```

- [ ] `{'a': 1, 'b': 2}`
- [ ] `{'a': 1, 'b': 2, 'c': 1}`
- [ ] `{'a': 1, 'b': 2, 'c': 3}`
- [X] These statements cause a runtime error.


### Rationale
- The `+=` operator looks up the key to get the old value before adding `1`.
- The `+=` operator looks up the key to get the old value before adding `1`.
- The `+=` operator looks up the key to get the old value before adding `1`.
- Because `c` does not appear as a key in the dictionary, the second statement causes a `KeyError`.

<!-- #endregion -->

<!-- #region -->
### Question
What happens when the following statements run?

```
d1 = {'a': 1, 'b': 2}
d2 = {d1: 3}
```

- [ ] They add `d1` as a key in `d3`.
- [ ] They cause a `KeyError` because `d1` is not in `d2`.
- [ ] They cause a `ValueError` because `3` cannot appear as a value in a dictionary.
- [X] They cause a `TypeError` because a dictionary cannot appear as a key in a dictionary.


### Rationale
- Dictionaries are mutable, so they are not hashable, so they cannot appear as a key in a dictionary.
- Dictionaries are mutable, so they are not hashable, so they cannot appear as a key in a dictionary, but that's not a `KeyError.`
- Dictionaries are mutable, so they are not hashable, so they cannot appear as a key in a dictionary, but that's not a `ValueError.`
- Dictionaries are mutable, so they are not hashable, so they cannot appear as a key in a dictionary.
<!-- #endregion -->

# Title
Chapter 11

## Quiz Type
Formative

<!-- #region -->
### Question
Which one of these expressions is NOT a tuple?
- [ ] `tuple('abc')`
- [ ] `'abc',`
- [ ] `('abc',)`
- [X] `('abc')`


### Rationale
- The value of this expression is a tuple with the elements `'a'`, `'b'`, and `'c'`.
- Because of the comma at the end, the value if this expression is a tuple with on element, `'abc'`.
- Because of the comma, the value if this expression is a tuple with on element, `'abc'`. The parentheses are not required.
- The parentheses alone do not make a tuple, so the value of this expression is just the string `'abc'`.

<!-- #endregion -->

<!-- #region -->
### Question
What is the result of these statements?

```
t = tuple('abc')
s = [1, 2, 3]
d = {t: s}
```

- [ ] A `TypeError` because a tuple can't appear as a key in a dictionary.
- [ ] A `TypeError` because a list can't appear as a value in a dictionary.
- [ ] A syntax error because there should be a comma before the closing brace on the third line.
- [X] A dictionary with one item that maps from a tuple to a list.


### Rationale
- A tuple is immutable, so it can appear as a key in a dictionary -- as long as its elements are also immutable.
- Any type can appear as a value in a dictionary, including lists.
- The syntax is correct -- if there is a single item in a dictionary, a comma is legal but not required.
- These statements create a dictionary with one item that maps from a tuple to a list.

<!-- #endregion -->

<!-- #region -->
### Question
What does this function do?

```
def printall(*args):
    for value in reversed(args):
        print(value)
```
- [ ] It has a syntax error because the `*` operator is not legal before a parameter.
- [ ] It causes a `TypeError` because `args` is a tuple, which is immutable and cannot be reversed.
- [ ] It takes a single list or tuple and prints the values in reversed order.
- [X] It takes any number of arguments and prints them in reversed order.


### Rationale
- When the `*` operator appears before a parameter, it "packs" any number of arguments into a tuple.
- It's true that `args` is a tuple, which is immutable, but `reversed` does not modify the tuple, it makes a new object that loops through the tuple in reverse order.
- This function can take any number of arguments, not just a single argument.
- It takes any number of arguments and "packs" them into a tuple, then loops through the tuple in reverse order and prints the elements.

<!-- #endregion -->

### Question
What is the value of this expression?

```
('a', 3) < ('b', 1)
```

- [ ] `False` because `3` is greater than `1`.
- [ ] These values can't be compared because `'a'` is less than `'b'`, but `3` is greater than `1`.
- [ ] A `TypeError` because the `<` operator doesn't work with tuples.
- [X] `True` because `'a'` is less than `'b'`.

### Rationale
- When tuples are compared, the first elements are compared first. The other elements are only compared if the first elements are the same.
- When tuples are compared, the first elements are compared first. The other elements are only compared if the first elements are the same.
- The `<` operator compares the first elements of each tuple, and then compares other elements in the event of a tie.
- When tuples are compared, the first elements are compared first.



# Title
Chapter 12

## Quiz Type
Formative

<!-- #region -->
### Question
Assuming that `t` is a list of strings, what does the following line of code do?
```
sorted(t, key=len)
```

- [ ] Modifies `t` and sorts the elements in alphabetical order.
- [ ] Makes a new list that contains the elements in alphabetical order.
- [ ] Modifies `t` and sorts the elements from shortest to longest
- [X] Makes a new list that contains the elements in order from shortest to longest. 


### Rationale
- `sorted` makes a new list -- it doesn't modify `t` -- and `key=len` sorts the elements from shortest to longest. 
- With `key=len`, `sorted` sorts the elements from shortest to longest. 
- `sorted` makes a new list -- it doesn't modify `t`.
- `sorted` makes a new list, and `key=len` sorts the elements from shortest to longest.
<!-- #endregion -->

<!-- #region -->
### Question
What is the effect of running this program?

```
word_counter = {}
for line in open(filename):
    for word in split_line(line):
        word_counter[word] += 1
```
- [ ] It makes a dictionary that maps from each word to the number of times it appears.
- [ ] It has a syntax error because the indentation is not correct.
- [ ] It has a semantic error because all the keys in `word_counter` map to the value `1`.
- [X] It causes a `KeyError` when it tries to increment a value in `word_counter`.


### Rationale
- Because `word_counter` is initially empty, the program causes a `KeyError` when it tries to increment a value in `word_counter`.
- The indentation is correct, but the program causes a `KeyError` when it tries to increment a value in `word_counter`.
- Because `word_counter` is initially empty, the program causes a `KeyError` when it tries to increment a value in `word_counter`.
- Because `word_counter` is initially empty, the program causes a `KeyError` when it tries to increment a value in `word_counter`.

<!-- #endregion -->

<!-- #region -->
### Question

If we run the following lines of code, what is the probability that the result is `'a'`?

```
letters = ['a', 'b', 'c']
weights = [1, 2, 3]
random.choices(letters, weights=weights)
```

- [ ] 1/3
- [ ] 1/4
- [ ] 1/5
- [X] 1/6


### Rationale
- The weight associated with `'a'` is `1` and the total of the weights is `6`.
- The weight associated with `'a'` is `1` and the total of the weights is `6`.
- The weight associated with `'a'` is `1` and the total of the weights is `6`.
- The weight associated with `'a'` is `1` and the total of the weights is `6`, so the probability of choosing `'a'` is `1/6`.

<!-- #endregion -->

# Title
Chapter 13

## Quiz Type
Formative

<!-- #region -->
### Question
If the current working directory is `/home/dinsdale/photos` and you open a file using the relative path `mar-2023/photo1.jpg`, which of these expressions computes the absolute path of the file that gets opened?
- [ ] `''.join('/home/dinsdale/photos', 'mar-2023/photo1.jpg')`
- [ ] `'mar-2023/photo1.jpg' + '/home/dinsdale/photos'`
- [ ] `'/home/dinsdale/photos' + 'mar-2023/photo1.jpg'`
- [X] `os.path.join('/home/dinsdale/photos', 'mar-2023/photo1.jpg')`


### Rationale
- This way of using the string `join` method does not put a slash between the directories in the path.
- The order of the working directory and the relative path is reversed. Also, this way of using the string concatenation does not put a slash between the directories in the path.
- This way of using the string concatenation does not put a slash between the directories in the path.
- The `os.path.join` function joins the two paths with either a forward or backward slash, depending on which operating system is running.

<!-- #endregion -->

<!-- #region -->
### Question
After these statements run, what is the value of `s`?

```
x = 1
t = 1,
s = f'x is an int, {x}. t is a tuple, {t}'
```

- [ ] This is an error because `{x}` and `{t}` are not valid dictionaries.
- [ ] This is an error because a tuple can't be used as a value in an f-string.
- [ ] `'x is an int, {x}. t is a tuple, {t}'`
- [X] `'x is an int, 1. t is a tuple, (1,)'`


### Rationale
- `{x}` and `{t}` are not dictionaries -- the curly braces indicate that they are expressions that get replaced with string representations of their values. 
- Any valid expression can be used in an f-string.
- Inside the f-string, the expressions in curly braces are replaced with string representations of their values.
- Inside the f-string, the expressions in curly braces are replaced with string representations of their values.
<!-- #endregion -->

<!-- #region -->
### Question

After these statements run, what is the value of `db[key]`?

```
db = shelve.open('anagram_map', 'n')
key = 'opst'
db[key] = []
db[key].append('stop')
```

- [ ] `['stop']`
- [ ] `'stop'`
- [ ] `[], 'stop'`
- [X] `[]`


### Rationale
- The `append` method does not work as intended here because it modifies only the list in memory, not the one in the database.
- The `append` method does not work as intended here because it modifies only the list in memory, not the one in the database.
- The `append` method does not work as intended here because it modifies only the list in memory, not the one in the database.
- The `append` method does not work as intended here because it modifies only the list in memory, not the one in the database.
<!-- #endregion -->

# Title
Chapter 14

## Quiz Type
Formative

<!-- #region -->
### Question
To create an instance of a programmer-defined type, what is the correct order for these steps?
- [ ] Assign values to attributes, define a class, instantiate an object.
- [ ] Instantiate an object, define a class, assign values to attributes.
- [ ] Define a class, assign values to attributes, instantiate an object.
- [X] Define a class, instantiate an object, assign values to attributes.


### Rationale
- You can't assign attributes before you instantiate an object.
- You can't instantiate an object before you define its class.
- You can't assign attributes before you instantiate an object.
- You have to define a class, instantiate an object, and assign values to attributes, in that order.

<!-- #endregion -->

<!-- #region -->
### Question

These statements are intended to define a `Date` class and create a `Date` object. What is wrong with them?

```
def Date:
    """Represents a day of the year."""
    
date = Date()
date.year = 2024
date.month = 'January'
date.day = 11
``` 
   
- [ ] You can't have a class named `Date` and a variable named `date`.
- [ ] All of the attributes have to have the same type.
- [ ] The syntax is not correct for adding attributes to the object.
- [X] A class definition has to start with `class`, not `def`. 


### Rationale
- It is legal -- and common -- for a class name and a variable to be the same word, but the class name starts with an uppercase letter.
- The attributes of an object can be any type, and they don't have to be the same.
- Dot notation is used to set the value of an attribute and to read the value.
- A class definition has to start with `class`. A function definition starts with `def`.
<!-- #endregion -->

<!-- #region -->
### Question
Which of these is a correct description of this function? You can assume that `date` is a `Date` object that has a `day` attribute.

```
def increment_day(date):
    date.day += 1
    return date
```

- [ ] It is a pure function that returns `None`.
- [ ] It is an impure function that returns `None`.
- [ ] It is a pure function that returns a `Date` object.
- [X] It is an impure function that returns a `Date` object.


### Rationale
- This function modifies an attribute of the `Date` object it gets as a parameter, so it is an impure function. And it returns a reference to the same object, not `None`.
- This function returns a reference to a `Date` object, not `None`.
- This function modifies an attribute of the `Date` object it gets as a parameter, so it is an impure function.
- This function modifies an attribute of the `Date` object it gets as a parameter, so it is an impure function -- and it returns a reference to the same `Date` object.

<!-- #endregion -->

# Title
Chapter 15

## Quiz Type
Formative

<!-- #region -->
### Question
Suppose `time` is a `Time` object, and `increment` is an instance method defined in the `Time` class. 
What happens when we invoke `increment` like this?

```
time.increment(42)
```

- [ ] `42` is assigned to the first parameter of the method, and `time` is assigned to the second.
- [ ] This is an error because `increment` requires one arguments and two are provided.
- [ ] This is an error because `increment` requires two argument and only one is provided.
- [X] `time` is assigned to the first parameter of the method and `42` is assigned to the second.


### Rationale
- `time` is assigned to the first parameter of the method.
- This method requires two arguments -- `time` is the first and `42` is the second.
- Only one argument appears in parentheses, but `time` is passed to `increment` as the first argument.
- `time` is assigned to the first parameter of the method, which is conventionally called `self`, and `42` is assigned to the second.

<!-- #endregion -->

<!-- #region -->
### Question
Suppose `time` is a `Time` object, and `int_to_time` is a static method defined in the `Time` class. 
What happens when we invoke `int_to_time` like this?

```
start = Time.int_to_time(34800)
```

- [ ] This is an error because `int_to_time` requires one argument and two are provided.
- [ ] The `Time` class object is assigned to the first parameter of the method and `34800` is assigned to the second. 
- [ ] `34800` is assigned to the first parameter of the method and the `Time` class object is assigned to the second.
- [X] `34800` is assigned to the first parameter of `int_to_time`.


### Rationale
- There is only one argument here, `34800`.
- Because `Time` is a class, it is not passed as an argument.
- Because `Time` is a class, it is not passed as an argument.
- `34800` is assigned to the first parameter of `int_to_time`. Because `Time` is a class, it is not passed as an argument.

<!-- #endregion -->

<!-- #region -->
### Question
Which of the following statements is NOT correct?

- [ ] When we instantiate an object, its `__init__` method is invoked.
- [ ] When we use the `+` operator with an object, its `__add__` method is invoked.
- [ ] When we print an object, its `__str__` method is invoked.
- [X] When we define a new class, its `__init__` method is invoked.


### Rationale
- This statement is correct. 
- This statement is correct. 
- This statement is correct. 
- Defining a new class does not invoke its `__init__` method. 

<!-- #endregion -->

# Title
Chapter 16

## Quiz Type
Formative

<!-- #region -->
### Question
Which of these is the term for a function or method that works with more than one type of object?
- [ ] pure
- [ ] equivalent
- [ ] static
- [X] polymorphic


### Rationale
- A pure function or method does not modify the parameters or have other effects.
- If two values are considered equal, they are equivalent.
- A static method is associated with a class, rather than an object.
- A function that works with more than one type is polymorphic.

<!-- #endregion -->

<!-- #region -->
### Question

What is wrong with this class definition?

```
class Point:
    """Represents a point in 2-D space."""
    
    def __init__(self, x, y):
        x = self.x
        y = self.y
```

- [ ] `__init__` is not a legal name for a method because it does not start with a letter.
- [ ] The triple-quoted string has to be inside a method definition.
- [ ] The first parameter of the method should be called `point`, not `self`.
- [X] The assignment statements should be the other way around, as in `self.x = x` and `self.y = y`.


### Rationale
- The names of special methods like `__init__` begin and end with a two underscore characters. 
- A triple-quoted string inside a class definition is a docstring that provides information about the class.
- The first parameter of a method is conventionally named `self`.
- The assignment statements should be the other way around, as in `self.x = x` and `self.y = y`.

<!-- #endregion -->

<!-- #region -->
### Question
Suppose we define a `Line` class so that each `Line` object has two attributes that refer to `Point` objects.

```
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
```

If we import the `copy` function from the `copy` module and use it to make a copy of a `Line` object, which of these statements is true?

- [ ] The result is a deep copy that copies the `Line` object and the `Point` objects it contains.
- [ ] The result is a deep copy that copies the `Line` object but not the `Point` objects it contains.
- [ ] The result is a shallow copy that copies the `Line` object and the `Point` objects it contains.
- [X] The result is a shallow copy that copies the `Line` object but not the `Point` objects it contains.


### Rationale
- The `copy` function copies the `Line` object but not the `Point` objects it contains.
- The `copy` function makes a shallow copy.
- The `copy` function copies the `Line` object but not the `Point` objects it contains.
- The `copy` function makes a shallow copy, which copies the `Line` object but not the `Point` objects it contains.

<!-- #endregion -->

# Title
Chapter 17

## Quiz Type
Formative

<!-- #region -->
### Question
Which of the following is NOT a correct statement about class variables.
- [ ] They are defined inside a class definition, but not inside a method definition.
- [ ] They can be accessed using a class object.
- [ ] They can have any type.
- [X] They are immutable.


### Rationale
- It is true that class variables are defined inside a class definition, but not inside a method definition
- It is true that class variables can be accessed using a class object.
- It is true that class variables can have any type.
- This statement is false -- that is, class variables are mutable.

<!-- #endregion -->

<!-- #region -->
### Question
Suppose we define a `Card` class like this:

```
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
```

If this class does not provide an `__eq__` method, what happens if we compare two cards using the `==` operator.

- [ ] That's an error.
- [ ] By default, only the first attribute is compared.
- [ ] By default, all of the attributes are compared as if they were in a tuple.
- [X] By default, the objects are equal only if they are identical.


### Rationale
- It is not an error -- if a class provides no `__eq__`, the `==` operator has a default behavior. 
- If a class provides no `__eq__`, the `==` operator checks whether objects are identical. 
- If a class provides no `__eq__`, the `==` operator checks whether objects are identical. 
- If a class provides no `__eq__`, the `==` operator checks whether objects are identical.

<!-- #endregion -->

<!-- #region -->
### Question
Which of the following statements is true when one class inherits from another, like this:

```
class Hand(Deck):
    """Represents a hand of playing cards."""
```

- [ ] `Hand` is a parent class and `Deck` is a child class.
- [ ] Every function that works with `Hand` should also work with `Deck`.
- [ ] Every `Hand` object has the same attributes as every `Deck` object, no more or less.
- [X] Every method defined in the `Deck` class can also be invoked on a `Hand` object.


### Rationale
- In this example, `Hand` inherits from `Deck`, so `Hand` is the child class and `Deck` is the parent.
- If `Hand` inherits from `Deck`, it could have additional methods that don't work with `Deck`.
- If `Hand` inherits from `Deck`, a `Hand` object should have all of the attributes of a `Deck` object, but it can have more.
- If `Hand` inherits from `Deck`, every method defined in the `Deck` class should work with a `Hand` object.

<!-- #endregion -->

<!-- #region -->
### Question
What do we call it when one method invokes another to do most or all of the work?
- [ ] inheritance
- [ ] generalization
- [ ] specialization
- [X] delegation


### Rationale
- Inheritance is the ability to define a new class that is a modified version of a previously defined class.
- Generalization is when we add a parameter to a function to make its capabilities more general.
- Specialization is a way of using inheritance to create a new class that is a specialized version of an existing class.
- Delegation is when one method passes responsibility to another method to do most or all of the work.
<!-- #endregion -->

# Title
Chapter 18

## Quiz Type
Formative

<!-- #region -->
### Question
What is the result of this operation?

```
set('abba') <= set('abc')
```

- [ ] `False` because `'abba'` is longer than `'abc'`.
- [ ] A runtime error because `'abba'` contains duplicate elements, so it is not a `set`.
- [ ] A runtime error because a string is immutable, so it cannot be transformed into a `set`. 
- [X] `True` because the elements of `'abba'` are a subset of the elements of `'abc'`.


### Rationale
- With `set` objects, the `<=` operator checks whether one set is a subset of another -- it does not compare the length of the strings.
- When the set is create, the duplicate elements of the string are removed.
- The `set` function creates a new set -- it does not modify the string.
- With `set` objects, the `<=` operator checks whether one set is a subset of another -- including the possibility that they are equal.

<!-- #endregion -->

### Question
What is the value of counter after these statements run?

```
from collections import Counter

t = (1, 1, 1, 2, 2, 3)
counter = Counter(t)
```

- [ ] `(1, 1, 1, 2, 2, 3)`
- [ ] `{1: 3, 2: 2, 3: 1}`
- [ ] `Counter(1, 1, 1, 2, 2, 3)`
- [X] `Counter({1: 3, 2: 2, 3: 1})`

### Rationale
- The result is a `Counter` object, not a tuple.
- The result is a `Counter` object, not a dictionary.
- The result is a `Counter` object that contains items like a dictionary, not a tuple.
- The result is a `Counter` object that contains the elements of the list and the number of times each one appears.

<!-- #region -->
### Question
Which comment about this class definition is correct?

```
class Game:
    """Represents a game with a dictionary that maps from teams to scores."""
    
    def __init__(self, scores={}):
        self.scores = score
```

- [ ] All `Game` objects refer to different dictionaries.
- [ ] All `Game` objects refer to the same dictionary.
- [ ] All `Game` objects created with the default value of `scores` refer to an empty dictionary.
- [X] All `Game` objects created with the default value of `scores` refer to the same dictionary.  


### Rationale
- The default value of `scores` is a dictionary that is created when the function is defined. All `Game` objects created with the default value get a reference to it. 
- All `Game` objects created with the default value get a reference to it, but a `Game` object that overrides `scores` will refer to a different dictionary.
- The initial value of `scores` is an empty dictionary, but items might be added to it later. 
- All `Game` objects created with the default value get a reference to the same dictionary -- so if any of them modify it, they all see the change.
<!-- #endregion -->

<!-- #region -->
### Question

What is the value of this expression?

```
all(number < 10 for number in [2, 4, 6, 8])
```

- [ ] `[2, 4, 6, 8]`, which contains all numbers in the list less than `10`. 
- [ ] An error because the list comprehension has to be in square brackets.
- [ ] `False` because there are not any numbers in the list that are not less than `10`.
- [X] `True` because all numbers in the list are less than `10`. 


### Rationale
- The `all` function returns `True` if all elements of a sequence are `True`, and `False` otherwise.
- The expression in parentheses is correct -- it is a generator expression, not a list comprehension.
- The values produced by the generator expression are all `True`.
- The values produced by the generator expression are all `True`, so the result from the `all` function is `True`.
<!-- #endregion -->

<!-- #region -->
### Question
What is the value of `d[key]` after these statements run, or is there an error?

```
from collections import defaultdict

d = defaultdict(list)
key = ('into', 'the')
d[key].append('woods')
```

- [ ] An error because a tuple cannot be used as a key in a `defaultdict`.
- [ ] An error because we have to add the key to the `defaultdict` before we can look it up. 
- [ ] `'woods'`
- [X] `['woods']`


### Rationale
- A tuple can appear as a key in a `defaultdict`, same as in a dictionary.
- When you look up a key that is not already in this `defaultdict`, the key is added with a new empty list as the value.
- When the key is added to the `defaultdict`, the corresponding value is an empty list. Then the `append` method add an element to the list.
- When the key is added to the `defaultdict`, the corresponding value is an empty list. After the `append` method is invoked, the list contains a single element, the string `'woods'`.
<!-- #endregion -->

### Question

What value is printed when this function runs?

```
def pack_and_print(**kwargs):
    print(kwargs)
    
pack_and_print(a=1, b=2)
```

- [ ] This is an error because the exponentiation operator `**` can't appear in a list of parameters.
- [ ] `[(a, 1), (b, 2)]`
- [ ] `{'a', 'b'}, [1, 2]`
- [X] `{'a': 1, 'b': 2}`

### Rationale
- In a parameter list, `**` is the pack operator, not the exponentiation operator.
- The pack operator, `**`, packs the keyword arguments into a dictionary, not a list of tuples.
- The pack operator, `**`, packs the keyword arguments into a dictionary, not a set and a list.
- The pack operator, `**`, packs the keyword arguments into a dictionary that maps from keyword names to values.


```python

```

# Title
Think Python

## Quiz Type
Summative

<!-- #region -->
### Question
What is the output of this program?

```
s = '3'
str(s) * int(s)
```

- [ ] The integer `9`
- [ ] The string `'9'`
- [ ] The integer `333`
- [X] The string `'333'`


### Rationale
- `str(s)` is the string `'3'`, and `int(s)` is the integer `3`. See Chapter 1, "chaptertitle".
- Multiplying a string by the integer `3` repeats the string three times. See Chapter 1, "chaptertitle".
- When we multiply a string by an integer, the result is a string. See Chapter 1, "chaptertitle".
- Multiplying a string by the integer `3` repeats the string three times. See Chapter 1, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
For this function to work without causing an error, what are the preconditions for `n`?

```
def countdown(n):
    if n == 0:
        print('Blastoff!')
    else:
        print(n)
        countdown(n-1)
```


- [ ] `n` must be a `float`.
- [ ] `n` must be negative.
- [ ] `n` must be strictly positive, not `0`.
- [X] `n` must be a positive integer or `0`.


### Rationale
- `n` can be a `float` with no fraction part, but it can also be an `int`. See Chapter 5, "chaptertitle".
- If `n` is negative, it recurses until the stack reaches its limit and causes a `RecursionError`. See Chapter 5, "chaptertitle".
- If `n` is `0`, the function prints `'Blastoff!'` and returns without making a recursive call. See Chapter 5, "chaptertitle".
- `n` must be non-negative -- that is, positive or `0`. See Chapter 5, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What is wrong with the following program?

```
def compare(x, y):
    if x < y:
        return -1
    else:
        return 1    
    return 0
```

- [ ] It has a syntax error because the last line is not indented.
- [ ] It has a runtime error because the return value cannot be negative. 
- [ ] It has a syntax error because it has more than one return statement.
- [X] It has a logic error because the last line is dead code.


### Rationale
- The syntax of the program is correct, but there is an error. See Chapter 6, "chaptertitle".
- Any value is a legal return value -- but there is a logic error because the last line can never run. See Chapter 6, "chaptertitle".
- The syntax of the program is correct, but there is a logic error because the last line can never run. See Chapter 6, "chaptertitle".
- There is a `return` statement in both branches of the `if` statement, so the last line can never run -- it is dead code. See Chapter 6, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What is the output of this program, or is there an error?
```
def rectangle_area(length, width):
    return length * width
    
area = rectangle_area(3, 5)
print(length)
```
- [ ] `3` because the first argument gets assigned to `length`.
- [ ] `5` because the second argument gets assigned to `length`.
- [ ] Syntax error because there are two variables in the return statement.
- [X] Runtime error because the parameter `length` does not exist outside the function.


### Rationale
- `3` does get assigned to `length`, but the parameter only exists inside the function. See Chapter 6, "chaptertitle".
- The first argument gets assigned to `length`, but the parameter only exists inside the function. See Chapter 6, "chaptertitle".
- The variables are part of an arithmetic expression, which can be used in a return statement. See Chapter 6, "chaptertitle".
- Parameters and local variables only exist inside the functions where they are defined. See Chapter 6, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What is wrong with the following program?

```
s = int('123')
for digit in s:
    print(digit)
```


- [ ] There is nothing wrong -- the program is correct.
- [ ] `digit` is not a legal name for a loop variable.
- [ ] `int` is a type, not a function.
- [X] `s` is not a sequence, so we can't loop through its elements.


### Rationale
- The program generates a `TypeError`. See Chapter 7, "chaptertitle".
- Any legal variable name can be used as a loop variable. See Chapter 7, "chaptertitle".
- `int` is a type, but it can be used as a function to convert other types to integers. See Chapter 7, "chaptertitle".
- `s` is an integer, which is not a sequence, so it can't be looped over. See Chapter 7, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
Which of these is a correct way to convert a string to lowercase?

- [ ] `lower(str)`
- [ ] `str = lower(str)`
- [ ] `str.lower()`
- [X] `str = str.lower()`


### Rationale
- `lower` is a method, so it has to be invoked on a string, as in `str.lower()`; and it creates a new string, which should be assigned to a variable. See Chapter 7, "chaptertitle".
- `lower` is a method, so it has to be invoked on a string, as in `str.lower()`. See Chapter 7, "chaptertitle".
- `str.lower()` creates a new string, but if the string is not assigned to a variable, there is no way to access it. See Chapter 7, "chaptertitle".
- `str.lower()` creates a new string -- if we assign it back to `str`, the new string replaces the old one. See Chapter 7, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
The following function takes two strings as parameters and returns a string.
Which of the following docstrings is a correct description of what this function does?

```
def compute(word1, word2):
    t = []
    for letter in word1:
        if letter in word2:
            t.append(letter)
    return ''.join(t)
```

- [ ] Returns the letters that appear in either `word1` or `word2` or both.
- [ ] Returns the letters that appear in either `word1` or `word2` but not both.
- [ ] Returns the letters that appear in `word1` but not  `word2`.
- [X] Returns the letters that appear in both `word1` and `word2`.


### Rationale
- In order to get to the `append` method, `letter` has to appear in both words. See Chapter 7, "chaptertitle".
- In order to get to the `append` method, `letter` has to appear in both words. See Chapter 7, "chaptertitle".
- In order to get to the `append` method, `letter` has to appear in both words. See Chapter 7, "chaptertitle".
- This function returns a string that contains the letters that appear in both `word1` and `word2`. See Chapter 7, "chaptertitle".
<!-- #endregion -->

<!-- #region -->
### Question
This function is intended to convert the first letter of a word to lowercase and the rest of the letters to uppercase.

```
def lower_upper(word):
    first = word[0]
    rest = word[1:]
    word = first.lower() + rest.upper()
```

What is the value of `word` if we call this function like this -- or is there an error?

```
word = lower_upper('Python')
```

- [ ] The result is a syntax error because a `:` character cannot appear inside the bracket operator.
- [ ] The result is a runtime error because `0` is not a valid index.
- [ ] The program is correct -- the value of `word` is `'pYTHON'`.
- [X] The program contains a logic error -- the value of `word` is `None`.


### Rationale
- A colon inside a bracket operator indicates a slice -- in this case, it selects all characters from the second to the end. See Chapter 8, "chaptertitle".
- `0` is a valid index -- it select the first character in the string. See Chapter 8, "chaptertitle".
- The function has no return statement, so it returns `None`. Assigning a new value to the parameter `word` has no effect outside the function. See Chapter 9, "chaptertitle".
- The function has no return statement, so it returns `None`. Assigning a new value to the parameter `word` has no effect outside the function. See Chapter 9, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
If we use the `search` function in the `re` module, which of the following strings matches this pattern: `r'^a(bc|de)f$'`?
- [ ] `'abcdef'`
- [ ] `'zadef'`
- [ ] `'abc'`
- [X] `'adef'`


### Rationale
- The pattern `'(bc|de)'` requires either `'bc'` or `'de'` but not both. See Chapter 8, "chaptertitle".
- The pattern `^a` requires the letter `a` at the beginning of the string. See Chapter 8, "chaptertitle".
- The pattern `f$` requires the letter `f` at the end of the string. See Chapter 8, "chaptertitle".
- This string has `'a'` at the beginning `'f'` at the end, and `'de'` in the middle. See Chapter 8, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What is the result of this program?

```
t = [1, 2, 3, 4]
t[1:-1]
```

- [ ] An `IndexError` because `-1` is not a legal index.
- [ ] `[1, 2, 3]`
- [ ] `[2, 3, 4]`
- [X] `[2, 3]`


### Rationale
- Negative indices count backward from the end of the sequence, so the slice index `1:-1` selects elements from the second to the second-to-last, including both. See Chapter 9, "chaptertitle".
- The slice index `1:-1` excludes the first element of the list. See Chapter 9, "chaptertitle".
- The slice index `1:-1` excludes the last element of the list. See Chapter 9, "chaptertitle".
- The slice index `1:-1` selects elements from the second to the second-to-last, including both. See Chapter 9, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
After these statements run, what are the values of `a` and `b`, or is there an error?

```
a, b = 1, 2
a, b = b, a
```

- [ ] There is a runtime error because the values on the right are tuples.
- [ ] There is a syntax error because the assignment statement has more than one variable.
- [ ] `a` is `1` and `b` is `2`.
- [X] `a` is `2` and `b` is `1`.


### Rationale
- The values on the right are tuples, but these are legal assignment statements. See Chapter 11, "chaptertitle".
- An assignment statement can have a tuple of variables on the left. See Chapter 11, "chaptertitle".
- After the first assignment `a` is `1` and `b` is `2`, but the second assignment swaps the values. See Chapter 11, "chaptertitle".
- After the first assignment `a` is `1` and `b` is `2`, and then the second assignment swaps the values. See Chapter 11, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
Why can't a list appear as a key in a dictionary?

- [ ] The elements in a list might not be totally ordered.
- [ ] The elements in a list can be different types.
- [ ] Lists can contain any number of elements.
- [X] Lists are mutable, which makes them unhashable.


### Rationale
- If the elements of a list are not totally ordered, they are not sortable, but that's not the reason a list can't appear as a key in a dictionary. See Chapter 10, "chaptertitle" and Chapter 11, "chaptertitle".
- The elements in a list can be different types, but that's not the reason a list can't appear as a key in a dictionary. See Chapter 10, "chaptertitle" and Chapter 11, "chaptertitle".
- Lists can contain any number of elements, but that's not the reason a list can't appear as a key in a dictionary. See Chapter 10, "chaptertitle" and Chapter 11, "chaptertitle".
- If an object is mutable, it isn't hashable, which means it can't be used as a key in a dictionary. See Chapter 10, "chaptertitle" and Chapter 11, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What is the primary difference between a list and a tuple?
- [ ] A list can contain any type; a tuple can only contain hashable types.
- [ ] A tuple can contain any type; a list can only contain hashable types.
- [ ] A tuple is mutable; a list is immutable.
- [X] A list is mutable; a tuple is immutable.


### Rationale
- Both lists and tuples can contain any type. Keys in dictionaries must be hashable. See Chapter 11, "chaptertitle".
- Both lists and tuples can contain any type. Keys in dictionaries must be hashable. See Chapter 11, "chaptertitle".
- It's the other way around: a list is mutable; a tuple is immutable. See Chapter 11, "chaptertitle".
- A tuple is immutable. See Chapter 11, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
Which of these is a correct way to reverse the elements of a list in place -- that is, by modifying an existing list without creating a new list?

- [ ] `t = reversed(t)`
- [ ] `reversed(t)`
- [ ] `t = t.reverse()`
- [X] `t.reverse()`


### Rationale
- This statement works, but it creates a new list and does not modify `t`. See Chapter 11, "chaptertitle".
- `reverse(t)` creates a new list, but if the list is not assigned to a variable, there is no way to access it. See Chapter 11, "chaptertitle".
- The return value from `t.reverse()` is `None`, so this statement sets `t` to `None`. See Chapter 11, "chaptertitle".
- `t.reverse()` reverses the elements of `t` without creating a new list. See Chapter 11, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What is the result of this program?

```
s = ['bbb', 'aa', 'c']
sorted(s, key=len, reverse=True)
```

- [ ] `['aa', 'bbb', 'c']`
- [ ] `['c', 'aa', 'bbb']`
- [ ] `['c', 'bbb', 'aa']`
- [X] `['bbb', 'aa', 'c']`


### Rationale
- `key=len` sorts by length, rather than alphabetical order, and `reverse=True` sorts in descending order. See Chapter 12, "chaptertitle".
- `reverse=True` sorts in descending order. See Chapter 12, "chaptertitle".
- `key=len` sorts by length, rather than alphabetical order. See Chapter 12, "chaptertitle".
- `key=len` sorts by length, rather than alphabetical order, and `reverse=True` sorts in descending order, so the result is `['bbb', 'aa', 'c']`. See Chapter 12, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What does the following function do?
```
def compute(d1, d2):
    res = {}
    for key in d1:
        res[key] = d1[key]
    for key in d2:
        res[key] = d2[key]
    return res
```

- [ ] Adds the keys from `d1` to `d2`.
- [ ] Adds the keys from `d2` to `d1`.
- [ ] Makes a new dictionary with all keys that are in both `d1` and `d2`.
- [X] Makes a new dictionary with all keys that are in either `d1` or `d2`.


### Rationale
- This function makes and returns a new dictionary. See Chapter 12, "chaptertitle".
- This function makes and returns a new dictionary. See Chapter 12, "chaptertitle".
- The new dictionary has all keys from either dictionary. See Chapter 12, "chaptertitle".
- The new dictionary has all keys from either dictionary. If the same key appears in both, it gets the value from `d2`. See Chapter 12, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
Suppose we run the following program to get the current working directory:

```
import os

os.getcwd()
```

And the result is `/home/dinsdale/photos`.
Now suppose we run the following program to check for the existence of a file:

```
os.path.exists('apr-2023/photo1.jpg')
```

What is the absolute path of the file that gets checked?

- [ ] `'photo1.jpg'`
- [ ] `'apr-2023/photo1.jpg'`
- [ ] `'/home/dinsdale/photo1.jpg'`
- [X] `'/home/dinsdale/photos/apr-2023/photo1.jpg'`


### Rationale
- Because `'apr-2023/photo1.jpg'` is a relative path, it gets joined to the current working directory. See Chapter 13, "chaptertitle".
- Because `'apr-2023/photo1.jpg'` is a relative path, it gets joined to the current working directory. See Chapter 13, "chaptertitle".
- Because `'apr-2023/photo1.jpg'` is a relative path, it gets joined to the current working directory. See Chapter 13, "chaptertitle".
- Because `'apr-2023/photo1.jpg'` is a relative path, it gets joined to the current working directory. See Chapter 13, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What is the result of this program?
```
class Day:
    def __init__(self, day):
        self.day = day

    def __str__(date):
        return f'Today is {date.day}'
    
print(Day('Wednesday'))
```
- [ ] `f'Today is Wednesday'`
- [ ] `'Today is {Wednesday}'`
- [ ] `f'Today is {date.day}'`
- [X] `'Today is Wednesday'`


### Rationale
- The `f` before the string indicates that it is a format string. See Chapter 15, "chaptertitle".
- The curly braces don't appear in the return value. See Chapter 15, "chaptertitle".
- The `f` before the string indicates that it is a format string, and the expression in curly braces gets replaced by its value. See Chapter 15, "chaptertitle".
- In a format string, the expression in curly braces gets replaced by its value. See Chapter 15, "chaptertitle".
<!-- #endregion -->

<!-- #region -->
### Question
Assuming that the `Animal` class exists, what is the output of this program?

```
class Cat(Animal):
    """Represents a cat."""
    
cat = Cat()
isinstance(cat, Animal)
```

- [ ] `False` because an instance of a parent class is not an instance of the child class.
- [ ] `False` because an instance of a child class is not an instance of the parent class.
- [ ] `True` because every instance of a parent class is also an instance of the child class.
- [X] `True` because every instance of a child class is also an instance of the parent class.


### Rationale
- It's true that an instance of a parent class is not an instance of the child class, but that's not what's being checked here. See Chapter 17, "chaptertitle".
- Every instance of a child class is also an instance of the parent class. See Chapter 17, "chaptertitle".
- An instance of a parent class is not an instance of the child class. See Chapter 17, "chaptertitle".
- In this example, `Cat` is a child class of `Animal`, so every `Cat` object is also an instance of `Animal`. See Chapter 17, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
What is the result of this program?

```
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
p[1]
```

- [ ] `AttributeError` because the attributes of `p` are `x` and `y`.
- [ ] `IndexError` because the attributes of `p` are `x` and `y`.
- [ ] `3` because `p` is a `namedtuple` and the element with index `1` is `3`.
- [X] `4` because `p` is a `namedtuple` and the element with index `1` is `4`.


### Rationale
- The attributes of `p` are `x` and `y`, but because `p` is a `namedtuple`, we can use the  bracket operator to access the elements by index. See Chapter 18, "chaptertitle".
- The attributes of `p` are `x` and `y`, but because `p` is a `namedtuple`, we can use the  bracket operator to access the elements by index. See Chapter 18, "chaptertitle".
- In a named tuple -- as in a tuple -- the index of the first element is `0`. See Chapter 18, "chaptertitle".
- In a named tuple -- as in a tuple -- the index of the second element is `1`. See Chapter 18, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
We can call the built-in function `round` like this:

```
import math

round(math.pi, ndigits=3)
```

The result is the value of `math.pi` round off to three decimal places.
Now suppose we have the positional argument in a tuple and the keyword argument in a dictionary, like this:

```
args = (math.pi,)
kwargs = {"ndigits": 3}
```

Which of these is a correct way to call `round` and get the same result?

- [ ] `round(args, kwargs)`
- [ ] `round(*args, *kwargs)`
- [ ] `round(**args, **kwargs)`
- [X] `round(*args, **kwargs)`


### Rationale
- In order to pass the elements of `args` as positional arguments, we have to unpack them with the `*` operator. Similarly, to pass the items in `kwargs` as keyword arguments, we have to unpack them with the `**` operator. See Chapter 18, "chaptertitle".
- To pass the items in `kwargs` as keyword arguments, we have to unpack them with the `**` operator. See Chapter 18, "chaptertitle".
- To pass the elements of `args` as positional arguments, we have to unpack them with the `*` operator. See Chapter 18, "chaptertitle".
- The `*` operator unpacks the elements of `args` and the `**` operator unpacks the items in `kwargs`. See Chapter 18, "chaptertitle".

<!-- #endregion -->

<!-- #region -->
### Question
- [ ] 
- [ ] 
- [ ] 
- [X] 


### Rationale
- 
- 
- 
- 

<!-- #endregion -->
