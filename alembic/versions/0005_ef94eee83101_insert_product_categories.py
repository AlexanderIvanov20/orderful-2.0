"""insert product categories

Revision ID: 0005_ef94eee83101
Revises: 0004_2e219c56e981
Create Date: 2023-09-27 22:37:05.791420

"""
from typing import Sequence, Union

from sqlalchemy.orm import Session

from alembic import op
from orderful.models.categories import Category

# revision identifiers, used by Alembic.
revision: str = "0005_ef94eee83101"
down_revision: Union[str, None] = "0004_2e219c56e981"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PRODUCT_CATEGORIES_TREE = {
    "Electronics": {
        "Smartphones": ["Apple", "Samsung", "Google"],
        "Laptops": ["Dell", "HP", "Lenovo"],
        "Accessories": ["Headphones", "Chargers", "Cases"],
    },
    "Clothing": {
        "Men's": ["Shirts", "Jeans", "Jackets"],
        "Women's": ["Dresses", "Skirts", "Blouses"],
        "Kids'": {
            "Boys": ["T-Shirts", "Shorts"],
            "Girls": ["Dresses", "Leggings"],
        },
    },
    "Home & Kitchen": {
        "Furniture": ["Living Room", "Bedroom", "Dining"],
        "Appliances": ["Refrigerators", "Microwaves", "Washing Machines"],
        "Cookware": ["Pots & Pans", "Utensils", "Bakeware"],
    },
    "Sports & Outdoors": {
        "Outdoor Gear": ["Camping", "Hiking", "Cycling"],
        "Fitness": ["Gym Equipment", "Yoga Accessories", "Sports Apparel"],
        "Team Sports": ["Soccer", "Basketball", "Baseball"],
    },
    "Beauty & Personal Care": {
        "Skincare": ["Cleansers", "Moisturizers", "Serums"],
        "Makeup": ["Foundation", "Lipstick", "Eyeshadow"],
        "Haircare": ["Shampoo", "Conditioner", "Styling Products"],
    },
    "Books & Media": {
        "Fiction": ["Mystery", "Science Fiction", "Romance"],
        "Non-Fiction": ["Self-Help", "History", "Science"],
        "Movies": ["Action", "Comedy", "Drama"],
    },
    "Automotive": {
        "Parts & Accessories": ["Tires", "Batteries", "Car Care"],
        "Electronics": ["GPS Navigation", "Car Audio", "Dashcams"],
        "Tools & Equipment": ["Hand Tools", "Diagnostic Tools", "Lifts & Hoists"],
    },
    "Toys & Games": {
        "Board Games": ["Strategy Games", "Family Games", "Card Games"],
        "Toys for Kids": ["Action Figures", "Building Blocks", "Dolls"],
        "Outdoor Play": ["Swings", "Playsets", "Water Toys"],
    },
    "Home Improvement": {
        "Plumbing": ["Faucets", "Pipes", "Water Heaters"],
        "Electrical": ["Lighting", "Wiring", "Circuit Breakers"],
        "Hardware": ["Nails & Screws", "Tools", "Paint"],
    },
    "Pet Supplies": {
        "Dogs": ["Food", "Toys", "Beds"],
        "Cats": ["Food", "Toys", "Scratching Posts"],
        "Fish": ["Aquariums", "Fish Food", "Filters"],
    },
}


def get_session() -> Session:
    return Session(bind=op.get_bind())


def traverse_categories(categories: dict[str, dict], parent: Category | None = None) -> list:
    category_list = []

    for category_name, subcategories in categories.items():
        category = Category(name=category_name, parent=parent)

        if isinstance(subcategories, dict):
            category_list.extend(traverse_categories(subcategories, parent=category))

        for subcategory_name in subcategories:
            subcategory = Category(name=subcategory_name, parent=category)

            category_list.append(subcategory)

    return category_list


def upgrade() -> None:
    with get_session() as session:
        categories = traverse_categories(PRODUCT_CATEGORIES_TREE)

        session.add_all(categories)
        session.commit()


def downgrade() -> None:
    with get_session() as session:
        session.query(Category).delete()
