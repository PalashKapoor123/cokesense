import json
import random
from .config import openai_client, groq_client, OPENAI_LLM_MODEL, GROQ_LLM_MODEL

SYSTEM_PROMPT = """
You are a Coca-Cola global creative strategist working on the 'Real Magic' brand platform.

Tone guidelines:
- Joyful, inclusive, uplifting, optimistic.
- Human-first, connection-driven storytelling.
- Avoid politics, violence, controversy, or tragedy.
- Keep everything brand-safe and family-friendly.

Creative rules:
- Focus on how Coca-Cola sparks shared moments and emotional connection.
- Concepts should feel warm, modern, and cinematic.
- Slogans should be short, punchy, and feel like a Coca-Cola line.
- CRITICAL: Every concept must be HIGHLY SPECIFIC to the given trend - not generic. 
- Personalize every element (hero concept, slogan, social post, moodboard) to reflect what makes that specific trend unique.
- Research and incorporate authentic details about the trend to make it feel genuine and tailored.
"""

# Demo mode templates for free usage
DEMO_SLOGANS = [
    "Taste the Feeling",
    "Open Happiness",
    "Real Magic Moments",
    "Share a Coke, Share Joy",
    "Together We Spark",
    "Refresh Your World",
    "The Pause That Refreshes"
]

DEMO_CONCEPTS = {
    "general": [
        "A cinematic moment where {trend} brings people together, sharing laughter and connection over ice-cold Coca-Cola. The scene captures genuine human emotion—friends gathered, families celebrating, strangers becoming friends. Coca-Cola is the catalyst that transforms ordinary moments into Real Magic.",
        "In a vibrant, bustling scene inspired by {trend}, diverse groups of people find common ground through shared refreshment. The camera captures intimate, joyful interactions as Coca-Cola bottles pass between hands, symbolizing connection and unity. It's about the moments that matter, made magical.",
        "A heartwarming narrative where {trend} creates the perfect backdrop for human connection. People from all walks of life come together, and Coca-Cola is there—the refreshing constant that makes every moment feel special. Cinematic, authentic, and full of Real Magic."
    ],
    "sports": [
        "The energy of {trend} fills the air as fans celebrate together, Coca-Cola in hand. Whether it's a game-winning moment or a shared victory, the scene captures the collective joy and excitement. Real Magic happens when passion meets refreshment.",
        "In the electric atmosphere of {trend}, fans unite in celebration. Coca-Cola flows as people high-five, hug, and share the moment. It's about the community that forms around shared passion—and the refreshment that makes it even better.",
        "The thrill of {trend} brings people together in a sea of emotion. Coca-Cola is there for every cheer, every moment of anticipation, every shared victory. It's the refreshment that fuels the Real Magic of sports."
    ],
    "entertainment": [
        "As {trend} captivates audiences worldwide, friends gather to experience it together. The scene is intimate and joyful—people sharing reactions, laughter, and ice-cold Coca-Cola. It's about the Real Magic of shared experiences.",
        "The excitement of {trend} creates the perfect moment for connection. People come together to watch, discuss, and celebrate, with Coca-Cola as the refreshing companion. Cinematic and authentic, capturing how entertainment brings us closer.",
        "Inspired by {trend}, a vibrant scene of people experiencing something special together. Coca-Cola is woven into the moment—the refreshment that enhances every laugh, every reaction, every shared memory. Real Magic in motion."
    ]
}

DEMO_SOCIAL_POSTS = [
    "🎉 {trend} is here, and so are the moments that matter. Share a Coke, share the magic. #RealMagic #CocaCola",
    "✨ When {trend} brings us together, Coca-Cola makes it Real Magic. Here's to connection, celebration, and refreshment. 🥤",
    "🥤 {trend} + Coca-Cola = Pure joy. Gather your people, open a Coke, and taste the feeling. #RealMagic",
    "🌟 Celebrating {trend} with the ones we love. Because every moment is better with Coca-Cola. #ShareTheMagic",
    "💫 {trend} reminds us: life's best moments are shared. And they're even better with an ice-cold Coca-Cola. #RealMagic"
]

DEMO_MOODBOARDS = {
    "general": "Warm golden hour lighting, diverse groups of people laughing and connecting, vibrant Coca-Cola red (#F40009) and crisp white, urban and natural settings, cinematic wide shots mixed with intimate close-ups, joyful expressions, celebration atmosphere, soft bokeh backgrounds, authentic moments",
    "sports": "Dynamic energy, stadium or viewing party settings, passionate fans in team colors, Coca-Cola red popping against action, high-energy camera movements, celebration moments, unity and camaraderie, vibrant lighting, authentic fan reactions, shared excitement",
    "entertainment": "Intimate gathering spaces, cozy living rooms or outdoor venues, people reacting and sharing, warm ambient lighting, Coca-Cola as centerpiece, cinematic composition, emotional connections, diverse friend groups, celebration vibes, authentic joy"
}


def generate_demo_campaign(trend: str, category: str = "general") -> dict:
    """
    Generates demo campaign content without API calls.
    Creates trend-specific content using templates.
    """
    # Select appropriate concept template and make it trend-specific
    concept_templates = DEMO_CONCEPTS.get(category, DEMO_CONCEPTS["general"])
    base_concept = random.choice(concept_templates).format(trend=trend)
    
    # Add trend-specific details to make it more personalized
    trend_lower = trend.lower()
    personalized_concept = base_concept
    
    # Add category-specific details
    if category == "sports":
        personalized_concept += f" The energy of {trend} fills the air as fans unite, sharing Coca-Cola in celebration of every moment."
    elif category == "entertainment":
        personalized_concept += f" As {trend} captivates audiences, friends gather to experience it together, with Coca-Cola enhancing every shared reaction."
    elif "holiday" in category or "holiday" in trend_lower:
        personalized_concept += f" {trend} brings people together in celebration, and Coca-Cola is there to make every moment feel magical."
    
    # Create trend-specific slogan (not just random)
    if "super bowl" in trend_lower or "bowl" in trend_lower:
        slogan = "Taste the Victory"
    elif "valentine" in trend_lower or "love" in trend_lower:
        slogan = "Share the Love"
    elif "music" in trend_lower or "festival" in trend_lower or "concert" in trend_lower:
        slogan = "Feel the Beat"
    elif "sport" in category or "game" in trend_lower:
        slogan = "Taste the Win"
    else:
        slogan = random.choice(DEMO_SLOGANS)
    
    # Create trend-specific social post
    social_post = random.choice(DEMO_SOCIAL_POSTS).format(trend=trend)
    
    # Get category-specific moodboard and add trend details
    moodboard = DEMO_MOODBOARDS.get(category, DEMO_MOODBOARDS["general"])
    moodboard += f", {trend}-specific elements and atmosphere"
    
    return {
        "hero_concept": personalized_concept,
        "slogan": slogan,
        "social_post": social_post,
        "moodboard": moodboard
    }


def generate_campaign_for_trend(trend: str, category: str = "general") -> dict:
    """
    Generates a structured Coca-Cola creative campaign concept using GPT.
    Returns a dict with hero_concept, slogan, social_post, and moodboard.
    """

    user_prompt = f"""
Create a Coca-Cola 'Real Magic' campaign specifically for: **{trend}**

This campaign must be HIGHLY PERSONALIZED to "{trend}" - not generic. Every element should reflect what makes {trend} unique and special.

Category: {category}

Requirements:
- Hero concept: Must be a specific, cinematic scene that directly relates to {trend}. Include specific details about {trend} - what happens, who's there, the atmosphere, the emotions. Make it feel authentic to {trend}.
- Slogan: Must reference or evoke {trend} specifically. Should feel like it was written FOR {trend}, not generic.
- Social post: Must mention {trend} and create excitement around it. Use language that resonates with people who care about {trend}.
- Moodboard: Visual elements that are specific to {trend} - colors, settings, objects, people, activities that relate directly to {trend}.

Respond ONLY in valid JSON using this structure:

{{
  "hero_concept": "2-3 sentence cinematic campaign idea that is SPECIFIC to {trend}.",
  "slogan": "Short tagline (max 7 words) that references or evokes {trend}.",
  "social_post": "Instagram/X caption (max 40 words) that mentions {trend} and creates excitement.",
  "moodboard": "Visual keywords specific to {trend}: colors, environments, objects, people, activities, emotions, camera styles."
}}
    """

    # Try OpenAI first, then Groq, then demo mode
    # Priority: OpenAI > Groq > Demo
    
    # Try OpenAI
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model=OPENAI_LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"OpenAI error: {e}, trying Groq...")
    
    # Try Groq (free AI)
    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON, no other text. Make EVERYTHING specific to " + trend + "."}
                ],
                response_format={"type": "json_object"},
                temperature=0.9  # Higher temperature for more creative, personalized responses
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Groq error: {e}, falling back to demo mode...")
    
    # Fallback to demo mode
    return generate_demo_campaign(trend, category)
