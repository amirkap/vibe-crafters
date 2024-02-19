from enum import Enum

class Mood(Enum):
    SAD = 'sad'
    CALM = 'calm'
    HAPPY = 'happy'
    RELAXING = 'relaxing'
    ENERGETIC = 'energetic'
    ROMANTIC = 'romantic'
    ANGRY = 'angry'
    MOTIVATIONAL = 'motivational'
    NOSTALGIC = 'nostalgic'
    PARTY = 'party'
    CHILL = 'chill'
    FOCUS = 'focus'
    ADVENTUROUS = 'adventurous'
    MELANCHOLIC = 'melancholic'
    UPBEAT = 'upbeat'
    SENSUAL = 'sensual'
    GROOVY = 'groovy'
    MYSTERIOUS = 'mysterious'
    SPIRITUAL = 'spiritual'
    SOOTHING = 'soothing'
    FUNKY = 'funky'
    DREAMY = 'dreamy'
    INTENSE = 'intense'
    JAZZY = 'jazzy'
    ECLECTIC = 'eclectic'
    ETHNIC = 'ethnic'
    EMPOWERED = 'empowered'
    HOPEFUL = 'hopeful'
    LONELY = 'lonely'
    CONFIDENT = 'confident'
    JOYFUL = 'joyful'
    PENSIVE = 'pensive'
    REFLECTIVE = 'reflective'
    SERENE = 'serene'
    VULNERABLE = 'vulnerable'
    WISTFUL = 'wistful'
    TRIUMPHANT = 'triumphant'
    HEARTBROKEN = 'heartbroken'
    OPTIMISTIC = 'optimistic'
    UPLIFTING = 'uplifting'
    DETERMINED = 'determined'

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, values : dict):
        if isinstance(value, cls):
            return value
        try:
            value = value.lower()
        except AttributeError:
            raise ValueError(f"Invalid value for Mood: {value}")
        return cls(value)