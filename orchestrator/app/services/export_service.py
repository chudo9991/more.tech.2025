"""
Export service for resume analysis results
"""
import json
import csv
import io
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import Resume, ResumeBlock, ResumeSkill, Vacancy
from app.services.resume_service import ResumeService


class ExportService:
    """Service for exporting resume analysis results"""
    
    def __init__(self, db: Session):
        self.db = db
        self.resume_service = ResumeService(db)
    
    def export_resume_to_json(self, resume_id: str) -> Dict[str, Any]:
        """Export single resume analysis to JSON"""
        try:
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise Exception("Resume not found")
            
            # Get vacancy info
            vacancy = None
            if resume.vacancy_id:
                vacancy = self.db.query(Vacancy).filter(Vacancy.id == resume.vacancy_id).first()
            
            # Get resume blocks
            blocks = self.db.query(ResumeBlock).filter(ResumeBlock.resume_id == resume_id).all()
            
            # Get resume skills
            skills = self.db.query(ResumeSkill).filter(ResumeSkill.resume_id == resume_id).all()
            
            export_data = {
                "resume_info": {
                    "id": resume.id,
                    "filename": resume.original_filename,
                    "file_type": resume.file_type,
                    "file_size": resume.file_size,
                    "upload_date": resume.upload_date.isoformat() if resume.upload_date else None,
                    "status": resume.status,
                    "total_score": resume.total_score,
                    "confidence_score": resume.confidence_score
                },
                "vacancy_info": {
                    "id": vacancy.id if vacancy else None,
                    "title": vacancy.title if vacancy else None,
                    "code": vacancy.vacancy_code if vacancy else None
                },
                "analysis_blocks": [
                    {
                        "id": block.id,
                        "block_type": block.block_type,
                        "block_name": block.block_name,
                        "extracted_text": block.extracted_text,
                        "relevance_score": block.relevance_score,
                        "confidence_score": block.confidence_score,
                        "matched_requirements": block.matched_requirements,
                        "missing_requirements": block.missing_requirements,
                        "analysis_notes": block.analysis_notes
                    } for block in blocks
                ],
                "skills": [
                    {
                        "id": skill.id,
                        "skill_name": skill.skill_name,
                        "category": skill.category,
                        "experience_level": skill.experience_level,
                        "confidence_score": skill.confidence_score
                    } for skill in skills
                ],
                "export_metadata": {
                    "export_date": datetime.now().isoformat(),
                    "export_format": "json",
                    "version": "1.0"
                }
            }
            
            return export_data
            
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")
    
    def export_resume_to_csv(self, resume_id: str) -> str:
        """Export single resume analysis to CSV"""
        try:
            resume = self.resume_service.get_resume(resume_id)
            if not resume:
                raise Exception("Resume not found")
            
            # Get vacancy info
            vacancy = None
            if resume.vacancy_id:
                vacancy = self.db.query(Vacancy).filter(Vacancy.id == resume.vacancy_id).first()
            
            # Get resume blocks
            blocks = self.db.query(ResumeBlock).filter(ResumeBlock.resume_id == resume_id).all()
            
            # Get resume skills
            skills = self.db.query(ResumeSkill).filter(ResumeSkill.resume_id == resume_id).all()
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Header
            writer.writerow(["Resume Analysis Export"])
            writer.writerow(["Export Date", datetime.now().isoformat()])
            writer.writerow([])
            
            # Resume Info
            writer.writerow(["RESUME INFORMATION"])
            writer.writerow(["Field", "Value"])
            writer.writerow(["ID", resume.id])
            writer.writerow(["Filename", resume.original_filename])
            writer.writerow(["File Type", resume.file_type])
            writer.writerow(["File Size", resume.file_size])
            writer.writerow(["Upload Date", resume.upload_date.isoformat() if resume.upload_date else ""])
            writer.writerow(["Status", resume.status])
            writer.writerow(["Total Score", resume.total_score])
            writer.writerow(["Confidence Score", resume.confidence_score])
            writer.writerow([])
            
            # Vacancy Info
            writer.writerow(["VACANCY INFORMATION"])
            writer.writerow(["Field", "Value"])
            writer.writerow(["ID", vacancy.id if vacancy else ""])
            writer.writerow(["Title", vacancy.title if vacancy else ""])
            writer.writerow(["Code", vacancy.vacancy_code if vacancy else ""])
            writer.writerow([])
            
            # Analysis Blocks
            if blocks:
                writer.writerow(["ANALYSIS BLOCKS"])
                writer.writerow(["Block Type", "Block Name", "Relevance Score", "Confidence Score", "Matched Requirements", "Missing Requirements", "Analysis Notes"])
                for block in blocks:
                    writer.writerow([
                        block.block_type,
                        block.block_name,
                        block.relevance_score,
                        block.confidence_score,
                        ", ".join(block.matched_requirements) if block.matched_requirements else "",
                        ", ".join(block.missing_requirements) if block.missing_requirements else "",
                        block.analysis_notes or ""
                    ])
                writer.writerow([])
            
            # Skills
            if skills:
                writer.writerow(["SKILLS"])
                writer.writerow(["Skill Name", "Category", "Experience Level", "Confidence Score"])
                for skill in skills:
                    writer.writerow([
                        skill.skill_name,
                        skill.category,
                        skill.experience_level,
                        skill.confidence_score
                    ])
            
            return output.getvalue()
            
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")
    
    def export_vacancy_resumes_to_json(self, vacancy_id: str) -> Dict[str, Any]:
        """Export all resumes for a specific vacancy to JSON"""
        try:
            # Get vacancy
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
            if not vacancy:
                raise Exception("Vacancy not found")
            
            # Get all resumes for this vacancy
            resumes = self.db.query(Resume).filter(Resume.vacancy_id == vacancy_id).all()
            
            export_data = {
                "vacancy_info": {
                    "id": vacancy.id,
                    "title": vacancy.title,
                    "code": vacancy.vacancy_code,
                    "description": vacancy.description
                },
                "resumes": [],
                "summary": {
                    "total_resumes": len(resumes),
                    "processed_resumes": len([r for r in resumes if r.status == "analyzed"]),
                    "average_score": 0,
                    "score_distribution": {
                        "excellent": 0,
                        "good": 0,
                        "average": 0,
                        "poor": 0
                    }
                },
                "export_metadata": {
                    "export_date": datetime.now().isoformat(),
                    "export_format": "json",
                    "version": "1.0"
                }
            }
            
            # Process each resume
            total_score = 0
            scores_count = 0
            
            for resume in resumes:
                resume_data = {
                    "id": resume.id,
                    "filename": resume.original_filename,
                    "upload_date": resume.upload_date.isoformat() if resume.upload_date else None,
                    "status": resume.status,
                    "total_score": resume.total_score,
                    "confidence_score": resume.confidence_score
                }
                
                # Add score to summary
                if resume.total_score is not None:
                    total_score += resume.total_score
                    scores_count += 1
                    
                    if resume.total_score >= 80:
                        export_data["summary"]["score_distribution"]["excellent"] += 1
                    elif resume.total_score >= 60:
                        export_data["summary"]["score_distribution"]["good"] += 1
                    elif resume.total_score >= 40:
                        export_data["summary"]["score_distribution"]["average"] += 1
                    else:
                        export_data["summary"]["score_distribution"]["poor"] += 1
                
                export_data["resumes"].append(resume_data)
            
            # Calculate average score
            if scores_count > 0:
                export_data["summary"]["average_score"] = round(total_score / scores_count, 2)
            
            return export_data
            
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")
    
    def export_vacancy_resumes_to_csv(self, vacancy_id: str) -> str:
        """Export all resumes for a specific vacancy to CSV"""
        try:
            # Get vacancy
            vacancy = self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
            if not vacancy:
                raise Exception("Vacancy not found")
            
            # Get all resumes for this vacancy
            resumes = self.db.query(Resume).filter(Resume.vacancy_id == vacancy_id).all()
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Header
            writer.writerow(["Vacancy Resume Analysis Export"])
            writer.writerow(["Export Date", datetime.now().isoformat()])
            writer.writerow([])
            
            # Vacancy Info
            writer.writerow(["VACANCY INFORMATION"])
            writer.writerow(["Field", "Value"])
            writer.writerow(["ID", vacancy.id])
            writer.writerow(["Title", vacancy.title])
            writer.writerow(["Code", vacancy.vacancy_code])
            writer.writerow(["Description", vacancy.description or ""])
            writer.writerow([])
            
            # Summary
            processed_resumes = [r for r in resumes if r.status == "analyzed"]
            total_score = sum(r.total_score for r in processed_resumes if r.total_score is not None)
            avg_score = round(total_score / len(processed_resumes), 2) if processed_resumes else 0
            
            writer.writerow(["SUMMARY"])
            writer.writerow(["Field", "Value"])
            writer.writerow(["Total Resumes", len(resumes)])
            writer.writerow(["Processed Resumes", len(processed_resumes)])
            writer.writerow(["Average Score", avg_score])
            writer.writerow([])
            
            # Resumes
            writer.writerow(["RESUMES"])
            writer.writerow(["ID", "Filename", "Upload Date", "Status", "Total Score", "Confidence Score"])
            for resume in resumes:
                writer.writerow([
                    resume.id,
                    resume.original_filename,
                    resume.upload_date.isoformat() if resume.upload_date else "",
                    resume.status,
                    resume.total_score or "",
                    resume.confidence_score or ""
                ])
            
            return output.getvalue()
            
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")
    
    def export_statistics_to_json(self) -> Dict[str, Any]:
        """Export system statistics to JSON"""
        try:
            stats = self.resume_service.get_resume_statistics()
            
            export_data = {
                "statistics": stats,
                "export_metadata": {
                    "export_date": datetime.now().isoformat(),
                    "export_format": "json",
                    "version": "1.0"
                }
            }
            
            return export_data
            
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")
    
    def export_statistics_to_csv(self) -> str:
        """Export system statistics to CSV"""
        try:
            stats = self.resume_service.get_resume_statistics()
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Header
            writer.writerow(["Resume System Statistics Export"])
            writer.writerow(["Export Date", datetime.now().isoformat()])
            writer.writerow([])
            
            # General Statistics
            writer.writerow(["GENERAL STATISTICS"])
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Resumes", stats["total_resumes"]])
            writer.writerow(["Processed Resumes", stats["processed_resumes"]])
            writer.writerow(["Error Resumes", stats["error_resumes"]])
            writer.writerow(["Average Score", stats["average_score"]])
            writer.writerow([])
            
            # Score Distribution
            writer.writerow(["SCORE DISTRIBUTION"])
            writer.writerow(["Category", "Count"])
            for category, count in stats["score_distribution"].items():
                writer.writerow([category.title(), count])
            writer.writerow([])
            
            # Top Vacancies
            if stats["top_vacancies"]:
                writer.writerow(["TOP VACANCIES"])
                writer.writerow(["Vacancy ID", "Code", "Title", "Resume Count"])
                for vacancy in stats["top_vacancies"]:
                    writer.writerow([
                        vacancy["vacancy_id"],
                        vacancy["vacancy_code"] or "",
                        vacancy["title"],
                        vacancy["count"]
                    ])
            
            return output.getvalue()
            
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")
