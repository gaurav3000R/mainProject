"""Run the FastAPI server with custom configuration."""
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    import uvicorn
    from src.core.config import settings
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload and settings.is_development,
        log_level=settings.log_level.lower(),
        access_log=True,
    )
