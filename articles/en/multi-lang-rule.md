# How I Solved Translation Chaos on a Multilingual Website with a Single Rule

> The moment your site goes from one language to three, the chaos begins.

---

## From "Chinese Is Fine" to "Wait, I Need Translations Too?"

When I started this blog, the idea was simple: write in Chinese, for Chinese readers, everything in Chinese.

Then I realized that wouldn't cut it.

First, I have friends who don't speak Chinese. Second, projects I've built deserve a wider audience. And third, I wanted to practice writing in English and Japanese. So I decided: **sync all content in Chinese, English, and Japanese.**

That's when the trouble started.

---

## How the Chaos Began

At first, there were no rules. I'd change things on a whim.

I changed "About" to "About Me" in the nav bar — but only in the Chinese template. The English and Japanese pages still showed "About" and "について." My thinking was, "I'll fix Chinese first, then come back to the other two."

"Come back" never happened.

A month later, I looked at `base.html` and found three different states of text: Chinese hard-coded, English half-translated, Japanese untouched. The `.po` files had over a dozen untranslated entries. Even I couldn't tell which strings had been translated and which hadn't.

**That's what happens when you have no rules.**

---

## Where the Problem Really Lies

Vibe Coding (building with AI) has one defining quality: **speed**.

You tell the AI "update the nav bar," and it's done in 10 seconds. You see the result, it looks good, and you move on. As for the English and Japanese pages? Forgotten.

It's not a matter of attitude — it's a process problem. Vibe Coding makes it so easy to change code that you'll naturally forget that "changing Chinese also means changing the other two languages."

And the AI won't remind you — it only does what you ask. You say "change '关于' to '关于我'," and it changes exactly that. It has no idea your site has three languages.

---

## The Solution: One Rule

The fix isn't about remembering — it's about **rules**.

I wrote a single rule and put it in the project's `.trae/skills/` directory, so the AI would automatically reference it before making any changes. The core of the rule is just one sentence:

> **Before changing anything, ask yourself: how many languages does this change affect?**

The rule breaks down into a few parts:

### 1. When Does This Rule Apply?

It's not just UI text. These changes all involve language sync:

- Editing nav bar items, buttons, titles, and other interface text
- Writing or publishing blog articles
- Adding new page templates
- Changing descriptive text on any page

### 2. Standard Procedure for UI Text Changes

```
Edit code → Run makemessages to extract translations → Edit three .po files → Compile .mo
```

In short: use `{% trans "xxx" %}` or `_('xxx')` in your code to mark translatable strings, extract them into `.po` files with Django's commands, fill in translations one by one, then compile.

### 3. Handling Blog Content

Blog articles don't go through `.po` files. You need to maintain three language versions manually:

```
blog/content/
├── zh-hans/article.md    ← Chinese original
├── en/article.md         ← English translation
└── ja/article.md         ← Japanese translation
```

The rule says: **At minimum, the Chinese version must be complete. English and Japanese can start as shorter versions, but they can't be blank.**

### 4. The Post-Change Checklist

This is a "foolproof" checklist to run through after every change:

- Are all three languages translated?
- Are all three `.po` files filled in?
- Have you compiled the `.mo` files?
- Have you switched languages to check how it looks?

---

## How Well Does It Work?

After adding the rule as a skill, whenever I ask the AI to change something, it follows the rule automatically.

For example, I said, "Change the homepage title to '探索日志'":

Before: AI would only change Chinese → Done → English and Japanese untouched.

Now: AI reads the rule → recognizes this involves multiple languages → changes Chinese → extracts translations → waits for me to fill in English and Japanese → compiles → Done.

**It went from "relying on human memory" to "relying on rule enforcement."**

---

## What You Can Learn from This

If you're building a multilingual site (regardless of your tech stack), these suggestions might help:

1. **Set up the translation framework from day one.** Even if you only need one language now, get the i18n infrastructure in place. Adding a language later is just a config change, not a rewrite.
2. **Write the rules inside your project.** Don't bury them in a document somewhere. Put them where the AI can read them (like `.trae/skills/`, `.cursorrules`).
3. **A checklist is faster than re-reading docs.** Ticking a few checkboxes after every change is way more efficient than re-reading an entire rules document.
4. **Systems and people both get lazy.** It's not about attitude — it's about process. Replace memory with rules, replace manual steps with automation.

---

## Appendix: Where to Put the Rule File

I use Trae IDE, so my rule lives at:

```
.trae/skills/multi-lang-maintenance/SKILL.md
```

If you use Cursor, the equivalent is:

```
.cursorrules
```

Alternatively, you can write it in a plain markdown file and glance at it before every change. The key isn't the tool — it's **having a rule at all**.

> A multilingual site without rules? Three months later, even you won't understand it. 😅

---

*This article itself was written following this same rule. The version you're reading is the English translation. The Chinese original and Japanese versions were published simultaneously.*
