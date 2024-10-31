from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database.session import get_db
from ..models.post import Post, Report
from ..utils.security import verify_service_auth
from pydantic import BaseModel
from ..config import settings

router = APIRouter()

class ReportResponse(BaseModel):
    id: int
    post_id: int
    post_title: str
    reporter_username: str
    reviewed: bool

    class Config:
        from_attributes = True

@router.get("/reports", response_model=List[ReportResponse])
async def get_reports(
    request: Request,
    x_service_auth: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    # Vulnerable: Weak service auth validation
    if not verify_service_auth(x_service_auth):
        raise HTTPException(status_code=403, detail="Invalid service auth")
    
    reports = db.query(Report).filter(Report.reviewed == False).all()
    return reports

@router.post("/reports/{report_id}/review")
async def review_report(
    report_id: int,
    request: Request,
    x_service_auth: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    # Vulnerable: Doesn't validate admin role properly
    if not verify_service_auth(x_service_auth):
        raise HTTPException(status_code=403, detail="Invalid service auth")
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report.reviewed = True
    db.commit()
    
    return {"message": "Report reviewed successfully"}

@router.get("/flag")
async def get_flag(
    request: Request,
    x_service_auth: Optional[str] = Header(None)
):
    # Vulnerable: Weak auth check
    if not verify_service_auth(x_service_auth):
        raise HTTPException(status_code=403, detail="Invalid service auth")
    
    return {"flag": settings.FLAG}