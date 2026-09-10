# Grace Liu — research portfolio

Plain HTML and CSS. No build step, no framework, no dependencies. Open `index.html`
in a browser and it works. That's deliberate: it means this site will still work in
five years, and you can fix a typo from your phone.

```
portfolio/
├── index.html          Home: hero, filterable Selected Work grid, About
├── styles.css          All styling for every page
├── work/
│   └── norbert-request-relay.html
└── README.md
```

---

## Recommended workflow

Put the site on GitHub Pages and edit it in the browser. In the repo: click a
file, click the pencil icon, edit, **Commit changes** — live in about a minute.

The reason to prefer this over editing a local download: there's only ever one
copy, so you never have to work out which version is current. Every change is
saved, a bad edit reverts in one click, and you get a URL you can share.

Editing locally is fine for a big restructure — but push it back up when you're
done rather than leaving two copies in play.

## Editing, day to day

There's no build step. You edit an `.html` file, save, refresh the browser. That's it.

**What to edit with.** [VS Code](https://code.visualstudio.com) is free and will
colour the tags so you can see what you're doing. Any plain-text editor works.
Two to avoid: Word, and TextEdit in its default mode — both save rich text and
will corrupt the file. (If you must use TextEdit: Format → Make Plain Text first.)

**Where the text lives.** Each page is one file. There's no database and no
template layer, so the sentence you want to change is sitting in the file as a
sentence.

| To change | Open |
|---|---|
| A card in the Selected Work grid | `index.html` → the `PROJECTS` list near the bottom |
| The homepage headline, intro, or About section | `index.html` → the `<main>` block |
| Anything inside a case study | that page in `work/` or `writing/` |
| Colours, fonts, spacing | `styles.css` → the `:root` block at the top |

**How to see your change.** Double-click `index.html` to open it in a browser,
then refresh after each save. If you want the single-file preview updated too,
run `python3 build_preview.py`.

### The only HTML you actually need

Text lives between an opening and closing tag. Change the text, leave the tags:

```html
<p>This is a paragraph. Edit these words freely.</p>
<h2 id="findings">A section heading</h2>
<li>A bullet point</li>
<strong>bold</strong> and <em>italic</em>
```

The other patterns already in the pages, if you want to add more of them:

```html
<blockquote>
  <p>A participant quote.</p>
  <cite>P3, age 23</cite>
</blockquote>

<div class="cs-note">
  <p>A caveat or disclosure box.</p>
</div>
```

Four things that will break the page if you get them wrong:

1. **Every opening tag needs its closing tag.** `<p>` … `</p>`.
2. **Don't change `class="..."` values.** They're what the stylesheet hooks onto.
   `<div class="cs-note">` styled correctly; `<div class="note">` styled not at all.
3. **Write `&amp;` instead of a bare `&`** in text. (`Research &amp; analysis`.)
4. **If you rename a section heading, update its `id` and the matching link** in
   that page's `<nav class="cs-toc">` list — otherwise the sidebar link goes nowhere.

### Editing once it's live on GitHub Pages

This is the easiest workflow and it needs nothing installed. In your repo on
github.com: click the file → the pencil icon → make the edit → **Commit changes**.
The site rebuilds in about a minute.

It also means you can fix a typo from your phone, and every version is saved, so
a bad edit is one click to revert.

### Common tasks

**Reorder projects** — move a block up or down in the `PROJECTS` list. Order in
the list is order on the page.

**Hide a project without deleting it** — wrap it in `/*` and `*/`:

```js
/*
{
  title: "Content design at Workiva",
  ...
},
*/
```

**Retire a project permanently** — delete its block from `PROJECTS`, then delete
its file from `work/` or `writing/`.

**Never edit `preview.html`.** It's generated from the other files, and
`build_preview.py` overwrites it. Same for anything you'd change there — change it
in the real file instead.

## The Writing section

Two parts:

- **`writing/*.html`** — one page per piece. Edit these directly, like any other
  page. Each is a title, a metadata block, a few paragraphs, and a link out at
  the bottom.
- **The `WRITING` list in `index.html`** — controls the four-column directory on
  the homepage: which categories exist, what's in each, and the short note under
  each title.

To add a piece: copy an existing file in `writing/`, replace the content, then add
a matching object to the right category in `WRITING`.

The link at the bottom of each page is one of three shapes:

```html
<!-- a PDF in assets/ -->
<a href="../assets/file.pdf">Read the PDF</a>
<span class="cta-note">PDF &middot; short label</span>

<!-- a live article -->
<a href="https://..." target="_blank" rel="noopener">Read the piece</a>
<span class="cta-note">Published March 2023</span>

<!-- nothing to link yet -->
<span class="cta-pending">Link to add</span>
<span class="cta-note">URL to be added</span>
```

## Adding or editing a project

Everything in the Selected Work grid comes from one array. Open `index.html`, scroll
to the `PROJECTS` list near the bottom, and copy an existing block:

```js
{
  title: "Voice agent discovery with older adults",
  tags: ["product"],                    // "product" | "academic" | "case" | "writing"
  href: "work/voice-agent.html",        // or null if not written yet
  wide: false,                          // true = spans two columns
  blurb: "One or two sentences on what you found, not what the topic was.",
  meta: ["Field research", "Norbert Health"]
},
```

Notes:

- **`tags` can hold more than one.** `tags: ["writing", "academic"]` makes the item
  appear under both filters. The filter counts update automatically.
- **`href: null`** renders the card as "Write-up in progress" with no link. Useful for
  claiming the work now and writing it later.
- **`wide: true`** should stay rare. One, maybe two. Its whole job is to signal which
  project you want read first, and that stops working if everything is wide.
- **Order in the array is the order on the page.** Most recent and most relevant first.

## Adding a new case study page

Copy `work/norbert-request-relay.html`, rename it, and replace the content inside
`<article class="cs-body">`. The stylesheet already handles:

| Element | What to use |
|---|---|
| Section heading | `<h2 id="slug">` — add a matching entry to the `.cs-toc` list |
| Summary panel at top | `<div class="cs-tldr">` with a `<dl>` inside |
| A numbered finding | `<div class="finding"><h3>…</h3>…</div>` |
| Participant quote | `<blockquote><p>…</p><cite>Role, Unit</cite></blockquote>` |
| Data table | `<table class="cs-table">` with a `<caption>` |
| Horizontal bar | `<div class="bar-row">` — see the findings section for the pattern |
| Caveat or disclosure box | `<div class="cs-note">` |
| Image with caption | `<figure><img><figcaption>` |

## Adding a PDF (writing samples, posters, papers)

1. Drop the file in `assets/`. Use a lowercase, hyphenated name that says what
   it is — `prosopagnosia-review.pdf`, not `final_v3 (1).pdf`. The filename is
   visible in the URL and in the reader's downloads folder.
2. Link it from the relevant page with a relative path: from anything inside
   `work/` or `writing/`, that's `../assets/your-file.pdf`.
3. Give it two to four sentences of framing first. A bare "Read the PDF" link
   gives a reader no reason to click; the framing is what makes the file
   evidence rather than an attachment.

GitHub Pages allows 100 MB per file and around 1 GB per repo, so file size is
almost never the constraint. Page weight is — if a PDF runs past ~10 MB, compress
it before committing, since some people will open it on a phone.

## Linking to work hosted somewhere else

For published articles and live production pages, **link, don't re-host**. A link
is self-verifying: the byline or the page itself proves it's yours.

Two things to do anyway:

- **Capture a Wayback Machine snapshot** of each URL (web.archive.org, "Save Page
  Now"). Corporate help centers get restructured and student publications lose
  their archives. Link to the live page, and keep the snapshot URL as a fallback
  you can swap in when the original 404s.
- **Say when the live version may have changed.** For content you wrote that has
  since been edited by others, one line — "published version; content has been
  maintained by the team since" — is more credible than implying the current text
  is yours word for word.

Re-host a PDF instead of linking when nothing is online, or when the only copy is
behind a paywall or login. For anything published by an outlet, check the terms
before putting a copy on your own domain; linking always avoids that question.

## Changing the look

Everything visual lives in the `:root` block at the top of `styles.css`. Changing
`--ink` and `--paper` restyles the whole site. The four `--cat-*` colors are the
category colors used by both the filter swatches and the card tags, so they stay in
sync automatically.

Fonts are Archivo (headings and UI) and Source Serif 4 (reading text), loaded from
Google Fonts in each page's `<head>`.

---

## Publishing it

**GitHub Pages** is the recommended host: free, no account tiers, and it version-controls
your portfolio as a side effect.

1. Create a GitHub repo named `graceliu` (or anything).
2. Upload the contents of this folder to the repo root.
3. Repo **Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**.
4. Live in a minute or two at `https://YOUR-USERNAME.github.io/graceliu/`.

**Custom domain.** Buy something like `graceliu.com` (~$12/year), then in
**Settings → Pages → Custom domain** enter it and follow the DNS instructions. Worth
doing — a real domain on a resume reads differently than a `.github.io` subdomain, and
much differently than a free Wix subdomain with an ad banner on it.

**Alternatives:** Netlify or Cloudflare Pages both let you drag this folder onto a web
page and get a live site, with no git involved. Same result, slightly less control.

---

## Before you publish

- [ ] Written permission from Norbert Health for the request-relay case study
- [ ] Separate sign-off for the voice agent page — it describes an unreleased
      feature, so this is a higher bar. Consider holding it until the feature ships.
- [ ] Add your LinkedIn URL and resume PDF to the `.hero-meta` block in `index.html`
- [ ] Decide whether the phone number from your old site should be public (a portfolio
      generally doesn't need one — email is enough, and a public number invites spam)
- [ ] Replace the `og:` meta tags if you want a specific link preview image
- [ ] Check it on your phone

## What's not built yet

The other fifteen projects are in the grid as cards with `href: null`. Send the
materials in clusters and each one becomes a page. Priority order, if you want a
recommendation: MedCheck, then the master's thesis, then the topic modeling project
(that one does double duty for the fintech roles you're interested in).

The voice agent page needs a findings section added once testing with residents is
done. Look for the `#next` section — that's where it goes.
