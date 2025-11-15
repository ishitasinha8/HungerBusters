"""
Claude AI Service for Bhookh Buster
Provides intelligent food recommendations using Claude API
"""

import json
from datetime import datetime


class ClaudeAIService:
    """
    Service for getting AI-powered food recommendations using Claude API
    """
    
    def __init__(self):
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-sonnet-4-20250514"
    
    def get_personalized_suggestions(self, user, available_items, mood=None, context=None):
        """
        Get personalized food suggestions using Claude AI
        
        Args:
            user: User object with preferences and history
            available_items: List of available food items
            mood: User's current mood (optional)
            context: Additional context like time of day, weather (optional)
        
        Returns:
            List of suggested items with explanations
        """
        
        # Prepare user profile for Claude
        user_profile = self._build_user_profile(user)
        
        # Prepare food items data
        items_data = self._prepare_items_for_claude(available_items)
        
        # Build the prompt for Claude
        prompt = self._build_recommendation_prompt(user_profile, items_data, mood, context)
        
        try:
            # Make API call to Claude
            response = self._call_claude_api(prompt)
            
            # Parse and return suggestions
            suggestions = self._parse_claude_response(response, available_items)
            return suggestions
            
        except Exception as e:
            print(f"Error getting Claude recommendations: {e}")
            # Fallback to basic recommendations
            return self._fallback_recommendations(available_items, user)
    
    def get_meal_insights(self, user, selected_items):
        """
        Get nutritional insights and meal balance analysis from Claude
        
        Args:
            user: User object
            selected_items: List of items user has selected
        
        Returns:
            Dictionary with insights and suggestions
        """
        
        prompt = f"""Analyze this meal selection for a student at Cornell University:

User Profile:
- Dietary preferences: {', '.join(user.dietary_preferences) if user.dietary_preferences else 'None specified'}
- Location: {user.location}

Selected Items:
{json.dumps(selected_items, indent=2)}

Please provide:
1. A brief nutritional overview (2-3 sentences)
2. Balance assessment (is it well-rounded?)
3. One suggestion for improvement if needed

Respond in JSON format:
{{
    "nutritional_overview": "brief overview here",
    "balance_score": 1-10,
    "balance_assessment": "assessment here",
    "suggestion": "suggestion here or null if none needed"
}}

IMPORTANT: Your response must be ONLY valid JSON. Do not include any text outside the JSON structure."""
        
        try:
            response = self._call_claude_api(prompt)
            insights = json.loads(response.strip())
            return insights
        except Exception as e:
            print(f"Error getting meal insights: {e}")
            return {
                "nutritional_overview": "Analysis unavailable",
                "balance_score": 7,
                "balance_assessment": "Your selection looks good!",
                "suggestion": None
            }
    
    def generate_food_waste_impact(self, num_items_saved, total_cost_saved):
        """
        Generate personalized impact message about food waste reduction
        
        Args:
            num_items_saved: Number of food items saved
            total_cost_saved: Total cost of food saved
        
        Returns:
            Motivational message about impact
        """
        
        prompt = f"""Generate a brief, encouraging message (2-3 sentences) about the positive impact of saving {num_items_saved} food items worth ${total_cost_saved:.2f} from going to waste at Cornell dining halls.

Make it:
- Uplifting and motivational
- Include a concrete environmental fact
- Personal and relevant to college students
- End with an emoji

Keep it under 50 words. Respond with ONLY the message text, no quotes or extra formatting."""
        
        try:
            response = self._call_claude_api(prompt, max_tokens=150)
            return response.strip()
        except Exception as e:
            print(f"Error generating impact message: {e}")
            return f"Amazing! You've saved {num_items_saved} meals from waste. Every meal saved makes a difference! 🌍"
    
    def _build_user_profile(self, user):
        """Build a structured user profile for Claude with all dietary information"""
        return {
            "name": user.name,
            "location": user.location,
            "dietary_preferences": user.dietary_preferences,
            "dietary_restrictions": getattr(user, 'dietary_restrictions', []),
            "allergens": getattr(user, 'allergens', []),
            "food_categories": getattr(user, 'food_categories', []),
            "quick_preferences": getattr(user, 'quick_preferences', []),
            "dislikes": getattr(user, 'dislikes', []),
            "food_type_preferences": user.preferences_score,
            "interaction_count": len(user.interaction_history)
        }
    
    def _prepare_items_for_claude(self, available_items):
        """Prepare food items data for Claude analysis"""
        items_summary = []
        
        for item in available_items[:20]:  # Limit to 20 items for context window
            hours_until_expiry = (
                datetime.fromisoformat(item['expiry']) - datetime.now()
            ).total_seconds() / 3600
            
            items_summary.append({
                "id": item['item_id'],
                "name": item['name'],
                "type": item['food_type'],
                "restaurant": item.get('restaurant', 'Unknown'),
                "location": item.get('restaurant_location', 'Unknown'),
                "price_cents": item['original_price'],
                "hours_until_expiry": round(hours_until_expiry, 1),
                "urgent": hours_until_expiry < 4
            })
        
        return items_summary
    
    def _build_recommendation_prompt(self, user_profile, items_data, mood, context):
        """Build the prompt for Claude API with strict dietary filtering"""
        
        time_of_day = datetime.now().hour
        meal_time = "breakfast" if time_of_day < 11 else "lunch" if time_of_day < 16 else "dinner"
        
        # Build dietary restrictions message
        dietary_msg = ""
        if user_profile.get('dietary_restrictions'):
            dietary_msg = f"\n⚠️ CRITICAL DIETARY RESTRICTIONS:\n"
            for restriction in user_profile['dietary_restrictions']:
                dietary_msg += f"  - {restriction.upper()}\n"
        
        # Build allergens message  
        allergens_msg = ""
        if user_profile.get('allergens'):
            allergens_msg = f"\n🚨 CRITICAL ALLERGENS (NEVER RECOMMEND):\n"
            for allergen in user_profile['allergens']:
                allergens_msg += f"  - {allergen.upper()} - ABSOLUTE EXCLUSION\n"
        
        # Build food categories preference
        categories_msg = ""
        if user_profile.get('food_categories'):
            categories_msg = f"\nPreferred Food Categories:\n  {', '.join(user_profile['food_categories'])}\n"
        
        # Build dislikes message
        dislikes_msg = ""
        if user_profile.get('dislikes'):
            dislikes_msg = f"\nUser Dislikes (lower priority):\n  {', '.join(user_profile['dislikes'])}\n"
        
        prompt = f"""You are a food recommendation AI helping Cornell students reduce food waste by suggesting surplus food items from campus dining halls.

IMPORTANT: All items provided have ALREADY been filtered for safety. They are all safe for this user based on their dietary restrictions and allergens.

User Profile:
- Name: {user_profile['name']}
- Location: {user_profile['location']}{dietary_msg}{allergens_msg}{categories_msg}{dislikes_msg}
- Current mood: {mood if mood else 'Not specified'}
- Meal time: {meal_time}

Available Food Items (ALL PRE-FILTERED FOR SAFETY):
{json.dumps(items_data, indent=2)}

Task: Recommend the TOP 8 items that best match this user's preferences, mood, and the current time. 

Prioritization Criteria:
1. Items matching preferred food categories ({', '.join(user_profile.get('food_categories', [])) if user_profile.get('food_categories') else 'any'})
2. Items expiring soon (urgent = true) to reduce waste
3. Items that fit the current meal time ({meal_time})
4. Variety in food types
5. Mood appropriateness
6. Avoid items containing dislikes if possible

Respond with ONLY a JSON array of item IDs with scores and brief reasons:
[
    {{
        "item_id": "id here",
        "score": 0-40,
        "reason": "One brief sentence why this is recommended"
    }}
]

CRITICAL: Respond with ONLY the JSON array. Do not include any text before or after the JSON."""
        
        return prompt
    
    def _call_claude_api(self, prompt, max_tokens=2000):
        """
        Make API call to Claude
        This would normally use the requests library, but in the sandbox we'll use fetch
        """
        import requests
        
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(
            self.api_url,
            headers={
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['content'][0]['text']
        else:
            raise Exception(f"Claude API error: {response.status_code} - {response.text}")
    
    def _parse_claude_response(self, response, available_items):
        """Parse Claude's JSON response and map to actual items"""
        try:
            # Clean up response - remove markdown code blocks if present
            cleaned = response.strip()
            if cleaned.startswith("```"):
                # Remove markdown code block markers
                lines = cleaned.split('\n')
                cleaned = '\n'.join(lines[1:-1]) if len(lines) > 2 else cleaned
            
            recommendations = json.loads(cleaned)
            
            # Create a lookup dict for available items
            items_dict = {item['item_id']: item for item in available_items}
            
            # Map recommendations to actual items
            suggestions = []
            for rec in recommendations:
                item_id = rec['item_id']
                if item_id in items_dict:
                    item = items_dict[item_id]
                    suggestions.append({
                        'item': item,
                        'score': rec['score'],
                        'ai_reason': rec.get('reason', ''),
                        'discount_price': round(item['original_price'] * 0.3, 2)
                    })
            
            return suggestions
            
        except json.JSONDecodeError as e:
            print(f"Error parsing Claude response: {e}")
            print(f"Response was: {response}")
            return []
    
    def _fallback_recommendations(self, available_items, user):
        """Fallback recommendations if Claude API fails"""
        # Simple scoring based on dietary preferences and expiry
        scored = []
        
        for item in available_items[:12]:
            score = 20  # Base score
            
            # Dietary match
            if item['food_type'] in user.dietary_preferences:
                score += 10
            
            # Urgency
            hours_until_expiry = (
                datetime.fromisoformat(item['expiry']) - datetime.now()
            ).total_seconds() / 3600
            
            if hours_until_expiry < 4:
                score += 15
            elif hours_until_expiry < 8:
                score += 10
            
            scored.append({
                'item': item,
                'score': score,
                'ai_reason': 'Recommended based on your preferences',
                'discount_price': round(item['original_price'] * 0.3, 2)
            })
        
        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored[:8]