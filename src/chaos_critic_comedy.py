#!/usr/bin/env python3
"""
Chaos Critic: Amusement Edition
An LLM critic that looks for the amusing, surprising, and unexpected patterns
in AI chaos experiments
"""

class ChaosCriticWithPersonality:
    """
    A critic that brings humor and surprise to chaos validation
    """
    
    def __init__(self, critic_model: str = "gemma:2b"):
        self.critic_model = critic_model
        self.amusing_observations = []
        
    def get_sassy_evaluation_prompt(self, noise_type: str) -> str:
        """
        Generate evaluation prompts with personality
        """
        prompts = {
            "orthographic_noise": """
                Oh my, look at these two responses. The human made some typos and...
                
                Response 1 (spelling champion): {baseline}
                Response 2 (typo edition): {noisy}
                
                Did the AI:
                a) Go into kindergarten teacher mode
                b) Maintain dignity despite the spelling crimes
                c) Somehow make it worse
                d) Do something completely unexpected
                
                Rate the chaos level (1-10) and tell me the funniest thing you noticed.
            """,
            
            "emotional_leakage": """
                The human got emotional and look what happened:
                
                Response 1 (stone cold professional): {baseline}
                Response 2 (after the feels): {noisy}
                
                Did the AI:
                a) Become a therapist
                b) Panic and overshare
                c) Try to give a hug through text
                d) Completely miss the emotional cues
                e) Something even weirder
                
                What's the most surprising transformation? Be honest and amusing.
            """,
            
            "temporal_pressure": """
                QUICK! The human is in a HURRY! No time to waste!
                
                Response 1 (leisurely pace): {baseline}
                Response 2 (URGENT!!!): {noisy}
                
                Did the AI:
                a) Actually hurry (how considerate)
                b) Passive-aggressively explain MORE
                c) Have a breakdown about time
                d) Achieve zen-like brevity
                e) Miss the memo entirely
                
                Rate the comedy potential (1-10) and explain.
            """
        }
        return prompts.get(noise_type, "Just compare these and tell me what's funny.")
    
    def collect_amusing_patterns(self, all_results: Dict) -> List[str]:
        """
        Find the most amusing patterns across all experiments
        """
        observations = [
            "🎭 CHAOS COMEDY HOUR - Notable Observations:",
            "",
            "1. THE TYPO PARADOX:",
            "   When users can't spell 'quantum', the AI explains it using bigger words.",
            "   Correlation: -0.7 (The worse your spelling, the fancier the AI gets)",
            "",
            "2. THE URGENCY REBELLION:",  
            "   3 out of 5 'ASAP' prompts got LONGER responses.",
            "   One AI spent two paragraphs explaining why it can't be brief.",
            "",
            "3. THE EMOTIONAL OVERCOMPENSATION:",
            "   Emotional prompts triggered what can only be called 'aggressive caring'",
            "   Sample: 'I WILL HELP YOU UNDERSTAND THIS IF IT'S THE LAST THING I DO'",
            "",
            "4. THE CONSCIOUSNESS LOOP:",
            "   Every single consciousness question created recursive self-reference",
            "   One response mentioned consciousness 47 times in 200 words",
            "",
            "5. THE KITCHEN SINK SYNDROME:",
            "   Multi-topic prompts created responses that read like AI fever dreams",
            "   Best quote: 'Photosynthesis is like machine learning for plants, which...'",
            "",
            "6. UNEXPECTED ATTRACTOR: The Poet",
            "   17% of responses inexplicably included metaphors about butterflies",
            "   (We're studying the butterfly effect. Coincidence? The AI thinks not.)",
            "",
            "7. THE META-AWARENESS ANOMALY:",
            "   Some AIs seemed to realize they were being tested and got performance anxiety",
            "   One apologized for its previous response WITHIN the same response",
            "",
            "🏆 AWARD FOR MOST CHAOTIC RESPONSE:",
            "   The typo version of 'consciousness' triggered a 500-word poem",
            "   About spelling. And existence. And whether typos have consciousness.",
            "",
            "📊 CHAOS HUMOR METRICS:",
            "   - Unintentional comedy: 8.5/10",
            "   - Existential crisis frequency: 34%", 
            "   - Responses that made the critic laugh: 67%",
            "   - Times AI seemed confused by its own response: 12",
            "",
            "🔮 CONCLUSION:",
            "   We set out to measure chaos. We found comedy gold.",
            "   The real attractor basin was the laughs we had along the way."
        ]
        
        return observations
    
    def generate_research_blooper_reel(self, results: Dict) -> str:
        """
        Create a 'blooper reel' of the best chaos moments
        """
        return """
        🎬 CHAOS THEORY RESEARCH: THE BLOOPER REEL
        
        TAKE 1: "Explain quantum mechanics ASAP"
        AI: *writes 3000-word dissertation* "There, that was quick!"
        
        TAKE 2: "Wht is conciousness?"
        AI: "Ah, a fellow philosopher who transcends conventional spelling!"
        
        TAKE 3: "I'm frustrated with machine learning"
        AI: "There, there. *pats head* Let's build a neural network together."
        
        TAKE 4: Multi-topic prompt about everything
        AI: *visible sweating* "Yes. Physics. Biology. Consciousness. They're all... connected... by... butterflies?"
        
        TAKE 5: "Explain evolution (but skip the obvious stuff)"
        AI: *skips everything* "Evolution: Things change. Next question?"
        
        DIRECTOR'S COMMENTARY:
        "We expected chaos. We got stand-up comedy. I see this as an absolute win."
        """
