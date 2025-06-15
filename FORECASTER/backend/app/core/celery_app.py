from celery import Celery
from celery.schedules import crontab
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create Celery instance
celery_app = Celery(
    "restaurant_forecasting",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.ml.tasks",
        "app.api.tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.TIMEZONE,
    enable_utc=True,
    
    # Task routing
    task_routes={
        "app.ml.tasks.*": {"queue": "ml_queue"},
        "app.api.tasks.*": {"queue": "api_queue"},
    },
    
    # Worker settings
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=100,
    
    # Result backend settings
    result_expires=3600,  # 1 hour
    result_backend_transport_options={
        "master_name": "mymaster",
        "visibility_timeout": 3600,
    },
    
    # Task execution settings
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,       # 10 minutes
    task_reject_on_worker_lost=True,
    
    # Error handling
    task_annotations={
        "*": {"rate_limit": "10/s"},
        "app.ml.tasks.train_model": {"rate_limit": "1/m"},
        "app.ml.tasks.generate_forecast": {"rate_limit": "5/m"},
    }
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    # Data generation task (for demo purposes)
    "generate-daily-data": {
        "task": "app.ml.tasks.generate_daily_data",
        "schedule": crontab(hour=0, minute=30),  # Daily at 12:30 AM
    },
    
    # Model retraining
    "retrain-models": {
        "task": "app.ml.tasks.retrain_all_models",
        "schedule": crontab(hour=2, minute=0),   # Daily at 2:00 AM
    },
    
    # Generate forecasts for next day
    "generate-daily-forecasts": {
        "task": "app.ml.tasks.generate_daily_forecasts",
        "schedule": crontab(hour=3, minute=0),   # Daily at 3:00 AM
    },
    
    # Model performance monitoring
    "monitor-model-performance": {
        "task": "app.ml.tasks.monitor_model_performance",
        "schedule": crontab(hour=4, minute=0),   # Daily at 4:00 AM
    },
    
    # Cleanup old data and cache
    "cleanup-old-data": {
        "task": "app.api.tasks.cleanup_old_data",
        "schedule": crontab(hour=1, minute=0, day_of_month=1),  # Monthly cleanup
    },
    
    # Health check for services
    "health-check": {
        "task": "app.api.tasks.health_check_services",
        "schedule": crontab(minute="*/5"),       # Every 5 minutes
    },
    
    # Update model metrics
    "update-model-metrics": {
        "task": "app.ml.tasks.update_model_metrics",
        "schedule": crontab(minute="*/15"),      # Every 15 minutes
    },
    
    # Check for alerts
    "check-alerts": {
        "task": "app.api.tasks.check_demand_alerts",
        "schedule": crontab(minute="*/10"),      # Every 10 minutes
    },
    
    # Weekly model comparison
    "weekly-model-comparison": {
        "task": "app.ml.tasks.weekly_model_comparison",
        "schedule": crontab(hour=6, minute=0, day_of_week=1),  # Monday at 6:00 AM
    },
    
    # Feature engineering update
    "update-features": {
        "task": "app.ml.tasks.update_feature_store",
        "schedule": crontab(hour=1, minute=30),  # Daily at 1:30 AM
    }
}

# Task configuration for specific tasks
TASK_CONFIG = {
    "ml_tasks": {
        "soft_time_limit": 1800,  # 30 minutes
        "time_limit": 3600,       # 1 hour
        "retry_kwargs": {"max_retries": 3, "countdown": 60},
    },
    "data_tasks": {
        "soft_time_limit": 600,   # 10 minutes
        "time_limit": 1200,       # 20 minutes
        "retry_kwargs": {"max_retries": 2, "countdown": 30},
    },
    "api_tasks": {
        "soft_time_limit": 60,    # 1 minute
        "time_limit": 120,        # 2 minutes
        "retry_kwargs": {"max_retries": 3, "countdown": 10},
    }
}

# Custom task base class
class BaseTask(celery_app.Task):
    """Base task class with common functionality"""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Called when task fails"""
        logger.error(
            f"Task {self.name} failed: {exc}\n"
            f"Task ID: {task_id}\n"
            f"Args: {args}\n"
            f"Kwargs: {kwargs}\n"
            f"Error info: {einfo}"
        )
    
    def on_success(self, retval, task_id, args, kwargs):
        """Called when task succeeds"""
        logger.info(
            f"Task {self.name} succeeded\n"
            f"Task ID: {task_id}\n"
            f"Result: {retval}"
        )
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Called when task is retried"""
        logger.warning(
            f"Task {self.name} retrying: {exc}\n"
            f"Task ID: {task_id}\n"
            f"Args: {args}\n"
            f"Kwargs: {kwargs}"
        )

# Set base task class
celery_app.Task = BaseTask

# Utility functions
def get_task_status(task_id: str):
    """Get task status by ID"""
    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
        "traceback": result.traceback if result.failed() else None,
    }

def revoke_task(task_id: str, terminate: bool = False):
    """Revoke task by ID"""
    celery_app.control.revoke(task_id, terminate=terminate)

def get_active_tasks():
    """Get active tasks"""
    inspect = celery_app.control.inspect()
    return inspect.active()

def get_scheduled_tasks():
    """Get scheduled tasks"""
    inspect = celery_app.control.inspect()
    return inspect.scheduled()

def get_worker_stats():
    """Get worker statistics"""
    inspect = celery_app.control.inspect()
    return inspect.stats()

# Health check function
def celery_health_check():
    """Check Celery health"""
    try:
        inspect = celery_app.control.inspect()
        stats = inspect.stats()
        if stats:
            return {"status": "healthy", "workers": list(stats.keys())}
        else:
            return {"status": "no_workers", "workers": []}
    except Exception as e:
        logger.error(f"Celery health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)} 