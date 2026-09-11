"""Institution routes."""

from app.api.deps import AdminUser, CurrentUserDep, DbSession
from app.models.institution import Institution
from app.schemas.academic import InstitutionResponse, InstitutionUpdate
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/institutions", tags=["institutions"])


def _to_response(institution: Institution) -> InstitutionResponse:
    return InstitutionResponse(
        id=str(institution.id),
        name=institution.name,
        logo_url=institution.logo_url,
        description=institution.description,
    )


@router.get("/me", response_model=InstitutionResponse)
def get_my_institution(current: CurrentUserDep, db: DbSession):
    institution = (
        db.query(Institution).filter(Institution.id == current.institution_id).first()
    )
    if not institution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")
    return _to_response(institution)


@router.patch("/me", response_model=InstitutionResponse)
def update_my_institution(body: InstitutionUpdate, current: AdminUser, db: DbSession):
    institution = (
        db.query(Institution).filter(Institution.id == current.institution_id).first()
    )
    if not institution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")
    if body.name is not None:
        institution.name = body.name
    if body.logo_url is not None:
        institution.logo_url = body.logo_url
    if body.description is not None:
        institution.description = body.description
    db.commit()
    db.refresh(institution)
    return _to_response(institution)
