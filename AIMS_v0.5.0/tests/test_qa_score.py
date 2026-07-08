from packages.aims_architecture.qa_score import compute_quality_score
from packages.aims_core.adf import ADFDocument, ADFEntity, ValidationIssue


def test_quality_score_penalizes_issues():
    doc = ADFDocument(source_file="x.dxf")
    doc.entities.append(ADFEntity(entity_type="LINE", issues=[ValidationIssue(code="X", severity="error", message="bad")]))
    assert compute_quality_score(doc) == 92


def test_empty_document_score_is_zero():
    assert compute_quality_score(ADFDocument(source_file="empty.dxf")) == 0
