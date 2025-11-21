"""
SQLAlchemy ORM models for database tables.
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Text, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class JobStatus(str, enum.Enum):
    """Job status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    RETRY = "retry"
    COMPLETED = "completed"
    FAILED = "failed"


class ClipStatus(str, enum.Enum):
    """Clip status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    PUBLISHED = "published"
    FAILED = "failed"


class CampaignStatus(str, enum.Enum):
    """Campaign status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class RuleStatus(str, enum.Enum):
    """Rule status enumeration."""
    CANDIDATE = "candidate"
    APPROVED = "approved"
    ACTIVE = "active"
    DEPRECATED = "deprecated"


# Video Assets
class VideoAsset(Base):
    """Video asset model."""
    __tablename__ = "video_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    release_date = Column(DateTime, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    idempotency_key = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    clips = relationship("Clip", back_populates="video_asset")
    jobs = relationship("Job", back_populates="video_asset")
    best_clip_decisions = relationship("BestClipDecisionModel", back_populates="video_asset")


# Jobs
class Job(Base):
    """Job model for processing tasks."""
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_type = Column(String(50), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    params = Column(JSON, nullable=True)
    dedup_key = Column(String(255), unique=True, nullable=True)
    video_asset_id = Column(UUID(as_uuid=True), ForeignKey("video_assets.id"), nullable=True)
    clip_id = Column(UUID(as_uuid=True), ForeignKey("clips.id"), nullable=True)
    result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    video_asset = relationship("VideoAsset", back_populates="jobs")
    clip = relationship("Clip", back_populates="jobs", foreign_keys=[clip_id])


# Clips
class Clip(Base):
    """Clip model."""
    __tablename__ = "clips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    video_asset_id = Column(UUID(as_uuid=True), ForeignKey("video_assets.id"), nullable=False)
    start_ms = Column(Integer, nullable=False)
    end_ms = Column(Integer, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    visual_score = Column(Float, nullable=True)
    status = Column(Enum(ClipStatus), default=ClipStatus.PENDING, nullable=False)
    params = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    video_asset = relationship("VideoAsset", back_populates="clips")
    variants = relationship("ClipVariant", back_populates="clip")
    jobs = relationship("Job", back_populates="clip", foreign_keys=[Job.clip_id])
    campaigns = relationship("Campaign", back_populates="clip")
    publications = relationship("Publication", back_populates="clip")


# Clip Variants
class ClipVariant(Base):
    """Clip variant model for platform-specific versions."""
    __tablename__ = "clip_variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    clip_id = Column(UUID(as_uuid=True), ForeignKey("clips.id"), nullable=False)
    variant_number = Column(Integer, nullable=False)
    platform = Column(String(50), nullable=True)
    file_path = Column(String(500), nullable=True)
    url = Column(String(500), nullable=True)
    status = Column(String(50), default="pending")
    params = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    clip = relationship("Clip", back_populates="variants")


# Publications
class Publication(Base):
    """Publication tracking model."""
    __tablename__ = "publications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    clip_id = Column(UUID(as_uuid=True), ForeignKey("clips.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    post_url = Column(String(500), nullable=True)
    post_id = Column(String(255), nullable=True)
    published_at = Column(DateTime, nullable=True)
    confirmed_by = Column(UUID(as_uuid=True), nullable=True)
    trace_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    clip = relationship("Clip", back_populates="publications")


# Campaigns
class Campaign(Base):
    """Campaign model for ad campaigns."""
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    clip_id = Column(UUID(as_uuid=True), ForeignKey("clips.id"), nullable=False)
    budget_cents = Column(Integer, nullable=False)
    targeting = Column(JSON, nullable=True)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    clip = relationship("Clip", back_populates="campaigns")


# Platform Rules
class PlatformRule(Base):
    """Platform rules model."""
    __tablename__ = "platform_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    rules = Column(JSON, nullable=False)
    status = Column(Enum(RuleStatus), default=RuleStatus.CANDIDATE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Rule Engine Weights
class RuleEngineWeights(Base):
    """Rule engine weights model."""
    __tablename__ = "rules_engine_weights"

    platform = Column(String(50), primary_key=True)
    weights = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Best Clip Decision Model
class BestClipDecisionModel(Base):
    """Best clip decision model for campaigns engine."""
    __tablename__ = "best_clip_decisions"

    id = Column(Integer, primary_key=True, index=True)
    video_asset_id = Column(Integer, ForeignKey("video_assets.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    selected_clip_id = Column(Integer, ForeignKey("clips.id"), nullable=True)
    decision_data = Column(JSON, nullable=True)  # Store decision metadata
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    video_asset = relationship("VideoAsset", back_populates="best_clip_decisions")
    selected_clip = relationship("Clip")


# Social Account Model (for publishing engine)
class SocialAccountModel(Base):
    """Social media account model for publishing."""
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)  # instagram, tiktok, youtube, etc.
    handle = Column(String(100), nullable=False)    # @username
    display_name = Column(String(200), nullable=True)
    account_data = Column(JSON, nullable=True)      # Platform-specific data
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    publish_logs = relationship("PublishLogModel", back_populates="social_account")


# Publish Log Model (for publishing engine)
class PublishLogModel(Base):
    """Publishing log model to track publishing attempts."""
    __tablename__ = "publish_logs"

    id = Column(Integer, primary_key=True, index=True)
    clip_id = Column(Integer, ForeignKey("clips.id"), nullable=False)
    social_account_id = Column(Integer, ForeignKey("social_accounts.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)     # pending, published, failed, etc.
    platform_post_id = Column(String(100), nullable=True)  # ID from platform
    publish_data = Column(JSON, nullable=True)      # Platform response data
    error_message = Column(Text, nullable=True)
    attempt_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    clip = relationship("Clip")
    social_account = relationship("SocialAccountModel", back_populates="publish_logs")
