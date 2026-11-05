from app.models import Institution

CATEGORY_LABELS = {
    "regulator": "Regulator",
    "exchange": "Exchange",
    "unit_trust": "Unit Trust",
    "broker": "Licensed Broker",
}


def filter_by_category(category: str | None):
    query = Institution.query.order_by(Institution.category, Institution.name)
    if category and category in CATEGORY_LABELS:
        query = query.filter_by(category=category)
    return query.all()
