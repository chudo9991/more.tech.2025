"""
Export service for generating reports
"""
import csv
import json
import io
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, func

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from jinja2 import Template

from app.models import Session as SessionModel, QA, QAScore, Question, Criteria, Vacancy
from app.services.session_service import SessionService


class ExportService:
    def __init__(self, db: DBSession):
        self.db = db

    async def export_session_report(
        self, 
        session_id: str, 
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export session report in specified format"""
        try:
            session_service = SessionService(self.db)
            results = await session_service.aggregate_session_results(session_id)
            
            if format.lower() == "json":
                return self._export_json(results)
            elif format.lower() == "csv":
                return self._export_csv(results)
            elif format.lower() == "summary":
                return self._export_summary(results)
            elif format.lower() == "pdf":
                return self._export_pdf(results)
            elif format.lower() == "html":
                return self._export_html(results)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")

    async def export_vacancy_report(
        self, 
        vacancy_id: str, 
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export all sessions for a vacancy"""
        try:
            # Get all sessions for this vacancy
            sessions = self.db.query(SessionModel).filter(
                SessionModel.vacancy_id == vacancy_id
            ).all()
            
            vacancy = self.db.query(Vacancy).filter(
                Vacancy.id == vacancy_id
            ).first()
            
            if not vacancy:
                raise Exception("Vacancy not found")
            
            # Aggregate results for all sessions
            vacancy_results = {
                "vacancy_id": vacancy_id,
                "vacancy_title": vacancy.title,
                "total_sessions": len(sessions),
                "completed_sessions": len([s for s in sessions if s.status == "completed"]),
                "avg_total_score": 0,
                "avg_pass_rate": 0,
                "sessions": []
            }
            
            total_score_sum = 0
            pass_rate_sum = 0
            completed_count = 0
            
            for session in sessions:
                session_service = SessionService(self.db)
                session_results = await session_service.aggregate_session_results(session.id)
                vacancy_results["sessions"].append(session_results)
                
                if session.status == "completed":
                    total_score_sum += session_results["total_score"]
                    pass_rate_sum += session_results["pass_rate"]
                    completed_count += 1
            
            if completed_count > 0:
                vacancy_results["avg_total_score"] = total_score_sum / completed_count
                vacancy_results["avg_pass_rate"] = pass_rate_sum / completed_count
            
            if format.lower() == "json":
                return self._export_json(vacancy_results)
            elif format.lower() == "csv":
                return self._export_vacancy_csv(vacancy_results)
            elif format.lower() == "pdf":
                return self._export_vacancy_pdf(vacancy_results)
            elif format.lower() == "html":
                return self._export_vacancy_html(vacancy_results)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            raise Exception(f"Vacancy export failed: {str(e)}")

    def _export_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Export data as JSON"""
        return {
            "format": "json",
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }

    def _export_csv(self, session_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export session results as CSV"""
        csv_rows = []
        
        # Header
        csv_rows.append([
            "Question ID", "Question Text", "Answer Text", 
            "Transcription Confidence", "Pre-answer Pause (s)", 
            "Speech Rate (wpm)", "Average Score", "Criteria Scores"
        ])
        
        # Data rows
        for question in session_results["questions"]:
            criteria_scores = "; ".join([
                f"{score['criterion_id']}:{score['score']:.2f}"
                for score in question["scores"]
            ])
            
            csv_rows.append([
                question["question_id"],
                question["question_text"],
                question["answer_text"],
                f"{question['transcription_confidence']:.2f}",
                f"{question['pre_answer_pause_s']:.2f}",
                f"{question['speech_rate_wpm']:.1f}",
                f"{question['avg_score']:.2f}",
                criteria_scores
            ])
        
        # Convert to CSV string
        csv_content = "\n".join([",".join(row) for row in csv_rows])
        
        return {
            "format": "csv",
            "timestamp": datetime.utcnow().isoformat(),
            "filename": f"session_{session_results['session_id']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
            "content": csv_content
        }

    def _export_vacancy_csv(self, vacancy_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export vacancy results as CSV"""
        csv_rows = []
        
        # Header
        csv_rows.append([
            "Session ID", "Status", "Total Questions", "Answered Questions",
            "Completion Rate", "Total Score", "Pass Rate", "Started At", "Completed At"
        ])
        
        # Data rows
        for session in vacancy_results["sessions"]:
            csv_rows.append([
                session["session_id"],
                session["status"],
                str(session["total_questions"]),
                str(session["answered_questions"]),
                f"{session['completion_rate']:.2f}",
                f"{session['total_score']:.2f}",
                f"{session['pass_rate']:.2f}",
                session["started_at"] or "",
                session["completed_at"] or ""
            ])
        
        # Convert to CSV string
        csv_content = "\n".join([",".join(row) for row in csv_rows])
        
        return {
            "format": "csv",
            "timestamp": datetime.utcnow().isoformat(),
            "filename": f"vacancy_{vacancy_results['vacancy_id']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
            "content": csv_content
        }

    def _export_summary(self, session_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export session summary"""
        summary = {
            "session_id": session_results["session_id"],
            "status": session_results["status"],
            "completion_rate": f"{session_results['completion_rate']:.1%}",
            "total_score": f"{session_results['total_score']:.2f}",
            "pass_rate": f"{session_results['pass_rate']:.1%}",
            "questions_answered": session_results["answered_questions"],
            "total_questions": session_results["total_questions"],
            "duration": self._calculate_duration(
                session_results["started_at"], 
                session_results["completed_at"]
            ),
            "top_performing_questions": self._get_top_questions(session_results["questions"]),
            "areas_for_improvement": self._get_improvement_areas(session_results["questions"])
        }
        
        return {
            "format": "summary",
            "timestamp": datetime.utcnow().isoformat(),
            "data": summary
        }

    def _calculate_duration(self, started_at: Optional[str], completed_at: Optional[str]) -> str:
        """Calculate session duration"""
        if not started_at or not completed_at:
            return "N/A"
        
        try:
            start = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            end = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
            duration = end - start
            return str(duration)
        except:
            return "N/A"

    def _get_top_questions(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get top performing questions"""
        sorted_questions = sorted(questions, key=lambda x: x["avg_score"], reverse=True)
        return [
            {
                "question_text": q["question_text"][:100] + "..." if len(q["question_text"]) > 100 else q["question_text"],
                "avg_score": f"{q['avg_score']:.2f}"
            }
            for q in sorted_questions[:3]
        ]

    def _get_improvement_areas(self, questions: List[Dict[str, Any]]) -> List[str]:
        """Get areas for improvement"""
        low_score_questions = [
            q for q in questions if q["avg_score"] < 0.6
        ]
        
        areas = []
        for q in low_score_questions:
            areas.append(f"Question: {q['question_text'][:50]}... (Score: {q['avg_score']:.2f})")
        
        return areas[:3]  # Top 3 areas for improvement

    def _export_pdf(self, session_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export session results as PDF"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Center
            )
            story.append(Paragraph("Interview Session Report", title_style))
            story.append(Spacer(1, 12))

            # Session Info
            info_data = [
                ['Session ID', session_results['session_id']],
                ['Status', session_results['status']],
                ['Total Questions', str(session_results['total_questions'])],
                ['Answered Questions', str(session_results['answered_questions'])],
                ['Completion Rate', f"{session_results['completion_rate']:.1%}"],
                ['Total Score', f"{session_results['total_score']:.1%}"],
                ['Pass Rate', f"{session_results['pass_rate']:.1%}"],
                ['Started At', session_results['started_at'] or 'N/A'],
                ['Completed At', session_results['completed_at'] or 'N/A']
            ]
            
            info_table = Table(info_data, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(info_table)
            story.append(Spacer(1, 20))

            # Questions and Answers
            if session_results['questions']:
                story.append(Paragraph("Questions & Answers", styles['Heading2']))
                story.append(Spacer(1, 12))

                for i, question in enumerate(session_results['questions'], 1):
                    # Question header
                    q_header = f"Question {i} (Score: {question['avg_score']:.1%})"
                    story.append(Paragraph(q_header, styles['Heading3']))
                    story.append(Spacer(1, 6))

                    # Question text
                    story.append(Paragraph(f"<b>Question:</b> {question['question_text']}", styles['Normal']))
                    story.append(Spacer(1, 6))

                    # Answer text
                    story.append(Paragraph(f"<b>Answer:</b> {question['answer_text']}", styles['Normal']))
                    story.append(Spacer(1, 6))

                    # Metrics
                    metrics_data = [
                        ['Confidence', f"{question['transcription_confidence']:.1%}"],
                        ['Pre-answer Pause', f"{question['pre_answer_pause_s']:.1f}s"],
                        ['Speech Rate', f"{question['speech_rate_wpm']:.0f} WPM"]
                    ]
                    
                    metrics_table = Table(metrics_data, colWidths=[1.5*inch, 1.5*inch])
                    metrics_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                    ]))
                    story.append(metrics_table)
                    story.append(Spacer(1, 12))

            # Build PDF
            doc.build(story)
            buffer.seek(0)
            pdf_content = buffer.getvalue()
            buffer.close()

            return {
                "format": "pdf",
                "timestamp": datetime.utcnow().isoformat(),
                "filename": f"session_{session_results['session_id']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf",
                "content": pdf_content
            }

        except Exception as e:
            raise Exception(f"PDF export failed: {str(e)}")

    def _export_html(self, session_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export session results as HTML"""
        try:
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Interview Session Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .header { text-align: center; margin-bottom: 30px; }
                    .info-table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
                    .info-table th, .info-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    .info-table th { background-color: #f2f2f2; }
                    .question { border: 1px solid #ddd; margin-bottom: 20px; padding: 15px; }
                    .question-header { background-color: #f9f9f9; padding: 10px; margin-bottom: 10px; }
                    .metrics { display: flex; gap: 20px; margin: 10px 0; }
                    .metric { flex: 1; padding: 10px; background-color: #f5f5f5; }
                    .score { font-weight: bold; color: #007bff; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Interview Session Report</h1>
                    <p>Generated on {{ timestamp }}</p>
                </div>

                <table class="info-table">
                    <tr><th>Session ID</th><td>{{ session_id }}</td></tr>
                    <tr><th>Status</th><td>{{ status }}</td></tr>
                    <tr><th>Total Questions</th><td>{{ total_questions }}</td></tr>
                    <tr><th>Answered Questions</th><td>{{ answered_questions }}</td></tr>
                    <tr><th>Completion Rate</th><td>{{ completion_rate }}%</td></tr>
                    <tr><th>Total Score</th><td class="score">{{ total_score }}%</td></tr>
                    <tr><th>Pass Rate</th><td class="score">{{ pass_rate }}%</td></tr>
                    <tr><th>Started At</th><td>{{ started_at }}</td></tr>
                    <tr><th>Completed At</th><td>{{ completed_at }}</td></tr>
                </table>

                <h2>Questions & Answers</h2>
                {% for question in questions %}
                <div class="question">
                    <div class="question-header">
                        <h3>Question {{ loop.index }} (Score: {{ "%.1f"|format(question.avg_score * 100) }}%)</h3>
                    </div>
                    <p><strong>Question:</strong> {{ question.question_text }}</p>
                    <p><strong>Answer:</strong> {{ question.answer_text }}</p>
                    <div class="metrics">
                        <div class="metric">
                            <strong>Confidence:</strong> {{ "%.1f"|format(question.transcription_confidence * 100) }}%
                        </div>
                        <div class="metric">
                            <strong>Pre-answer Pause:</strong> {{ "%.1f"|format(question.pre_answer_pause_s) }}s
                        </div>
                        <div class="metric">
                            <strong>Speech Rate:</strong> {{ "%.0f"|format(question.speech_rate_wpm) }} WPM
                        </div>
                    </div>
                </div>
                {% endfor %}
            </body>
            </html>
            """

            template = Template(html_template)
            html_content = template.render(
                session_id=session_results['session_id'],
                status=session_results['status'],
                total_questions=session_results['total_questions'],
                answered_questions=session_results['answered_questions'],
                completion_rate=f"{session_results['completion_rate']:.1%}",
                total_score=f"{session_results['total_score']:.1%}",
                pass_rate=f"{session_results['pass_rate']:.1%}",
                started_at=session_results['started_at'] or 'N/A',
                completed_at=session_results['completed_at'] or 'N/A',
                questions=session_results['questions'],
                timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            )

            return {
                "format": "html",
                "timestamp": datetime.utcnow().isoformat(),
                "filename": f"session_{session_results['session_id']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html",
                "content": html_content
            }

        except Exception as e:
            raise Exception(f"HTML export failed: {str(e)}")

    def _export_vacancy_pdf(self, vacancy_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export vacancy results as PDF"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph(f"Vacancy Report: {vacancy_results['vacancy_title']}", title_style))
            story.append(Spacer(1, 12))

            # Vacancy Summary
            summary_data = [
                ['Total Sessions', str(vacancy_results['total_sessions'])],
                ['Completed Sessions', str(vacancy_results['completed_sessions'])],
                ['Average Total Score', f"{vacancy_results['avg_total_score']:.1%}"],
                ['Average Pass Rate', f"{vacancy_results['avg_pass_rate']:.1%}"]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 20))

            # Sessions Table
            if vacancy_results['sessions']:
                story.append(Paragraph("Session Details", styles['Heading2']))
                story.append(Spacer(1, 12))

                sessions_data = [['Session ID', 'Status', 'Questions', 'Score', 'Pass Rate']]
                for session in vacancy_results['sessions']:
                    sessions_data.append([
                        session['session_id'][:8] + '...',
                        session['status'],
                        f"{session['answered_questions']}/{session['total_questions']}",
                        f"{session['total_score']:.1%}",
                        f"{session['pass_rate']:.1%}"
                    ])

                sessions_table = Table(sessions_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
                sessions_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(sessions_table)

            # Build PDF
            doc.build(story)
            buffer.seek(0)
            pdf_content = buffer.getvalue()
            buffer.close()

            return {
                "format": "pdf",
                "timestamp": datetime.utcnow().isoformat(),
                "filename": f"vacancy_{vacancy_results['vacancy_id']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf",
                "content": pdf_content
            }

        except Exception as e:
            raise Exception(f"Vacancy PDF export failed: {str(e)}")

    def _export_vacancy_html(self, vacancy_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export vacancy results as HTML"""
        try:
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Vacancy Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .header { text-align: center; margin-bottom: 30px; }
                    .summary-table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
                    .summary-table th, .summary-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    .summary-table th { background-color: #f2f2f2; }
                    .sessions-table { width: 100%; border-collapse: collapse; }
                    .sessions-table th, .sessions-table td { border: 1px solid #ddd; padding: 8px; text-align: center; }
                    .sessions-table th { background-color: #f2f2f2; }
                    .score { font-weight: bold; color: #007bff; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Vacancy Report: {{ vacancy_title }}</h1>
                    <p>Generated on {{ timestamp }}</p>
                </div>

                <table class="summary-table">
                    <tr><th>Total Sessions</th><td>{{ total_sessions }}</td></tr>
                    <tr><th>Completed Sessions</th><td>{{ completed_sessions }}</td></tr>
                    <tr><th>Average Total Score</th><td class="score">{{ avg_total_score }}%</td></tr>
                    <tr><th>Average Pass Rate</th><td class="score">{{ avg_pass_rate }}%</td></tr>
                </table>

                <h2>Session Details</h2>
                <table class="sessions-table">
                    <tr>
                        <th>Session ID</th>
                        <th>Status</th>
                        <th>Questions</th>
                        <th>Score</th>
                        <th>Pass Rate</th>
                    </tr>
                    {% for session in sessions %}
                    <tr>
                        <td>{{ session.session_id[:8] }}...</td>
                        <td>{{ session.status }}</td>
                        <td>{{ session.answered_questions }}/{{ session.total_questions }}</td>
                        <td class="score">{{ "%.1f"|format(session.total_score * 100) }}%</td>
                        <td class="score">{{ "%.1f"|format(session.pass_rate * 100) }}%</td>
                    </tr>
                    {% endfor %}
                </table>
            </body>
            </html>
            """

            template = Template(html_template)
            html_content = template.render(
                vacancy_title=vacancy_results['vacancy_title'],
                total_sessions=vacancy_results['total_sessions'],
                completed_sessions=vacancy_results['completed_sessions'],
                avg_total_score=f"{vacancy_results['avg_total_score']:.1%}",
                avg_pass_rate=f"{vacancy_results['avg_pass_rate']:.1%}",
                sessions=vacancy_results['sessions'],
                timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            )

            return {
                "format": "html",
                "timestamp": datetime.utcnow().isoformat(),
                "filename": f"vacancy_{vacancy_results['vacancy_id']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html",
                "content": html_content
            }

        except Exception as e:
            raise Exception(f"Vacancy HTML export failed: {str(e)}")
