# How to Make a Personal Website: From Idea to Launch

> Everyone can have their own website — and it's easier now than ever.

---

## 1. What Kind of Site Do You Need?

Don't think about tech yet. First, figure out what you want.

### Three Common Types of Personal Sites

```
Personal Website
 ├─ Static Portfolio — Show off projects, portfolio, resume
 ├─ Blog — Write articles, record thoughts, share knowledge
 └─ Combo — Landing page + blog
```

### How to Decide?

Ask yourself one question:

> **Do I have things I want to write down and share?**

- **Yes** → Build a blog. You built something, read something, had a thought — and you want to tell people about it.
- **No** → A static portfolio is enough. Put up your project links, a bio, and contact info.

> If you're not sure, start with a static site. You can always add a blog later.

---

## 2. What Makes Up a Website?

A lot of people get intimidated by words like "frontend" and "backend." But it's actually pretty simple:

### Think of It Like a Restaurant

```
Website = A Restaurant
 ├─ Frontend = The dining area, decor, menu — everything you see
 │    ├─ Table arrangement, lighting = CSS (styles)
 │    ├─ Menu categories = HTML (structure)
 │    └─ Host greeting you, seating you = JavaScript (interaction)
 │
 └─ Backend = The kitchen, storage — stuff you don't see but makes everything work
      ├─ Ingredients in the fridge = Database (stores articles, user info)
      ├─ Chef's cooking process = Server logic (registration, login, search)
      └─ Utilities (gas, electricity) = Server (24/7 operations support)
```

### Minimum Requirements for a Personal Site

| Element | Description | Required? |
|---------|-------------|-----------|
| **Domain** | Website address, like `yourname.com` | Recommended |
| **Frontend pages** | Homepage, about page, project showcase | ✅ |
| **Styles** | Nice colors, typography, animations | ✅ |
| **Hosting** | Keeps your site online 24/7 | ✅ |
| **Database** | Stores articles, comments | Needed for blogs |
| **Admin panel** | Management interface for writing | Needed for blogs |

---

## 3. How Easy Is It to Make a Website Now?

In the old days, making a website required:
1. Learning HTML / CSS / JavaScript
2. Learning a framework (React / Vue / Django)
3. Learning server deployment
4. Configuring a domain and HTTPS

Now, with **Vibe Coding** (using AI to write code), the process looks like this:

```
Have an idea
    ↓
Describe it in natural language to AI (e.g., "Make me a personal homepage")
    ↓
AI generates the code
    ↓
Tweak and refine
    ↓
One-click deploy
```

**The hard part is no longer the technology — it's the ideas.**

> If you don't know what to build, go look at other people's websites first.

---

## 4. Finding Inspiration from Other Sites

Here are the sites I referenced when building my own. Each one taught me something different:

### Personal Homepages

| Site | What to Learn |
|------|---------------|
| [brittanychiang.com](https://brittanychiang.com) | Clean personal homepage layout, timeline for experience |
| [joshwcomeau.com](https://joshwcomeau.com) | Beautiful interactions and animations |
| [overreacted.io](https://overreacted.io) | Dan Abramov's blog — content-focused design |
| [leerob.io](https://leerob.io) | Minimal personal homepage + blog |

### Inspiration Sources

| Site | What to Learn |
|------|---------------|
| [cssauthor.com](https://cssauthor.com) | Tons of ready-made website templates |
| [awwwards.com](https://awwwards.com) | Award-winning website designs for inspiration |
| [dribbble.com](https://dribbble.com) | UI designers' portfolios |

> How to use these: Find a layout you like → Screenshot it → Ask AI to generate something similar → Replace with your own content.

---

## 5. On Design and Styling

### The Most Important Thing First

> **A website is for other people to see. Content is king. Fancy styling doesn't matter.**

Look at the big players' sites: \[link to a prominent website\]

They might not have flashy animations or complex layouts, but the content is solid and comfortable to read. That's a good website.

> Style serves content. Write good content first. As long as the styling is "clean and readable," that's enough.

### If You Want to Go Further

If "clean and readable" isn't satisfying enough and you want to make something more polished, here's a process:

```
Version 1: Copy someone's layout, get the functionality working
     ↓
Version 2: Swap out colors, change the font
     ↓
Version 3: Adjust spacing, add a little animation
     ↓
Version 4: Redo the layout, try a different style
     ↓
……Keep going until Version 20
```

**Set yourself a goal: iterate 20 times.**

Not all at once — redesign every so often. Each time you'll get a little better.

### How to Actually Iterate

1. **Reference → Copy → Innovate**
   - Start by imitating layouts you like
   - Understand why they look good
   - Then add your own twist

2. **Let AI Generate Styles for You**
   - "Give me 5 different color schemes"
   - "Redesign this page with glassmorphism"
   - "Make the nav bar look more modern"

3. **Changing the Font Changes Everything**
   - Chinese font recommendations: Source Han Sans, Noto Serif SC
   - English font recommendations: Inter, JetBrains Mono

4. **Minimalism Is Never Wrong**
   - More whitespace
   - Fewer colors (stick to 3 main colors max)
   - Fine-tune letter spacing and line height for comfort

---

## 6. Common Pitfalls (Avoid These)

Most people don't give up because building a website is hard. They give up because they fall into these traps.

### Trap Zero: Forgetting Why You're Making a Site

> A personal website is about **presenting yourself and making an impression**.

What projects have you worked on? What are your thoughts? What are you good at? — Show it all through your site so people remember you.

But keep this in mind:

> **A good craftsman needs good tools, but the skill matters more.**

A website is just a display case. What's inside is what counts. If you have no projects to show and nothing to write, even the prettiest site is empty.

**The right order:**

```
First, have content (projects, work, thoughts)
    ↓
Then, build the site (showcase them)
    ↓
Keep updating (more content → richer site)
```

> The traps below all stem from getting this order backwards.

### Trap One: Waiting Until You've Mastered the Basics

> "I'll start once I've learned HTML, CSS, JavaScript, React, Django…"

**Result**: Month after month of studying, never quite done with the "basics," and the project never starts.

**The right approach:**

```
Want an effect → Look up how to do it → Build it → Get stuck → Learn as you go
```

> Don't "learn first, then do." **Learn by doing.** You only need to know enough to get the job done, not master everything before starting.

### Trap Two: Learning a Ton That You Never Use

> Spent three weeks learning the entire React ecosystem, then picked a static template, tweaked it, and called it a day.

**Result**: All that learning went to waste, and so did your motivation.

**The right approach**:
- Think first: what does this site actually need?
- A static site? You don't need a backend.
- A blog? Pick Django or WordPress — one is enough.
- **Only learn what you need right now. Learn the rest when you actually need it.**

### Trap Three: Overwhelmed by Too Many Choices

Search engines will throw dozens of technologies at you:

```
Frontend: React, Vue, Svelte, Next.js, Nuxt, Astro, Hugo……
Backend: Django, Flask, FastAPI, Spring Boot, Express, Ruby on Rails……
Databases: MySQL, PostgreSQL, MongoDB, SQLite……
Deployment: AWS, Vercel, Netlify, PythonAnywhere, Railway……
```

**Result**: Analysis paralysis. You give up before even starting.

**Remember: everything comes back to the same fundamentals.**

| Layer | What It Does | No Matter the Framework |
|-------|-------------|-------------------------|
| Frontend | Renders pages, handles user interaction | It's all HTML + CSS + JS |
| Backend | Processes data, runs business logic | Receive request → Process → Return response |
| Database | Stores data | It's all CRUD (create, read, update, delete) |

> **Pick the language you know best and use its ecosystem.** If you know Python, use Django. If you know JavaScript, use Next.js. Tech is a tool, not the goal.

### Trap Four: Trying to Invent Your Own Style from Scratch

> "I'm going to design a completely unique website that no one has seen before."

**Result**: Staring at a blank editor all afternoon without writing a single line.

**The right approach:**

```
Copy first → Modify → Develop your own style
```

- See a nice nav bar? Copy it.
- See a color scheme you like? Copy it.
- See a good layout? Copy it.

> Copying isn't plagiarism — it's learning. Combine elements from multiple designs you like, adapt them to your content, and your own style will emerge naturally.

**Set a goal for yourself: iterate 20 versions.**
Version 1 might look terrible. That's fine. Version 10 will be better. By Version 20, it'll be something you're proud of.

---

## 7. Summary

```
The right order to build a website:

1. Figure out what you want (static site or blog)
2. Browse other people's sites for inspiration
3. Use AI to quickly generate a first version
4. Launch it so others can visit
5. Keep iterating — aim for 20 versions
6. Develop your own style over time
```

> Don't wait for "perfect" before launching. Build it first, then improve.
> Perfection isn't designed — it's iterated.

---

### Appendix: My Tech Stack

If you want to build a similar Django blog project, here's what I used:

| Technology | Purpose |
|------------|---------|
| Django 6.0 | Python web framework |
| SQLite | Database |
| django-ckeditor-5 | Rich text editor |
| PythonAnywhere | Server hosting |
| GitHub Actions | Auto-deployment |
