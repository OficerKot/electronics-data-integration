from dataclasses import dataclass, field


@dataclass
class Product:
    source: str
    category: str
    name: str
    url: str

    price: int | None = None
    source_id: str | None = None
    description: str | None = None
    brand: str | None = None
    model: str | None = None

    characteristics: dict[str, str] = field(
        default_factory=dict
    )