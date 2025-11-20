"""
Background worker for processing jobs.
Handles asynchronous job execution and E2B sandbox dispatching.
"""
import asyncio
import logging
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.database import Job, JobStatus
from app.core.database import async_session_maker
from app.ledger import log_job_event

logger = logging.getLogger(__name__)


async def process_single_job(db: AsyncSession) -> dict:
    """
    Process a single pending job from the queue.
    
    This is a simplified worker that handles E2B jobs.
    In a production environment, this would be replaced with
    a proper job queue system (Celery, RQ, etc.).
    
    Args:
        db: Database session
        
    Returns:
        Dictionary with processing result
    """
    # Get first pending job
    result = await db.execute(
        select(Job)
        .where(Job.status == JobStatus.PENDING)
        .order_by(Job.created_at)
        .limit(1)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        return {
            "processed": False,
            "message": "No pending jobs in queue"
        }
    
    # Update job status
    job.status = JobStatus.PROCESSING
    await db.commit()
    
    try:
        # Route based on job type
        if job.job_type == "cut_analysis_e2b":
            # Use the new services layer for E2B
            from app.services.e2b_service import dispatch_e2b_job, handle_e2b_callback
            
            # Run E2B simulation
            result = await dispatch_e2b_job(
                job_id=job.id,
                video_asset_id=job.video_asset_id,
                params=job.params or {},
                db=db
            )
            
            # Handle callback
            await handle_e2b_callback(
                job_id=job.id,
                result=result,
                db=db
            )
            
            return {
                "processed": True,
                "job_id": str(job.id),
                "job_type": job.job_type,
                "status": "completed",
                "result": job.result,
                "processing_time_ms": result.processing_time_ms
            }
        else:
            # Unknown job type
            job.status = JobStatus.FAILED
            job.error_message = f"Unknown job type: {job.job_type}"
            await db.commit()
            
            return {
                "processed": True,
                "job_id": str(job.id),
                "job_type": job.job_type,
                "status": "failed",
                "error": f"Unknown job type: {job.job_type}"
            }
    
    except Exception as e:
        # Handle errors
        job.status = JobStatus.FAILED
        job.error_message = str(e)
        await db.commit()
        
        return {
            "processed": True,
            "job_id": str(job.id),
            "job_type": job.job_type,
            "status": "failed",
            "error": str(e)
        }


async def worker_loop(poll_interval: int = 5) -> None:
    """
    Main worker loop that polls for pending jobs.
    
    Args:
        poll_interval: Seconds between polling cycles
    """
    logger.info(f"Worker loop started with poll interval {poll_interval}s")
    
    while True:
        try:
            async with async_session_maker() as db:
                result = await process_single_job(db)
                
                if result["processed"]:
                    logger.info(f"Processed job: {result}")
                
        except Exception as e:
            logger.error(f"Worker loop error: {str(e)}")
        
        await asyncio.sleep(poll_interval)
