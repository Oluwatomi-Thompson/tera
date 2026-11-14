# Design Tokens

Source of truth for the values is `tailwind.config.js`. This file explains what
each token is **for**. Change both together.

## Colours

Each colour has one job. If a screen is using a colour outside its job, change the screen.

| Token | Values | Job |
|---|---|---|
| `kivu` (deep lake blue-green) | 50 `#EAF1F3`, 100 `#D3E1E6`, 200 `#A9C3CC`, 400 `#4F8294`, 600 `#1F5A70`, 700 `#14475C`, 800 `#0D3B4F`, 900 `#082A39` | Text, nav, footer, hero panel, standard buttons |
| `mist` | DEFAULT `#EFF3F1`, deep `#E2E9E6` | Page ground. Cool, not cream |
| `sun` (the one accent) | 100 `#FDF0CC`, 300 `#F9D26B`, 400 `#F6B72B`, 500 `#E3A01A` | **The next thing to do**: the page's primary button and the "Next up" lesson. One per page |
| `hill` | 100 `#DDEEE3`, 600 `#2C7A4B`, 700 `#236240` | Progress, completion, correct answers |
| `clay` | 100 `#F6DFD9`, 600 `#B4432F` | Wrong answers and errors only |
| `slate2` | `#4A6672` | Muted text on mist and white (5.9:1 on mist) |

Focus rings: `kivu-600` on light surfaces, `sun-300` on dark ones (`.on-dark`).

## Typography

| Role | Face | Where |
|---|---|---|
| UI and headings | Bricolage Grotesque (400–800) | Nav, headings, buttons, forms, numerals |
| Reading | Source Serif 4 (400–700) | Lesson prose (`prose prose-tera`), About, institution descriptions |

- Page title: `text-4xl font-extrabold` (`text-3xl` on form pages). Section title: `text-2xl font-bold`.
- Lesson prose: 19px (`1.1875rem`), line-height 1.72, column `max-w-2xl` (about 62 characters).
- Sentence case everywhere. No all-caps labels.

## Shape and spacing

- Radius: `rounded-lg` for buttons and inputs, `rounded-xl` for panels, `rounded-2xl` for the hero and score cards, `rounded-full` for chips, badges and lesson nodes.
- Surfaces use a 1px `kivu-100` border, not shadows.
- Touch targets are at least 44px (`.btn`) or 36px (`.btn-sm`, admin only).
- Page widths: `max-w-5xl` (hero, admin), `max-w-3xl` (lists), `max-w-2xl` (reading, quiz, calculator), `max-w-md` (forms).

## Component classes (`app/static/css/input.css`)

`.btn` with `.btn-sun` / `.btn-kivu` / `.btn-quiet` / `.btn-quiet-dark` / `.btn-danger` (and `.btn-sm`),
`.panel`, `.rows`, `.link`, `.field` (`.field-error`), `.chip`, `.badge`, `.fill-in` (progress bar grows once on load).

## Motion

One moment: the dashboard progress bar fills on load. Everything else is a colour transition on hover.
All motion is disabled under `prefers-reduced-motion`.
