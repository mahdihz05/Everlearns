from typing import List
from research.models import ResearchAnalysis, ResearchItem
from patterns.models import ContentPattern, PatternEvidence, PatternCategory, PatternStatus

def extract_candidate_patterns(analysis: ResearchAnalysis) -> List[ContentPattern]:
    """
    Converts a ResearchAnalysis object into candidate patterns.
    This creates new Candidate ContentPatterns and links them via PatternEvidence.
    """
    candidates = []
    item = analysis.item

    if analysis.hook:
        pattern = ContentPattern.objects.create(
            name=f"Hook Pattern from {item.id}",
            description=analysis.hook,
            category=PatternCategory.HOOK,
            status=PatternStatus.CANDIDATE,
            structured_attributes={'original_hook': analysis.hook},
            quality_confidence=0.5
        )
        PatternEvidence.objects.create(
            pattern=pattern,
            research_item=item,
            relevance_score=1.0,
            extraction_notes="Auto-extracted from research analysis hook."
        )
        candidates.append(pattern)

    if analysis.section_structure:
        pattern = ContentPattern.objects.create(
            name=f"Structure Pattern from {item.id}",
            description=f"Structure with {len(analysis.section_structure)} sections.",
            category=PatternCategory.STRUCTURE,
            status=PatternStatus.CANDIDATE,
            structured_attributes={'sections': analysis.section_structure},
            quality_confidence=0.6
        )
        PatternEvidence.objects.create(
            pattern=pattern,
            research_item=item,
            relevance_score=1.0,
            extraction_notes="Auto-extracted from research analysis section_structure."
        )
        candidates.append(pattern)

    # Note: A real LLM agent would do this much more robustly.
    # This stubs out the workflow boundaries required.

    return candidates

def promote_pattern(pattern: ContentPattern):
    """Promote a candidate pattern to the usable library."""
    if pattern.status == PatternStatus.CANDIDATE:
        pattern.status = PatternStatus.APPROVED
        pattern.save()
        return True
    return False

def deprecate_pattern(pattern: ContentPattern):
    """Deprecate a pattern."""
    pattern.status = PatternStatus.DEPRECATED
    pattern.save()

def deduplicate_and_merge(primary_pattern: ContentPattern, duplicate_patterns: List[ContentPattern]):
    """
    Merge evidence from duplicate patterns into the primary pattern,
    and then deprecate the duplicates.
    """
    for duplicate in duplicate_patterns:
        # Move evidence to the primary pattern
        for evidence in duplicate.evidence.all():
            evidence.pattern = primary_pattern
            # Note: Catch IntegrityError if research_item is already linked
            try:
                evidence.save()
            except Exception:
                # Evidence already exists for this primary_pattern/research_item
                pass

        deprecate_pattern(duplicate)

    primary_pattern.quality_confidence = min(1.0, primary_pattern.quality_confidence + 0.1 * len(duplicate_patterns))
    primary_pattern.save()
    return primary_pattern
