from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import Base

class ContentMap(Base):
    __tablename__ = "content_maps"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("ContentMapItem", back_populates="content_map")

class ContentMapItem(Base):
    __tablename__ = "content_map_items"
    id = Column(Integer, primary_key=True, index=True)
    content_map_id = Column(Integer, ForeignKey("content_maps.id"))
    source_idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=True)

    target_platform = Column(String)
    content_type = Column(String)
    content_form = Column(String)
    priority = Column(Integer, default=0)
    proposed_date = Column(DateTime, nullable=True)
    sequence_order = Column(Integer, default=0)
    series_grouping = Column(String, nullable=True)
    relation_to_other_items = Column(String, nullable=True)
    status = Column(String) # planned, in_progress, scheduled, published

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    content_map = relationship("ContentMap", back_populates="items")

    # We could add relationship to Idea, but keeping it simple based on requirements
