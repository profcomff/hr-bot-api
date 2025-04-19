import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseDbModel
from sqlalchemy import JSON, Boolean, DateTime, Integer, String



class Poll(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    message: Mapped[str] = mapped_column(String, nullable=True)
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    # frequency_days: Mapped[int] = mapped_column(nullable=True)  # high-level
    cron_expression: Mapped[str] = mapped_column(String, nullable=True)  # low-level
    id_groups: Mapped[List[int]] = mapped_column(JSON)
    id_users: Mapped[List[int]] = mapped_column(JSON)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    create_ts: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    update_ts: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)