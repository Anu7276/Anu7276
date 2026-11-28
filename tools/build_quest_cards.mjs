import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, '..', 'assets');

const RARITY_STYLES = {
  BOSS: { border: '#ff3b30', badgeBg: '#ff3b30', badgeText: '#fff1e0', accent: '#ffb347', bar: 96 },
  MYTHIC: { border: '#ffb347', badgeBg: '#3a220d', badgeText: '#ffb347', accent: '#ff6a3d', bar: 98 },
  LEGENDARY: { border: '#ff6a3d', badgeBg: '#3a160e', badgeText: '#ff6a3d', accent: '#ffb347', bar: 92 },
  EPIC: { border: '#ff8f7a', badgeBg: '#2e1510', badgeText: '#ff8f7a', accent: '#ffb347', bar: 86 },
  RARE: { border: '#7a3320', badgeBg: '#251410', badgeText: '#c9aa9c', accent: '#ff6a3d', bar: 78 },
};

function esc(str) {
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function buildBossCard(card) {
  const r = RARITY_STYLES.BOSS;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="168" viewBox="0 0 1000 168">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2a110b"/>
      <stop offset="0.55" stop-color="#190b08"/>
      <stop offset="1" stop-color="#120806"/>
    </linearGradient>
    <linearGradient id="ember" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ff3b30"/>
      <stop offset="0.5" stop-color="#ff6a3d"/>
      <stop offset="1" stop-color="#ffb347"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="rgba(255,179,71,0)"/>
      <stop offset="0.5" stop-color="rgba(255,179,71,0.14)"/>
      <stop offset="1" stop-color="rgba(255,179,71,0)"/>
    </linearGradient>
    <clipPath id="clip"><rect x="4" y="4" width="992" height="160" rx="14"/></clipPath>
    <style>
      .pulse{animation:pulse 1.6s ease-in-out infinite}
      @keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
      .sweep{animation:sweep 5s ease-in-out infinite}
      @keyframes sweep{0%{transform:translateX(-260px)}55%,100%{transform:translateX(1040px)}}
      .rise{animation:rise 4s ease-in infinite}
      @keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:.9}100%{transform:translateY(-95px);opacity:0}}
      .bar{transform-box:fill-box;transform-origin:left center;animation:grow 1.8s ease-out both}
      @keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
    </style>
  </defs>
  <rect x="4" y="4" width="992" height="160" rx="14" fill="url(#bg)" stroke="${r.border}" stroke-width="2"/>
  <rect x="10" y="10" width="980" height="148" rx="10" fill="none" stroke="#4a2015" stroke-width="1"/>
  <rect x="4" y="4" width="220" height="160" fill="url(#shine)" clip-path="url(#clip)" class="sweep"/>
  <circle cx="880" cy="146" r="2.2" fill="#ff6a3d" class="rise"/>
  <circle cx="930" cy="150" r="1.8" fill="#ffb347" class="rise" style="animation-delay:1.2s"/>
  <circle cx="760" cy="148" r="2" fill="#ff3b30" class="rise" style="animation-delay:2.1s"/>

  <circle cx="30" cy="30" r="5" fill="#ff3b30" class="pulse"/>
  <rect x="44" y="19" width="112" height="22" rx="6" fill="${r.badgeBg}"/>
  <text x="100" y="34" font-family="'Courier New',Consolas,monospace" font-size="11" font-weight="bold" fill="${r.badgeText}" text-anchor="middle" letter-spacing="1">BOSS QUEST</text>
  <rect x="164" y="19" width="104" height="22" rx="6" fill="#251410" stroke="#ffb347" stroke-width="1"/>
  <text x="216" y="34" font-family="'Courier New',Consolas,monospace" font-size="11" font-weight="bold" fill="#ffb347" text-anchor="middle">${esc(card.badge)}</text>
  <text x="970" y="34" font-family="'Courier New',Consolas,monospace" font-size="11" fill="#ffb347" text-anchor="end">${esc(card.meta)}</text>

  <text x="26" y="76" font-family="'Trebuchet MS','Segoe UI',sans-serif" font-size="24" font-weight="bold" fill="#fff1e0">${esc(card.title)}</text>
  <text x="26" y="102" font-family="'Trebuchet MS','Segoe UI',sans-serif" font-size="14" fill="#c9aa9c">${esc(card.line1)}</text>
  <text x="26" y="122" font-family="'Trebuchet MS','Segoe UI',sans-serif" font-size="14" fill="#c9aa9c">${esc(card.line2)}</text>

  <text x="26" y="148" font-family="'Courier New',Consolas,monospace" font-size="11" fill="#ffb347">${esc(card.stack)}</text>
  <text x="970" y="120" font-family="'Courier New',Consolas,monospace" font-size="10" fill="#c9aa9c" text-anchor="end">QUEST POWER</text>
  <rect x="770" y="130" width="200" height="10" rx="5" fill="#120a08" stroke="#7a3320" stroke-width="1"/>
  <rect x="770" y="130" width="${Math.round(200 * (r.bar / 100))}" height="10" rx="5" fill="url(#ember)" class="bar"/>
</svg>`;
}

function buildMiniCard(card, idx) {
  const r = RARITY_STYLES[card.rarity] || RARITY_STYLES.RARE;
  const delay = (idx * 0.45).toFixed(2);
  const badgeW = Math.max(58, card.rarity.length * 8 + 18);
  const barW = Math.round(130 * (r.bar / 100));

  return `<svg xmlns="http://www.w3.org/2000/svg" width="480" height="186" viewBox="0 0 480 186">
  <defs>
    <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1e0f0b"/>
      <stop offset="1" stop-color="#120a08"/>
    </linearGradient>
    <linearGradient id="cbar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="${r.border}"/>
      <stop offset="1" stop-color="${r.accent}"/>
    </linearGradient>
    <linearGradient id="cshine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="rgba(255,179,71,0)"/>
      <stop offset="0.5" stop-color="rgba(255,179,71,0.11)"/>
      <stop offset="1" stop-color="rgba(255,179,71,0)"/>
    </linearGradient>
    <clipPath id="cclip"><rect x="3" y="3" width="474" height="180" rx="12"/></clipPath>
    <style>
      .pulse{animation:pulse 1.8s ease-in-out infinite}
      @keyframes pulse{0%,100%{opacity:1}50%{opacity:.32}}
      .sweep{animation:sweep 6s ease-in-out infinite}
      @keyframes sweep{0%{transform:translateX(-160px)}45%,100%{transform:translateX(520px)}}
      .rise{animation:rise 4.2s ease-in infinite}
      @keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:.85}100%{transform:translateY(-80px);opacity:0}}
      .bar{transform-box:fill-box;transform-origin:left center;animation:grow 1.6s ease-out both}
      @keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
    </style>
  </defs>
  <rect x="3" y="3" width="474" height="180" rx="12" fill="url(#cbg)" stroke="${r.border}" stroke-width="1.8"/>
  <rect x="9" y="9" width="462" height="168" rx="8" fill="none" stroke="#3a1a10" stroke-width="1"/>
  <rect x="3" y="3" width="130" height="180" fill="url(#cshine)" clip-path="url(#cclip)" class="sweep" style="animation-delay:${delay}s"/>
  <circle cx="430" cy="166" r="2" fill="${r.border}" class="rise" style="animation-delay:${delay}s"/>
  <circle cx="452" cy="170" r="1.6" fill="${r.accent}" class="rise" style="animation-delay:${(Number(delay) + 1.4).toFixed(2)}s"/>

  <circle cx="26" cy="29" r="4" fill="${r.border}" class="pulse" style="animation-delay:${delay}s"/>
  <rect x="38" y="19" width="${badgeW}" height="20" rx="5" fill="${r.badgeBg}" stroke="${r.border}" stroke-width="1"/>
  <text x="${38 + badgeW / 2}" y="33" font-family="'Courier New',Consolas,monospace" font-size="10" font-weight="bold" fill="${r.badgeText}" text-anchor="middle">${esc(card.rarity)}</text>
  <text x="458" y="33" font-family="'Courier New',Consolas,monospace" font-size="11" font-weight="bold" fill="${r.accent}" text-anchor="end">${esc(card.meta)}</text>

  <text x="22" y="70" font-family="'Trebuchet MS','Segoe UI',sans-serif" font-size="20" font-weight="bold" fill="#fff1e0">${esc(card.title)}</text>
  <text x="22" y="96" font-family="'Trebuchet MS','Segoe UI',sans-serif" font-size="13" fill="#c9aa9c">${esc(card.line1)}</text>
  <text x="22" y="115" font-family="'Trebuchet MS','Segoe UI',sans-serif" font-size="13" fill="#c9aa9c">${esc(card.line2)}</text>

  <line x1="22" y1="136" x2="458" y2="136" stroke="#3a1a10" stroke-width="1"/>
  <text x="22" y="158" font-family="'Courier New',Consolas,monospace" font-size="11" fill="#ffb347">${esc(card.stack)}</text>
  <rect x="328" y="149" width="130" height="8" rx="4" fill="#0d0605" stroke="#5c2818" stroke-width="1"/>
  <rect x="328" y="149" width="${barW}" height="8" rx="4" fill="url(#cbar)" class="bar"/>
</svg>`;
}

const bossCard = {
  file: 'card_boss_ayush.svg',
  badge: 'SIH 1345',
  meta: 'MINISTRY OF AYUSH · TEAM MINDMESH',
  title: 'Startup-AYUSH Portal',
  line1: 'Multimodal pitch-deck intake agent + market search + ~20-min adaptive AI voice interview.',
  line2: 'FAISS RAG scoring (/30) routes top startups to investors and others to mentors.',
  stack: 'Gemini · Groq · FAISS (RAG) · Voice AI',
};

const miniCards = [
  {
    file: 'card_claim_verifier.svg',
    rarity: 'MYTHIC',
    meta: '#119 / 1,773 · 100% ACC',
    title: 'Insurance Claim Verifier',
    line1: 'Jointly reasons over text, images & docs with disk caching.',
    line2: 'Top ~7% globally; led to direct HackerRank outreach.',
    stack: 'Groq · Gemini 2.5 · Cache',
  },
  {
    file: 'card_maya.svg',
    rarity: 'LEGENDARY',
    meta: 'DESKTOP AGENT',
    title: 'Maya — Personal AI',
    line1: 'Full voice pipeline (Faster-Whisper + Edge-TTS) & memory.',
    line2: 'Executes real Windows desktop & system control tools.',
    stack: 'Llama 3.3 · ChromaDB · SQLite',
  },
  {
    file: 'card_vivora.svg',
    rarity: 'EPIC',
    meta: '30-MIN SESSIONS',
    title: 'VIVORA',
    line1: 'Multi-agent viva & interview simulator for students.',
    line2: 'Adaptive examiner agents for school, college & jobs.',
    stack: 'Multi-Agent · LLMs · React',
  },
  {
    file: 'card_campaignix.svg',
    rarity: 'EPIC',
    meta: 'AUTO STRATEGY PDF',
    title: 'CAMPAIGNIX',
    line1: 'Firecrawl ingestion + specialist marketing agent chain.',
    line2: 'Outputs competitor gaps, 21-day calendars & copy briefs.',
    stack: 'Python · Firecrawl · Agents',
  },
  {
    file: 'card_community_hero.svg',
    rarity: 'RARE',
    meta: 'VIBE2SHIP · CLOUD RUN',
    title: 'Community Hero',
    line1: 'Real-time AI civic issue reporting & tracking platform.',
    line2: 'Deployed on Cloud Run with full B2G SaaS pitch deck.',
    stack: 'React · Node · Gemini · Firestore',
  },
  {
    file: 'card_support_triage.svg',
    rarity: 'RARE',
    meta: '#306 / 1,349',
    title: 'Support Triage Agent',
    line1: 'Multi-domain ticket triage with hybrid semantic + keyword.',
    line2: 'FAISS + BM25 + CrossEncoder reranking before escalation.',
    stack: 'FAISS · BM25 · CrossEncoder',
  },
  {
    file: 'card_procuremind.svg',
    rarity: 'RARE',
    meta: 'SIH · BIS ENGINE',
    title: 'ProcureMind AI',
    line1: 'Recommends Indian Standards (BIS) for procurement.',
    line2: 'Matches tender specs against a structured standards KB.',
    stack: 'Python · RAG · LLMs',
  },
  {
    file: 'card_financial_agent.svg',
    rarity: 'RARE',
    meta: 'BUY OR WAIT?',
    title: 'AI Financial Agent',
    line1: 'Affordability decision engine with explainable output.',
    line2: 'Deterministic money math + Claude NL detail extraction.',
    stack: 'Python · Claude · Rules',
  },
  {
    file: 'card_college_discovery.svg',
    rarity: 'RARE',
    meta: 'INTERNSHIP TASK',
    title: 'College Discovery',
    line1: 'Full-stack college search, browsing & comparison app.',
    line2: 'Designed, built, and shipped end-to-end in a few days.',
    stack: 'Full Stack · REST APIs',
  },
];

fs.writeFileSync(path.join(OUT_DIR, bossCard.file), buildBossCard(bossCard), 'utf8');
miniCards.forEach((c, i) => {
  fs.writeFileSync(path.join(OUT_DIR, c.file), buildMiniCard(c, i), 'utf8');
});

console.log(`Generated ${1 + miniCards.length} animated quest cards in ${OUT_DIR}`);
