from datetime import datetime
from ..extensions.extensions import db


class Task(db.Model):
    __tablename__ = "ttasktbl"
    __table_args__ = {"schema": "todoapp"}

    task_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("todoapp.tusertbl.user_id"), nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    due_date = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("tasks", lazy=True))

    def to_dict(self):
        return {
            "task_id": int(self.task_id) if self.task_id is not None else None,
            "user_id": int(self.user_id) if self.user_id is not None else None,
            "title": self.title,
            "description": self.description,
            "is_completed": bool(self.is_completed),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
