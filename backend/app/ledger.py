"""
Ledger system for event logging.
Provides simple event tracking for jobs and system operations.
"""
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

logger = logging.getLogger(__name__)


async def log_event(
    event_type: str,
    data: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a general system event.
    
    Args:
        event_type: Type of event (e.g., "video_upload", "job_created")
        data: Event data
        metadata: Optional metadata
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "data": data,
        "metadata": metadata or {}
    }
    logger.info(f"Event logged: {event_type}", extra=log_entry)


async def log_job_event(
    job_id: UUID,
    event_type: str,
    status: Optional[str] = None,
    message: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a job-specific event.
    
    Args:
        job_id: Job UUID
        event_type: Type of event (e.g., "job_started", "job_completed", "job_failed")
        status: Job status
        message: Optional message
        data: Optional additional data
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "job_id": str(job_id),
        "event_type": event_type,
        "status": status,
        "message": message,
        "data": data or {}
    }
    logger.info(f"Job event: {event_type} for job {job_id}", extra=log_entry)
