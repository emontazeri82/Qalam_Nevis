from app import app
from models.extensions import db
from models import Role, Category

roles = {
    "admin": "Platform administrator",
    "editor": "Reviews and approves articles",
    "writer": "Creates and submits articles"
}
categories = {
    "stories": ("Stories", "داستان‌ها", 1),
    "poetry": ("Poetry", "شعر", 2),
    "reports": ("Reports", "گزارش‌ها", 3),
    "criticism": ("Criticism", "نقدها", 4)
}

with app.app_context():
    for code, description in roles.items():
      existing_role = db.session.scalar(
          db.select(Role).where(Role.code == code)
        )
      
      if existing_role is None:
        role = Role(
            code=code,
            description=description
        )
        db.session.add(role)

    db.session.commit()

    for slug, (name_en, name_fa, sort_order) in categories.items():
       existing_category = db.session.scalar(
          db.select(Category).where(Category.slug == slug)
       )
       
       if existing_category is None:
         category = Category(
            slug=slug,
            name_en=name_en,
            name_fa=name_fa,
            sort_order=sort_order
         )
         db.session.add(category)

    db.session.commit()