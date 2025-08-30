"""
Export API endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.services.export_service import ExportService

router = APIRouter()


@router.get("/resume/{resume_id}/json")
async def export_resume_json(
    resume_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Export single resume analysis to JSON"""
    try:
        export_service = ExportService(db)
        result = export_service.export_resume_to_json(resume_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/resume/{resume_id}/csv")
async def export_resume_csv(
    resume_id: str,
    db: Session = Depends(get_db)
):
    """Export single resume analysis to CSV"""
    try:
        export_service = ExportService(db)
        csv_content = export_service.export_resume_to_csv(resume_id)
        
        # Create streaming response
        def generate():
            yield csv_content
        
        return StreamingResponse(
            generate(),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=resume_{resume_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/vacancy/{vacancy_id}/resumes/json")
async def export_vacancy_resumes_json(
    vacancy_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Export all resumes for a vacancy to JSON"""
    try:
        export_service = ExportService(db)
        result = export_service.export_vacancy_resumes_to_json(vacancy_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/vacancy/{vacancy_id}/resumes/csv")
async def export_vacancy_resumes_csv(
    vacancy_id: str,
    db: Session = Depends(get_db)
):
    """Export all resumes for a vacancy to CSV"""
    try:
        export_service = ExportService(db)
        csv_content = export_service.export_vacancy_resumes_to_csv(vacancy_id)
        
        # Create streaming response
        def generate():
            yield csv_content
        
        return StreamingResponse(
            generate(),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=vacancy_{vacancy_id}_resumes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/statistics/json")
async def export_statistics_json(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Export system statistics to JSON"""
    try:
        export_service = ExportService(db)
        result = export_service.export_statistics_to_json()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics/csv")
async def export_statistics_csv(
    db: Session = Depends(get_db)
):
    """Export system statistics to CSV"""
    try:
        export_service = ExportService(db)
        csv_content = export_service.export_statistics_to_csv()
        
        # Create streaming response
        def generate():
            yield csv_content
        
        return StreamingResponse(
            generate(),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=resume_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/batch/{batch_id}/results/json")
async def export_batch_results_json(
    batch_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Export batch processing results to JSON"""
    try:
        from app.services.batch_processing_service import BatchProcessingService
        from app.services.cache_service import cache_service
        
        # Get batch status from cache
        batch_status = cache_service.get("batch_processing", batch_id)
        if not batch_status:
            raise HTTPException(status_code=404, detail="Batch not found")
        
        export_data = {
            "batch_info": batch_status,
            "export_metadata": {
                "export_date": datetime.now().isoformat(),
                "export_format": "json",
                "version": "1.0"
            }
        }
        
        return export_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/batch/{batch_id}/results/csv")
async def export_batch_results_csv(
    batch_id: str,
    db: Session = Depends(get_db)
):
    """Export batch processing results to CSV"""
    try:
        from app.services.cache_service import cache_service
        import csv
        import io
        
        # Get batch status from cache
        batch_status = cache_service.get("batch_processing", batch_id)
        if not batch_status:
            raise HTTPException(status_code=404, detail="Batch not found")
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Batch Processing Results Export"])
        writer.writerow(["Export Date", datetime.now().isoformat()])
        writer.writerow([])
        
        # Batch Info
        writer.writerow(["BATCH INFORMATION"])
        writer.writerow(["Field", "Value"])
        writer.writerow(["Batch ID", batch_status["batch_id"]])
        writer.writerow(["Status", batch_status["status"]])
        writer.writerow(["Total Files", batch_status["total_files"]])
        writer.writerow(["Successful", batch_status["successful"]])
        writer.writerow(["Failed", batch_status["failed"]])
        writer.writerow(["Processing Time", f"{batch_status.get('processing_time_seconds', 0):.2f} seconds"])
        writer.writerow([])
        
        # Results
        if batch_status.get("results"):
            writer.writerow(["PROCESSING RESULTS"])
            writer.writerow(["File Index", "Filename", "Status", "Resume ID", "Sections Found", "Skills Found", "Error"])
            for result in batch_status["results"]:
                writer.writerow([
                    result.get("file_index", ""),
                    result.get("filename", ""),
                    result.get("status", ""),
                    result.get("resume_id", ""),
                    result.get("sections_found", ""),
                    result.get("skills_found", ""),
                    result.get("error", "")
                ])
        
        csv_content = output.getvalue()
        
        # Create streaming response
        def generate():
            yield csv_content
        
        return StreamingResponse(
            generate(),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=batch_{batch_id}_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
