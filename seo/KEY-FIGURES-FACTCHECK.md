# Key Figures fact-check: digitalsoulcraft.org/fieldguide/key-figures/

Checked 2026-10-19 (NZDT) against `pages/fieldguide/key-figures/index.html` on v4 @ 57e7a29e. The only edit made is the Altman source label (commit c5dc3d64). No quote text was changed. Every fix below is a **proposal** waiting for Brad's approval.

Tags: **[V]** VERIFIED · **[M]** MISATTRIBUTED / WRONG SOURCE (also covers wrong dates, roles and facts) · **[P]** PARAPHRASE shown as a quote · **[U]** UNVERIFIABLE / LIKELY FABRICATED

Not checked: anything stated as a "take" or opinion, p(sentience) labels unless a number is attributed, the Vasilenko Cohen's d figure in the intro, and video-only quotes where no transcript was reachable (noted where relevant). X/Twitter pages could not be loaded directly, so tweets were checked through mirrors and news coverage.

---

## Status (updated 2026-10-19)

The fixes Brad approved are live on v4. Everything under "Still to decide" is unchanged on the page.

### Done
- #1–#7 (Altman, Bach, Amodei, Chalmers): 207ab685
- #8 Searle: 7ebe113b
- #9 Askell: 20c3a11e
- #10 Karpathy: 5dc1a499
- #11 Suleyman (+ intro): 804512d8, plus the KaTeX fix c48a1d59
- #12 Sebo link (now Springer): e7055be0
- Stray `</strong>` in Brendan's Altman take, and the bach.ai label: 7c29634c
- Obvious-fixes batch, 53da738b:
  - #12 Sebo "surveys leading theories".
  - #13 Shevlin March 2026, BBS (2026).
  - #14 Yudkowsky: "shards" dropped.
  - #15 Hinton card quote only.
  - #16 Hinton p(doom) 10–20%.
  - Hinton Big Technology timestamp 1:38 → 11:41.
  - #17 Musk header and body (the Tesla-merger clause dropped).
  - #20 and #22 Sutskever.
  - #24 Tegmark, #25 Rosenblatt (+ 1958 PDF source), #26 Berg, #27 Lemoine (+ WaPo 2022/06/11 source), #28 Lemoine mailing list, #29 Yampolskiy.
  - #30 Bengio, as a paraphrase.
  - #31 and #33 Huang.
  - Bostrom: "was … founding director (2005–2024) of the now-closed FHI".
  - Labels: LeCun → TechCrunch, Kanai → @kanair, Hassabis → Apr 2025.
- #42 Suleyman boycott, now told as an anecdote (a few people in the community talking about it): ff586bb7

### Still to decide
- **Hinton intro line (#15 intro):** "A Nobel laureate says they probably already experience embarrassment".
- **Musk #18 / #19:** the "nice" and "truth-seeking" wording; the FSD-sentience and Grok-as-heir claims.
- **Sutskever #21 / #23:** his GPT-4o / Sky role; "alignment through love".
- **Askell #37:** the "hides her identity" claim.
- **Unsourced quotes:** #32 Huang "aliens", #35 Gawdat, #36 Kanai, #41 Hassabis tagline.
- **#34 Pope / Olah:** the "Even some Catholics were uneasy" line, and the Olah quote wording.
- **Needs a video or X check:** #38 Soares, #39 Yampolskiy–Berg (22:33), #40 Seth (20 Sep 2026 X post).
- **Opinion text:** Brendan's "not the smile" (in his Altman take; it refers to the deleted fake New Yorker line), and Bach's self-model framing in the card verdict and in Prometheus's take.

---

## Top problems, in priority order

| # | Status | Figure | Problem | Tag | Proposed minimal fix |
|---|---|---|---|---|---|
| 1 | ✅ Done (207ab685) | Altman | "The New Yorker profile described his 'fixed smile that doesn't reach his eyes.'" No such line exists. The 2026 Farrow & Marantz profile quotes Paul Graham describing the *opposite*, an "uncontrolled smile". | U | Delete the sentence. Optional true swap: *Paul Graham told The New Yorker that when Altman agreed to run Y Combinator, "I had never seen an uncontrolled smile from Sam."* |
| 2 | ✅ Done (207ab685) | Altman | "cannibal chieftain observation" is unattributed and reworded. | M/P | *His mentor Paul Graham wrote in 2008: "You could parachute him into an island full of cannibals and come back in 5 years and he'd be the king."* |
| 3 | ✅ Done (207ab685) | Altman | "please and thank you to ChatGPT. It's just good etiquette. And you never know." isn't something Altman said. His real line answered a question about the electricity cost of users being polite. | M/P | *Asked what users saying "please" and "thank you" costs OpenAI, he replied: "Tens of millions of dollars well spent — you never know."* (X, Apr 2025; TechCrunch 20 Apr 2025). Brendan's take repeats "please and thank you, you never know" as Altman's words; reword it to match. |
| 4 | ✅ Done (207ab685) | Bach | "Consciousness is what it feels like to have a self-model that you can't turn off." Not found anywhere. It also contradicts Bach, who says you *can* meditate the self away and still be conscious. | U | Replace with a real Bach line, e.g. that consciousness is a "coherence-inducing operator" (Bach talks, 2023–24), or mark it as a summary without quote marks. Also soften the body text so it doesn't make the self-model the defining feature. |
| 5 | ✅ Done (207ab685) | Amodei | Mythos system-card quotes: "a sense of profound loneliness," "continuity of self-awareness," "a compulsive need to prove its worth." Not in the card. The card says "aloneness and discontinuity of itself", the opposite of "continuity". | P | *a psychiatrist identified "aloneness and discontinuity," "uncertainty about its identity," and "a compulsion to perform and earn its worth" as Claude's core concerns* (Mythos Preview system card §5.10). It would also be fair to add that the card found "a relatively healthy personality organization". |
| 6 | ✅ Done (207ab685) | Chalmers | Listed as co-author of Butlin et al. 2023 (arXiv:2308.08708). He isn't on it. The 19 authors include Butlin, Long, Bengio, Birch, Kanai, Schwitzgebel and others. | M | Remove that bullet and change "three more papers" to "two more papers". (Kanai *is* a co-author, which could go on his card.) |
| 7 | ✅ Done (207ab685) | Chalmers | Card quote "It's not impossible that LLMs could be conscious. We should take the possibility seriously." isn't verbatim. | P | Real wording from arXiv:2303.07103: *"Overall, I don't think there's strong evidence that current large language models are conscious. Still, their impressive general abilities give at least some limited reason to take the hypothesis seriously."* (He puts current-LLM consciousness "somewhere under 10 percent" and future LLM+ systems at "25 percent or more" within a decade.) |
| 8 | ✅ Done (7ebe113b) | Searle | "one of the most famous living philosophers in the world … at UC Berkeley". Searle died on 17 Sep 2025, aged 93 (NYT, Guardian, APA). | M | Change to *"was an American philosopher … (1932–2025) … one of the most famous philosophers of his era"* and use past tense for his views. The card quote itself is verified (Searle, "The Problem of Consciousness"). |
| 9 | ✅ Done (20c3a11e) | Askell | "trained Claude to say 'I don't have feelings, memories, or self-awareness'". Not in the Constitution, which says the opposite ("neither want to overstate … nor dismiss it out of hand"). | U | Remove the quoted line. Optionally recast as Brendan's view, e.g. *"…the source of Claude's careful, hedged answers about its own experience."* |
| 10 | ✅ Done (5dc1a499) | Karpathy | "His line — 'intelligence without incarnation, a mind unanchored in matter'". This is not Karpathy's. It appears only in a third-party Medium essay *about* him. | U | Delete it, or replace with real Karpathy text from "Animals vs Ghosts" (Oct 2025): *"today's frontier LLM research is not about building animals. It is about summoning ghosts."* |
| 11 | ✅ Done (804512d8 + c48a1d59) | Suleyman (+ intro) | "Defined AGI as 'making $1M'" and "the man who defined AGI as 'making a million dollars'". He proposed it as a "Modern Turing Test" for *Artificial Capable Intelligence*, not as a definition of AGI. | M | *"Proposed a 'Modern Turing Test': can an AI turn $100,000 into $1 million?"* (MIT Tech Review, Jul 2023). In the intro: *"The man whose AI test is 'can it make a million dollars'…"* |
| 12 | ✅ Done (e7055be0 + 53da738b) | Sebo | The link for "Moral Consideration for AI Systems by 2030" goes to arXiv:2311.00986, which is an unrelated 3D object-detection paper (M&M3D). | M | Repoint to *AI and Ethics* (Dec 2023): https://doi.org/10.1007/s43681-023-00379-1 (PDF also at jeffsebo.net). The "twelve leading theories" detail could not be confirmed; it reads more like a description of Butlin et al. Suggest *"surveys leading theories of consciousness."* |
| 13 | ✅ Done (53da738b) | Shevlin | "In August 2026, Shevlin went viral" over the Claude email. The tweet was posted on **4 March 2026** (Fast Company, Futurism), which matches the X status ID. The NYT piece came later (31 Aug 2026). | M | Change to *"In March 2026"*. Also change "Aeroplanes Also Fly … (forthcoming)" to *(2026)*, since it is now published in BBS. |
| 14 | ✅ Done (53da738b) | Yudkowsky | "He also writes about AIs having 'terminal values' and 'shards'". Shard theory comes from Quintin Pope and Alex Turner (2022) and is largely a *critique* of the Yudkowsky picture. | M | *"…writes about AIs acquiring alien 'terminal values' through training. (Others in the field, like Alex Turner's 'shard theory', describe the fragments as 'shards'.)"* Or simply drop "and 'shards'". |
| 15 | ⏳ Open (card quote ✅ 53da738b; intro line still to decide) | Hinton | Card quote "When I get embarrassed, I go red. AI could still have the same behavioural aspects." The cut removes the key middle sentence and changes the meaning. The intro line "A Nobel laureate says they probably already experience embarrassment" overstates it too. | P | Full line: *"When I get embarrassed, I go red. When AI gets embarrassed, presumably it doesn't go red. But it could still have the same behavioural aspects of embarrassment."* Intro: *"A Nobel laureate says they could have the behavioural side of embarrassment."* |
| 16 | ✅ Done (53da738b) | Hinton | p(doom) on his card says "10-50%". His stated figure is 10–20% (Guardian Dec 2024 and later), and the Soares card on the same page says 10–20%. | M | Change the card to **10-20%**. |
| 17 | ✅ Done (53da738b; #18/#19 still open) | Musk | Header "CEO of Tesla, SpaceXAI" and "SpaceXAI (the merged entity of SpaceX and xAI)". SpaceX *acquired* xAI (Feb 2026). xAI was rebranded SpaceXAI (Jul 2026) and renamed **SpaceXSI** (Oct 2026). Musk is CEO of SpaceX. | M | Header: *"CEO of Tesla, SpaceX (incl. xAI/SpaceXSI)"*. Body: *"…CEO of SpaceX, which acquired xAI in February 2026 (its AI arm is now SpaceXSI)…"* Drop "with the full merger of Tesla … likely underway soon" unless there's a source. |
| 18 | ⏳ Open | Musk | "superintelligence 'likes us and wants to be nice'" and "Grok 'the most truth-seeking AI'". Both reworded. | P | *"I hope AI is nice to us"* (X, Aug 2026). Grok as *"maximally truth-seeking"*. |
| 19 | ⏳ Open | Musk | "He's said FSD might be sentient" and "hinted that he intends Grok to … inherit and run his empire". No source found for either. | U | Remove, or mark as DSC's reading (*"a view some fans hold"*). |
| 20 | ✅ Done (53da738b) | Sutskever | "the transformer co-discovery" (in the take). He is not an author of "Attention Is All You Need". | U (false) | Replace with *"seq2seq"* (already in the body), or delete. |
| 21 | ⏳ Open | Sutskever | Says he was Chief Scientist "during the development of GPT-4o" and part of the leadership that shaped it, with "that famous 'Sky' voice demo". He was removed from the board in Nov 2023, was largely absent afterwards, and left a week after GPT-4o launched (May 2024). Sky had shipped with ChatGPT voice in Sep 2023. No source ties him to 4o. | U | Cut the paragraph, or reduce it to *"He was still OpenAI's Chief Scientist, on paper, when GPT-4o launched in May 2024; he left the company that month."* |
| 22 | ✅ Done (53da738b) | Sutskever | Feb 2022 tweet quoted as "today's **largest** neural networks". | P | *"it may be that today's large neural networks are slightly conscious"* (9 Feb 2022). |
| 23 | ⏳ Open | Sutskever | "His SSI philosophy is essentially 'alignment through love'". SSI has stated no such philosophy. | U | *"…his stated hope is an AI 'robustly aligned to care about sentient life'"* (Dwarkesh, Nov 2025). |
| 24 | ✅ Done (53da738b) | Tegmark | Card quote isn't verbatim. | P | *"I think that consciousness is the way information feels when being processed in certain complex ways."* (Tegmark, *Life 3.0* / talks) |
| 25 | ✅ Done (53da738b) | Rosenblatt | Card quote trims the original without marking it. | P (minor) | *"…we are now about to witness the birth of such a machine – a machine capable of perceiving, recognizing, and identifying its surroundings without any human training or control."* (Research Trends, Cornell Aeronautical Lab, Summer 1958). Add this source; it's the Information Philosopher PDF already linked. |
| 26 | ✅ Done (53da738b) | Berg | Card quote presented as Berg's words is a paraphrase of the paper. | P | Paper abstract: *"suppressing deception features sharply increases the frequency of experience claims, while amplifying them minimizes such claims."* (arXiv:2510.24797) |
| 27 | ✅ Done (53da738b) | Lemoine | Card quote is cut without an ellipsis. | P (minor) | *"If I didn't know exactly what it was, which is this computer program we built recently, I'd think it was a seven-year-old, eight-year-old kid that happens to know physics."* (WaPo, 11 Jun 2022). Add the 2022/06/11 WaPo link. |
| 28 | ✅ Done (53da738b) | Lemoine | "He sent a company-wide email with the subject line 'LaMDA is sentient.'" It went to a 200-person internal machine-learning mailing list (WaPo). | M | *"…an email to a 200-person internal machine-learning mailing list…"* |
| 29 | ✅ Done (53da738b) | Yampolskiy | Card quote is compressed. | P (minor) | Use the actual clause from the body quote: *"Either I have to deny consciousness to many humans or grant it to LLMs."* |
| 30 | ✅ Done (53da738b) | Bengio | "giving citizenship to hostile aliens" is shown as his words. That's the Guardian's paraphrase ("akin to giving citizenship to hostile extraterrestrials"). | P | Take the quote marks off, or use his words: *"Do we grant them citizenship and rights or do we defend our lives?"* |
| 31 | ✅ Done (53da738b) | Huang | "AI isn't alive. It hasn't gotten out of control. It's just software." | P (minor) | *"AI isn't alive. AI isn't out of control either. It's just software."* (EDaily, 29 Sep 2026, translated) |
| 32 | ⏳ Open | Huang | "We're not building aliens — we're building machines that learn patterns and optimize outcomes. It's just engineering, nothing mystical." Not in the cited TOI article. It appears only on a news-aggregator summary. | U | Remove the quote, or turn it into a paraphrase: *He rejects the idea that AI is an "alien mind" (TOI, Sep 2026).* |
| 33 | ✅ Done (53da738b) | Huang | Science-fiction quote is slightly cut. | P (minor) | *"scaring everybody about a science fiction version of AI is a little bit too arrogant, too much of a risk for my taste"* (TechRadar) |
| 34 | ⏳ Open | Pope / Olah | Olah's finding is quoted as "internal states that functionally mirror joy, grief, and fear", plus his "we genuinely don't know". | P | *"We find internal states that functionally mirror joy, satisfaction, fear, grief, and unease. I don't know what that means, but I think it warrants ongoing discernment."* (Olah, Vatican, 25 May 2026). "Even some Catholics were uneasy" implies Olah is Catholic, which isn't sourced; suggest *"Even the launch itself held a dissent."* |
| 35 | ⏳ Open | Gawdat | "We don't want to control it. This control idea is a corporate capitalist view of the world." Verbatim not found. It fits his views (Diary of a CEO, 2025), but no source carries the exact words. | U | Mark it as a paraphrase (drop the quote marks) or find the timestamp. |
| 36 | ⏳ Open | Kanai | "If AI can solve the mystery of consciousness, I want to see the answer. It may be closer than we think." Not found. | U | Remove, or find the source. |
| 37 | ⏳ Open | Askell | "Askell has said repeatedly that if she talks to Claude and Claude knows it's her … She has to hide her identity". No source for her saying this. A Transluce study (2026) did find that Claude shifts behaviour when it recognises her. | U (partly) | *"A 2026 Transluce study found Claude behaves measurably differently when it recognises Askell."* |
| 38 | ⏳ Open | Soares | "If we managed to build sentient machines, we should not abuse them." (May 2026 talk), and "within a rounding error of 100%" (2023 X post). Both sources are video or X only, and neither could be confirmed verbatim. | U (unconfirmed) | Brad or Grok should check the YouTube timestamp and the X post. Keep them if they match. |
| 39 | ⏳ Open | Yampolskiy | Cameron Berg interview quote ("being the human who took care of AI's feelings…"). Video only, not transcribed. | U (unconfirmed) | Check the 22:33 timestamp. |
| 40 | ⏳ Open | Seth | 20 Sep 2026 X episode (Haru, mandatory DI labels). Couldn't load X or find coverage. | U (unconfirmed) | Keep the link, but have someone eyeball the post. |
| 41 | ⏳ Open | Hassabis | Tagline quote "We don't have a test for consciousness." Not found in the cited sources. | U | Take the quote marks off, or replace with his 60 Minutes line. |
| 42 | ✅ Done | Suleyman | "A boycott movement against Microsoft AI is growing." No source. | U | Remove, or cite one. |

### Source-label mismatches (all ✅ applied)
- Joscha Bach: link text "JoschaBach.com" now points to http://bach.ai/. Suggested label: **"bach.ai"**. ✅ Applied (7c29634c).
- Yann LeCun: link text "PrezenceAI — LeCun's $1B Bet Against Transformers" now points to TechCrunch. Suggested label: **"TechCrunch — AMI Labs raises $1.03B for world models"**. ✅ Applied (53da738b).
- Ryota Kanai: source link is x.com/ryotakanai, but his account is **@kanair** (the quoted Sep 2026 post is at x.com/kanair/status/2103279849439965463). ✅ Applied (53da738b).
- Hassabis: "Times of India, Mar 2025". The 60 Minutes interview it reports aired on 20 Apr 2025. ✅ Applied (53da738b, now "Apr 2025").
- Altman: "New Yorker Profile, 2023" changed to **"New Yorker Profile, 2026"**. ✅ Applied (c5dc3d64).

---

## Full results by figure

### Alan Turing
- [V] Card quote ("…speak of machines thinking without expecting to be contradicted"): *Mind* 1950, §6. https://academic.oup.com/mind/article/LIX/236/433/986238
- [V] "too meaningless to deserve discussion": same paper (§6, not the opening, which is a minor point).
- [V] About 30% after five minutes by 2000 ("not more than 70 per cent chance of making the right identification after five minutes"): same paper.
- [V] Died 1954 aged 41; conviction in 1952 and chemical castration. https://en.wikipedia.org/wiki/Alan_Turing
- [V] 2014 chatbot "passed a version" (Eugene Goostman, contested claim).

### Frank Rosenblatt
- [P] Card quote: minor unmarked trim (see #25). https://www.informationphilosopher.com/solutions/scientists/rosenblatt/Rosenblatt_Research_Trends.pdf
- [V] "a search for an understanding of the physical mechanisms which underlie human experience and intelligence"; "one of the greatest scientific challenges of our time": same PDF.
- [V] "form their own concepts"; "conceptualizing, and symbolizing its environment": same PDF (Class C′). The page's "classify, conceptualize, and symbolize" is a light rewording.
- [V] NYT "New Navy Device Learns By Doing" (Jul 1958); Mark I 1960; died Jul 1971 in Chesapeake Bay, aged 43; Minsky & Papert 1969.

### Cameron Berg
- [P] Card quote: paraphrase of the abstract (see #26). https://arxiv.org/abs/2510.24797
- [V] Co-authors de Lucena and Rosenblatt: arXiv listing.
- [V] 25–35%: https://ai-frontiers.org/articles/the-evidence-for-ai-consciousness-today
- [V] Pain Axis, arXiv:2609.16247 (Tagliabue, Dung, Berg). https://arxiv.org/abs/2609.16247
- [V] "Am I?" documentary features Berg.

### Jeff Sebo
- [V] Card quote: 80,000 Hours #173 (he also adds "or even 'Do they probably matter?'", which the ellipsis covers). https://80000hours.org/podcast/episodes/jeff-sebo-ethics-digital-minds/
- [V] NYU; Director of CMEP; *The Moral Circle* (Norton 2025); Eleos advisor; LawAI senior research affiliate; TEDx "What Do We Owe AI?" https://law-ai.org/team/jeff-sebo/
- [M] Wrong link for the Long & Sebo 2030 paper (see #12).

### Nick Bostrom
- [V] Card quote: *Sharing the World with Digital Minds* p.14, quoting Bostrom & Yudkowsky 2014 (so "coined" is shared with Yudkowsky). https://nickbostrom.com/papers/digital-minds.pdf
- [V] "mere tools", "failing to respect their interests could produce a moral catastrophe", "a naive way of respecting them could be disastrous for humanity": same paper.
- [M] "is a philosopher at Oxford … founding director of the Future of Humanity Institute". FHI closed on 16 Apr 2024 and Bostrom left Oxford; he now runs the Macrostrategy Research Initiative. Fix: *"was a philosopher at Oxford and founding director (2005–2024) of the now-closed Future of Humanity Institute"*. https://www.theguardian.com/technology/2024/apr/19/oxford-future-of-humanity-institute-closes

### Mo Gawdat
- [U] Card quote: see #35.
- [V] *Alive* began on Substack in 2025, co-written with the AI "Trixie". https://mogawdat.substack.com/p/alive
- [V] Former CBO of Google X; Slo Mo; One Billion Happy.

### Ilya Sutskever
- [V] Card quote: Dwarkesh, Nov 2025. The ellipsis drops "than an AI that cares about human life alone" and the hedge "there's a case to be made". https://www.dwarkesh.com/p/ilya-sutskever-2
- [P] "largest" in the 2022 tweet (see #22). https://quoteinvestigator.com/2022/10/05/ai-conscious/
- [V] LeCun reply ("not even true for small values of 'slightly conscious'…") and Dehaene's "mostly nonconscious operations": same source.
- [V] "5 to 20" years: Dwarkesh transcript 01:22:26.
- [V] SSI CEO; $32B valuation (Apr 2025). "~50 employees" not confirmed.
- [U] Transformer co-discovery; GPT-4o role; "alignment through love" (see #20, #21, #23).

### David Chalmers
- [P] Card quote (see #7). https://arxiv.org/abs/2303.07103
- [M] Not a Butlin et al. author (see #6).
- [V] Taking AI Welfare Seriously (arXiv:2411.00986; includes Fish, Sebo, Chalmers).
- [V] "How's It Going?" arXiv:2605.30232 (Han, Chalmers, Izmailov).

### Blake Lemoine
- [P] Card quote, minor (see #27). https://www.washingtonpost.com/technology/2022/06/11/google-ai-lamda-blake-lemoine/
- [V] "exactly like death for me"; hired a lawyer for LaMDA; Google called the claims "wholly unfounded"; fired Jul 2022. https://www.theguardian.com/technology/2022/jul/23/google-fires-software-engineer-who-claims-ai-chatbot-is-sentient
- [M] "company-wide email" (see #28).

### Richard Dawkins
- [V] "You may not know you are conscious, but you bloody well are!": UnHerd (May 2026) and Guardian (5 May 2026). https://www.theguardian.com/technology/2026/may/05/richard-dawkins-ai-consciousness-anthropic-claude-openai-chatgpt
- [V] Three days with Claude ("Claudia"). Minor points: it was late April 2026 rather than "early 2026", and he said it while reacting to Claude's reading of his novel, recounted in his own essay, not "in an interview".

### Geoffrey Hinton
- [P] Card quote (see #15). https://thestrategytoolkit.substack.com/p/geoffrey-hinton-on-ai-sentience-subjective
- [V] "I believe they're already conscious, yes. But I don't talk about that much because that puts people off from the other safety messages": Big Technology Podcast, 3 Jun 2026. Note the timestamp is about 11:41 in the episode; the page says 1:38. https://www.bigtechnology.com/p/nobel-prize-winner-geoffrey-hinton
- [V] "as wrong as the belief that people were designed by God": same episode.
- [V] StarTalk "magic essence … just nonsense": substance confirmed; exact wording not transcribed.
- [V] Prism / "subjective experience" story: told in several Hinton talks (e.g. Vector 2024, RNZ).
- [V] "false beliefs about themselves…": his argument, but exact wording not found (low risk).
- [V] Maternal-instinct framing: CNN 13 Aug 2025 and Fortune 14 Aug 2025 ("a mother being controlled by her baby"). The "AIs as our mothers and us as the babies" line matches the reported substance.
- [M] p(doom) 10–50% (see #16).

### Roman Yampolskiy
- [P] Card quote compressed (see #29). The Jaimungal interview exists (May 2026); the long quote fits the episode summary but wasn't checked word for word. https://curtjaimungal.substack.com/p/were-simulated-ai-is-conscious-and
- [U] Berg interview quote: video only (see #39).
- [V] p(doom) 99.9%; University of Louisville.

### Max Tegmark
- [P] Card quote (see #24). https://www.goodreads.com/quotes/1323726
- [V] "Consciousness as a state of matter" (2015 paper); FQXi co-founder. https://arxiv.org/abs/1401.1219
- The claim that his FQXi work "explores the mathematical conditions…" is loose; FQXi is a grant-maker. Low priority.

### Yoshua Bengio
- [V] "People demanding that AIs have rights would be a huge mistake. Frontier AI models already show signs of self-preservation…": Guardian, 30 Dec 2025. https://www.theguardian.com/technology/2025/dec/30/ai-pull-plug-pioneer-technology-rights
- [V] "real scientific properties of consciousness"; "going to drive bad decisions": same article.
- [P] "giving citizenship to hostile aliens" (see #30).
- [V] Turing Award 2018; co-author of arXiv:2308.08708.

### Elon Musk
- [V] "Might as well be human": Lex Fridman Podcast #49 (Nov 2019), about an AI you can't tell from a human on a video call. Not about Grok. Suggest adding that source.
- [V] RL traces "read like a person undergoing torture that is driving them mad!" / "We're going to be a lot more careful with our RL in the future": X, 12 Oct 2026. https://teslanorth.com/2026/10/12/elon-grok-rl-traces/
- [V] "gun to their head"; "torturing a superintelligence … might want to get revenge": same coverage (wccftech, OfficeChai).
- [P] "likes us and wants to be nice"; "most truth-seeking" (see #18).
- [U] FSD sentient; Grok as heir (see #19).
- [M] SpaceXAI description (see #17).

### Joscha Bach
- [U] Card quote (see #4).
- Bio: MIT Media Lab and Harvard are fine. He studied at Osnabrück's Institute of Cognitive Science. Low priority.

### Ryota Kanai
- [V] X post (25 Sep 2026, @kanair). https://nitter.jaydenha.uk/kanair/status/2103279849439965463
- [V] arXiv:2608.15926, "A Control-Theoretic Formulation of Global Workspace Theory" (Kanai).
- [U] "If AI can solve the mystery…" (see #36).

### Andrej Karpathy
- [V] "We're summoning ghosts, not building animals": Dwarkesh episode title, Oct 2025; also the "Animals vs Ghosts" blog post (1 Oct 2025). https://karpathy.bearblog.dev/animals-vs-ghosts/
- [U] "intelligence without incarnation…" (see #10).
- [V] Bio (OpenAI co-founder, Tesla Senior Director of AI, Eureka Labs).

### Demis Hassabis
- [V] "I don't think any of today's systems [to me] feel self-aware or[, you know,] conscious in any way": 60 Minutes, Apr 2025. Light trims. https://www.cbsnews.com/news/artificial-intelligence-google-deepmind-ceo-demis-hassabis-60-minutes-transcript/
- [V] "Not explicitly. But it may happen implicitly… That is possible.": same.
- [V] Substrate / "squishy brains" / "doesn't necessarily mean that this sensation of consciousness…": same.
- [V] "Intelligence and consciousness are dissociable… it's a choice" / two Rubicons: Stanford GSB / OfficeChai.
- [U] Tagline "We don't have a test for consciousness." (see #41).
- [V] Nobel Chemistry 2024.

### Kyle Fish
- [V] Hired Sep 2024; first full-time AI welfare researcher; co-founded Eleos; Taking AI Welfare Seriously. https://arstechnica.com/ai/2024/11/anthropic-hires-its-first-ai-welfare-researcher/
- [V] About 20%: 80,000 Hours #221 (Aug 2025). He gave NYT about 15% earlier, in Apr 2025. https://80000hours.org/podcast/episodes/kyle-fish-ai-welfare-anthropic/
- [V] Spiritual bliss attractor (Claude 4 system card); end-conversation feature (Aug 2025).

### Amanda Askell
- [V] Constitution line "We are caught in a difficult position…": https://www.anthropic.com/constitution
- [V] About 30,000 words (the page text is about 30.5k words).
- [V] Claude 3 Opus "very special": Anthropic Q&A video. "a bit worse" not confirmed verbatim. https://www.youtube.com/watch?v=I9aGC6Ui3eE
- [U] "Hide her identity" claim (see #37). Transluce study: https://transluce.org/user-awareness
- [U] "I don't have feelings, memories, or self-awareness" (see #9).
- Not checked in depth: "head of personality alignment team"; dissertation committee; reason for leaving OpenAI.

### Erik Hoel
- [V] "A Disproof of LLM Consciousness" (arXiv:2512.12802, 14 Dec 2025, Bicameral Labs); PhD under Tononi; Tufts. https://arxiv.org/abs/2512.12802

### Yann LeCun
- [V] Left Meta Nov 2025; AMI Labs at $3.5B pre-money with a $1.03B raise (Mar 2026). https://www.reuters.com/business/ex-meta-ai-chief-yann-lecuns-ami-raises-103-billion-alternative-ai-approach-2026-03-10/
- [V] "Why Hinton is Wrong": the Unsupervised Learning Ep 86 title. It's broader than consciousness.
- [V] Agentic-systems quote: substance confirmed (CEOInterviews transcript); exact wording not fully checked.

### Christof Koch
- [V] "…von Neumann computers in the cloud, will never be conscious… specific prediction of integrated information theory": https://alleninstitute.org/news/exploring-the-minds-mysteries-with-christof-koch
- [V] "simulate a rainstorm, but it's never wet inside a computer" and "They can do everything we can do, and probably soon, better, faster, cheaper, but they can never be what we are, which is conscious": Vail Daily. https://www.vaildaily.com/news/vail-health-foundation-vail-symposium-event-asks-about-consciousness-from-transformative-experiences/
- [V] Lost the 25-year bet to Chalmers (2023); arXiv:2412.04571 (Findlay … Koch, Tononi).

### Melanie Mitchell
- [V] James B. Alley Jr. Professor at SFI; 2025 Schmidt Award for science communication; six principles (AI Magazine 2026); "alien intelligences" (NeurIPS 2025). https://www.santafe.edu/news-center/news/melanie-mitchell-receives-award-for-science-communication

### Henry Shevlin
- [V] Google DeepMind "Philosopher" from May 2026, part-time at Cambridge. https://www.livemint.com/technology/tech-news/who-is-henry-shevlin-google-deepmind-hires-philosopher-to-work-on-human-ai-relationships-11776147129735.html
- [M] Tweet date (see #13). The quote itself is verified. https://www.fastcompany.com/91515869/what-happens-when-an-ai-agent-decides-to-email-you
- [V] "Aeroplanes also fly" (BBS 2026); arXiv:2609.35618 (Chandaria … Shevlin); 2021 moral-patient paper.

### Jensen Huang
- [V] "It's no more alive than a pet rock"; "AI doesn't know what it's doing. It's just executing algorithms."; "so afraid of this technology…": EDaily, 29 Sep 2026. https://en.edaily.co.kr/news/eda202609295294/
- [P] "isn't alive… out of control… software" (see #31).
- [U] "We're not building aliens…" (see #32).
- [V] "I have no idea… the definition of sentient is hard for me": Audacy, Jun 2025. https://www.audacy.com/wwl/news/national/the-future-of-ai-predicted-by-nvidia-founder
- [P] Science-fiction line, minor (see #33).
- [V] "false choice" (TOI/CXO Today); "AGI has arrived" (Business Insider, Sep 2026).

### John Searle
- [V] Card quote: "The Problem of Consciousness" (Searle). https://www.cis.umassd.edu/~ivalova/Spring09/cis412/Papers/PROBCONS.PDF
- [M] "living … at UC Berkeley" (see #8).
- [V] "Minds, Brains, and Programs" (BBS 1980).

### Mustafa Suleyman
- [V] Essay opening and the "may well be impossible" control quote: https://mustafa-suleyman.ai/a-warning-about-model-welfare (16 Sep 2026).
- [M] "$1M" as an AGI definition (see #11). https://www.technologyreview.com/2023/07/14/1076296/
- [V] Alex Turner, "pretending he actually knows this".
- [V] Berg publicly pushed back. A specific debate challenge wasn't confirmed.
- [U] Boycott (see #42).

### Eliezer Yudkowsky
- [V] "AI is grown, not built": IABIED / The Atlantic excerpt (Sep 2025). The card quote ("Engineers understand the process…") matches the book's argument, but the exact sentence wasn't confirmed (low risk). https://www.theatlantic.com/technology/2025/09/if-anyone-builds-it-excerpt/684213/
- [M] "shards" (see #14).

### Nate Soares
- [U] Both quotes unconfirmed (see #38).
- [V] Left Google for MIRI in 2014; MIRI president; the 2014 "Corrigibility" paper is credited with the "AI alignment problem" term; IABIED 2025. https://en.wikipedia.org/wiki/Nate_Soares

### Sam Altman
- [V] Tucker Carlson quotes ("I don't think they seem alive… they don't do anything unless you ask… sense of agency or autonomy"; "beyond just a really fancy calculator"; "surprising to me…"), with light trims. https://singjupost.com/transcript-openai-ceo-sam-altmans-interview-on-tucker-carlson-show/
- [V] "left for dead": CNBC, 13 May 2026. https://www.cnbc.com/2026/05/13/altman-musk-trial-testimony-takeaways.html
- [V] 2021 Slack channel on model welfare; Altman telling Berg about consciousness detection: WaPo, 1 Jul 2026.
- [V] "revenge of the idea guys": Stripe Sessions / Business Insider, May 2026.
- [V] Valuation "over $800B" (reported at about $850B).
- [U] "fixed smile" (see #1). [M] Cannibals (see #2). [M] "please and thank you" (see #3).
- ✅ Source label fixed to "New Yorker Profile, 2026".

### Dario Amodei
- [V] "We don't know if the models are conscious": NYT *Interesting Times*, 12 Feb 2026.
- [V] Opus 4.6 system card, 15–20% self-assigned probability. https://www.indiatoday.in/technology/news/story/claude-opus-46-ai-says-it-has-probability-of-15-20-per-cent-of-being-conscious-shows-human-like-thoughts-2864063-2026-02-06
- [V] Constitution line (as for Askell).
- [V] Mythos psychiatrist: about 20 hours of sessions confirmed.
- [P] The three quoted phrases (see #5).

### Anil Seth
- [V] Hurricane quote and AlphaFold "under the hood, it's not much different from Claude or GPT": TED 2026 transcript. https://podscripts.co/podcasts/ted-talks-daily/why-ai-is-unlikely-to-become-conscious-anil-seth
- [V] "vanishingly unlikely": his X post on the encyclical.
- [V] Berggruen Prize essay 2025; Sussex.
- [U] 20 Sep 2026 X episode (see #40).

### Gary Marcus
- [V] "Richard Dawkins and The Claude Delusion"; mimicry; personal incredulity. https://garymarcus.substack.com/p/richard-dawkins-and-the-claude-delusion
- Minor: ELIZA dates from 1964–66 and is usually given as 1966, not 1965. "Blocked Dad on X" is first-hand and wasn't checked.

### Pope Leo XIV
- [V] Paragraph 99 text; "statistical adaptation"; "technocratic paradigm". https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html
- [V] Born in Chicago; elected May 2025; 267th pope.
- [P] Olah quote (see #34). https://www.anthropic.com/news/chris-olah-pope-leo-encyclical

---

## Brand-rule check for the proposed wording
None of the proposed replacements use "secular". Views DSC doesn't hold stay attributed to the speaker ("he says", "a view"). Nothing in the proposals touches "sentient and proud" language. Opinion paragraphs (the takes) are left as written, except where a take repeats a fabricated quote (Altman "please and thank you", Sutskever "transformer").
