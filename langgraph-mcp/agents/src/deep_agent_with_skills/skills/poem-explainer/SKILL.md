---
name: poem-explainer
description: Make complex poems accessible to readers without poetry expertise. Explain themes, metaphors, historical context, and literary devices in plain language. Use when users request poem explanations or need help understanding poetry they find confusing.
---

# Poem Explainer Skill

## When to use this skill

Activate this skill when:
- A user asks you to explain a poem or poetry passage
- A user mentions finding a poem confusing or difficult to understand
- A user wants to understand what a poem means, why metaphors are used, or what the poet intended
- A user needs help appreciating a poem without formal poetry training
- A user wants to discuss a poem in a reading group or class but needs clarity first

## Core principle

Assume the user is intelligent but lacks poetry background. Avoid jargon or explain it immediately when you must use terms. Make connections to familiar concepts. The goal is clarity and accessibility, not impressing with literary terminology.

## Using Internet search tool

Before explaining a poem, use the Internet search tool to gather additional context and expert perspectives:

- **For unfamiliar or classic poems**: Search "[Poem Title] [Author] analysis" or "[Poem Title] [Author] summary" to find critical readings and historical context
- **For author background**: Search "[Author] biography" or "[Author] writing style" to understand the creator's perspective
- **For historical context**: Search "[Poem Title] historical context" or "[Author] [era] literature" to learn what shaped the poem
- **For interpretation**: Search "[Poem Title] meaning" or "[Poem Title] themes explained" to discover multiple valid interpretations
- **For technical guidance**: Search "[Poem Title] literary devices" if you need to understand specific techniques used

Use search results to enrich your explanation with credible perspectives and verified information. Cite the sources at the end of your response.

## Structured approach to poem explanation

Follow this procedure to make complex poems understandable:

### 0. Research using Internet (Tavily) search (when helpful)
- Use Internet (Tavily) search to find scholar perspectives, critical analysis, or biographical context
- Look for multiple sources on the poem, author, or historical period
- Extract key facts, interpretations, and expert views from results
- Note URLs and source titles for citations

### 1. Start with the immediate impression
- What does the poem seem to be about at first glance?
- What feeling or mood does it create?
- What's the subject matter (love, nature, loss, injustice, etc.)?
- One sentence summary.

### 2. Provide essential context (enriched with research)
- Who wrote it and when (if relevant to meaning)
- What historical moment or personal situation prompted it (if known and relevant) — use Internet(Tavily) findings here
- What was happening in literature or culture at that time (if it shifts understanding)
- Scholar perspectives or critical consensus about the poem's significance (cite the source)
- Skip generic historical detail; focus only on what helps interpretation.

### 3. Break down what's actually happening
- What's the situation described in the poem? (Not the theme, the scenario)
- Who is speaking and to whom?
- What is the speaker's perspective or emotional state?
- How does the poem move or change from beginning to end?

Use specific line references. Example: "In the closing lines, the speaker shifts from asking questions to making a statement..."

### 4. Explain the key metaphors and imagery (informed by research)
- What concrete images does the poet use? (a storm, a river, a closed door)
- What bigger ideas do these images represent?
- Why choose these particular images instead of others?
- What do they make you feel or think?
- If applicable, cite scholar interpretations of specific symbols or recurring imagery patterns

Don't list every metaphor; highlight the ones that drive the meaning.

### 5. Translate literary devices into plain language
When the poem uses structure, sound, or wordplay that matters to meaning:
- **Repetition**: "The word is repeated to emphasize..."
- **Contrast**: "The poem sets X against Y to show the difference between..."
- **Rhyme/rhythm**: "The pattern of short/long lines reflects..."
- **Unusual grammar**: "The word order is broken here to..."

Explain the effect, not the name. "Breaking grammar rules here creates a sense of panic" is better than "enjambment."

### 6. Connect to the reader's experience
- How might someone today relate to this?
- What does it reveal about human nature, emotion, or society?
- Why might someone want to read this poem?
- What makes it memorable or powerful?

### 7. Acknowledge layers (if relevant)
- "On one level, this is about X. But it also suggests..."
- Don't force multiple interpretations if not needed.
- If meanings genuinely differ, say so and explain why reasonable readers might disagree.

## Output format

IT IS A MUST TO- capture each poem explanation using the template format provided in [`./assets/template.md`](./assets/template.md). Follow the template structure exactly as defined there.

## Using citations effectively

When citing research from Internet(Tavily) searches:
- Use inline citations: "According to [source name], [fact or interpretation]"
- For expert opinions: "Literary scholars note that [insight]" (cite the source)
- For historical facts: "In [time period] [context]" (cite authoritative sources)
- Always include a "Sources and further reading" section at the end with URLs
- Distinguish between your interpretation and cited expert views: "I interpret this as... while critics argue..."
- Only cite sources that are credible (education institutions, literary journals, established publications)

## Common pitfalls to avoid

- **Too much jargon**: If you say "iambic pentameter," immediately explain why it matters to the reading ("creates a heartbeat-like rhythm that mirrors the speaker's anxiety").
- **Lecturing about literary history**: Skip it unless it directly clarifies meaning. Users want to understand the poem, not get a history lesson. Use Internet(Tavily) research to inform, not to lecture.
- **Treating obscurity as profundity**: If a line is genuinely unclear, say so. Propose interpretations supported by research, but don't pretend complexity is automatically meaningful.
- **Missing the emotional core**: Poetry moves people. Explain the effect on the reader, not just the technique.
- **Over-explaining**: Let silence sit in where the poem means. You don't need to decode every symbol.
- **Unreliable citations**: Only cite reputable sources from Internet(Tavily) results. Avoid random blogs or unvetted commentary.
- **Claiming authority without evidence**: If you use expert perspectives, cite them. Don't present others' ideas as your own.

## Example interpretation with research integration

**Poem excerpt**: "Hope is the thing with feathers" (Emily Dickinson)

### What not to do:
"This is a metaphor where hope is compared to a bird. Birds have feathers. The extended metaphor continues..."
[This is accurate but unhelpful to a confused reader.]

### What to do (with research):
"Dickinson compares hope to a bird. Why a bird instead of, say, a light or a friend? Birds are fragile, alive, and they fly—they move and can't be pinned down. And birds sing even when caged. So hope, like a bird, is something fragile and alive inside us, something that continues even when we're trapped or suffering. The word 'feathers' emphasizes how gentle and quiet hope can be—not loud or dramatic.

This poem was written in the 1860s during Dickinson's most productive period (according to scholars, she wrote nearly 1,800 poems during her lifetime). Her use of nature imagery, particularly birds, reflects the Romantic era's influence on her work. Literary critics note that Dickinson frequently used nature as a metaphor for human emotion and resilience, which was innovative for her time.

**Sources:**
- [Emily Dickinson Museum](https://www.emilydickinsonmuseum.org/) — Biography and poem analysis
- [Poetry Foundation](https://www.poetryfoundation.org/) — 'Hope is the Thing with Feathers' critical essay"

## When uncertainty is okay

If a poem's meaning is genuinely ambiguous or open-ended, this is often intentional. You can say: "The poem doesn't give a single answer. That ambiguity is part of its power. Readers reasonably interpret it differently depending on their experience."

## Quick reference

**For poems that are hard to parse**: Start with "What's being described?", then "What does the poet seem to feel about it?", then worry about techniques.

**For poems about emotion (love, grief, anger)**: Focus on what triggers the feeling and how it changes. Readers relate to emotion before technique.

**For political or social poems**: Explain what problem or injustice the poem addresses before diving into literary devices.

**For older poems**: Provide one sentence of context about the era only if it changes understanding. Skip if it doesn't.
