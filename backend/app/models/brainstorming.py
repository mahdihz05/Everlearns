from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from . import Base

class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("BrainstormingSession", back_populates="workspace")
    ideas = relationship("Idea", back_populates="workspace")

class BrainstormingSession(Base):
    __tablename__ = "brainstorming_sessions"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    workspace = relationship("Workspace", back_populates="sessions")
    messages = relationship("SessionMessage", back_populates="session")
    ideas = relationship("Idea", back_populates="session")

class SessionMessage(Base):
    __tablename__ = "session_messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("brainstorming_sessions.id"))
    role = Column(String) # user, ai, system
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    traceability_metadata = Column(JSON, nullable=True) # traceability to AI/provider

    session = relationship("BrainstormingSession", back_populates="messages")

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    session_id = Column(Integer, ForeignKey("brainstorming_sessions.id"), nullable=True)

    topic = Column(String)
    angle = Column(String)
    content_goal = Column(String)
    audience = Column(String)
    suggested_platform = Column(String)
    suggested_content_type = Column(String)
    series_group_relation = Column(String, nullable=True)
    priority = Column(Integer, default=0)
    rationale_context = Column(Text)
    status = Column(String) # generated, selected, rejected

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    workspace = relationship("Workspace", back_populates="ideas")
    session = relationship("BrainstormingSession", back_populates="ideas")
