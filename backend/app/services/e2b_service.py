"""
E2B Service Layer
Provides high-level interface for E2B sandbox operations.
"""
from typing import Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.database import Job, JobStatus
from app.e2b.dispatcher import dispatch_e2b_job as _dispatch_e2b_job
from app.e2b.models import E2BSandboxResult
from app.ledger import log_job_event


async def dispatch_e2b_job(
    job_id: UUID,
    video_asset_id: UUID,
    params: Dict[str, Any],
    db: AsyncSession
) -> E2BSandboxResult:
    """
    Dispatch E2B job by parameters.
    
    Args:
        job_id: Job UUID
        video_asset_id: Video asset UUID
        params: Job parameters
        db: Database session
        
    Returns:
        E2BSandboxResult from simulation
    """
    # Fetch job from database
    result = await db.execute(select(Job).filter(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise ValueError(f"Job {job_id} not found")
    
    # Dispatch to E2B
    return await _dispatch_e2b_job(job=job, db=db)


async def handle_e2b_callback(
    job_id: UUID,
    result: E2BSandboxResult,
    db: AsyncSession
) -> None:
    """
    Handle E2B simulation callback result.
    
    Args:
        job_id: Job UUID
        result: E2B simulation result
        db: Database session
    """
    # Fetch job
    query_result = await db.execute(select(Job).filter(Job.id == job_id))
    job = query_result.scalar_one_or_none()
    
    if not job:
        raise ValueError(f"Job {job_id} not found")
    
    # Update job with result
    job.status = JobStatus.COMPLETED
    job.result = {
        "status": result.status,
        "cuts": [cut.model_dump() for cut in result.cuts],
        "yolo_detections": [d.model_dump() for d in result.yolo_detections],
        "embeddings": [e.model_dump() for e in result.embeddings],
        "trend_features": result.trend_features.model_dump() if result.trend_features else None,
        "processing_time_ms": result.processing_time_ms
    }
    
    await db.commit()
    
    await log_job_event(
        job_id=job_id,
        event_type="e2b_callback_handled",
        status=JobStatus.COMPLETED.value,
        message="E2B result processed successfully",
        data={
            "num_cuts": len(result.cuts),
            "num_detections": len(result.yolo_detections),
            "processing_time_ms": result.processing_time_ms
        }
    )
