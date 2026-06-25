from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.ANTHROPIC_API_KEY)

async def analyze_match(match, user) -> str:
    first_serve_pct = 0
    if match.first_serve_total > 0:
        first_serve_pct = round((match.first_serve_in / match.first_serve_total) * 100, 1)
    winner_error_ratio = 0
    if match.unforced_errors > 0:
        winner_error_ratio = round(match.winners / match.unforced_errors, 2)

    prompt = f"""You are an expert tennis coach analyzing a match for one of your players.

Player profile:
- Skill level: {user.skill_level}
- Dominant hand: {user.dominant_hand}
- Play style: {user.play_style}

Match details:
- Result: {match.result.upper()} vs {match.opponent_name or 'Unknown opponent'}
- Score: {match.score or 'Not recorded'}
- Surface: {match.surface}

Serve statistics:
- First serve percentage: {first_serve_pct}% ({match.first_serve_in}/{match.first_serve_total})
- Aces: {match.aces}
- Double faults: {match.double_faults}

Rally statistics:
- Winners: {match.winners}
- Unforced errors: {match.unforced_errors}
- Winner/Error ratio: {winner_error_ratio}

Break points won: {match.break_points_won}/{match.break_points_faced}
Player notes: {match.notes or 'None'}

Please provide a detailed coaching analysis with these exact sections using ** for headers:
**Match Summary** — 2-3 sentences on overall performance
**What Went Well** — 2-3 specific strengths from the stats
**Key Areas to Improve** — top 2-3 weaknesses with specific stats
**Tactical Recommendations** — 3 concrete things to work on
**Training Focus** — 1-2 specific drills targeting the weaknesses

Be specific, data-driven, and encouraging. Speak directly to the player as their coach."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    return response.choices[0].message.content

async def generate_session_tip(session_data: dict, user) -> str:
    prompt = f"""You are a tennis coach. A player just finished a training session.

Player: {user.skill_level} level, {user.play_style} style, {user.dominant_hand}-handed
Focus: {session_data['focus_area']}
Duration: {session_data['duration_mins']} minutes
Intensity: {session_data['intensity']}
Self-rating: {session_data.get('performance_rating', 'Not rated')}/10
Notes: {session_data.get('notes', 'None')}

Give a short, motivating coaching tip (3-4 sentences) specific to what they worked on today.
Include one concrete thing to focus on in their next session."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content
