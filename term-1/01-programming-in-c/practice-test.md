# Module 1 Practice Test: Programming in C

> [Cybersecurity and Digital Forensics](../../README.md) › [Term 1](../README.md) › [Module 1](README.md) › **Practice Test**

| ⬅ [Last session](session-09-pointers.md) | [Module overview](README.md) ➡ |
|:---|---:|

Answer every question first, then open the hidden answers to check yourself. Aim for 16/20 or better before moving on.

---

## Part A: Multiple-choice questions

**1.** Which line is needed to use `printf`?
A) `#include <stdlib.h>` B) `#include <stdio.h>` C) `#include <string.h>` D) `#define printf`

**2.** A step-by-step, finite procedure for solving a problem is a(n):
A) Compiler B) Flowchart C) Algorithm D) Header

**3.** In a flowchart, a decision is drawn as a:
A) Rectangle B) Oval C) Parallelogram D) Diamond

**4.** What does `printf("%d", 7 / 2);` print?
A) 3.5 B) 3 C) 4 D) 3.0

**5.** Which format specifier reads a `double` with `scanf`?
A) `%f` B) `%d` C) `%lf` D) `%c`

**6.** Why does `scanf("%d", &age);` use `&`?
A) It makes the value positive B) `scanf` needs the address to store the value C) It converts to text D) It is optional style

**7.** What is the value of `17 % 5`?
A) 3 B) 2 C) 3.4 D) 5

**8.** `if (x = 0)` is a bug because:
A) It compares x to 0 B) It assigns 0 to x and the condition is always false C) It does not compile D) It crashes

**9.** What is `5 & 3`?
A) 1 B) 7 C) 8 D) 15

**10.** Without `break` in a `switch` case, execution:
A) Stops B) Falls through to the next case C) Restarts the switch D) Fails to compile

**11.** Which loop always runs its body at least once?
A) `for` B) `while` C) `do...while` D) None

**12.** `continue` inside a loop:
A) Exits the loop B) Ends the program C) Skips to the next iteration D) Repeats the same iteration

**13.** C passes ordinary arguments to functions:
A) By reference B) By value C) By name D) Globally

**14.** A function prototype tells the compiler:
A) The function body B) Its name, return type and parameter types C) Where it is stored D) How long it runs

**15.** For `int a[5];` the valid indexes are:
A) 1 to 5 B) 0 to 5 C) 0 to 4 D) 1 to 4

**16.** How many visible characters can `char name[8];` safely hold as a string?
A) 8 B) 7 C) 9 D) 6

**17.** Which function should never be used because it cannot limit input length?
A) `fgets` B) `gets` C) `snprintf` D) `strncpy`

**18.** If `int x = 10; int *p = &x;` then `*p` is:
A) The address of x B) 10 C) The address of p D) Undefined

**19.** After `malloc`, you must first:
A) Call `free` B) Check the result is not `NULL` C) Cast it to `char` D) Print it

**20.** Using a pointer after its memory has been freed is called:
A) Stack overflow B) Memory leak C) Use-after-free D) Integer overflow

<details>
<summary>✅ Answers to Part A</summary>

| Q | Ans | Q | Ans |
|---|---|---|---|
| 1 | B | 11 | C |
| 2 | C | 12 | C |
| 3 | D | 13 | B |
| 4 | B | 14 | B |
| 5 | C | 15 | C |
| 6 | B | 16 | B (one byte for `'\0'`) |
| 7 | B | 17 | B |
| 8 | B | 18 | B |
| 9 | A (`101 & 011 = 001`) | 19 | B |
| 10 | B | 20 | C |

</details>

## Part B: Scenarios

**Scenario 1: The login lockout.** A lab login program lets a user try a PIN forever. Design the fix: which loop would you use, what variable counts attempts, and what happens after 3 failures?

<details>
<summary>Model answer</summary>

Use a `do...while` (or `while`) loop with an `attempts` counter starting at 0. Each wrong PIN increments it; the loop condition is `pin != correct && attempts < 3`. After the loop, if `attempts == 3` print "Account locked" and exit. This limits brute-force guessing, the same idea real systems use for lockout.

</details>

**Scenario 2: The name that crashed the program.** This code crashes when a student types a long name:

```c
char name[10];
scanf("%s", name);
```

Explain why and rewrite it safely.

<details>
<summary>Model answer</summary>

`%s` copies as many characters as typed into a 10-byte array, writing past its end: a **buffer overflow** that can corrupt memory or be exploited. Safe version:

```c
char name[10];
if (fgets(name, sizeof name, stdin)) {
    name[strcspn(name, "\n")] = '\0';
}
```

`fgets` never writes more than `sizeof name` bytes, including the terminating `'\0'`.

</details>

**Scenario 3: The growing memory.** A log-processing program calls `malloc` for every line it reads but the machine slowly runs out of memory. Another version crashes randomly after a cleanup step. Name both bugs and the fix for each.

<details>
<summary>Model answer</summary>

- **Memory leak:** memory from `malloc` is never released. Fix: `free` each buffer once it is no longer needed.
- **Use-after-free / dangling pointer:** the cleanup frees a buffer but the code keeps using the pointer. Fix: set the pointer to `NULL` right after `free` and check for `NULL` before use.

Always check `malloc`'s return value for `NULL` too.

</details>

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Cybersecurity and Digital Forensics</sub>
