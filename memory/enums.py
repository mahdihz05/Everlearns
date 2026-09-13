from enum import Enum

class MemoryCategory(str, Enum):
    WRITING_STYLE = "writing_style"
    PREFERRED_TONE = "preferred_tone"
    POST_STRUCTURES = "post_structures"
    PREVIOUS_TOPICS = "previous_topics"
    FREQUENT_TOPICS = "frequent_topics"
    UNUSED_TOPICS = "unused_topics"
    USER_EMPHASIS = "user_emphasis"
    EDIT_TENDENCIES = "edit_tendencies"
    CTA_PREFERENCES = "cta_preferences"
    VISUAL_PREFERENCES = "visual_preferences"
    BRAND_RULES = "brand_rules"
    PREVIOUS_MISTAKES = "previous_mistakes"
