from packages.aims_architecture.metrics import compute_architectural_metrics
from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry, ValidationIssue


def test_architectural_metrics_counts_categories_and_issues():
    doc = ADFDocument(source_file="x.dxf")
    doc.entities.append(
        ADFEntity(
            entity_type="LWPOLYLINE",
            layer="A-WALL",
            category=ADFCategory.WALL,
            geometry=ADFGeometry(type="polyline", points=[[0, 0, 0], [1, 0, 0]], closed=False),
            issues=[ValidationIssue(code="OPEN_BOUNDARY", severity="warning", message="open")],
        )
    )
    metrics = compute_architectural_metrics(doc)
    assert metrics.category_counts["Wall"] == 1
    assert metrics.layer_counts["A-WALL"] == 1
    assert metrics.issue_counts["OPEN_BOUNDARY"] == 1
    assert metrics.severity_counts["warning"] == 1
